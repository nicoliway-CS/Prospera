# Project Overview

## What it is

**Verify Me** is a real, working identity-verification web app built on top of
**Prospera's public API**. Conceptually it is *"Sign in with Prospera"* with a
biometric check layered on top.

The end-to-end flow:

1. A user authenticates with their Prospera identity.
2. The app fetches their **profile** and **official face photo** from Prospera.
3. The browser captures a **live selfie**.
4. A **face comparison** runs between the official photo and the selfie.
5. The app issues a **verification badge** (match / no-match + confidence).

## Why it exists

It is the build project for a 6-week internship. The goal is a polished,
demoable product plus hands-on learning across HTTP/APIs, web UI, testing, and a
practical introduction to face-matching ML. No prior ML experience is assumed.

## Context

- **Prospera** is the platform whose public API backs the app. The app talks to
  the **staging** environment: `https://staging-portal.eprospera.com`.
- Identities are keyed by a **Resident Permit Number (RPN)** and exposed through
  `/api/v1/me/...` endpoints using a personal bearer token.

## Schedule & roadmap

The internship runs 6 weeks, June 6 – July 18. Each week has a concrete
deliverable:

| Week | Dates | Deliverable |
|------|-------|-------------|
| 1 | Jun 6  | Project walkthrough, API + staging credentials, first real API calls |
| 2 | Jun 15 | **(current)** Python/HTTP fundamentals: a script that authenticates and fetches the user's profile |
| 3 | Jun 22 | First product: a Streamlit page showing a live verification badge from real data |
| 4 | Jun 29 | Fetch & display the official face photo; first real tests |
| 5 | Jul 6  | ML core: live selfie capture, face match, threshold tuning, accuracy eval |
| 6 | Jul 13 | Polish, tagged GitHub release, 10-minute demo |

## Current status

- The repository is **scaffolded** with a clean package layout (see
  [architecture.md](architecture.md)).
- **Week 2 is in progress.** The application modules (`config`, `api`,
  `profile`, `__main__`) currently contain **docstrings + `TODO` stubs**, not
  finished logic.
- `scripts/scope_probe.py` is a working week-1 exploratory tool that lists which
  API scopes the current tokens can reach.
- The Streamlit UI and DeepFace face-matching are **future work** (weeks 3 & 5)
  and are not yet dependencies.

## Working conventions

- Weekly Monday check-in; mid-week calls as needed.
- Credentials live only in a local, gitignored `.env`. Never commit tokens.
- AI coding tools (Claude Code) assist, but the author reads and understands all
  generated code.
