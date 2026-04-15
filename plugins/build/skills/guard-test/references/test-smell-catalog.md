# Test Smell Catalog

Patterns for identifying tests to remove, rewrite, or fix. Each pattern has a confidence level and action.

## Contents

- [Test Type Detection](#test-type-detection) — Classify tests as unit, integration, or E2E
- [Transform Ordering](#transform-ordering) — Apply changes in correct order (removals → structural → assertions)
- [Confidence Rules](#confidence-rules) — When to auto-apply (clear) vs. ask for approval (judgment)
- [Category 1: Removable Tests](#category-1-removable-tests) — Tautological, framework-testing, skipped, empty, duplicate
- [Category 2: Structural Anti-Patterns](#category-2-structural-anti-patterns) — Over-mocking, implementation testing, conditional logic, interdependence
- [Category 3: Weak Assertions](#category-3-weak-assertions) — No meaningful assertion, overly broad, status-code-only

## Test Type Detection

Before evaluating smells, classify each test file by type. Look for these signals:

| Type | Signals |
|------|---------|
| **Unit test** | No I/O, no DB fixtures, no HTTP clients, no container setup, mocks/stubs for all dependencies |
| **Integration test** | DB fixtures or test containers, real HTTP calls to own service, queue/event bus setup, multiple real components wired together |
| **E2E test** | Browser drivers, page objects, UI selectors, full application boot, external service URLs |

E2E tests are out of scope — skip them during analysis and note: "E2E tests detected, not evaluated by this skill."

Smell thresholds differ by test type. The tables below note where integration tests have different rules.

## Transform Ordering

Apply changes in this order within each test file:

| Order | Category | Rationale |
|-------|----------|-----------|
| 1 | Remove worthless tests | Eliminating dead weight simplifies remaining analysis |
| 2 | Fix structural anti-patterns | Fixing structure before assertions avoids rework |
| 3 | Fix weak assertions | Final polish once test structure is sound |

Within each category, process bottom-up (last test first) to preserve line numbers.

## Confidence Rules

Every transform is classified as **clear** (apply without asking) or **judgment** (present for approval).

**Default to clear when:**
- The test is provably useless (no meaningful assertion, tautological, tests framework)
- The fix is mechanical (restructure, replace assertion method)
- Removing the test cannot reduce regression protection (it had none)

**Default to judgment when:**
- The test might cover a real concern despite flawed structure
- Removal requires confirming no other test covers the same path
- The fix changes what the test verifies (not just how)
- The test is in a critical path (payments, auth, data integrity)

**Override to judgment** any normally-clear transform if:
- The test file has very few tests (removing one significantly reduces coverage)
- The test name suggests it covers a business requirement

## Category 1: Removable Tests

These apply equally to unit and integration tests.

| Pattern | Confidence | Detection Signal | Action |
|---------|------------|-----------------|--------|
| Tautological test | Clear | Asserts a value against itself, `true == true`, or mock returns what it was configured to return | Delete |
| Testing the framework | Clear | Tests ORM/router/stdlib behavior with no custom logic | Delete |
| Permanently skipped | Clear | `@skip`/`@ignore`/`xit`/`pytest.mark.skip` with no linked issue | Delete |
| Empty test body | Clear | No assertions, only comments | Delete |
| Exact duplicate | Clear | Identical setup, action, and assertion as another test | Delete one |
| Asserting on stub return | Clear | Configures mock to return X, asserts result is X | Delete |

### Subtle Tautological Forms

- `assertEqual(user.name, mock_user.name)` where `user` IS `mock_user`
- `assertTrue(result is not None)` when the return type guarantees a value
- `assertEqual(len(result), len(input))` when the function is a trivial map

### Framework Test Litmus

Ask: "If I deleted all my production code, would this test still pass with just the framework?" If yes, it tests the framework.

## Category 2: Structural Anti-Patterns

| Pattern | Confidence | Detection Signal | Fix | Integration test adjustment |
|---------|------------|-----------------|-----|----------------------------|
| Over-mocking (pure function) | Clear | Any mocks on a function with no collaborators | Remove mocks, pass real inputs | Same |
| Over-mocking (few collaborators) | Judgment | >2 mocks; test verifies wiring between mocks | Reduce to boundary mocks only | **Does not apply** — integration tests are expected to have multiple real collaborators |
| Testing implementation details | Judgment | Asserts on private fields, internal call counts, or exact call sequences | Rewrite to assert on observable output/state | Same — integration tests should assert on observable outcomes, not internal wiring |
| Conditional logic in test | Clear | `if`/`else`/`switch` inside test body | Split into separate test cases | Same |
| Test interdependence | Judgment | Shared mutable state, execution order dependency | Isolate — each test gets its own setup | **Higher priority** — shared DB state between integration tests is a common source of flaky tests |
| Assertion roulette | Judgment | >5 assertions with no grouping | Split into focused tests or add messages | **Relaxed** — integration tests legitimately assert on multiple outputs (response code + body + DB state). Flag only at >8 assertions or when assertions span unrelated concerns |

### Over-Mocking Decision Tree (Unit Tests)

```
Pure function (no I/O, no side effects)?
  → Yes: 0 mocks. Any mock = over-mocking. [Clear]
  → No: Count out-of-process dependencies
    → 0-1: At most 1 boundary mock. >1 = over-mocking. [Judgment]
    → 2+: Boundary mocks OK. Internal mocks = over-mocking. [Judgment]
```

### Mock Assessment (Integration Tests)

Integration tests should use real collaborators for components under your control. Flag mocking as a smell only when:
- The test mocks an in-process dependency that could be used directly (same smell as unit tests)
- The test mocks your own database or message queue instead of using a test instance
- The test mocks so many things that it's effectively a unit test with extra setup overhead

## Category 3: Weak Assertions

| Pattern | Confidence | Detection Signal | Fix | Integration test adjustment |
|---------|------------|-----------------|-----|----------------------------|
| No meaningful assertion | Clear | Only asserts `!= nil`, `is not None`, `toBeDefined` | Add assertions on actual return value/state | Same |
| Overly broad assertion | Judgment | `assertIsInstance(result, dict)` when specific keys matter | Narrow to specific field assertions | Same |
| String containment on error | Judgment | `assertIn("error", str(result))` | Assert on error type/code instead | Same |
| Snapshot overuse | Judgment | Large snapshot where only 2-3 fields matter | Replace with targeted field assertions | Same |
| Status-code-only assertion | Judgment | Integration test asserts HTTP status but not response body or side effects | Add body and/or DB state assertions | **Integration-specific** |
