# Tech Stack

## Summary

| Layer | Technology | Status | Purpose |
|-------|-----------|--------|---------|
| Language | **Python 3.11+** | in use | Everything |
| HTTP | **requests** | in use | Calls to the Prospera API |
| Config | **python-dotenv** | in use | Load secrets from `.env` |
| Packaging | **setuptools** + `pyproject.toml` | in use | `src/` layout, editable install |
| Testing | **pytest** | configured | Unit tests for pure helpers |
| Web UI | **Streamlit** | scaffolded (week 3) | Browser interface + verification badge |
| Face match | **DeepFace** | planned (week 5) | Compare official photo vs. live selfie |
| VCS / release | **Git + GitHub** | in use | Source control; tagged release in week 6 |

## In use today

- **Python 3.11+** — minimum version pinned in `pyproject.toml`
  (`requires-python = ">=3.11"`).
- **requests** (`>=2.32`) — the HTTP client behind `ProsperaClient`.
- **python-dotenv** (`>=1.0`) — loads `.env` into the environment so `config.py`
  can read credentials.
- **pytest** (`>=8.0`, dev dependency) — test runner. Config lives in
  `pyproject.toml` under `[tool.pytest.ini_options]` (`pythonpath = ["src"]`,
  `testpaths = ["tests"]`), so tests import the package and need no manual path
  setup.
- **setuptools** — build backend; package discovery is configured for the
  `src/` layout.

Pinned transitive runtime deps live in `requirements.txt`
(`certifi`, `charset-normalizer`, `idna`, `urllib3` alongside `requests` and
`python-dotenv`).

## Scaffolded (optional extra, not in base install)

- **Streamlit** (`>=1.40`, `ui` extra) — turns the script into a web app: a page
  that shows a live verification badge from real data, and later hosts the
  webcam selfie capture. The UI is scaffolded under `src/verify_me/ui/` with a
  branded theme in `.streamlit/config.toml`. It is a deferred dependency
  (`pip install -e ".[ui]"`), kept out of the pinned base install. The page
  becomes fully live once the week-2 `config`/`api`/`profile` stubs are filled in.

## Planned (not yet installed)

- **DeepFace** (week 5) — the ML core. Runs face detection + embedding +
  comparison between the official Prospera photo and the captured selfie, with a
  tunable match threshold. Pulls in heavier transitive dependencies (e.g. a
  TensorFlow/Keras backend), so it is deliberately deferred until needed.

## Dependency management

Two complementary files:

- **`pyproject.toml`** — the source of truth for declared dependencies and the
  preferred install path: `pip install -e ".[dev]"`.
- **`requirements.txt`** — pinned versions for a reproducible `pip install -r`
  if you prefer not to use the editable install.

## Tooling

- **Claude Code** — AI coding agent used during development.
- **VS Code** + Python extension — recommended editor.
- A local **virtual environment** (`venv/`) holds installed packages and is
  gitignored.
