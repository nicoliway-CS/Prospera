"""A thin HTTP client for the Prospera public API.

Wrap only the endpoints we need. Each method returns parsed JSON and lets HTTP
errors surface to the caller (via ``raise_for_status``), so the UI layer can
decide how to present them.
"""

import requests


class ProsperaClient:
    """Wraps the Prospera REST API with bearer-token auth."""

    def __init__(self, base_url=None, token=None, timeout=30):
        self.base_url = (base_url or "").rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        )

    def _get(self, path):
        """GET ``path`` relative to the base URL, raising on non-2xx."""
        response = self.session.get(f"{self.base_url}{path}", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_natural_person(self):
        """GET /api/v1/me/natural-person — the user's profile."""
        return self._get("/api/v1/me/natural-person")

    def get_residency(self):
        """GET /api/v1/me/natural-person/residency — residency status."""
        return self._get("/api/v1/me/natural-person/residency")
