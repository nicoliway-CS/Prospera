# Setup & Usage

## Prerequisites

- Python 3.11+
- Git
- A Prospera **staging** user token (`sk-...`) and, optionally, an agent token
  (`ak-...`)

## Install

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows (PowerShell/CMD)
# source venv/bin/activate     # macOS/Linux

# 2. Install the package + dev tools (editable mode)
pip install -e ".[dev]"
```

`pip install -e ".[dev]"` reads `pyproject.toml`, installs the runtime
dependencies plus `pytest`, and makes `verify_me` importable from anywhere.

Alternative (pinned, no editable install):

```bash
pip install -r requirements.txt
```

## Configure credentials

```bash
copy .env.example .env         # Windows  (cp on macOS/Linux)
```

Then edit `.env` and fill in real values:

```ini
PROSPERA_BASE_URL="https://staging-portal.eprospera.com"
PROSPERA_API_TOKEN="sk-your-token-here"
PROSPERA_AGENT_TOKEN="ak-your-token-here"
```

`.env` is gitignored — **never commit it**.

## Run

```bash
python -m verify_me
```

Week-2 behaviour: authenticate against the API, fetch profile + residency, and
print a formatted summary. (Currently a stub — see project status in
[overview.md](overview.md).)

Explore which scopes your tokens can reach:

```bash
python scripts/scope_probe.py
```

## Test

```bash
pytest
```

Test discovery and the `src/` path are configured in `pyproject.toml`, so no
extra flags or `PYTHONPATH` are needed.

## Troubleshooting

- **`No module named pytest`** — run `pip install -e ".[dev]"` inside the
  activated venv.
- **`Missing PROSPERA_API_TOKEN`** — you haven't created `.env` or the key is
  blank. Copy `.env.example` and fill it in.
- **`401`/`403` from the API** — token is invalid or lacks the required scope;
  re-check the token and the endpoint's scope in [api-reference.md](api-reference.md).
