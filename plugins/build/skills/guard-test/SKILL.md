---
name: guard-test
description: "Guard test quality — find missing unit and integration tests for important logic, remove worthless tests, and fix anti-patterns. Covers unit tests (Domain Model code) and integration tests (Controllers/orchestration). E2E tests are out of scope. Triggers: 'check my tests', 'guard tests', 'are my tests good enough', 'find missing tests', 'clean up tests', 'remove useless tests', 'test quality check', 'what should I test'."
---

# Test Guardian

Guard unit and integration tests. If E2E test files are encountered (browser drivers, page objects), note "E2E tests not evaluated by this skill" and skip them.

## Arguments

Parse from the user's request:

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| scope | no | changed files | Files, directories, or modules to guard |
| focus | no | all | Action filter: `prune`, `fill`, or `all` |

**Parsing examples:**

- "check my tests" → scope: changed files, focus: all
- "find missing tests for src/billing/" → scope: src/billing/, focus: fill
- "clean up tests in this module" → scope: current module, focus: prune
- "remove useless tests" → scope: changed files, focus: prune
- "what should I test in the auth service" → scope: auth service, focus: fill

## References

- [references/test-smell-catalog.md](references/test-smell-catalog.md) — Catalog of test smells organized by category (removable, structural, weak assertions), each with confidence level, detection signals, fix actions, and integration test threshold adjustments. Read at the start of Step 3 before evaluating existing tests.
- [references/coverage-gap-model.md](references/coverage-gap-model.md) — Quadrant classification model for production code (Domain Model / Trivial / Controllers / Overcomplicated), unit and integration test gap type tables, and unified prioritization rules. Read at the start of Step 4 before classifying functions.
- [references/test-writing-standards.md](references/test-writing-standards.md) — Test style hierarchy (output-based > state-based > interaction-based), mock strategy per dependency type, test case design techniques (boundary value, equivalence partitioning, error paths), and integration test assertion targets. Read at the start of Step 6 before writing any test.

## Process

1. Determine scope
2. Map production code to tests
3. Analyze existing tests (prune)
4. Detect coverage gaps (fill)
5. Present plan
6. Apply changes
7. Verify

### Step 1: Determine Scope

Resolve target production files:

- **Explicit paths** — use what the user specified
- **"changed files"** (default) — `git diff --name-only HEAD` and `git diff --name-only --staged`, filtered to source files (exclude test files from production scope)
- **Directory/module** — glob for source files, excluding generated/vendored/test files

Skip auto-generated files (protobuf, OpenAPI codegen, migrations), vendored code, and config files.

If no changed files and no scope specified → ask what to guard.
If scope resolves to >15 production files → ask: "That's N files. Focus on the highest-complexity ones, or work through all?"

### Step 2: Map Production Code to Tests

For each production file in scope:

1. Find corresponding test files using the project's conventions
2. Classify each test file as **unit** or **integration** test (see test-smell-catalog.md for detection signals: DB fixtures, test containers, HTTP clients → integration; pure mocks/stubs → unit)
3. If no test file exists, record as **missing test file**
4. If test files exist, build a function-to-test mapping — for each public function/method, grep the test files for calls to it

Read all production and test files in this step — they are needed for both analysis paths. Note E2E test files (browser drivers, page objects) and skip them.

### Step 3: Analyze Existing Tests (Prune)

Skip if focus is `fill`.

Read [references/test-smell-catalog.md](references/test-smell-catalog.md). Evaluate each existing test against the three smell categories (removable → structural → weak assertions), applying the catalog's integration test threshold adjustments for integration tests. For each finding, record: smell name, test type (unit/integration), test file:line, drafted fix, and confidence level.

**Worked example:**

```
test_create_order (test_orders.py:42) [unit]:
  Smell: Conditional logic in test — has `if order.is_premium:` branch at L47
  Confidence: Clear (mechanical split)
  Fix: Split into test_create_order_premium and test_create_order_standard

test_payment_processed (test_payments.py:15) [unit]:
  Smell: Over-mocking — mocks PaymentGateway, EmailService, AuditLogger for `calculate_total()` which is pure
  Confidence: Clear (pure function, 0 collaborators needed)
  Fix: Remove all mocks, pass real inputs, assert on return value

test_refund_endpoint (test_refunds_integration.py:30) [integration]:
  Smell: Status-code-only assertion — asserts response.status == 200 but not body or DB state
  Confidence: Judgment (status check has some value, but missing side-effect verification)
  Fix: Add assertions on response body and DB state after refund
```

### Step 4: Detect Coverage Gaps (Fill)

Skip if focus is `prune`.

Read [references/coverage-gap-model.md](references/coverage-gap-model.md). For each production function:

1. **Classify into quadrant** — state reasoning explicitly: "`process_refund` has 5 branches, 0 collaborators → Domain Model"
2. **Determine action** per the quadrant's prescribed test type (see the model's Quadrant Actions table)
3. **Classify gap types** per the model's unit test gaps table (Domain Model) or integration test gaps table (Controllers)
4. **Prioritize** using the model's unified prioritization rules

**Worked example:**

```
process_refund (orders/refunds.py:30):
  Classification: 5 branches, 0 collaborators → Domain Model
  Coverage: test_refund_full_amount exists (happy path only)
  Gaps:
    - [High] Missing error path: order.status != "completed" guard (L32) — untested
    - [High] Missing boundary: 30-day refund window (L35) — test at day 30, 31, 29
    - [Medium] Missing equivalence: "changed_mind" partial refund path (L40) — untested
  Proposed: 5 unit tests

handle_refund_request (orders/api.py:80):
  Classification: 1 branch, 3 collaborators (DB + payment API + event bus) → Controllers
  Coverage: no integration test exists
  Gaps:
    - [High] Untested controller — no integration tests at all
    - [High] Missing failure handling — no test for payment API failure mid-refund
    - [High] Missing side-effect verification — DB write and event publish unverified
  Proposed: 3 integration tests (happy path with DB + event assertions, payment API failure, invalid order ID)

get_order_total (orders/models.py:10):
  Classification: 0 branches, 0 collaborators → Trivial
  Action: Skip
```

### Step 5: Present Plan

Group findings into sections by test type:

```
## Test Guardian Plan

### Prune: Tests to Remove or Fix

#### test_orders.py [unit]

- [clear] FIX `test_create_order` (L42) — conditional logic → split into 2 tests
- [judgment] DELETE `test_handler_calls_service` (L78) — tests implementation: asserts mock call sequence

#### test_refunds_integration.py [integration]

- [judgment] FIX `test_refund_endpoint` (L30) — status-code-only → add body + DB assertions

### Fill: Missing Unit Tests

#### orders/refunds.py → tests/test_refunds.py

- `process_refund` (L30) — Domain Model, 5 branches, 0 collaborators
  - [gap] Happy path only, missing error + boundary + equivalence
  - Proposed: 5 unit tests

### Fill: Missing Integration Tests

#### orders/api.py → tests/test_orders_integration.py

- `handle_refund_request` (L80) — Controllers, 1 branch, 3 collaborators
  - [gap] No integration tests exist
  - Proposed: 3 integration tests (happy path, payment failure, invalid order)

#### Skipped

- `get_order_total` (L10) — Trivial

**Total: 2 to prune (1 clear, 2 judgment) | 5 unit tests + 3 integration tests to write (all need review)**
```

Ask: "Apply clear prune changes now? I'll show judgment calls and proposed new tests individually."

### Step 6: Apply Changes

Read [references/test-writing-standards.md](references/test-writing-standards.md) before writing any new test.

**Order of operations:**
1. Apply clear prune changes (deletions and mechanical fixes)
2. Walk through judgment prune changes one by one — show before/after, wait for approval
3. Write proposed unit tests one function at a time — show the full test, explain which gap it fills, wait for approval
4. Write proposed integration tests one controller at a time — show the full test, explain assertions and mock setup, wait for approval

For prune fixes, follow the catalog's transform ordering (removals → structural → assertions) and process bottom-up within each category.

For new tests, match the existing test file's conventions (imports, fixtures, runner). If no test file exists, create one. Each test includes a comment noting which gap it fills.

### Step 7: Verify

1. **Run tests** — execute the test suite on affected files using the project's configured runner
2. **Check results** — if a new test fails, investigate whether the test or the production code has the bug. Present findings before proceeding.
3. **Summarize**:
   - Unit tests: removed, fixed, added (count and names)
   - Integration tests: removed, fixed, added (count and names)
   - Functions skipped with reason (trivial, overcomplicated, e2e)
   - Any production bugs discovered

## Escalation

If the user's intent is ambiguous (test cleanup vs. full test strategy vs. code review):
→ Ask: "Are you looking for test cleanup, new test coverage, or both?"

If a production function is Overcomplicated:
→ Flag for refactoring instead of writing tests: "This function mixes business logic with I/O. Recommend extracting the logic into a pure function first, then testing the extraction."

If a removed test was the only test for a function:
→ Classify as judgment even if the test is clearly bad. Note: "This is the only test for `function_name`. Remove it, but also add it to the fill list."

If the project has no test infrastructure (no test runner, no test directory):
→ Ask: "No test setup detected. Want me to set up the test infrastructure first, or just identify what needs testing?"

If integration tests require infrastructure the project doesn't have (test containers, in-memory DB):
→ Note the required infrastructure and ask: "Integration tests for this controller need [X]. Want me to set that up, or write the tests assuming it will be available?"

## Edge Cases

- **No test smells found** — report tests as healthy, proceed to gap detection
- **No coverage gaps** — report coverage as adequate, proceed to prune only
- **All functions are Trivial** — report no tests needed, suggest broadening scope
- **Test file imports nothing from production** — flag as orphaned test file, judgment for removal
- **Function covered by integration tests only** — accept integration coverage as sufficient, note: "Covered by integration test at [path]"
- **Function covered by unit tests only but is a Controller** — note: "Unit test exists but integration test recommended for full path coverage"
- **E2E test files found** — skip with note: "E2E tests not evaluated by this skill"
