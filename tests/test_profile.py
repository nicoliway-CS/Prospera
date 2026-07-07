"""Unit tests for the pure profile helpers.

These take plain dicts (the JSON shapes from ``api.py``) and return strings/URLs,
so they need no network or mocks.
"""

from verify_me import profile


def test_residency_status_active_returns_type():
    residency = {"wasEverResident": True, "activeResidency": {"residencyType": "Resident"}}
    assert profile.residency_status(residency) == "Resident"


def test_residency_status_lapsed_and_never():
    assert profile.residency_status({"wasEverResident": True, "activeResidency": None}) == "Not active"
    assert profile.residency_status({"wasEverResident": False, "activeResidency": None}) == "Never a resident"


def test_format_profile_renders_expected_lines():
    person = {
        "name": "Nicolas Liway",
        "residentPermitNumber": "90000000000123",
        "dateOfBirth": "1990-05-15",
        "citizenships": ["Honduras", "United States"],
    }
    residency = {"wasEverResident": True, "activeResidency": {"residencyType": "Resident"}}

    summary = profile.format_profile(person, residency)

    assert "Name:        Nicolas Liway" in summary
    assert "RPN:         90000000000123" in summary
    assert "Residency:   Resident" in summary
    assert "Born:        1990-05-15" in summary
    assert "Citizenship: Honduras, United States" in summary


def test_face_photo_url_present():
    id_verification = {
        "status": "approved",
        "documents": {"face": "https://cdn.example.com/face.jpg?sig=abc"},
    }
    assert profile.face_photo_url(id_verification) == "https://cdn.example.com/face.jpg?sig=abc"


def test_face_photo_url_missing_returns_none():
    # The "no verification on file" response is all-null, including documents.face.
    all_null = {
        "id": None,
        "status": None,
        "documents": {"documentFront": None, "documentBack": None, "face": None},
    }
    assert profile.face_photo_url(all_null) is None
    # Defensive: a None response or a missing documents object must not raise.
    assert profile.face_photo_url(None) is None
    assert profile.face_photo_url({}) is None
