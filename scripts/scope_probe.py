import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE = (
    os.getenv("PROSPERA_BASE_URL")
    or os.getenv("base_url")
    or "https://staging-portal.eprospera.com"
)
AK = os.getenv("PROSPERA_AGENT_TOKEN") or os.getenv("myAgentToken")
H = {"Authorization": f"Bearer {AK}", "Content-Type": "application/json"}

SAMPLE_RPN = "80000000000012"


def show(label, scope, method, path, **kw):
    url = f"{BASE}{path}"
    try:
        r = requests.request(method, url, headers=H, timeout=30, **kw)
    except Exception as e:
        print(f"\n### {label}  [{scope}]\n{method} {path}\n  ERROR: {e}")
        return None
    print(f"\n### {label}  [{scope}]")
    print(f"{method} {path} -> {r.status_code}")
    body = r.text
    try:
        body = json.dumps(r.json(), indent=2)
    except Exception:
        pass
    if len(body) > 1500:
        body = body[:1500] + "\n...[truncated]"
    print(body)
    return r


print(f"BASE = {BASE}")
print(f"Agent key = {AK[:8]}...{AK[-4:]}")

# --- READ scopes ---
show("Person details", "agent:person.details.read", "GET",
     "/api/v1/me/natural-person")
show("Person residency", "agent:person.residency.read", "GET",
     "/api/v1/me/natural-person/residency")
for p in ["/api/v1/me/natural-person/id-verification",
          "/api/v1/me/id-verification",
          "/api/v1/me/id_verification"]:
    r = show("ID verification", "agent:person.id_verification.read", "GET", p)
    if r is not None and r.status_code != 404:
        break

# verify_rpn
show("Verify RPN", "agent:verify_rpn", "POST",
     "/api/v1/verify_rpn", json={"rpn": SAMPLE_RPN})

# registry search
search = show("Registry search", "agent:registry.search", "POST",
              "/api/v1/registries/legal_entities/search",
              json={"query": "a"})

# Try to discover an entity id from search results to test entity reads
entity_id = None
if search is not None and search.status_code == 200:
    try:
        data = search.json()
        results = data.get("results") or data.get("data") or []
        if isinstance(results, list) and results:
            entity_id = results[0].get("id") or results[0].get("legalEntityId")
    except Exception:
        pass
print(f"\n[discovered entity_id = {entity_id}]")

if entity_id:
    show("Entity read", "agent:entity.read", "GET",
         f"/api/v1/legal_entities/{entity_id}")
    show("Entity documents", "agent:entity.documents.read", "GET",
         f"/api/v1/legal_entities/{entity_id}/documents")

# application list (read)
show("Application list", "agent:entity.application.read", "GET",
     "/api/v1/legal_entity_applications")

# --- WRITE scopes (NON-DESTRUCTIVE probe: empty/invalid body so nothing is created) ---
# 403 => scope missing; 400 => scope present but body rejected (nothing created)
show("Application create (empty-body scope probe)",
     "agent:entity.application.create", "POST",
     "/api/v1/legal_entity_applications", json={})

# pay voucher against a non-existent application id
fake_id = "00000000-0000-4000-8000-000000000000"
show("Application pay voucher (scope probe, fake id)",
     "agent:entity.application.pay", "POST",
     f"/api/v1/legal_entity_applications/{fake_id}/pay_voucher", json={})
