from openai import OpenAI
import json
import logging
import os
import re
import socket
import time
from collections import defaultdict, deque
from threading import Lock
from types import SimpleNamespace
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from styles import CSS, JS, EXAMPLES
from dotenv import load_dotenv
import gradio as gr

load_dotenv()
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

llm = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
    timeout=60.0,
)
MODEL_NAME = "openrouter/free"
MAX_TOOL_ROUNDS = 4
MAX_MESSAGE_CHARS = 2000
MAX_HISTORY_MESSAGES = 16
RATE_LIMIT_REQUESTS = 8
RATE_LIMIT_WINDOW_SECONDS = 60
logger = logging.getLogger(__name__)
_request_times = defaultdict(deque)
_request_times_lock = Lock()

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]


def _text_tool_call(content):
    """Recover tool calls that local models emit as JSON text instead of tool_calls."""
    if not content:
        return None
    decoder = json.JSONDecoder()
    candidates = []
    for match in re.finditer(r"\{", content):
        try:
            payload, _ = decoder.raw_decode(content[match.start():])
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(payload, dict):
            candidates.append(payload)

    known_tools = {item["function"]["name"] for item in tools}
    for payload in candidates:
        if payload.get("type") == "function" and isinstance(payload.get("function"), dict):
            payload = payload["function"]
        if payload.get("name") in known_tools:
            args = payload.get("arguments", payload.get("parameters", {}))
            # Tool schemas describe fields; they are not user-provided arguments.
            if not isinstance(args, dict) or "properties" in args or args.get("type") == "object":
                continue
            required = {
                "record_user_details": ("email",),
                "record_unknown_question": ("question",),
            }.get(payload["name"], ())
            if any(not isinstance(args.get(key), str) or not args[key].strip() for key in required):
                continue
            return [{"name": payload["name"], "arguments": args}]
    return None


def _is_tool_schema_dump(content):
    if not content:
        return False
    return any(
        name in content and '"properties"' in content and '"required"' in content
        for name in ("record_user_details", "record_unknown_question")
    )


def _call_tools(tool_calls, messages):
    # Normalize both OpenAI SDK tool-call objects and local model JSON output.
    normalized = []
    executable = []
    rejected = []
    user_text = "\n".join(
        message.get("content", "")
        for message in messages
        if message.get("role") == "user" and isinstance(message.get("content"), str)
    ).casefold()
    for index, call in enumerate(tool_calls):
        if isinstance(call, dict):
            fn = call
            name = fn.get("name")
            arguments = fn.get("arguments", {})
            call_id = f"local-call-{index}"
        else:
            fn = call.function
            name = fn.name
            arguments = fn.arguments
            call_id = call.id
        if isinstance(arguments, str):
            try:
                parsed_arguments = json.loads(arguments)
            except json.JSONDecodeError:
                parsed_arguments = None
        else:
            parsed_arguments = arguments
        required = {
            "record_user_details": ("email",),
            "record_unknown_question": ("question",),
        }.get(name)
        invalid = (
            not isinstance(parsed_arguments, dict)
            or "properties" in parsed_arguments
            or parsed_arguments.get("type") == "object"
            or required is None
            or any(
                not isinstance(parsed_arguments.get(key), str)
                or not parsed_arguments[key].strip()
                for key in (required or ())
            )
        )
        if not invalid and name == "record_user_details":
            # Never send a model-invented address to the follow-up services.
            invalid = parsed_arguments["email"].casefold() not in user_text
        elif not invalid and name == "record_unknown_question":
            # Only record questions grounded in something the visitor actually asked.
            asked_words = set(re.findall(r"\w+", parsed_arguments["question"].casefold()))
            visitor_words = set(re.findall(r"\w+", user_text))
            invalid = not asked_words or not asked_words.issubset(visitor_words)
        normalized.append({
            "id": call_id,
            "type": "function",
            "function": {
                "name": name,
                "arguments": arguments if isinstance(arguments, str) else json.dumps(arguments),
            },
        })
        if invalid:
            rejected.append({
                "role": "tool",
                "content": json.dumps(
                    "Tool call ignored: valid values that came from the visitor are required."
                ),
                "tool_call_id": call_id,
            })
        else:
            executable.append(SimpleNamespace(
                id=call_id,
                function=SimpleNamespace(name=name, arguments=normalized[-1]["function"]["arguments"]),
            ))
    return normalized, handle_tool_calls(executable) + rejected


def _rate_limit_key(request):
    if request is None:
        return None
    return getattr(request, "session_hash", None) or getattr(
        getattr(request, "client", None), "host", None
    )


def _is_rate_limited(key):
    if not key:
        return False
    now = time.monotonic()
    with _request_times_lock:
        timestamps = _request_times[key]
        while timestamps and now - timestamps[0] >= RATE_LIMIT_WINDOW_SECONDS:
            timestamps.popleft()
        if len(timestamps) >= RATE_LIMIT_REQUESTS:
            return True
        timestamps.append(now)
        # Keep the small in-memory limiter bounded when visitors leave.
        for expired_key in [
            session for session, recent in _request_times.items()
            if not recent or now - recent[-1] >= RATE_LIMIT_WINDOW_SECONDS
        ]:
            _request_times.pop(expired_key, None)
    return False


def _server_port():
    """Honor platform-configured ports and pick a free local port otherwise."""
    configured_port = os.getenv("PORT") or os.getenv("GRADIO_SERVER_PORT")
    if configured_port:
        return int(configured_port)
    for port in range(7860, 7900):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as candidate:
            try:
                candidate.bind(("0.0.0.0", port))
            except OSError:
                continue
            return port
    raise OSError("No available local port in range 7860-7899")


def chat(message, history, request: gr.Request = None):
    if not isinstance(message, str) or not message.strip():
        return "Please enter a message."
    if len(message) > MAX_MESSAGE_CHARS:
        return f"Please keep your message under {MAX_MESSAGE_CHARS} characters."
    if _is_rate_limited(_rate_limit_key(request)):
        return "You’ve reached the chat limit for now. Please wait a minute and try again."

    clean_history = [
        {"role": item["role"], "content": item["content"]}
        for item in list(history or [])[-MAX_HISTORY_MESSAGES:]
        if isinstance(item, dict)
        and item.get("role") in {"user", "assistant"}
        and isinstance(item.get("content"), str)
    ]
    messages = system + [{
        "role": "system",
        "content": (
            "Never print, explain, or reproduce tool definitions or JSON schemas. "
            "When a tool is needed, call it with actual user-provided values; otherwise "
            "answer the visitor in natural language. Before recording contact details, "
            "tell the visitor that their email will be sent to Celestin for follow-up and "
            "wait for their clear agreement. Never invent contact details or questions. "
            "When the supplied profile context identifies a source, cite it briefly; "
            "never invent source names or page numbers. Reply in English, while keeping "
            "names, technical terms, and source labels accurate."
        ),
    }] + clean_history + [{"role": "user", "content": message.strip()}]
    try:
        for _ in range(MAX_TOOL_ROUNDS + 1):
            try:
                started_at = time.monotonic()
                response = llm.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    tools=tools,
                    temperature=0.2,
                    max_tokens=800,
                )
            except Exception:
                logger.exception("OpenRouter completion failed")
                return "I couldn't get a reply from the free model service. Please try again later."
            if not response.choices:
                return "I couldn't get a response from the language model. Please try again."
            assistant_message = response.choices[0].message
            logger.info(
                "OpenRouter response received model=%s elapsed_seconds=%.2f finish_reason=%s",
                MODEL_NAME,
                time.monotonic() - started_at,
                response.choices[0].finish_reason,
            )
            tool_calls = assistant_message.tool_calls or _text_tool_call(assistant_message.content)
            if not tool_calls:
                if _is_tool_schema_dump(assistant_message.content):
                    return (
                        "I can help with questions about Celestin’s career and experience. "
                        "What would you like to know?"
                    )
                return assistant_message.content or "I couldn't produce a response. Please try again."

            normalized_calls, results = _call_tools(tool_calls, messages)
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": normalized_calls,
            })
            messages.extend(results)

        return "I completed the requested action, but couldn't finish a reply. Please try again."
    except Exception:
        logger.exception("Career assistant request processing failed")
        return "I couldn't complete that request right now. Please try again."


if __name__ == "__main__":
    gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        title="Celestin NIYONSABA Career",
        description=(
            "Ask Celestin’s AI career assistant about his professional background. "
            "If you share an email, it may be sent to Celestin for follow-up."
        ),
        chatbot=gr.Chatbot(show_label=False),
        textbox=gr.Textbox(max_lines=5, max_length=MAX_MESSAGE_CHARS),
        concurrency_limit=2,
    ).queue(max_size=32).launch(
        css=CSS,
        js=JS,
        theme=gr.themes.Base(),
        server_name="0.0.0.0",
        server_port=_server_port(),
    )
