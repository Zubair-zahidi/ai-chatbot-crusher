# Crusher — Flask Chatbot

A Python and Flask chatbot prototype with a browser interface and configurable AI API integrations. It explores conversational workflows and supporting text, voice, and information-service integrations in the application source.

## Run locally

```bash
git clone https://github.com/Zubair-zahidi/ai-chatbot-crusher.git
cd ai-chatbot-crusher
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to a local `.env` and configure only the services you intend to use. Read `app.py` for the required providers and settings. Keep real keys outside Git; provider API usage can incur charges.

```bash
python app.py
```

Open the local address printed by Flask.

## Project structure

- `app.py` — Application routes and integrations.
- `templates/` — Browser pages.
- `static/` — Client assets.
- `.env.example` — Configuration names with blank credential values.

## Status and security

This is a development prototype. Review its request handling, authentication, and configuration before deployment. AI responses need human verification.

A real `.env` file was previously tracked. It has been removed from the current branch, but historical commits can retain old values. Revoke or rotate affected provider credentials before using new ones.

Created by **Zubair Zahidi**.
