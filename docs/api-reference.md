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

- **User token** (`sk-...`) → `PROSPERA_API_TOKEN`. Acts as "you" against the
  `/api/v1/me/...` endpoints. This is what Verify Me uses.
- **Agent token** (`ak-...`) → `PROSPERA_AGENT_TOKEN`. Carries agent scopes; used
  by `scope_probe.py` and agent-scoped registry/entity endpoints.

Access is scope-gated. A `403` means the token lacks the required scope; a `400`
means the scope is present but the request body was rejected (nothing created).

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
| GET | `/api/v1/me/natural-person/id-verification` | `agent:person.id_verification.read` |
| POST | `/api/v1/registries/legal_entities/search` | `agent:registry.search` |
| GET | `/api/v1/legal_entities/{id}` | `agent:entity.read` |
| GET | `/api/v1/legal_entities/{id}/documents` | `agent:entity.documents.read` |
| GET | `/api/v1/legal_entity_applications` | `agent:entity.application.read` |
| POST | `/api/v1/legal_entity_applications` | `agent:entity.application.create` |
| POST | `/api/v1/legal_entity_applications/{id}/pay_voucher` | `agent:entity.application.pay` |

> The **official face photo** needed in week 4 is expected to come from an
> ID-verification / person endpoint; the exact field is still to be confirmed
> against the live API.

## Error handling convention

`ProsperaClient` is intended to raise on non-2xx responses (via
`requests`' `raise_for_status`), so callers handle `requests.HTTPError` rather
than inspecting status codes inline.
