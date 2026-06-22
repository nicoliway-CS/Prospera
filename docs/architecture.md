# Architecture

## File structure

```
Prospera/
├── src/verify_me/          # the application package (importable as `verify_me`)
│   ├── __init__.py         # package marker; holds __version__
│   ├── __main__.py         # entry point for `python -m verify_me`
│   ├── config.py           # loads credentials/settings from .env
│   ├── api.py              # ProsperaClient — HTTP calls to the Prospera API
│   └── profile.py          # pure helpers that format profile/residency data
├── scripts/
│   └── scope_probe.py      # standalone tool: probe which API scopes the tokens have
├── tests/
│   ├── __init__.py
│   └── test_profile.py     # unit tests for the pure helpers (placeholder for now)
├── docs/                   # this documentation
├── pyproject.toml          # package metadata, dependencies, pytest config
├── requirements.txt        # pinned runtime dependencies
├── .env.example            # template for credentials (copy to .env)
├── .env                    # real secrets (gitignored, not in repo)
├── .gitignore
└── README.md               # top-level quickstart
```

Uses a **`src/` layout**: the package lives under `src/` so tests run against the
installed package rather than accidentally importing loose files from the repo
root.

## Module responsibilities

Each module owns exactly one concern. This separation is deliberate so the
project can grow through the 6-week roadmap without tangling.

| Module | Responsibility | Talks to network? |
|--------|----------------|-------------------|
| `config.py` | Read secrets/settings from `.env`; expose `BASE_URL`, `API_TOKEN`, `AGENT_TOKEN` and a `require_api_token()` guard. Single source of credentials. | No |
| `api.py` | `ProsperaClient` — wrap the Prospera REST endpoints we use, add bearer auth, return parsed JSON, surface HTTP errors. | **Yes** |
| `profile.py` | Pure functions that turn API dicts into human-readable strings (e.g. `residency_status()`, `format_profile()`). No I/O. | No |
| `__main__.py` | Wire it together for week 2: build a client, fetch profile + residency, print a summary. | Indirectly (via `api`) |
| `scripts/scope_probe.py` | One-off exploration tool, independent of the package; reports endpoint reachability per scope. | **Yes** |

## Data flow (week 2 target)

```
.env ──load──> config.py ──tokens──> api.ProsperaClient
                                          │
                          GET /me/natural-person ─┐
                          GET /me/.../residency ──┤
                                          │       │
                                          ▼       ▼
                                   raw JSON dicts (person, residency)
                                          │
                                          ▼
                            profile.format_profile(person, residency)
                                          │
                                          ▼
                                  printed summary (__main__.py)
```

Future weeks extend this: week 3 replaces the `print` with a Streamlit page;
week 4 adds a face-photo fetch; week 5 adds selfie capture + DeepFace comparison.

## Design rules

- **Credentials in one place.** Only `config.py` reads the environment. Other
  modules receive values or call `config`.
- **Network isolated from logic.** `api.py` is the only module that performs
  HTTP. `profile.py` is pure and therefore unit-testable without mocks.
- **Errors surface.** API methods call `raise_for_status()`-style handling so
  failures aren't silently swallowed; the entry point decides how to present them.
- **Secrets never committed.** `.env` is gitignored; `.env.example` documents the
  required keys with placeholder values.

## Configuration & environment variables

Loaded from `.env` by `config.py` (via `python-dotenv`):

| Variable | Meaning | Example |
|----------|---------|---------|
| `PROSPERA_BASE_URL` | API base URL | `https://staging-portal.eprospera.com` |
| `PROSPERA_API_TOKEN` | Personal user token (`sk-...`); authenticates `/me` calls | `sk-...` |
| `PROSPERA_AGENT_TOKEN` | Agent token (`ak-...`); used by scope probing / agent-scoped endpoints | `ak-...` |

Legacy lowercase names from week 1 (`base_url`, `mytoken`, `myAgentToken`) are
accepted as a fallback so older scripts keep working.

## How to run & test

- Run the app: `python -m verify_me`
- Run tests: `pytest` (configured via `pyproject.toml` to put `src/` on the path
  and discover tests under `tests/`).

See [setup.md](setup.md) for full install instructions.
