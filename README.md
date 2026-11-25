---
title: Celestin NIYONSABA Career Assistant
app_file: app.py
sdk: gradio
sdk_version: 6.14.0
---

# Celestin NIYONSABA Career Assistant

An AI-powered career profile and chat app for visitors who want to learn about
Celestin Niyonsaba's professional background, skills, and experience.

**Live deployment:** [https://celestins-ai-career-assistant.onrender.com](https://celestins-ai-career-assistant.onrender.com)

## What it does

- Answers career-related questions using Celestin's profile summary and LinkedIn
  profile.
- Keeps the conversation focused on professional background, skills, and
  experience.
- Explains that it is an AI assistant representing Celestin when asked.
- Lets an interested visitor provide an email address for follow-up.
- Sends contact-interest and unanswered-question notifications through
  Pushover when Pushover credentials are configured, and can save records in an
  optional Supabase database.
- Limits message size, chat history, and per-session request frequency.
- Adds source labels to LinkedIn profile pages so answers can cite their source.
- Lets visitors choose English, French, or Kinyarwanda responses.
- Provides a Gradio chat interface with example questions and custom styling.

## How it works

1. At startup, `context.py` extracts text from `linkedin.pdf` and reads
   `summary.txt`.
2. The app uses those details to build the assistant's system prompt.
3. `app.py` sends the prompt, chat history, and visitor's message to OpenRouter
   using the OpenAI-compatible Chat Completions API.
4. The app uses OpenRouter's `openrouter/free` router. It selects from available
   free models and filters for features requested by the app, including tool
   calling.
5. If the model requests a tool, the Python app validates the arguments and
   executes the matching function in `tools.py`. The tool result is sent back
   to the model so it can write a visitor-facing reply.
6. The `record_user_details` and `record_unknown_question` functions validate
   visitor-provided values, then save them to Supabase and/or send a Pushover
   notification if those services are configured.

The model does not execute Python functions itself. It asks the application to
run a tool, and the application handles validation and execution.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Gradio interface, OpenRouter client, chat flow, and tool-call handling. |
| `context.py` | Loads profile sources and builds the assistant's instructions. |
| `summary.txt` | Short career summary included in the assistant context. |
| `linkedin.pdf` | LinkedIn profile source used to add career details. |
| `tools.py` | Contact and unanswered-question tools, with Pushover notifications. |
| `styles.py` | Gradio examples, CSS theme, and small browser-side behavior. |
| `requirements.txt` | Python dependencies. |
| `render.yaml` | Render Blueprint for creating the web service. |
| `.env.example` | Names of supported environment variables, with empty secret values. |
| `supabase/schema.sql` | Optional database tables and access restrictions for lead/question storage. |

## Run locally

Requires Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your OpenRouter key to `.env`:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
```

The model route is fixed to OpenRouter's free router to avoid accidentally
selecting a paid model. Free-model availability and request limits can change.
To persist contact requests and unanswered questions, create a free Supabase
project, run `supabase/schema.sql` in its SQL Editor, then set `SUPABASE_URL`
and `SUPABASE_SECRET_KEY` in `.env`. Keep the Supabase secret key server-side;
never put it in browser code or commit it. Pushover credentials are optional;
they enable push notifications, but receiving push notifications may require a
one-time device license. Then start the app:

```bash
python app.py
```

Open the local URL printed by Gradio. It starts at port `7860` and automatically
tries the next available port if that port is already in use.

## Deployment

The app is deployed as a **Render Web Service** at
[celestins-ai-career-assistant.onrender.com](https://celestins-ai-career-assistant.onrender.com).
Render runs the Python Gradio server; OpenRouter provides the hosted language
model API.

The repository includes `render.yaml` with these service settings:

- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`
- Health check: `/`
- Plan: Render Free

To create or redeploy it from this repository, connect the Git repository in
Render with **New → Blueprint**, then set these environment variables in Render:

| Variable | Required | Purpose |
| --- | --- | --- |
| `OPENROUTER_API_KEY` | Yes | Authenticates chat requests to OpenRouter. |
| `SUPABASE_URL` | No | Supabase project URL for optional persistence. |
| `SUPABASE_SECRET_KEY` | No | Server-only key used to save leads and questions. |
| `PUSHOVER_USER` | No | Pushover user or group receiving optional notifications. |
| `PUSHOVER_TOKEN` | No | Pushover application token used for optional notifications. |

Render supplies the `PORT` value. The app binds to that port and to `0.0.0.0`.
Free Render web services can spin down when idle, so the first request after a
period of inactivity may take longer.

The app limits each Gradio session to 8 chat requests per minute, caps a message
at 2,000 characters, and keeps only the most recent 16 history messages. The
rate limit is held in process memory, so it resets when Render restarts the
service; it is a lightweight free-tier guard, not a persistent abuse-prevention
service.

## Free-service limits

The app uses OpenRouter's free-model router; model availability and request
limits can change. [OpenRouter's free router](https://openrouter.ai/openrouter/free)
filters for request features such as tool calling. Supabase's Free plan
currently includes a 500 MB database and pauses projects after a week of
inactivity. See [Supabase pricing](https://supabase.com/pricing). Pushover API
sending has a free monthly quota, but receiving push notifications may require a
one-time device license. See [Pushover pricing](https://pushover.net/pricing).
For a no-payment setup, use Render Free, OpenRouter Free, and optional Supabase
Free storage without configuring Pushover.

## Data and secrets

The assistant sends the visitor's message, chat history, and profile context
from `summary.txt` and `linkedin.pdf` to OpenRouter to generate a reply. If a
visitor shares contact details, the app stores those details in Supabase when
configured and may send them to Pushover when configured. Unanswered questions
can be stored in Supabase and sent through Pushover. The app does not save full
chat transcripts. Review the providers' current privacy and retention terms
before using the app with sensitive information.

Keep `.env` and API tokens private. `.gitignore` excludes local environment
files; configure deployment secrets in Render rather than committing them.
