# Resilience & Scalability Patterns

## Table of Contents

- [Error Handling Architecture](#error-handling-architecture)
- [Resilience Patterns](#resilience-patterns)
- [Error Handling Anti-Patterns](#error-handling-anti-patterns)
- [Scalability Anti-Patterns](#scalability-anti-patterns)

## Error Handling Architecture

### Characteristics of Good Error Architecture

1. **Typed errors with context** — domain-specific error types carrying error codes, retry eligibility, and correlation IDs. Not generic `Error("something went wrong")`.
2. **Explicit propagation** — errors surface through return types (`Result`/`Either`) or checked exceptions, never silently swallowed.
3. **Idempotency at boundaries** — any operation that may be retried is safe to repeat (same result regardless of call count).
4. **Correlation IDs** — every request carries a trace ID propagated across all downstream calls and logs.
5. **Deadline propagation** — if a top-level request has a 2s budget and 500ms is used, downstream calls receive a 1.5s deadline.

### Error Boundary Design

- Define clear error boundaries at service/module edges
- Translate internal errors to appropriate external representations at boundaries
- Never expose internal error details (stack traces, SQL errors) to external consumers
- Map domain errors to appropriate HTTP status codes / gRPC codes at the adapter layer

## Resilience Patterns

### Circuit Breaker

Three states: **Closed** (normal) → **Open** (fail-fast) → **Half-open** (probe).

**When to look for it:** Any code calling external services (HTTP clients, database connections, third-party APIs).

**Absence indicators:**
- External dependency calls with no timeout
- A single slow downstream service causes thread pool exhaustion
- No fallback behavior when a dependency is unavailable
- Cascading failures across services

**Anti-patterns in implementation:**
- Single global circuit breaker for all operations
- Thresholds too sensitive (trips on small sample sizes)
- No monitoring/alerting on circuit state changes

### Retry with Exponential Backoff + Jitter

Formula: `delay = min(cap, base * 2^attempt) + random_jitter`

**Jitter** prevents thundering herd on recovery.

**Anti-patterns:**
- Retrying non-idempotent operations (payment charges, account debits)
- Retrying 4xx client errors (will never succeed)
- Not respecting open circuit breakers during retry
- No cap on retry count
- No backoff (tight retry loops amplify load)

### Bulkhead

Isolate resources by operation type — separate thread pools / connection pools for critical vs non-critical paths.

**Absence indicators:**
- All operations share a single thread/connection pool
- One slow external call starves critical business logic
- No resource isolation between tenants or operation types

### Saga Pattern

For multi-step operations across services, define compensating transactions for each step.

**Absence indicators:**
- Distributed transactions using 2PC (fragile, locks resources)
- Operations spanning service boundaries with no rollback strategy
- Partial failures leave data in inconsistent state

## Error Handling Anti-Patterns

| Anti-Pattern | Detection | Severity |
|-------------|-----------|----------|
| **Silent swallow** | `catch(e) {}` or `catch(e) { log(e) }` with no re-throw or user feedback | High |
| **Retry amplification** | Service A retries 3x → calls B which retries 3x → 9x load on C | High |
| **Missing timeout** | HTTP/DB client calls with no timeout configured | High |
| **Error type erasure** | All errors caught as generic `Exception` and re-thrown as `RuntimeException` | Medium |
| **Cascade failure** | No circuit breaker; downstream failure propagates to all upstream callers | High |
| **Non-idempotent retry** | Mutation operations retried without idempotency keys | Critical |
| **Missing correlation ID** | Errors logged without trace context; impossible to reconstruct request path | Medium |
| **Overly broad catch** | Single catch block handles all error types identically | Medium |

## Scalability Anti-Patterns

### N+1 Query Problem

For database-specific N+1 detection heuristics and framework patterns, see `logic/database-patterns.md`. At the architecture level, N+1 queries signal missing batching abstractions or ORM misconfiguration.

**Severity:** High — O(N) database round-trips degrade severely under load.

### N+1 Service Call Pattern

Same downstream service called once per item instead of in bulk.

**Detection:**
- For-each loop making an HTTP/gRPC call per item
- No batch/bulk API usage where one exists
- \> 5 service calls per end-to-end use case

**Severity:** High — latency accumulates; multiplies under load.

### Synchronous Call Chains

A single user request initiates serial chain of synchronous calls across multiple services.

**Detection:**
- Request dependency graph with depth > 3 sequential synchronous hops
- Any service with I/O wait > 50% of total request time
- No async/parallel execution where steps are independent

**Severity:** High — tail latency compounds multiplicatively.

### Stateful Services

Services storing session or request state in memory, preventing horizontal scaling.

**Detection:**
- In-process session stores (not Redis/external cache)
- Class-level mutable state accessed across requests
- Singleton services with mutable fields modified per-request
- Sticky session requirements in load balancer config

**Severity:** High — cannot scale horizontally.

### Missing Caching Layer

Expensive computations or database reads repeated on every request.

**Detection:**
- Repeated identical queries in logs
- No cache-aside/read-through pattern
- Expensive aggregate queries on hot paths
- Static/reference data fetched from DB on every request

**Severity:** Medium-High.

### Tight Database Coupling

Multiple services share a single database schema.

**Detection:**
- Two or more services referencing the same database tables
- Foreign keys crossing service ownership boundaries
- Shared sequences or enums in database schema
- Schema changes require coordinated multi-service deployment

**Severity:** High — database becomes bottleneck; services cannot scale independently.

### Missing Idempotency

Mutation operations under load can be triggered multiple times but are not safe to repeat.

**Detection:**
- Mutation operations without idempotency keys
- Event consumers with no deduplication logic
- No unique constraint enforcement at service boundary
- Payment/financial operations without transaction IDs

**Severity:** Critical — data corruption under load.
