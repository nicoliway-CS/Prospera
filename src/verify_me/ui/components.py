"""Reusable render helpers for the Verify Me page.

Each ``render_*`` function takes plain dicts (the JSON from ``api.py``) and draws
Streamlit widgets. Formatting logic is delegated to the pure ``profile`` helpers;
credential/network status is read from ``config`` and the cached ``data`` seams.
These helpers never read the environment or make HTTP calls themselves.
"""

from __future__ import annotations

import streamlit as st

from verify_me import config, profile

from .data import load_identity

# UI constant: maps a residency state to its badge presentation. The boolean key
# is whether ``residency["activeResidency"]`` is set — an active residency is the
# verified happy path (green); anything else is shown red.
_BADGE = {
    True: ("✅", "Identity verified", st.success),
    False: ("❌", "Residency not active", st.error),
}


def render_header() -> None:
    """Page title + tagline."""
    st.title("🪪 Verify Me")
    st.caption("Sign in with Prospera — with a biometric check on top.")


def render_sidebar() -> None:
    """Connection / credential status, kept out of the main column."""
    with st.sidebar:
        st.header("Connection")
        base_url = getattr(config, "BASE_URL", None) or "(not configured)"
        st.caption(f"Base URL: `{base_url}`")
        token = getattr(config, "AGENT_TOKEN", None)
        st.caption("Agent token: " + ("✅ set" if token else "❌ missing"))
        if st.button("Refresh data"):
            # Clear the cached fetch so the next run pulls fresh data.
            load_identity.clear()
            st.rerun()


def render_badge(person: dict, residency: dict) -> None:
    """Render the week-3 verification badge from real profile + residency data.

    Week 3 scope: the badge reflects *identity + residency* status. The
    biometric match (week 5) layers a confidence score on top of this later.
    """
    person = person or {}

    # The agent token resolves to your identity, but `natural-person` comes back
    # empty until you complete your profile in the e-Próspera portal. Treat that
    # as an expected "not set up yet" state, not an error.
    if not person:
        st.info(
            "ℹ️ Your Prospera profile isn't filled out yet. Complete your "
            "natural-person profile in the e-Próspera portal, then use "
            "**Refresh data** in the sidebar."
        )
        return

    status = profile.residency_status(residency)
    name = person.get("name") or person.get("givenName") or "Unknown"
    rpn = person.get("residentPermitNumber") or "—"

    is_active = bool((residency or {}).get("activeResidency"))
    emoji, label, present = _BADGE[is_active]
    present(f"{emoji} {label} — **{name}** · RPN {rpn} · {status}")

    # TODO (week 5): once the face match runs, show match / no-match + the
    # confidence score here (e.g. st.metric("Face match confidence", ...)).


def render_profile(person: dict, residency: dict) -> None:
    """Show the formatted profile summary and a raw-data expander."""
    st.subheader("Profile")
    st.text(profile.format_profile(person, residency))

    with st.expander("Raw API response"):
        st.json({"natural-person": person, "residency": residency})


def render_photo(photo: bytes | None) -> None:
    """Show the official ID selfie photo, or a friendly note if none is on file.

    The photo is the reference image the week-5 face match will compare a live
    selfie against. ``photo`` is ``None`` when there's no approved verification on
    file (``documents.face`` was null) or the fetch failed — both are expected
    states here, not errors.
    """
    st.subheader("Official photo")
    if photo:
        st.image(photo, caption="Official ID photo", width=200)
    else:
        st.info(
            "ℹ️ No official photo on file yet. Complete ID verification in the "
            "e-Próspera portal, then use **Refresh data** in the sidebar."
        )
