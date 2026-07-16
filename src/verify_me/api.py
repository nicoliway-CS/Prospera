"""A thin HTTP client for the Prospera public API.

Wrap only the endpoints we need. Each method returns parsed JSON and lets HTTP
errors surface to the caller (via ``raise_for_status``), so the UI layer can
decide how to present them.
"""

import os
import tempfile

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

    def get_id_verification(self):
        """GET /api/v1/me/natural-person/id-verification — latest approved verification.

        ``documents.face`` is a signed URL (valid ~1 hour) for the selfie image,
        or ``null`` when there's no approved verification on file.
        """
        return self._get("/api/v1/me/natural-person/id-verification")


def download_image(url, timeout=30):
    """Download the image at a pre-signed ``url`` and return its bytes.

    Deliberately uses a plain ``requests.get`` (not a ``ProsperaClient`` session):
    the URL is already signed, so it needs no bearer header — and the signed
    query string grants temporary access, so it must be treated as a secret.

    The bytes are materialised to a temp file and read back, and that temp file is
    **always removed in the ``finally`` block**. On any request failure we raise a
    generic ``RuntimeError`` with ``from None`` — ``requests`` embeds the full URL
    in its exception text, and swallowing it here keeps the signed URL out of the
    caller's logs (e.g. ``logger.exception``).
    """
    tmp_path = None
    try:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
        except requests.RequestException:
            raise RuntimeError("Failed to download the official photo.") from None

        fd, tmp_path = tempfile.mkstemp(suffix=".img")
        with os.fdopen(fd, "wb") as handle:
            handle.write(response.content)
        with open(tmp_path, "rb") as handle:
            return handle.read()
    finally:
        if tmp_path is not None and os.path.exists(tmp_path):
            os.remove(tmp_path)
