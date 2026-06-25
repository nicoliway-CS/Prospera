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

## Run everything — quick reference

| Goal | Command |
|------|---------|
| CLI summary (week 2) | `python -m verify_me` |
| **Web app (week 3)** | `streamlit run src/verify_me/app.py` → http://localhost:8501 |
| Probe token scopes | `python scripts/scope_probe.py` |
| Run tests | `pytest` |

All of these read the same `.env` (loaded by `config.py`). The sections below
explain each one.

### CLI summary

```bash
python -m verify_me
```

Authenticate against the API, fetch profile + residency, and print a formatted
summary.

### Web app (Streamlit, week 3)

Streamlit is an optional extra so the base install stays light. Install it once,
then launch the page:

```bash
pip install -e ".[ui]"                       # adds streamlit (first time only)
streamlit run src/verify_me/app.py           # opens http://localhost:8501
```

The page reads your `.env` credentials (via `config.py`), fetches your profile +
residency through `ProsperaClient`, and shows a live verification badge:

- **Green badge** — identity + **active** residency (verified), with your name
  and RPN.
- **Red badge** — found, but residency is **not active**.
- **Blue notice** — *"Your Prospera profile isn't filled out yet…"*: the agent
  token resolves to you, but `natural-person` is still empty. Complete your
  natural-person profile in the e-Próspera portal, then click **Refresh data**.
- Any load failure (missing/invalid token, network error) shows a single
  friendly `st.error` — **never a raw Python traceback**.

A **spinner** ("Fetching your Prospera identity…") shows while the API loads;
data is cached for 5 minutes, and **Refresh data** in the sidebar clears it.

> Theme and server defaults live in `.streamlit/config.toml`. Stop the server
> with `Ctrl+C`. To run on another port: `--server.port 8502`.

**Which token?** The `/me/...` endpoints are authenticated with the **agent
token** (`PROSPERA_AGENT_TOKEN`, `ak-...`), not the user token — see
[api-reference.md](api-reference.md).

### Probe token scopes

```bash
python scripts/scope_probe.py
```

Reports which API scopes your tokens can reach.

## Test

```bash
pytest
```

Test discovery and the `src/` path are configured in `pyproject.toml`, so no
extra flags or `PYTHONPATH` are needed.

## Troubleshooting

- **`No module named pytest`** — run `pip install -e ".[dev]"` inside the
  activated venv.
- **`Missing PROSPERA_API_TOKEN` / `PROSPERA_AGENT_TOKEN`** — you haven't created
  `.env` or the key is blank. Copy `.env.example` and fill it in.
- **`403 "Standard API keys are not supported on this endpoint"`** — you're
  hitting `/me/...` with the `sk-` user token. Those endpoints use the **agent
  token** (`PROSPERA_AGENT_TOKEN`); the app already does this.
- **Badge shows "profile isn't filled out yet"** — expected when your
  `natural-person` record is empty (the API returns `null`). Complete your
  natural-person profile in the e-Próspera portal, then **Refresh data**.
- **Other `401`/`403` from the API** — token is invalid or lacks the required
  scope; re-check it and the endpoint's scope in
  [api-reference.md](api-reference.md).
