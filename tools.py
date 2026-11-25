import inspect
import json
import logging
import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")

pushover_url = "https://api.pushover.net/1/messages.json"


def push(text):
    """Send a Pushover notification, returning False when it is unavailable."""
    if not pushover_user or not pushover_token:
        return False
    try:
        response = requests.post(
            pushover_url,
            data={
                "token": pushover_token,
                "user": pushover_user,
                "message": text[:1024],
            },
            timeout=8,
        )
        response.raise_for_status()
        result = response.json()
        return isinstance(result, dict) and result.get("status") == 1
    except (requests.RequestException, ValueError, AttributeError):
        logger.exception("Pushover notification failed")
        return False


def save_to_supabase(table, record):
    """Persist a tool record when an optional Supabase project is configured."""
    project_url = os.getenv("SUPABASE_URL", "").rstrip("/")
    secret_key = os.getenv("SUPABASE_SECRET_KEY")
    if not project_url or not secret_key:
        return False
    if table not in {"career_leads", "unknown_questions"}:
        return False
    try:
        response = requests.post(
            f"{project_url}/rest/v1/{table}",
            headers={
                "apikey": secret_key,
                "Authorization": f"Bearer {secret_key}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            },
            json=record,
            timeout=8,
        )
        response.raise_for_status()
        return True
    except requests.RequestException:
        logger.exception("Supabase write failed for table %s", table)
        return False


def record_user_details(email, name="Name not provided", notes="not provided"):
    if not isinstance(email, str):
        return "The email address is invalid; no contact details were saved."
    email = email.strip()
    if len(email) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        return "The email address is invalid; no contact details were saved."
    name = (name if isinstance(name, str) else "Name not provided").strip()[:120]
    notes = (notes if isinstance(notes, str) else "not provided").strip()[:1000]
    saved = save_to_supabase(
        "career_leads",
        {"email": email, "name": name, "notes": notes},
    )
    notified = push(f"Recording interest from {name} with email {email} and notes {notes}")
    if saved and notified:
        return "Contact details saved and Celestin was notified."
    if saved:
        return "Contact details saved; the notification could not be delivered."
    if notified:
        return "Celestin was notified, but the details were not saved to a database."
    return "No contact details were saved because no storage or notification service succeeded."


def record_unknown_question(question):
    if not isinstance(question, str):
        return "No question was saved because it was invalid."
    question = question.strip()[:2000]
    if not question:
        return "No question was saved because it was empty."
    saved = save_to_supabase("unknown_questions", {"question": question})
    notified = push(f"Recording an unanswered question: {question}")
    if saved and notified:
        return "The question was saved and Celestin was notified."
    if saved:
        return "The question was saved; the notification could not be delivered."
    if notified:
        return "Celestin was notified, but the question was not saved to a database."
    return "The question could not be recorded because no storage or notification service succeeded."


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {
                "type": "string",
                "description": "Any additional info about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

tool_map = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}


def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        raw = tool_call.function.arguments
        try:
            arguments = json.loads(raw) if isinstance(raw, str) else dict(raw or {})
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            results.append(
                {"role": "tool", "content": json.dumps(f"Invalid tool arguments: {exc}"), "tool_call_id": tool_call.id}
            )
            continue
        logger.info("Tool called: %s", tool_name)
        tool = tool_map.get(tool_name)
        if not tool:
            result = "Unknown tool: " + tool_name
        else:
            # Small local models often echo schema keys such as "type" or nest values under "properties".
            if isinstance(arguments.get("properties"), dict):
                arguments = arguments["properties"]
            allowed = set(inspect.signature(tool).parameters)
            arguments = {key: value for key, value in arguments.items() if key in allowed}
            try:
                result = tool(**arguments)
            except (TypeError, ValueError) as exc:
                result = f"Tool error: {exc}"
        results.append(
            {"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id}
        )
    return results
