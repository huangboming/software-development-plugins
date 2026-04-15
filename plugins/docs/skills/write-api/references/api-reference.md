# API Documentation — Templates & Guide

## Overview Template

Use this structure for `docs/apis/overview.md`. This is the entry point — it maps the full external API surface and points readers to per-resource detail docs.

```markdown
# API Overview

> Last updated: <date>

## API Surface

Summary of the system's external API boundary: what resource groups exist,
what protocols are used (REST, GraphQL, gRPC, events, WebSocket), primary
consumers (frontend, mobile, third-party, internal services), and base URLs
or entry points.

## Resource Groups

| Resource Group | Protocols | Base Path / Entry Point | Auth | Detail |
|----------------|-----------|------------------------|------|--------|
| Users | REST | `/api/v1/users` | Bearer | [users.md](users.md) |
| Orders | REST, Events | `/api/v1/orders` | Bearer | [orders.md](orders.md) |
| Webhooks | HTTP callbacks | N/A | HMAC | [webhooks.md](webhooks.md) |

## API Relationships

How resource groups relate — which APIs call which, shared data contracts,
event chains. Include a Mermaid diagram if 3+ groups interact.

## Common Conventions

Patterns shared across APIs:
- Versioning strategy (URL path, header, none)
- Error response format (structure and status code usage)
- Pagination pattern (cursor, offset, none)
- Authentication and authorization model
- Rate limiting (if applicable)

Only document conventions that are actually consistent. Note deviations.
```

## Resource Group Detail Template

Use this structure for each `docs/apis/<resource-group>.md`. This document describes every external-facing contract for a domain module in enough detail that a consumer can integrate without reading the source.

```markdown
# <Resource Group> API

> Last updated: <date>

## Overview

What this resource group provides, who consumes it, and what protocols it
uses. One paragraph.

## Authentication & Authorization

How consumers authenticate and what authorization model applies.
Omit if covered entirely by system-wide conventions in overview.md.

## Endpoints / Methods

### <Sub-resource or Action>

#### `<METHOD> <path>` or `<function signature>`

<One-line description.>

**Request:**

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| id | path | string | yes | Resource identifier |
| limit | query | integer | no | Max results (default: 20) |

**Request body** (if applicable):

```json
{
  "field": "type -- description"
}
```

**Response** (`200`):

```json
{
  "field": "type -- description"
}
```

**Errors:**

| Status | Code | When |
|--------|------|------|
| 404 | NOT_FOUND | Resource does not exist |
| 422 | VALIDATION_ERROR | Invalid input |

**Side effects:** <state changes, events emitted, external calls>

<Repeat for each endpoint/method.>

## Events

### <Event Name>

| Property | Value |
|----------|-------|
| Topic / Channel | `orders.created` |
| Trigger | When a new order is persisted |
| Payload schema | See below |

```json
{
  "field": "type -- description"
}
```

**Consumers:** List known consumers.

## Error Conventions

How this resource group structures errors, if different from system-wide
conventions. Omit if fully covered by overview.md.
```

## Discovery Guide

When documenting from scratch:

| What to find | Where to look |
|-------------|---------------|
| REST endpoints | Route registrations, controller files, OpenAPI/Swagger specs |
| GraphQL APIs | Schema files (`.graphql`, `.gql`), resolver directories |
| gRPC services | `.proto` files, service definitions |
| Event contracts | Event bus config, message queue setup, event handler registrations |
| WebSocket channels | Socket setup, channel/room definitions |
| Webhook callbacks | Webhook dispatch code, payload builders |
| Auth patterns | Middleware chains, guard decorators, auth config |
| Shared conventions | Error handler middleware, response formatters, validation libraries |

### Extraction steps per resource group

1. **Find the public surface** — Route registrations, schema definitions, event publishers. These are the contracts.
2. **Document each contract** — For each endpoint: what it accepts, what it returns, what can go wrong, what side effects it has.
3. **Extract types** — Read request/response types, DTOs, validation schemas. Document actual types, not inferred ones.
4. **Identify error paths** — Read error handlers, validation logic, guard clauses. Document every error a consumer might receive.
5. **Note side effects** — Events emitted, external service calls, database writes. These are hidden contracts that break integrations when changed.
6. **Check for events** — Scan for event publishers. Document topic, trigger condition, and payload.

Use concrete examples. For each non-trivial endpoint, include a realistic request/response pair with anonymized data.

## Quality Checklist

### Overview

- [ ] Every externally-facing resource group is listed — none missing
- [ ] Each entry includes protocols, base path, auth method, and link to detail doc
- [ ] Relationships documented with diagram if 3+ groups interact
- [ ] Conventions reflect actual patterns, not aspirational standards
- [ ] Deviations from conventions are noted

### Resource Group Detail

- [ ] Every public endpoint/method/event is documented — none missing
- [ ] Request parameters include location (path, query, header, body), type, and required flag
- [ ] Response structures show actual field names and types, not placeholders
- [ ] Error cases list status code, error code, and trigger condition
- [ ] Side effects explicitly stated for state-changing operations
- [ ] Types match actual code (verified, not inferred)
- [ ] At least one request/response example for non-trivial endpoints
- [ ] A consumer could integrate using only overview.md + this document
