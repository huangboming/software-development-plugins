# Test Writing Standards

Standards for writing new tests. Apply these when generating tests — they encode non-obvious decisions that override Claude's defaults.

## Unit Tests

### Testing Style Hierarchy

Select the highest-ranked style that fits. Do not mix styles in a single test.

| Rank | Style | When to Use | Assert On |
|------|-------|-------------|-----------|
| 1 | **Output-based** | Function returns a value | Return value |
| 2 | **State-based** | Method mutates object state | Public observable state after the call |
| 3 | **Interaction-based** | Method calls external system | The interaction, ONLY when the interaction IS the behavior (e.g., "email sent", "event published") |

Never use interaction-based testing for internal method calls between your own classes.

### Mock Strategy

| Dependency Type | Strategy |
|-----------------|----------|
| In-process collaborator | Real implementation — mocking your own code reduces regression protection |
| Your own database | Real DB or test container preferred; stub only if unavoidable |
| External third-party API | Mock at the boundary |
| System clock / random | Injectable source or time-freeze library |

**Hard limit**: no more than 2 mocks per unit test. If more are needed, the production code is Overcomplicated — recommend refactoring first.

### Test Case Design

**Boundary Value Analysis** — for every threshold, range, or limit: write three tests — at boundary, one below, one above.

**Equivalence Partitioning** — one test per input class, not one test per value. Group inputs that should produce the same behavior.

**Error Path Coverage** — for every guard clause or error return:
1. Assert the error type/code is correct
2. Assert no side effects occurred (no partial writes, no events emitted)
3. Use the exact boundary that triggers the guard, not an obviously-invalid value

## Integration Tests

Integration tests verify that multiple components work together correctly. They differ from unit tests in scope, mock strategy, and what to assert.

### What to Assert

Integration tests should verify **observable outcomes at system boundaries**, not internal state:

| Boundary | What to assert |
|----------|---------------|
| **HTTP response** | Status code AND response body structure/values — not just status |
| **Database state** | Records created/updated/deleted after the operation — query the DB in the assertion |
| **Published events** | Event type, payload structure, and key fields — use a test event consumer or spy |
| **External API calls** | That the mocked external service received the correct request (this is one of the few cases where interaction-based assertion is appropriate) |
| **Error responses** | Correct error code/format AND that no partial side effects occurred (no half-written DB records, no events published before failure) |

### Mock Strategy

Integration tests should use **real implementations** for everything under your control and mock only what you cannot:

| Dependency | Strategy |
|------------|----------|
| Your own database | **Real** — use test container or in-memory instance. This catches schema drift, query bugs, and constraint violations. |
| Your own message queue / event bus | **Real** — use test instance or in-memory broker. Assert on published messages. |
| Your own internal services | **Real** if in-process, **test double** if separate process (use contract tests to keep doubles honest) |
| External third-party APIs | **Mock** — these are outside your control. Use recorded responses or hand-crafted stubs. |
| Infrastructure (email, SMS, payment gateways) | **Mock** — avoid real side effects in tests |

### Test Structure

Integration tests follow the same Arrange-Act-Assert structure but with broader scope:

- **Arrange**: Set up DB fixtures, configure test containers, seed test data, set up mock external services
- **Act**: Call the endpoint / invoke the controller — a single operation that exercises the full path
- **Assert**: Check response AND side effects (DB state, published events, calls to external mocks)

### Key Differences from Unit Tests

- **No mock limit** — integration tests naturally involve multiple real collaborators. The mock limit (2) applies only to unit tests.
- **Slower is acceptable** — integration tests trade speed for confidence. DB setup and teardown are expected.
- **Test isolation is critical** — each test must clean up its DB state. Use transactions that roll back, or truncate tables between tests. Shared mutable DB state is the #1 source of flaky integration tests.
- **Fewer tests, broader coverage** — one integration test through a controller exercises the full path. Write fewer integration tests than unit tests, but make each one cover the critical path end-to-end.

## Shared Standards

These apply to both unit and integration tests:

- **Naming**: test names communicate **what**, **under what conditions**, **what is expected**. Avoid generic names.
- **Prefer dependency injection over patching/mocking internals** — inject dependencies at construction time.
- **Prefer parametrized tests for equivalence classes** — use the language's parametrize/table-driven mechanism.
- **Prefer deterministic time and randomness** — inject clocks and random sources.
- **Prefer rich assertion output** — use assertion forms that show diffs on failure.
