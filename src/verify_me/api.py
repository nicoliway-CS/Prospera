"""A thin HTTP client for the Prospera public API.

Wrap only the endpoints we need. Each method should return parsed JSON and let
HTTP errors surface to the caller.
"""


class ProsperaClient:
    """Wraps the Prospera REST API with bearer-token auth."""

    def __init__(self, base_url=None, token=None, timeout=30):
        ...  # TODO (week 2)

    def get_natural_person(self):
        """GET /api/v1/me/natural-person — the user's profile."""
        ...  # TODO (week 2)

    def get_residency(self):
        """GET /api/v1/me/natural-person/residency — residency status."""
        ...  # TODO (week 2)
