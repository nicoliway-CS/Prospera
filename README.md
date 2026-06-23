# Verify Me

A real, working identity-verification app built on top of Prospera's public API
— *"Sign in with Prospera"* with a biometric check on top.

> **Status:** scaffolded · **Week 2 in progress** (authenticate + fetch profile).
> The application modules are currently stubs with `TODO`s; Streamlit and
> DeepFace land in later weeks.

**Stack:** Python · Streamlit (web UI) · DeepFace (face matching)

## How it works

1. A user authenticates with their **Prospera identity**.
2. The app fetches their **profile** and **official face photo** from Prospera.
3. The browser captures a **live selfie**.
4. A **face comparison** runs between the official photo and the selfie.
5. The app issues a **verification badge** (match / no-match + confidence).

## Documentation

Full project docs live in [`docs/`](docs/README.md) — read these to understand
the project without scanning the code.

| Doc | What's in it |
|-----|--------------|
| [overview.md](docs/overview.md) | What it is, the 6-week plan, current status |
| [architecture.md](docs/architecture.md) | File structure, module responsibilities, data flow |
| [tech-stack.md](docs/tech-stack.md) | Languages, libraries, tooling, and why |
| [api-reference.md](docs/api-reference.md) | Prospera API: auth, endpoints, response shapes |
| [setup.md](docs/setup.md) | Install, configure, run, test, troubleshoot |

## Project layout

```
Prospera/
├── src/verify_me/        # the application package
│   ├── config.py         # loads credentials from .env
│   ├── api.py            # ProsperaClient — HTTP calls to the API
│   ├── profile.py        # pure helpers that format profile/residency data
│   └── __main__.py       # `python -m verify_me` entry point
├── scripts/
│   └── scope_probe.py    # exploratory tool: which API scopes do our tokens have
├── tests/
│   └── test_profile.py   # unit tests for the pure helpers
├── docs/                 # project documentation
├── pyproject.toml        # package metadata, deps, pytest config
├── requirements.txt      # pinned runtime dependencies
└── .env.example          # template for your local .env (copy & fill in)
```

## Quick start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows (PowerShell/CMD)
# source venv/bin/activate     # macOS/Linux

# 2. Install the package (plus dev tools) in editable mode
pip install -e ".[dev]"

# 3. Configure your credentials
copy .env.example .env         # Windows  (cp on macOS/Linux)
#   then edit .env and paste in your real tokens
```

`.env` is gitignored — **never commit your tokens.** See [setup.md](docs/setup.md)
for the full guide.

### Run it

```bash
python -m verify_me
```

Authenticates against the Prospera API and prints your profile and residency
status.

### Test

```bash
pytest
```

## Configuration

Credentials are read from a local `.env` file (copy from `.env.example`):

| Variable | Meaning |
|----------|---------|
| `PROSPERA_BASE_URL` | API base URL (staging: `https://staging-portal.eprospera.com`) |
| `PROSPERA_API_TOKEN` | Personal user token (`sk-...`) — authenticates `/me` calls |
| `PROSPERA_AGENT_TOKEN` | Agent token (`ak-...`) — used by the scope probe |

## Roadmap

| Week | Goal |
|------|------|
| 2 | Authenticate and fetch your Prospera profile *(current milestone)* |
| 3 | Streamlit page showing a live verification badge from real data |
| 4 | Fetch & display the official face photo; first real tests |
| 5 | ML core: live selfie capture, face match, threshold tuning |
| 6 | Polish, tagged GitHub release, demo |
