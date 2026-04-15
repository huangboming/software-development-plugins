# Test Effectiveness Reference

Heuristics for evaluating whether tests would actually catch bugs — not just whether they exist or pass. Each section covers: concept, when to flag, static detection, and recommendation.

This reference supplements `test-strategy.md`. Load it when a codebase has existing tests and the question is whether those tests are effective.

## Table of Contents

- [Mutation Testing Insights (Static Approximation)](#mutation-testing-insights-static-approximation)
- [Property-Based and Fuzzing Candidates](#property-based-and-fuzzing-candidates)
- [Contract Testing at Service Boundaries](#contract-testing-at-service-boundaries)
- [Test Isolation and Determinism (Flakiness Risks)](#test-isolation-and-determinism-flakiness-risks)
- [Behavior-Driven vs Implementation-Driven Tests](#behavior-driven-vs-implementation-driven-tests)
- [Branch and Condition Coverage Without Tooling](#branch-and-condition-coverage-without-tooling)
- [Testing Concurrent and Async Code](#testing-concurrent-and-async-code)
- [Testing Error Handling Paths](#testing-error-handling-paths)
- [Test Effectiveness vs Coverage Inflation](#test-effectiveness-vs-coverage-inflation)
- [Approval and Characterization Testing](#approval-and-characterization-testing)

---

## Mutation Testing Insights (Static Approximation)

**Concept.** Mutation testing tools (PIT for Java/JVM, Stryker for JavaScript/TypeScript/C#, mutmut/Cosmic Ray for Python) generate modified versions of production code — "mutants" — and run the test suite against each one. A mutant that survives (tests still pass despite the change) reveals a gap in assertion quality. Mutation score measures the fraction of mutants killed. An AI reviewer cannot run mutations, but can reason about which code patterns would produce surviving mutants.

**When to flag.** Flag mutation risk whenever tests exist but assertions are thin — especially on arithmetic, comparison operators, conditional boundaries, or state-modifying side effects.

### Mutation Operator Patterns and What They Expose

The standard mutation operators map directly to testable patterns. For each, there is a detectable code smell in the test file.

**Conditional Boundary (`<` becomes `<=`, `>` becomes `>=`).**
Indicates off-by-one boundary conditions are untested. Production code uses `>` or `<` with a literal; tests only pass values clearly inside the boundary, never at the boundary itself.

Detection: Find comparisons like `count > 0`, `age >= 18`, `price < MAX`. Check whether any test uses exactly `0`, `18`, or `MAX` as input. If all test inputs are safely in the middle, boundary mutations survive.

**Negate Conditionals (`==` becomes `!=`, `&&` becomes `||`).**
Indicates that both branches of a condition are not independently tested. Tests only drive the "true" branch or only the "false" branch.

Detection: If a function has `if user.is_active and user.has_permission`, check whether tests exist for: active+permitted, inactive+permitted, active+not-permitted, and inactive+not-permitted. If only the fully-permitted case is tested, negation mutations survive.

**Return Value Mutations (return `true` replaced with `false`, return `0` with `1`, return non-null with `null`).**
Indicates the test calls the function but does not assert the return value — or asserts only loosely (e.g., asserts truthy instead of exactly `true`).

Detection: Tests that call a function and assert only `assertNotNull(result)` or `assert result` without checking the specific value. Any test whose assertion would pass for the wrong return value.

**Void Method Call Removal (call deleted entirely).**
Indicates that the side effect of calling a void method is not verified. Audit trails, event publishing, cache invalidation, and metric emission are common victims.

Detection: Production code calls `eventBus.publish(event)` or `auditLog.record(action)`. Test does not assert the call occurred. This is distinct from mock wiring waste — here the concern is that a meaningful side effect (external event publishing, audit log) has no test coverage at all.

**Arithmetic Operator Replacement (`+` becomes `-`, `*` becomes `/`).**
Indicates financial, metered, or computed values are asserted at too coarse a granularity (e.g., only that the result is greater than zero, not that it equals the expected amount).

Detection: Functions that calculate totals, discounts, interest, or scores. Tests that assert `result > 0` or `result is not None` rather than `result == expected_value`.

**Increment/Decrement Replacement.**
Counters and loop logic are not tested with values that exercise off-by-one behavior.

Detection: Loop termination logic, retry counters, pagination offset calculations. Tests that only verify the happy-path iteration count.

### Summary Heuristic for Surviving Mutants

A test is likely to let mutants survive when:
- It asserts presence or type rather than specific value (`assertNotNull` instead of `assertEqual(42, result)`)
- It tests only one branch of a boolean condition
- It uses inputs that are far from boundary values (e.g., `count = 100` when the boundary is `count = 0`)
- It verifies function was called but not what was done with the call's output
- It has more setup than assertion lines

### Tools by Language

| Language | Tool |
|----------|------|
| Java/Kotlin | PIT (pitest.org) |
| JavaScript/TypeScript | Stryker (stryker-mutator.io) |
| C# | Stryker.NET |
| Python | mutmut, Cosmic Ray |
| Go | go-mutesting |
| PHP | Infection |
| Ruby | mutant |

### Recommendation Text

> The tests for `<function>` assert `<weak assertion>`. A mutation replacing `<operator>` with `<mutated operator>` would survive — the test cannot distinguish correct from incorrect behavior here. Add an assertion that verifies the exact computed value, and add a test case at the boundary `<value>`.

---

## Property-Based and Fuzzing Candidates

**Concept.** Property-based testing (QuickCheck/Hypothesis/fast-check/PropTest) generates hundreds or thousands of random inputs and verifies that a stated invariant — a "property" — holds for all of them. It complements example-based tests by exploring the input space systematically rather than relying on the developer to anticipate edge cases manually. An AI reviewer cannot generate or run random inputs, but can identify functions that are strong candidates for this approach.

**When to flag.** Flag when a function: (1) has a large or continuous input space, (2) satisfies a mathematical or logical invariant independent of specific values, (3) is a serialization/deserialization pair, or (4) has example-based tests that cover only a handful of inputs for a function that accepts arbitrary data.

### Function Archetypes That Benefit Most

**Encode/Decode and Serialization Roundtrips.**
Property: `decode(encode(x)) == x` for all valid `x`. This catches asymmetries that example tests miss because developers typically test only the values they already encoded.

Detection: Functions named `serialize`/`deserialize`, `encode`/`decode`, `marshal`/`unmarshal`, `toJson`/`fromJson`, `pack`/`unpack`. Tests only verify a small handful of hardcoded examples.

**Sorting, Ranking, and Ordering.**
Properties: output length equals input length; output is a permutation of input; adjacent elements satisfy the ordering predicate; idempotent (sorting an already-sorted list returns the same list).

Detection: Functions that reorder collections. Example tests typically only verify one specific ordering.

**Set and Arithmetic Invariants.**
Properties: commutativity (`f(a,b) == f(b,a)`), associativity, identity element (`f(x, identity) == x`), idempotence (`f(f(x)) == f(x)`).

Detection: Functions that merge collections, combine permissions, or aggregate values. The invariant is often implicit in the domain.

**Validation Functions.**
Property: every input accepted as valid should pass all invariant checks; every input rejected as invalid should fail at least one check; the validation decision is deterministic.

Detection: Functions named `validate`, `is_valid`, `check`, `assert_valid`. Example tests often cover only a few specific valid and invalid cases; a fuzzer finds inputs that bypass or incorrectly trigger validation.

**State Machine Transitions.**
Property: applying a sequence of valid transitions always leaves the entity in a valid state; applying an invalid transition in any state always results in an error.

Detection: Enums with `PENDING`, `ACTIVE`, `CANCELLED` style states. Functions that accept a state and return a new state. Tests only verify specific transitions; arbitrary sequences are untested.

**String Parsing and Formatting.**
Property: any string produced by the formatter should be parseable back to the original value; formatting the same value twice produces the same result.

Detection: Date formatters, currency formatters, query builders, URL encoders.

### Detection Heuristic

Flag a function for property-based testing when:
- It accepts numbers, strings, or collections without tight domain constraints
- Its test file has fewer than 5 example inputs for a function with a large valid input space
- The function implements a mathematical or logical invariant that could be stated as "for all X, property(f(X)) holds"
- It is a serialization/deserialization pair with only example-based tests

### Tools by Language

| Language | Library |
|----------|---------|
| Python | Hypothesis |
| JavaScript/TypeScript | fast-check |
| Java | jqwik, QuickTheories |
| Kotlin | Kotest property testing |
| Scala | ScalaCheck |
| Go | gopter, rapid |
| Rust | proptest, quickcheck |
| Haskell | QuickCheck, Hedgehog |
| C# | FsCheck |

### Recommendation Text

> `<function>` operates over a large input space but is only tested with `<N>` specific examples. The function satisfies the invariant `<describe invariant>` — this is a strong candidate for property-based testing. A property test with Hypothesis/fast-check/jqwik would explore the input space systematically and is likely to find edge cases the current examples miss.

---

## Contract Testing at Service Boundaries

**Concept.** Contract testing verifies that a service consumer and provider agree on the shape, semantics, and behavior of their shared interface — independently, without requiring both services to run simultaneously. Consumer-driven contract testing (Pact, Spring Cloud Contract) lets the consumer define what it expects; the provider verifies it satisfies those expectations in isolation. This is distinct from integration testing, which requires both services to be running and coordinated.

**When to flag.** Flag when a codebase: (1) is one microservice that calls other services via HTTP or message queues, (2) the integration tests are absent or require running downstream services, (3) external API contracts are consumed without pinned schema validation, or (4) a service is consumed by multiple other teams.

### Signals That Contract Tests Are Missing

**HTTP Clients Without Schema Pinning.**
Production code calls an external service and deserializes the response. No contract or schema test pins the expected response shape. The only test is an integration test that mocks the entire client or calls a real staging environment.

Detection: Classes or functions named `*Client`, `*Gateway`, `*HttpAdapter`, `*ApiClient`. Look for how the response is deserialized — if it's direct field mapping without a schema validator, a breaking change in the provider goes undetected until runtime.

**Shared Message Schemas Without Consumer Tests.**
A service publishes events or messages. Multiple consumers are implied (fan-out queue, Kafka topic, SNS). No test verifies that the published payload matches what consumers expect.

Detection: `eventBus.publish()`, `kafka.produce()`, `sns.publish()` calls. If the payload is constructed inline and not tested against a schema or consumer expectation, any field rename or type change is a silent breaking change.

**Integration Tests That Require Both Services Running.**
Integration tests that spin up both the service under test and a real downstream dependency are fragile, slow, and test the wrong thing — they test a specific version of the dependency, not the contract.

Detection: Docker Compose files in the test directory, `@SpringBootTest` that wires real HTTP clients, `TestContainers` for the downstream service (not the database — that's valid).

**Provider Change With No Consumer Verification.**
A service that has consumers but no test verifying that a proposed API change is backward-compatible. This is particularly high-risk for internal APIs consumed by multiple teams.

Detection: Endpoint that appears to have consumers (referenced in other services' client code), but the provider's test suite contains no consumer contract verification step.

### When Integration Tests Are Sufficient vs Insufficient

| Scenario | Integration Tests Sufficient? | Reason |
|----------|------------------------------|--------|
| Single consumer, owned by same team, deployed together | Often yes | Breaking changes are caught in pre-deploy integration |
| Multiple consumers across teams | No | Cannot test all consumer versions simultaneously |
| Consumer and provider deployed on different cadences | No | Integration test catches only the currently deployed version |
| Provider is a third-party API | No | Cannot run a real integration test in CI reliably; use recorded contracts |
| Async/event-driven communication | No | Integration tests cannot easily verify message schema evolution |

### Recommendation Text

> `<ServiceName>` calls `<ExternalService>` at `<location>` and deserializes the response, but there is no contract test pinning the expected schema. If the provider changes the shape of `<field>`, this service will fail silently at runtime. Consider adding a Pact consumer test that records the expected contract, or at minimum a JSON schema validation on the deserialized response. The integration test at `<test location>` is insufficient here because it `<reason: mocks the entire client / requires the real service / only tests the current version>`.

---

## Test Isolation and Determinism (Flakiness Risks)

**Concept.** A flaky test produces different results across runs without any code change. Flakiness erodes trust in the test suite: teams begin ignoring failures, real bugs hide behind the noise, and CI reliability collapses. Empirical research (Google, Microsoft, and Uber internal studies) consistently identifies async/timing issues (45% of flaky tests), concurrency (20%), and test order dependency / shared state (12%) as the dominant root causes.

**When to flag.** Flag any pattern that makes a test's outcome dependent on time, execution order, external systems, or non-deterministic behavior.

### Flakiness Risk Patterns

**Fixed Sleeps and Static Timeouts.**
`Thread.sleep(2000)`, `time.sleep(2)`, `await delay(500)`. Tests that pause for a fixed duration to wait for an async operation assume that the operation always completes within the budget. This breaks on slow CI machines, resource-constrained environments, and GC pauses.

Detection: Literal numeric arguments to sleep/delay functions inside test bodies. Arguments less than 5 seconds are especially suspect.

Recommendation: Replace with a polling assertion that retries until a condition is true (e.g., `await expect(element).toBeVisible({ timeout: 5000 })` or a retry loop with exponential backoff). Await the actual event or signal rather than waiting for elapsed time.

**Shared Mutable State Between Tests.**
Class-level or module-level variables mutated in one test and read in another. In-memory caches, singleton instances, global registries, or static fields initialized once and reused. Tests pass in isolation but fail when run together.

Detection: `static` fields (Java/C#), module-level variables (Python), class-level setup that does not reset state. `@BeforeAll` / `setUpClass` that initializes shared mutable state. Tests that do not have a corresponding teardown for any state they create.

Recommendation: Isolate state per test. Use `@BeforeEach` / `setUp` for per-test initialization. Make singletons injectable so tests can provide fresh instances. Roll back database transactions instead of expecting cleanup.

**Database Tests Without Transaction Rollback or Separate Schemas.**
Tests write to a shared database table. If the test fails mid-execution, cleanup code does not run and state leaks into subsequent tests.

Detection: Database write operations in tests (INSERT, UPDATE, DELETE) without wrapping in a transaction that rolls back, without using a unique schema/database per test run, or without explicit cleanup in a `finally`/`tearDown` block.

Recommendation: Wrap each test in a transaction rolled back at the end. Use test-specific schemas created fresh per run. Use TestContainers with a per-test database if rollback is impractical.

**Test Order Dependencies.**
Test B only passes if Test A ran first and created some state. Often seen when tests share a database, file system, or in-memory cache and rely on insertion order.

Detection: Tests that load data by name (`"admin user"`, `"test product"`) rather than by ID generated in setup. Tests in a test class that reference data created by `test_` methods not in their own setup. A `beforeAll` that populates data used by multiple tests without `afterAll` cleanup.

**Time-Dependent Tests.**
Tests that assert on wall-clock time, call `new Date()` or `time.now()` in production code without injection, or compute expected values relative to the current timestamp.

Detection: `new Date()`, `DateTime.now()`, `time.time()`, `Instant.now()` called directly in production code being tested (not in the test itself). Tests that assert a timestamp equals "now" without time injection.

Recommendation: Inject a clock interface. In tests, provide a fixed clock implementation. Never assert that a timestamp equals wall-clock time — assert it is within a range or equals an injected value.

**Network Calls in Unit Tests.**
Tests that make real HTTP calls, DNS lookups, or connect to real external services. These fail on network outages, rate limits, and timeout variations.

Detection: HTTP client constructors invoked inside test bodies without dependency injection. URLs like `https://api.stripe.com` or `https://api.example.com` appearing in test files. No mock or stub for the HTTP layer.

**Random Values Without Seed.**
Tests that use random number generators, `uuid4()`, `Math.random()`, or shuffle operations without a fixed seed. The output varies per run, making assertions unstable.

Detection: `random.random()`, `uuid.uuid4()`, `Math.random()`, `Collections.shuffle()` called in production code being tested, with no seed injection in the test.

### Summary Table

| Pattern | Detection Signal | Risk Level |
|---------|-----------------|------------|
| `sleep()` / `delay()` with literal number | Literal numeric argument | High |
| Shared mutable static/module state | `static` fields, module-level vars, class-level setup without per-test reset | High |
| Database tests without rollback/cleanup | DB writes with no transaction or `tearDown` | High |
| Test order dependency | Data loaded by name, not by ID created in test setup | Medium |
| Wall-clock time in production code | `new Date()` / `time.now()` without injection | Medium |
| Real network calls in tests | HTTP URLs in test files without mocking | High |
| Unseeded randomness | `random()`, `uuid4()` in production code under test | Low-Medium |

---

## Behavior-Driven vs Implementation-Driven Tests

**Concept.** A behavior-driven test verifies what a function does (its observable outputs and side effects for given inputs), without asserting how it does it internally. An implementation-driven test couples to internal structure — which private methods are called, which internal data structures are used, which collaborators are invoked and in what order. Implementation-driven tests are "change detectors": they fail on refactors that preserve behavior, creating friction that discourages improvement. Behavior-driven tests are "bug detectors": they catch regressions while remaining stable across refactors.

**When to flag.** Flag when tests fail the refactoring test: if you could rename an internal method, swap an algorithm implementation, or change a data structure without altering observable behavior — and the test would still fail — the test is implementation-coupled.

### Detection Heuristics

**Excessive Mocking of Internal Collaborators.**
The test mocks classes or functions that are owned by the same service — not external dependencies. Mocking `PaymentProcessor` to test `OrderService` is fine if `PaymentProcessor` is an external boundary. Mocking `PriceCalculator` to test `OrderService` when `PriceCalculator` is an internal pure function is implementation coupling — the test assumes those two are separate objects rather than testing the composed behavior.

Detection: Mocks of classes that are not I/O boundaries (not database, not HTTP, not queue). Especially suspicious when a unit test has more mock setup lines than assertion lines, or when the tested class under test is the only thing not mocked.

**Asserting Internal Method Calls (Spy/Call Count Verification).**
`verify(internalService).processItems(anyList())`. This asserts that a specific internal method was called rather than asserting the result of the computation. The internal call is an implementation detail.

Detection: `verify(mock).methodName(...)`, `expect(spy).toHaveBeenCalledWith(...)`, `mock.assert_called_once_with(...)` — especially when the verified method is not at an external boundary (database, API, queue, filesystem).

**Tests Named After Implementation, Not Behavior.**
Test names that reference class names, method names, or implementation steps rather than the expected behavior.

- Implementation-coupled: `test_processOrderShouldCallPriceCalculator`, `test_userService_getUserById_callsRepository`
- Behavior-driven: `test_discount_applied_when_order_exceeds_threshold`, `test_returns_error_when_user_not_found`

Detection: Test method names containing internal class or method names rather than behavioral descriptions.

**Tests That Break on Extract-Method Refactoring.**
If extracting a private helper method from the production code would break the test, the test is coupled to method-level granularity rather than behavior.

Detection: Tests for private methods (via reflection or `@VisibleForTesting`). Any test that calls a method named with an internal step (e.g., `_build_query`, `_calculate_subtotal`) rather than the public interface.

**State vs Interaction Verification.**
Behavior-driven tests verify final state: the database contains the expected record, the return value equals the expected value, the event was published with the expected payload. Interaction-driven tests verify that specific calls happened in a specific order.

Prefer: `assertThat(orderRepository.findById(orderId).get().status()).isEqualTo(CONFIRMED)` over `verify(orderRepository, times(1)).save(captor.capture())`.

### The Refactoring Test

Apply this mental test to any existing test: "If I refactored the production code to use a different algorithm or internal structure that produces the same observable output, would this test still pass?" If no, the test is implementation-coupled.

### Recommendation Text

> The test at `<location>` asserts `<internal interaction>` rather than the observable output or final state. This couples the test to the current implementation structure. If `<describe the refactor that would be desirable>` were applied, this test would fail despite correct behavior. Replace the interaction assertion with a state assertion: verify the return value or the state of the system after the operation.

---

## Branch and Condition Coverage Without Tooling

**Concept.** Line coverage measures which statements executed. Branch coverage measures whether both the true and false sides of every conditional were exercised. Condition coverage goes further: each atomic boolean sub-expression must have evaluated to both true and false independently. MC/DC (Modified Condition/Decision Coverage, required in safety-critical domains like aviation and medical devices) requires that each condition independently affects the outcome of the decision. A reviewer can reason about branch and condition gaps by examining conditionals in the production code and asking: "does any test drive the other side of this branch?"

**When to flag.** Flag whenever a conditional block (if, switch, ternary, try-catch, guard clause) is not exercised from both sides in the test suite. Even with high line coverage, tests can miss entire branches by only driving the "success" code path.

### Static Branch Coverage Analysis

**The Branch Inventory Method.**
For each function in critical or high-priority code (Tier 1 and Tier 2), enumerate its decision points:
1. Each `if` / `else if` / `else` — two branches
2. Each `switch` case including the `default` branch
3. Each ternary expression — two branches
4. Each short-circuit operator (`&&`, `||`) — both outcomes
5. Each `try` / `catch` / `finally` — the exceptional path
6. Each loop: zero iterations, one iteration, many iterations

Then ask: does any test exercise the other side of each branch?

**All-True / All-False Patterns.**
Functions with compound boolean conditions (`if a and b and c`) tested only when all conditions are true. A bug in the individual condition logic for `a`, `b`, or `c` alone goes undetected.

Detection: The test inputs always satisfy all conditions. There is no test where exactly one condition is false while the others are true.

**Untested `else` and `default` Branches.**
Production code has an `else` branch or `default` case that is never the target of any test. Often disguised as "that branch never happens" — which means it's dead code or an untested error path, both of which are findings.

Detection: An `else` or `default` block exists in production code. No test input would naturally drive into that branch based on the test inputs visible in the test file.

**Catch Blocks Without Tests.**
`try { ... } catch (Exception e) { ... }` — the catch block contains logic (error translation, retries, fallback, logging) but no test ever causes the try block to throw.

Detection: Catch blocks that contain more than a simple rethrow. Production code uses a real dependency (not a mock) inside the try block, so tests cannot easily trigger the exception path without injecting a failing mock.

**Compound Condition Coverage.**
For a condition like `if (user.isActive() && user.hasRole(ADMIN))`, four combinations exist:
- `isActive=true`, `hasRole=true` — likely tested
- `isActive=true`, `hasRole=false` — often tested
- `isActive=false`, `hasRole=true` — often not tested (short-circuit means `hasRole` never evaluates)
- `isActive=false`, `hasRole=false` — often not tested

If only 2 of 4 combinations are tested, a bug where `isActive` always returns `true` would survive.

**Loop Boundary Coverage.**
Loop logic typically needs: zero iterations (empty input), one iteration, and many iterations (to detect index management bugs). Tests that only provide a non-empty list of size 3+ miss the zero and single-element cases.

Detection: Test inputs for functions that iterate are all non-empty collections. No test provides an empty list or a single-element list to a function that iterates.

### Practical Flags

| Pattern | Detection | Impact |
|---------|-----------|--------|
| Catch block with logic but no exception-triggering test | Catch block contains logic; no mock raises an exception | Error paths untested |
| `else` / `default` branch unreachable in all tests | All test inputs drive the `if` branch | Silent branch omission |
| Compound condition only tested "all true" | No test falsifies a single sub-condition | Logic bug in any sub-condition survives |
| Loop only tested with non-empty input | All test collections have 2+ elements | Off-by-one or empty-collection bugs survive |
| Switch statement missing case | No test provides an input matching a specific case | That case's behavior is unverified |

---

## Testing Concurrent and Async Code

**Concept.** Concurrent and async code is inadequately tested not because developers don't try, but because standard example-based tests do not expose race conditions — races are timing-dependent and require specific interleavings. A test suite with 100% line coverage can completely miss a data race. The challenge is not writing tests that pass; it is writing tests that would fail when a concurrent bug exists.

**When to flag.** Flag when: (1) concurrent code lacks tests that exercise the concurrent scenario specifically, (2) async code uses fixed sleeps instead of awaiting signals, (3) shared mutable state is accessed by multiple goroutines/threads without synchronization, or (4) tests for concurrent operations only test the "single caller" case.

### Patterns That Indicate Inadequate Concurrent Testing

**Concurrent Code Tested Only With a Single Caller.**
A function protected by a mutex, semaphore, or lock is only tested by sequential tests with a single goroutine/thread. The synchronization logic is never under contention.

Detection: Production code contains `sync.Mutex`, `synchronized`, `ReentrantLock`, `asyncio.Lock`, or similar. The test file creates only one instance and calls the function once. No test launches multiple goroutines/threads concurrently.

**Shared Maps or Collections Written to Without Synchronization.**
Go's built-in maps are not thread-safe. Java's `HashMap` is not thread-safe. Python's `dict` is thread-safe for simple operations but not for read-modify-write sequences. Tests that cover single-threaded write paths do not expose data races on concurrent writes.

Detection: Go: `map` used in code that also uses goroutines without `sync.RWMutex`. Java: `HashMap` used in a class with `Executors` or `Thread`. Look for the Uber data race pattern: mutex passed by value (Go-specific), which copies the lock instead of sharing it.

**Fixed Sleeps as Synchronization.**
`time.Sleep(100ms)` inside a test to "wait for the goroutine to finish." This is fragile: on a slow machine, the goroutine might not finish in 100ms; on a fast machine, the sleep wastes time; and critically, the sleep does not expose race conditions that occur during the concurrent period.

Detection: `time.Sleep`, `Thread.sleep`, `asyncio.sleep` with literal values in test bodies that also launch goroutines or threads.

**Missing Race Detector Usage (Go).**
Go has a built-in race detector (`-race` flag) that instruments memory accesses and reports data races. Tests that are only run without `-race` miss races that the detector would catch.

Detection: No evidence of `-race` in Makefile, CI pipeline configuration, or test run scripts. Go concurrent code that has no race-detector-specific test comments.

**Async Code Tested Without Awaiting Completion.**
Async functions called in tests without properly awaiting their completion. The test asserts state before the async operation finishes.

Detection: `Promise` or `Future` not awaited in test assertions. `fire-and-forget` calls in production code (e.g., `asyncio.create_task()`) with no mechanism to wait for completion in tests.

**Missing "Concurrent Access" Test for Critical Shared State.**
Optimistic locking, database transactions, and in-memory caches are all subject to concurrent modification. Tests that verify correctness for sequential access do not verify that concurrent access produces consistent state.

Detection: Production code uses `SELECT FOR UPDATE`, version fields (optimistic locking), or cache with a TTL. No test exercises two concurrent operations on the same entity.

### Testing Strategies to Recommend

| Problem | Recommended Approach |
|---------|---------------------|
| Race conditions in Go | Run tests with `go test -race`. Use `testing/synctest` (Go 1.24+) for deterministic concurrent testing |
| Race conditions in Java | Use jcstress for stress testing concurrent data structures; ThreadSanitizer for instrumented detection |
| Async completion | Await real signals (channels, futures, callbacks) rather than sleeping |
| Concurrent state | Write a test that launches N goroutines/threads simultaneously and asserts invariants hold afterward |
| Fixed clocks in async code | Inject a controllable clock; use fake timers in the test framework |

### Recommendation Text

> `<function>` modifies shared state `<describe state>` and is called concurrently, but the tests at `<location>` only test the single-caller path. A data race on `<state>` would not be detected by the current tests. Add a test that launches `<N>` goroutines/threads simultaneously and asserts the final state is consistent. Run the test suite with `<race detector flag>` enabled.

---

## Testing Error Handling Paths

**Concept.** The seminal study "Simple Testing Can Prevent Most Critical Failures" (Yuan et al., OSDI 2014) analyzed 198 production failures in Cassandra, HBase, HDFS, MapReduce, and Redis. The finding is striking: 92% of all catastrophic failures were the result of incorrect handling of non-fatal errors that were explicitly signaled in software. More specifically: the error handling code was present, but wrong — and the error handling code was untested. The study found that 35% of these failures were caused by trivially detectable error handling bugs: empty catch blocks, catch blocks that logged but did not propagate, or incorrect error type handling.

**When to flag.** Error handling paths are systematically undertested. Flag whenever: catch/except blocks contain logic beyond a simple rethrow, retry logic exists without tests for exhaustion, timeouts exist without tests for timeout behavior, or external dependencies are called without tests for their failure modes.

### Most Commonly Undertested Error Scenarios

**Empty Catch Blocks and Swallowed Exceptions.**
`catch (Exception e) { logger.error("failed", e); }` — the exception is absorbed. The caller never knows the operation failed. No test verifies this code path, so the silent failure goes undetected until production.

Detection: Catch blocks that do not rethrow, do not return an error value, and do not set error state — only log. These are some of the highest-risk patterns in backend code. The OSDI study found these to be disproportionately represented in catastrophic failures.

**Retry Logic Without Exhaustion Tests.**
Retry logic has at least three distinct behaviors: success on first try, success after N retries, and exhaustion after max retries. Tests typically only cover the first case.

Detection: Retry loops, `retryTemplate.execute(...)`, `tenacity.retry` decorators, exponential backoff implementations. Look for tests that verify retry success but not retry exhaustion. The exhaustion path is the one that fails in production.

**Timeout Tests Missing.**
Code that sets a timeout on an external call. What happens when the timeout fires? Does it retry? Return a fallback? Propagate an error? Tests only verify the non-timeout case.

Detection: `timeout=` parameters in HTTP clients, `DEADLINE_EXCEEDED` handling, `context.WithTimeout` in Go. Test files for the calling code that have no test inducing a timeout.

**Partial Failure in Batch Operations.**
A batch operation processes N items. Item 3 fails. What happens to items 4-N? Does the batch abort, continue, or partially commit? This is a common source of data inconsistency.

Detection: `forEach`, `map`, bulk insert, or batch API calls in production code. Tests that only provide all-succeeding inputs.

**Cascading Dependency Failure.**
Service A calls B and C. B fails. Does A propagate the failure? Return partial results? Use a circuit breaker? Tests for A typically stub B and C to succeed; the failure modes of B and C are not tested from A's perspective.

Detection: Production code that calls multiple external dependencies in sequence or parallel. Test mocks that are always configured to succeed. No test configures a dependency mock to throw.

**Incorrect Error Type or Code.**
The handler catches `IOException` but the library actually throws `SocketTimeoutException` (a subclass) — or the handler catches `Exception` broadly when it should only handle specific exceptions. The handler exists and looks correct, but handles the wrong exception type.

Detection: Broad catch clauses (`catch Exception`, `except Exception`) where the actual thrown exception types can be determined from the dependency's API. The OSDI study found many catastrophic failures were caused by mismatched exception types.

**Error Path State Corruption.**
When an operation fails partway through, is the entity left in a consistent state? Partial writes to multiple systems without compensation are a common source of data corruption.

Detection: Functions that write to multiple stores (database + cache + message queue) without a transaction or saga pattern. No test verifies the state of the system when the second or third write fails.

### The OSDI Study Findings (Key Statistics)

Reference: Yuan et al., "Simple Testing Can Prevent Most Critical Failures" (OSDI 2014, USENIX).
- 92% of catastrophic failures were caused by incorrect error handling of non-fatal errors
- 35% were caused by trivially detectable bugs (empty catch blocks, incorrect log-and-continue)
- 57% were triggered by a specific sequence of inputs — order-dependent
- Almost all (92%) production failures could be reproduced with 3 or fewer nodes

This research justifies treating untested error handling in distributed/backend systems as **High** severity, not Medium.

### Recommendation Text

> `<function>` calls `<dependency>` but the catch block at `<location>` `<describe behavior: swallows / logs only / returns wrong error type>`. The tests at `<test location>` only configure the mock to succeed. Research on distributed system failures shows that incorrect error handling is the leading cause of catastrophic production failures. Add a test that configures `<dependency>` to throw `<exception type>` and assert that `<function>` `<expected behavior: propagates / falls back / logs and rethrows>`.

---

## Test Effectiveness vs Coverage Inflation

**Concept.** Code coverage measures whether code was executed during tests. It does not measure whether tests would catch bugs. A test suite with 100% line coverage and zero assertions has 0% mutation score — it executes all code but detects no faults. Empirical research consistently shows that mutation score correlates with real fault detection; line coverage does not. An AI reviewer can reason about test effectiveness by looking at assertion quality, not just code execution.

**When to flag.** Flag when tests have high apparent coverage (all code paths appear to be exercised) but assertions are thin, generic, or missing for meaningful outputs.

### Patterns That Inflate Coverage Without Improving Effectiveness

**Execution-Only Tests.**
A test calls a function, does not assert any return value, and asserts only that no exception was thrown.
```
result = service.processOrder(order)
# no assertion on result
```
This line covers the function but kills no mutants. Any change to the return value or computed state goes undetected.

Detection: Test methods where the final assertion is `assertDoesNotThrow`, `assertNotNull`, or is absent entirely. Tests where the function return value is captured in a variable that is never asserted on.

**Assertion-Free Setup Code.**
A complex test setup creates entities, configures mocks, and calls the function under test — but the assertions only check one property of a multi-property output. A bug in any non-asserted property is invisible.

Detection: Functions that return or mutate complex objects (structs with 5+ fields). Test assertions that only check one field when multiple fields are computed.

**Trivial Return Assertions.**
Asserting that a function returned "something" without checking if it returned the right thing.
- `assertNotNull(result)` on a function that should return a specific value
- `assertTrue(result.isSuccess())` without checking what `result` contains
- `assert len(result) > 0` without checking what is in the result

Detection: Assertions using `isNotNull`, `isPresent`, `isNotEmpty`, `isSuccess`, `> 0` on values that have specific expected content.

**The Mock Coverage Illusion.**
Mocking a dependency and asserting the mock was called exercises the code path that calls the dependency — achieving line coverage — but does not verify the behavior when the dependency produces different return values, or verify that the calling code uses the return value correctly.

Detection: Test mocks configured with a specific `return_value` that the test never asserts is actually used correctly by the code under test. The mock is called (coverage achieved) but its result is discarded or incorrectly used.

**Coverage From Test Infrastructure.**
Shared fixtures, `setUp` methods, and test helpers that call production code as a side effect of setup — not as the subject of the test. This inflates coverage for code that is not the focus of any test.

Detection: Production code that is only covered by test fixture setup, not by any explicit test assertion.

### Effective Test Heuristic

An effective test satisfies all of these:
1. It exercises a specific scenario (not just "any execution path")
2. It asserts the specific expected output for that scenario (not just "something non-null")
3. If the output were wrong — different value, different error, missing side effect — the assertion would fail
4. It is the smallest test that would catch the bug it is designed to catch

A useful mental model: "If I introduced a bug into the production code right now, which test would catch it?" If the answer is "none of them," the tests are ineffective regardless of coverage percentage.

### Recommendation Text

> The test at `<location>` calls `<function>` but asserts only `<weak assertion>`. A bug where `<describe specific mutation>` would not be caught by this test. Replace with an assertion on the specific expected value: `assert result.field == expected_value`. The current test achieves line coverage but does not improve fault detection.

---

## Approval and Characterization Testing

**Concept.** Approval testing (also called Golden Master or Characterization testing) captures the current output of a function as a "golden file" and future tests verify the output matches exactly. It is a powerful tool for one specific scenario: adding test coverage to legacy code you do not yet understand, where you want a safety net before refactoring. Michael Feathers' "Working Effectively with Legacy Code" describes this as the first step before any refactoring. However, when applied inappropriately, approval tests become maintenance burdens: they capture bugs as well as correct behavior, they break on any output change (including legitimate improvements), and developers mechanically approve changes without reviewing them.

**When to flag.** Flag approval tests that are applied to: (1) code that is not legacy (has other tests, is understood), (2) outputs that change frequently for legitimate reasons, (3) large unstructured outputs where every change looks the same, or (4) as a substitute for behavioral assertions on code that is simple enough to assert precisely.

### Valid Use Cases

**Legacy Code With No Tests.**
A function or module with no tests, complex behavior, and no documentation. Before refactoring, a golden master test captures what the code currently does — bugs and all. This provides a safety net. The golden master is temporary scaffolding, not permanent documentation of correct behavior.

Signal that this is appropriate: No other tests exist for this code, the code is scheduled for refactoring, the output is complex enough that precise assertions would be more effort than capturing the output, and the team understands the captured output may contain bugs.

**Complex Structured Outputs (PDFs, XML, Reports).**
Outputs with hundreds of fields where writing assertions for each field would be impractical. A golden file for a PDF report or XML export is appropriate when: the output format is stable, changes are always intentional, and changes go through a review step.

Signal that this is appropriate: The output format is a well-defined document or structured file, changes to output are rare and intentional, and reviewers are expected to examine diffs carefully.

**Rendering and Serialization Outputs.**
Snapshot tests for API responses or serialized data structures — but only when the schema is intentionally stable and the snapshots are reviewed on change.

### When Approval Tests Become Waste

**Snapshots Updated Without Review.**
CI pipeline automatically updates snapshot files on any change. Developers commit updated snapshots without examining what changed. The test has become a formality — it runs but never rejects any output.

Detection: `.snap` files (Jest), `.approved.txt` files, or golden files that are updated in the same commit that changes production code, without explanation of what changed and why.

**Approval Tests on Frequently Changing Outputs.**
A golden file for an output that changes every sprint (new fields, reformatted values, renamed keys). Each sprint the team spends time approving changes that are obviously intentional, while simultaneously becoming desensitized to the content of the diff.

Detection: Golden files that have been updated more than 3-4 times in recent commits. Large golden files where the diff shows structural changes rather than isolated value changes.

**Approval Tests Replacing Behavioral Tests for Simple Code.**
A snapshot test on a function that computes a value, when a precise assertion (`assert result == 42`) would be clearer, faster to write, and more informative on failure.

Detection: Approval tests for functions that return scalars, single objects, or simple structures — cases where a precise assertion is both feasible and more informative.

**Bugs Baked Into the Golden Master.**
The golden file was generated from buggy code. Future tests pass because they verify that the bug is reproduced. The team believes the test is protecting them, but it is actually protecting the bug.

Detection: This is difficult to detect without domain knowledge, but a signal is: the golden file contains values that seem incorrect based on the domain (e.g., a total that does not match the line items, a status that contradicts business rules described in comments).

### The Temporary Scaffolding Principle

Approval tests on legacy code should be treated as temporary scaffolding: set up before refactoring, removed (or replaced with behavioral tests) after refactoring is complete and the code is understood. A codebase where approval tests are the primary test strategy for actively developed code is a warning sign.

### Recommendation Text

> The snapshot test at `<location>` captures the output of `<function>`, which `<is simple enough for precise assertions / changes frequently / has been updated N times recently>`. Approval tests are most valuable as temporary scaffolding for legacy code before refactoring. For this function, replace with a precise behavioral assertion: `assert result.<field> == <expected>`. The current snapshot test would pass even if `<describe specific bug>`.
