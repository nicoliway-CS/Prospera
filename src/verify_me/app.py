"""Streamlit web UI for Verify Me (week 3) — thin entry point.

A single page that authenticates against Prospera, fetches the user's profile +
residency, and shows a live **verification badge** from real data. Later weeks
extend this same page with the official face photo (week 4) and a live selfie +
face match (week 5).

Run it with:

    streamlit run src/verify_me/app.py

This module is intentionally **thin**: it sets page config and composes the
``render_*`` helpers from ``verify_me.ui``. Following the project's design rules,
it never reads the environment or makes HTTP calls itself — that wiring lives in
``verify_me.ui.data``, which reuses:

- ``verify_me.config``   for credentials (.env)
- ``verify_me.api``      for the network (``ProsperaClient``)
- ``verify_me.profile``  for pure formatting helpers
"""

from __future__ import annotations

import logging

import streamlit as st

from verify_me.ui import (
    load_face_photo,
    load_identity,
    render_badge,
    render_header,
    render_photo,
    render_profile,
    render_sidebar,
)

logger = logging.getLogger(__name__)

# Set this once, before any other Streamlit call.
st.set_page_config(
    page_title="Verify Me",
    page_icon="🪪",
    layout="centered",
)


def main() -> None:
    render_header()
    render_sidebar()

    # One guard around the whole data-load + render flow. Any failure — missing
    # token, HTTP error, or a malformed response that trips up the render helpers
    # — surfaces as a single friendly st.error. The traceback goes to the server
    # console (via logging), never onto the page.
    try:
        person, residency = load_identity()
        render_badge(person, residency)
        if person:  # skip the detail block until the profile is filled out
            render_profile(person, residency)

            # The official photo is fetched in its own guard: a failure here
            # (missing scope, expired signed URL, or no verification on file)
            # must not take down the badge + profile rendered above. download_image
            # already scrubs the signed URL, so logging the traceback is safe.
            try:
                photo = load_face_photo()
            except Exception:
                logger.exception("Failed to load official photo")
                photo = None
            render_photo(photo)
    except Exception:
        logger.exception("Failed to load/render Prospera identity")
        st.error(
            "Couldn't load your Prospera identity. Check that `.env` has a "
            "valid `PROSPERA_API_TOKEN`, then use **Refresh data** in the sidebar."
        )


if __name__ == "__main__":
    main()
