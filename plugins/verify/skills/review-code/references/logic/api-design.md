# API Design Patterns & Anti-Patterns

Detection catalog for implementation review. Each entry: pattern name, detection heuristic, severity, risk.

## Table of Contents

- [Endpoint Design](#endpoint-design)
- [Request & Response Design](#request--response-design)
- [Pagination & Filtering](#pagination--filtering)
- [Idempotency & Safety](#idempotency--safety)
- [Versioning](#versioning)
- [Error Responses](#error-responses)

---

## Endpoint Design

### Verbs in URLs

- **Detect**: Endpoints like `/getUsers`, `/createOrder`, `/deleteItem/{id}`, `/updateProfile`
- **Severity**: Medium
- **Risk**: Violates REST noun-based conventions; HTTP method already communicates the action
- **Fix**: Use `GET /users`, `POST /orders`, `DELETE /items/{id}`, `PATCH /profiles/{id}`

### Inconsistent Naming

- **Detect**: Mixed naming across endpoints: `/user-profiles` vs `/orderItems` vs `/Product_categories`
- **Severity**: Medium
- **Risk**: Unpredictable API surface; clients must memorize each convention
- **Fix**: Pick one convention (kebab-case or snake_case) and apply consistently

### Inconsistent Pluralization

- **Detect**: `/user/{id}` alongside `/orders/{id}`; singular and plural mixed
- **Severity**: Low
- **Risk**: Confusing for consumers; harder to auto-generate clients
- **Fix**: Use plural nouns for collection resources (`/users`, `/orders`)

### Deeply Nested Resources

- **Detect**: `/organizations/{orgId}/departments/{deptId}/teams/{teamId}/members/{memberId}/permissions`
- **Severity**: Medium
- **Risk**: Tight coupling; difficult URLs to construct; often signals missing top-level resources
- **Fix**: Limit nesting to 2 levels; use query parameters or top-level resources for deeper access

### Missing Resource Identifier Validation

- **Detect**: Route accepts `{id}` parameter but no validation of format (UUID vs integer vs slug)
- **Severity**: Medium
- **Risk**: Invalid IDs reach database layer; confusing errors; potential injection vector
- **Fix**: Validate ID format at the routing layer (type annotations, regex constraints)

---

## Request & Response Design

### Inconsistent Response Envelope

- **Detect**: Some endpoints return `{"data": [...]}`, others return raw arrays `[...]`, others return `{"results": [...]}`
- **Severity**: Medium
- **Risk**: Clients must handle each format differently; adding metadata later is a breaking change
- **Fix**: Consistent envelope: `{"data": ..., "meta": ...}` or always unwrapped — pick one

### Missing or Wrong HTTP Status Codes

- **Detect**: `200 OK` for creation (should be `201`); `200` for deletion with no body (should be `204`); `500` for user input errors (should be `4xx`); `200` with error message in body
- **Severity**: High
- **Risk**: Clients can't rely on status codes for control flow; monitoring/alerting is unreliable
- **Fix**: Use semantically correct codes: 200 (OK), 201 (Created), 204 (No Content), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 409 (Conflict), 422 (Unprocessable Entity), 429 (Too Many Requests), 500 (Internal Server Error)

### Returning Internal Details in Responses

- **Detect**: Stack traces in error responses; internal IDs, database column names, or ORM model structures leaked to clients; verbose error messages in production
- **Severity**: High
- **Risk**: Information disclosure; aids attackers; couples clients to internal implementation
- **Fix**: Map internal errors to safe external messages; use error codes for machine-readable identification

### No Content-Type Negotiation

- **Detect**: Endpoint always returns JSON regardless of `Accept` header; no `Content-Type` header set on responses
- **Severity**: Low
- **Risk**: Interoperability issues; unexpected parsing failures in clients

### Accepting Unvalidated Request Bodies

- **Detect**: Request body parsed directly without schema validation; fields accessed with `request.body.fieldName` without type or presence checks
- **Severity**: High
- **Risk**: Unexpected types cause runtime errors; missing fields cause null pointer exceptions; extra fields may be persisted

---

## Pagination & Filtering

### Missing Pagination on List Endpoints

- **Detect**: `GET /items` returns all records; no `limit`/`offset`, `page`/`per_page`, or cursor parameters; `SELECT *` without `LIMIT`
- **Severity**: High
- **Risk**: Memory exhaustion; slow responses; database strain; will fail as data grows
- **Fix**: Default pagination (e.g., limit=20, max=100); cursor-based for large datasets

### Unbounded Query Results

- **Detect**: User-supplied `limit` parameter with no maximum cap; `?limit=999999` accepted
- **Severity**: Medium
- **Risk**: DoS vector; memory exhaustion; extreme response times
- **Fix**: Cap `limit` to a reasonable maximum (e.g., 100-1000)

### No Default Sorting

- **Detect**: List endpoint returns results in non-deterministic order; pagination without `ORDER BY`
- **Severity**: Medium
- **Risk**: Duplicate or missing items across pages; inconsistent results between requests

### Filter Injection

- **Detect**: User-supplied filter parameters passed directly to ORM/query builder without allowlisting
- **Severity**: High
- **Risk**: Users can filter on internal fields, access unauthorized data, or cause expensive queries

---

## Idempotency & Safety

### Non-Idempotent PUT

- **Detect**: `PUT` handler that partially updates (should use `PATCH`); `PUT` that creates new resources with server-generated IDs
- **Severity**: Medium
- **Risk**: Retries cause duplicate resources or inconsistent state; violates HTTP semantics

### Non-Idempotent Mutation Endpoints

- **Detect**: `POST /charge` with no idempotency key support; payment/transfer endpoints without deduplication; no `Idempotency-Key` header handling
- **Severity**: High (for financial/critical operations)
- **Risk**: Network retries cause duplicate charges, double-sends, or data corruption
- **Fix**: Accept idempotency key; store and check before processing; return cached response on replay

### Unsafe GET Endpoints

- **Detect**: `GET` handler that modifies state (creates records, triggers side effects, sends emails)
- **Severity**: High
- **Risk**: Browser prefetch, crawlers, and caches will trigger mutations; violates HTTP safety contract

---

## Versioning

### No Versioning Strategy

- **Detect**: No version prefix in URLs; no `Accept: application/vnd.api+json; version=2` header handling; no versioning visible anywhere
- **Severity**: Medium (for public APIs)
- **Risk**: Breaking changes affect all consumers simultaneously; no migration path

### Breaking Changes Without Version Bump

- **Detect**: Renamed fields, removed endpoints, changed response shapes in the same API version; no deprecation notices
- **Severity**: High
- **Risk**: Breaks existing clients without warning

---

## Error Responses

### Inconsistent Error Format

- **Detect**: Some errors return `{"error": "msg"}`, others `{"message": "msg"}`, others `{"errors": [...]}`; different shapes for different status codes
- **Severity**: Medium
- **Risk**: Clients can't write generic error handling; each endpoint needs special error parsing

### Missing Error Codes

- **Detect**: Error responses with only human-readable messages; no machine-readable error code or type
- **Severity**: Medium
- **Risk**: Clients can't programmatically handle specific errors; internationalization impossible; fragile string matching
- **Fix**: Include error code: `{"error": {"code": "INSUFFICIENT_FUNDS", "message": "..."}}`

### Leaking Sensitive Data in Errors

- **Detect**: Error messages that include SQL queries, file paths, stack traces, or user data from other accounts
- **Severity**: Critical
- **Risk**: Information disclosure; aids attack reconnaissance; potential PII leaks
