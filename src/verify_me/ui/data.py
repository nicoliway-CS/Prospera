"""Cached data-access seams for the Streamlit UI.

This is the **only** UI module that touches ``config`` and ``api``. It keeps the
network/credential wiring in one place so the render helpers in
``components.py`` stay pure-ish (they just take dicts and draw widgets).

Caching matters because Streamlit reruns the whole script on every interaction:

- ``@st.cache_resource`` — for the shared, non-serialisable HTTP client. Built
  once per session.
- ``@st.cache_data`` — for the serialisable values it returns (the JSON dicts).
  TTL'd so data refreshes periodically without re-hitting the API every rerun.
"""

from __future__ import annotations

import streamlit as st

from verify_me import config
from verify_me.api import ProsperaClient


@st.cache_resource(show_spinner=False)
def get_client() -> ProsperaClient:
    """Build a ProsperaClient for the /me endpoints (cached once).

    Uses the **agent token**: the personal ``sk-`` user token is rejected (403)
    on ``/api/v1/me/natural-person`` and ``/residency`` because they require
    ``agent:*`` scopes. ``require_agent_token()`` raises a clear error if it's
    missing, so the UI can surface it instead of failing deep inside a request.
    """
    config.require_agent_token()
    return ProsperaClient(base_url=config.BASE_URL, token=config.AGENT_TOKEN)


@st.cache_data(ttl=300, show_spinner="Fetching your Prospera identity…")
def load_identity() -> tuple[dict, dict]:
    """Fetch ``(person, residency)`` from the API. Cached for 5 minutes."""
    client = get_client()
    person = client.get_natural_person()
    residency = client.get_residency()
    return person, residency
