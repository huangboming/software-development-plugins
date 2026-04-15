# Test Strategy Reference

What to test, how to evaluate coverage, and what to flag as waste.

## Table of Contents

- [What to Test: Priority Tiers](#what-to-test-priority-tiers)
- [Scenario Coverage Framework](#scenario-coverage-framework)
- [Test Waste Patterns](#test-waste-patterns)
- [Test Pyramid Assessment](#test-pyramid-assessment)

---

## What to Test: Priority Tiers

Not all code deserves equal test investment. Prioritize by damage potential.

### Tier 1 — Must Test (Critical)

Code where a bug causes data corruption, financial loss, security breach, or cascading system failure.

- **Core business rules**: Domain validation, invariant enforcement, state machine transitions, authorization logic, pricing/billing calculations
- **Data mutation paths**: Create/update/delete operations on primary entities, batch operations, cascading writes
- **Financial and metered operations**: Payment processing, credit/debit, usage tracking, quota enforcement
- **Security boundaries**: Authentication flows, permission checks, input sanitization at trust boundaries, token validation

**Detection**: Functions that write to databases, call payment APIs, check permissions, or enforce business invariants. High fan-in (many callers depend on correctness).

### Tier 2 — Should Test (High)

Code where a bug causes incorrect behavior visible to users or breaks integrations.

- **Complex pure functions**: Functions with multiple branches, non-trivial transformations, conditional logic. If you need to think to predict the output, it needs tests
- **Integration boundaries**: External API client wrappers, message serialization/deserialization, webhook payload handling, event publishing
- **Error handling paths**: Retry logic, fallback behavior, error translation, graceful degradation
- **Query logic**: Complex filters, aggregations, pagination logic, search ranking

**Detection**: Functions with cyclomatic complexity > 5, multiple return paths, or conditional chains. Functions that serialize/deserialize data crossing system boundaries.

### Tier 3 — Test If Complex (Medium)

Code where bugs cause inconvenience but are quickly caught and fixed.

- **Mapping and transformation**: DTO conversions, response shaping, data format conversions — but only when the mapping is non-trivial (conditional fields, computed values)
- **Configuration-driven behavior**: Feature flag evaluation, A/B test bucketing, dynamic routing
- **Orchestration with branching**: Workflow coordinators that make decisions, not just call steps in sequence

**Detection**: Functions with conditional logic that affects output shape or behavior. Skip if the mapping is mechanical (field-to-field copy).

### Tier 4 — Do Not Test (Low/None)

Code where tests add maintenance cost but catch no real bugs.

- **Trivial getters/setters**: Property access with no logic
- **Data classes and DTOs**: Plain structs/dataclasses with no methods
- **Framework glue**: Route registration, middleware wiring, dependency injection setup
- **One-line delegations**: Functions that only call another function with the same arguments
- **Generated code**: ORM migrations, API client stubs, protobuf output
- **Configuration constants**: Static config values, enum definitions without logic

**Key principle**: If removing the test would never allow a real bug to reach production, the test is waste.

---

## Scenario Coverage Framework

For each tested function, evaluate coverage across three scenario categories.

### Happy Path

The primary success scenario with valid, typical inputs.

**What to check:**
- At least one test verifies the main success case end-to-end
- Inputs are realistic (not `"test"`, `123`, `"foo"` — use domain-relevant values)
- Assertions verify the meaningful output, not just "no error thrown"
- Side effects are verified (database writes, events published, API calls made)

**Red flag**: Test only asserts no exception was raised, or only checks return type without checking value.

### Sad Path

Expected failure modes — what happens when things go wrong in foreseeable ways.

**What to check:**
- Invalid input: wrong types, missing required fields, out-of-range values
- Missing data: entity not found, empty query results, null references
- Authorization failures: wrong user, insufficient permissions, expired token
- Dependency failures: external API returns error, database connection lost, timeout
- Business rule violations: insufficient balance, duplicate submission, expired resource

**Red flag**: All test inputs are valid. No test exercises an error code path. No test verifies error messages or error types.

### Edge Cases

Boundary conditions and unusual-but-valid inputs that expose off-by-one errors, overflow, and assumption violations.

**What to check for each data type:**

| Type | Edge Cases |
|------|------------|
| **Numbers** | Zero, negative, max int/float, fractional values (for integers), NaN/Infinity |
| **Strings** | Empty string, whitespace-only, unicode/emoji, very long strings, strings with special characters (`<`, `'`, `\n`, `\0`) |
| **Collections** | Empty list/map, single element, duplicate elements, very large collections |
| **Dates/Times** | Midnight, DST transitions, leap years, time zone boundaries, epoch, far-future dates |
| **Booleans** | Both true and false (not just the "expected" value) |
| **Nullable** | Null/nil/None explicitly, especially when the type system allows it |
| **Concurrency** | Concurrent mutations on the same entity, race between read and write |

**Red flag**: All test inputs are "normal" middle-of-the-road values. No test uses empty, zero, negative, or maximum inputs.

---

## Test Waste Patterns

Tests that cost maintenance effort without catching real bugs. Flag these for removal or replacement.

### Testing the Framework

- **Detect**: Test verifies that a route exists, that middleware runs, that DI resolves, or that ORM saves to database — behaviors guaranteed by the framework
- **Example**: `assert response.status_code == 200` on an endpoint with no business logic, just returning a hardcoded response
- **Why waste**: The framework is already tested. These break on upgrades without catching application bugs

### Testing Mock Wiring

- **Detect**: Test sets up mocks, calls the function, then asserts the mocks were called with expected arguments. No assertion on output or state
- **Example**: `mock_repo.save.assert_called_once_with(user)` without checking that the user was constructed correctly
- **Why waste**: Verifies the function's internal wiring, not its behavior. Breaks on any refactor

### Testing Trivial Code

- **Detect**: Test for a getter, setter, constructor, or data class with no logic. Test for a function that is a one-line delegation
- **Example**: `assert user.name == "Alice"` immediately after `user = User(name="Alice")`
- **Why waste**: The language runtime guarantees this works. Test adds zero information

### Testing Constants

- **Detect**: Test asserts that a config value, enum, or constant equals its defined value
- **Example**: `assert STATUS_ACTIVE == "active"`
- **Why waste**: If the constant changes, the test changes too — it guards nothing

### Tautological Tests

- **Detect**: Test where the assertion is mathematically guaranteed by the setup. Test that asserts a mock returns what the mock was configured to return
- **Example**: `mock_service.get.return_value = user; result = mock_service.get(1); assert result == user`
- **Why waste**: The test cannot fail. It inflates coverage metrics while verifying nothing

### Snapshot Overkill

- **Detect**: Snapshot tests on large, frequently changing outputs (full API responses, HTML pages). Snapshots updated mechanically without review
- **Why waste**: Developers auto-approve snapshot changes. Test catches every change but distinguishes no change as important vs unimportant

---

## Test Pyramid Assessment

Evaluate whether the overall test distribution is healthy.

### Healthy Distribution

| Layer | Purpose | Relative Volume |
|-------|---------|-----------------|
| **Unit** | Business logic, pure functions, domain rules | Many — fast, isolated, focused |
| **Integration** | Database queries, external API contracts, message serialization | Some — verify boundaries work |
| **End-to-end** | Critical user journeys, smoke tests | Few — expensive, slow, brittle |

### Warning Signs

| Signal | Problem |
|--------|---------|
| No unit tests, many E2E tests | Inverted pyramid — slow feedback, brittle suite, hard to diagnose failures |
| All unit tests, no integration tests | Trust gap at boundaries — DB queries, API contracts untested |
| Tests require running infrastructure to pass | Integration tests masquerading as unit tests — slow, flaky |
| Test suite takes > 5 minutes for < 10K LOC | Likely too many integration/E2E tests or tests doing real I/O |
| All tests mock everything | False confidence — real integration bugs slip through |
| Tests only at the HTTP layer | Business logic only tested through the full request cycle — slow, coupled to API shape |
