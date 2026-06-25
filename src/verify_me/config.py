"""Configuration & credentials.

Single place that reads secrets from the local ``.env`` file, so the rest of the
code never touches the environment directly. Mirrors the env-loading convention
already used by ``scripts/scope_probe.py`` (canonical ``PROSPERA_*`` names with a
fallback to the lowercase week-1 names).
"""

import os

from dotenv import load_dotenv

# Load .env once at import so every consumer sees the same values.
load_dotenv()

BASE_URL = (
    os.getenv("PROSPERA_BASE_URL")
    or os.getenv("base_url")
    or "https://staging-portal.eprospera.com"
)
# Personal user token (sk-...): authenticates the /me endpoints the app uses.
API_TOKEN = os.getenv("PROSPERA_API_TOKEN") or os.getenv("mytoken")
# Agent token (ak-...): used by the scope probe / agent-scoped endpoints.
AGENT_TOKEN = os.getenv("PROSPERA_AGENT_TOKEN") or os.getenv("myAgentToken")


def require_api_token() -> str:
    """Return the user token, or raise a clear error if it's missing.

    Callers (e.g. the UI) use this to fail fast with a friendly message instead
    of making a doomed, unauthenticated request.
    """
    if not API_TOKEN:
        raise RuntimeError(
            "Missing PROSPERA_API_TOKEN — copy .env.example to .env and add your "
            "sk- token."
        )
    return API_TOKEN


def require_agent_token() -> str:
    """Return the agent token, or raise a clear error if it's missing.

    The ``/api/v1/me/...`` profile + residency endpoints are gated on ``agent:*``
    scopes that the personal ``sk-`` user token does not carry (it gets 403), so
    the app authenticates them with the ``ak-`` agent token — the same token the
    working ``scripts/scope_probe.py`` uses for these endpoints.
    """
    if not AGENT_TOKEN:
        raise RuntimeError(
            "Missing PROSPERA_AGENT_TOKEN — copy .env.example to .env and add your "
            "ak- agent token."
        )
    return AGENT_TOKEN
