"""Tests for the network helpers in ``verify_me.api``.

We mock ``requests`` (stdlib ``unittest.mock``) so nothing hits the network. The
key behaviours under test are that a signed download URL never leaks into an
error, and that the temp file used for the download is always cleaned up.
"""

import os
from unittest import mock

import pytest
import requests

from verify_me import api

# A realistic signed URL: the query string is the sensitive part that must never
# surface in logs or exceptions.
SIGNED_URL = "https://cdn.example.com/face.jpg?sig=SECRETSIGNATURE&exp=9999999999"


def test_download_image_error_never_leaks_signed_url():
    """A failed download raises a generic error — not one containing the URL.

    ``requests`` embeds the full URL in its exception message, so a naive re-raise
    would leak the signed URL to ``logger.exception``. Verify the sanitisation.
    """
    boom = requests.HTTPError(f"403 Client Error for url: {SIGNED_URL}")
    with mock.patch("verify_me.api.requests.get", side_effect=boom):
        with pytest.raises(RuntimeError) as excinfo:
            api.download_image(SIGNED_URL)

    message = str(excinfo.value)
    assert SIGNED_URL not in message
    assert "SECRETSIGNATURE" not in message
    # The original URL-bearing exception is suppressed from the chain, too.
    assert excinfo.value.__cause__ is None
    assert excinfo.value.__suppress_context__ is True


def test_download_image_returns_bytes_and_removes_temp_file():
    response = mock.Mock()
    response.content = b"\x89PNG image-bytes"
    response.raise_for_status = mock.Mock()

    real_mkstemp = api.tempfile.mkstemp
    created_paths = []

    def tracking_mkstemp(*args, **kwargs):
        fd, path = real_mkstemp(*args, **kwargs)
        created_paths.append(path)
        return fd, path

    with mock.patch("verify_me.api.requests.get", return_value=response), mock.patch(
        "verify_me.api.tempfile.mkstemp", side_effect=tracking_mkstemp
    ):
        result = api.download_image(SIGNED_URL)

    assert result == b"\x89PNG image-bytes"
    # The temp file was created and then cleaned up in the finally block.
    assert created_paths
    assert not os.path.exists(created_paths[0])
