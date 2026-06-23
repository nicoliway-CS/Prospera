"""Pure helpers for turning API responses into human-readable output.

These take plain dicts (the JSON from ``api.py``) and return strings — no network
calls, so they're easy to unit-test.
"""


def residency_status(residency):
    """Summarise a residency response as a short status string."""
    ...  # TODO (week 2)


def format_profile(person, residency):
    """Build a multi-line summary of a person + their residency status."""
    ...  # TODO (week 2)
