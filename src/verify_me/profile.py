"""Pure helpers for turning API responses into human-readable output.

These take plain dicts (the JSON from ``api.py``) and return strings — no network
calls, so they're easy to unit-test. Everything is read with ``.get()`` so a
sparse or unexpected response never raises.
"""


def residency_status(residency):
    """Summarise a residency response as a short status string.

    See ``docs/api-reference.md``:
    - ``activeResidency`` present → its ``residencyType`` (e.g. "Resident").
    - was ever a resident but no active residency → "Not active".
    - never a resident → "Never a resident".
    """
    residency = residency or {}
    active = residency.get("activeResidency")
    if active:
        return active.get("residencyType") or "Resident"
    if residency.get("wasEverResident"):
        return "Not active"
    return "Never a resident"


def format_profile(person, residency):
    """Build a multi-line summary of a person + their residency status."""
    person = person or {}
    citizenships = person.get("citizenships") or []

    lines = [
        f"Name:        {person.get('name') or 'Unknown'}",
        f"RPN:         {person.get('residentPermitNumber') or '—'}",
        f"Residency:   {residency_status(residency)}",
        f"Born:        {person.get('dateOfBirth') or '—'}",
        f"Citizenship: {', '.join(citizenships) if citizenships else '—'}",
    ]
    return "\n".join(lines)
