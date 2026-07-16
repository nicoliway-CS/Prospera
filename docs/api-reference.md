# Prospera API Reference

What the app knows about Prospera's public API. This is a working reference
gathered from the project's own usage and the `scripts/scope_probe.py` tool — it
is **not** the official API documentation.

## Base URL

```
https://staging-portal.eprospera.com
```

(staging environment). Configured via `PROSPERA_BASE_URL`.

## Authentication

Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
Content-Type: application/json
```

Two kinds of token are used in this project:

- **Agent token** (`ak-...`) → `PROSPERA_AGENT_TOKEN`. Carries the account
  owner's identity and explicit `agent:*` scopes. **This is what Verify Me uses**
  for the `/api/v1/me/...` endpoints (scopes `agent:person.details.read` /
  `agent:person.residency.read`), and what `scope_probe.py` uses too.
- **User token** (`sk-...`) → `PROSPERA_API_TOKEN`. A "standard" key for personal
  automation. **Not** accepted on the `/me/...` person endpoints — they return
  `403 {"error":"Standard API keys are not supported on this endpoint"}`. Kept
  for other/standard endpoints.

Access is scope-gated. A `403` means the token type/scope isn't accepted; a `400`
means the scope is present but the request body was rejected (nothing created).

> **Note:** `GET /me/natural-person` returns JSON `null` (HTTP 200) until you
> complete your natural-person profile in the e-Próspera portal, even though the
> agent token already resolves to your identity (residency still returns data).

## Endpoints used by Verify Me

### GET `/api/v1/me/natural-person`

Scope: `agent:person.details.read`. Returns the authenticated user's profile.

Example response shape:

```json
{
  "givenName": "Nicolas",
  "surname": "Liway",
  "name": "Nicolas Liway",
  "residentPermitNumber": "90000000000123",
  "countryOfBirth": "Honduras",
  "citizenships": ["Honduras", "United States"],
  "dateOfBirth": "1990-05-15",
  "sex": "Male",
  "address": {
    "country": "Honduras",
    "line1": "Calle Principal 123",
    "line2": "Apt 4B",
    "city": "Roatan",
    "state": "Islas de la Bahía",
    "postalCode": "34101"
  },
  "phoneNumber": "+50498765432"
}
```

### GET `/api/v1/me/natural-person/residency`

Scope: `agent:person.residency.read`. Returns the user's residency status.

Example response shapes:

```json
{
  "wasEverResident": true,
  "activeResidency": {
    "effectiveDate": "2024-03-15T00:00:00.000Z",
    "terminationDate": null,
    "residencyType": "Resident",
    "version": "v08.29.2024"
  }
}
```

`activeResidency` is `null` when residency has lapsed:

```json
{ "wasEverResident": true,  "activeResidency": null }
{ "wasEverResident": false, "activeResidency": null }
```

Interpretation used by `profile.residency_status()`:

| `wasEverResident` | `activeResidency` | Status |
|-------------------|-------------------|--------|
| true | present | the `residencyType` (e.g. "Resident") |
| true | null | "Not active" |
| false | null | "Never a resident" |

### GET `/api/v1/me/natural-person/id-verification`

Scope: `agent:person.id_verification.read` (agent key) — the personal `sk-` user
token is not accepted. A compatibility alias with an underscore exists:
`/api/v1/me/natural-person/id_verification`.

Returns the user's **most recent approved** ID-verification session, including
signed URLs for the captured document/selfie images. Used by Verify Me (week 4)
for the official face photo.

Example response shape:

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "type": "veriff",
  "date": "2024-01-15T10:30:00.000Z",
  "status": "approved",
  "documents": {
    "documentFront": "https://…signed…",
    "documentBack": "https://…signed…",
    "face": "https://…signed…"
  }
}
```

| Field | Type | Notes |
|-------|------|-------|
| `id` | string \| null | Verification-session ID |
| `type` | string \| null | Provider, e.g. `veriff` |
| `date` | string \| null | Session timestamp |
| `status` | string \| null | e.g. `approved` |
| `documents.documentFront` | string \| null | Signed URL for the ID front image |
| `documents.documentBack` | string \| null | Signed URL for the ID back (some ID types omit it) |
| `documents.face` | string \| null | **Signed URL for the selfie image** — the official face photo |

When there is **no verification on file**, every field (including
`documents.face`) comes back `null`:

```json
{ "id": null, "type": null, "date": null, "status": null,
  "documents": { "documentFront": null, "documentBack": null, "face": null } }
```

> **Signed URLs expire after ~1 hour** and grant temporary access to the image.
> Treat them as secrets: never log them, and don't cache the URL long-term (Verify
> Me downloads and caches the image *bytes* instead — see `verify_me.api.download_image`).

Errors: `401` (`missing_token` / `invalid_token`), `403` (`missing_scopes` /
insufficient permissions), `500` (server error).

### POST `/api/v1/verify_rpn`

Scope: `agent:verify_rpn`. Verifies a Resident Permit Number.

Request:

```json
{ "rpn": "80000000000012" }
```

## Other discovered endpoints (not used by the app yet)

Surfaced by `scope_probe.py`. Listed for context; the verification flow does not
depend on them today.

| Method | Path | Scope |
|--------|------|-------|
| POST | `/api/v1/registries/legal_entities/search` | `agent:registry.search` |
| GET | `/api/v1/legal_entities/{id}` | `agent:entity.read` |
| GET | `/api/v1/legal_entities/{id}/documents` | `agent:entity.documents.read` |
| GET | `/api/v1/legal_entity_applications` | `agent:entity.application.read` |
| POST | `/api/v1/legal_entity_applications` | `agent:entity.application.create` |
| POST | `/api/v1/legal_entity_applications/{id}/pay_voucher` | `agent:entity.application.pay` |

## Error handling convention

`ProsperaClient` is intended to raise on non-2xx responses (via
`requests`' `raise_for_status`), so callers handle `requests.HTTPError` rather
than inspecting status codes inline.
