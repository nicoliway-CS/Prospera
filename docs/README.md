# Documentation

Reference docs for the **Verify Me** project. Start here, then jump to the topic
you need. These are written so an agent or new contributor can understand the
project **without reading the source code**.

| Doc | What's in it |
|-----|--------------|
| [overview.md](overview.md) | What the product is, who it's for, the 6-week plan, current status |
| [architecture.md](architecture.md) | File structure, each module's job, data flow, design rules |
| [tech-stack.md](tech-stack.md) | Languages, libraries, tooling, and why each was chosen |
| [api-reference.md](api-reference.md) | The Prospera API: auth, endpoints, request/response shapes |
| [setup.md](setup.md) | How to install, configure credentials, run, and test |

## TL;DR

Verify Me is a "Sign in with Prospera" app with a biometric check. A user
authenticates with their Prospera identity; the app fetches their profile and
official face photo, captures a live selfie in the browser, and runs a face
comparison to issue a verification badge.

- **Stack:** Python · Streamlit (UI) · DeepFace (face match)
- **Status:** scaffolded; **week 2** in progress (auth + fetch profile). Most
  application modules are intentionally stubs with `TODO`s.
- **Run:** `python -m verify_me` · **Test:** `pytest`
