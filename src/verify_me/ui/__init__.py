"""UI subpackage for the Verify Me Streamlit page.

Re-exports the public render helpers and the cached data seams so the entry
point can do ``from verify_me.ui import render_header, load_identity, ...``.
"""

from .components import (
    render_badge,
    render_header,
    render_profile,
    render_sidebar,
)
from .data import get_client, load_identity

__all__ = [
    "render_header",
    "render_sidebar",
    "render_badge",
    "render_profile",
    "get_client",
    "load_identity",
]
