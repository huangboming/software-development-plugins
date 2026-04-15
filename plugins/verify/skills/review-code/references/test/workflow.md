# Test Review Workflow

Evaluate whether the right code is tested with the right cases. Identify critical business logic, complex functions, and high-risk paths that lack adequate test coverage. Flag test waste — trivial tests that add maintenance burden without catching real bugs.

This mode answers: **"If a bug ships, will the tests catch it?"** — not "are the existing tests well-written?" (that's maintainability mode).

## Process

1. Determine scope
2. Map critical code
3. Evaluate test coverage
4. Analyze findings
5. Verify findings
6. Write report

### 1. Determine Scope

Ask the user (skip if already clear from context):
- Which files, modules, or directories to review? (or full project)
- Any known areas of concern or recent bugs?
- Language/framework and test framework if not obvious from the codebase

### 2. Map Critical Code

Run the metrics scanner to identify complex code that warrants test coverage:

```
uv run --script ${CLAUDE_PLUGIN_ROOT}/skills/review-code/scripts/code_metrics.py --repo <path>
```

Use the hot spots (high complexity, long functions, many parameters) to identify code that should be tested. Cross-reference with test file locations to spot coverage gaps early.

Always run the script for fresh data, even if `.hand-offs/code-metrics.md` already exists.

### 3. Evaluate Test Coverage

Launch 2-3 explorer agents in parallel:

**Agent 1 — Critical Code Inventory:**
Identify the code that matters most — what would cause real damage if it broke:
- Core business logic: domain rules, state transitions, calculations, validation logic that enforces invariants
- Complex pure functions: functions with branching logic, multiple code paths, or non-trivial transformations
- High-risk mutation paths: payment processing, data writes, permission changes, cascading operations
- Critical integrations: external API calls, message publishing, webhook handling — the boundary code
- For each, note: file/function location, what it does, and whether a corresponding test file exists
- Return a list of 10-20 critical code locations with one-line descriptions

**Agent 2 — Test Case Completeness:**
For existing test files, evaluate whether they cover the scenarios that matter:
- Happy path: does at least one test verify the primary success scenario with realistic inputs?
- Sad path: are failure modes tested? (invalid input, missing data, unauthorized access, dependency failures, timeouts)
- Edge cases: are boundary conditions tested? (empty collections, zero/negative values, max values, concurrent access, unicode/special characters, null/nil)
- Branch coverage: are both sides of conditionals exercised? Check for untested `else`/`default` branches, catch blocks with logic but no exception-triggering test, compound conditions tested only in the all-true case
- Error handling paths: are dependency failures tested? (mocks always configured to succeed, retry exhaustion untested, timeout behavior untested, partial batch failure untested)
- Concurrent scenarios: if production code uses locks, shared state, or async patterns — are concurrent callers tested, or only the single-caller path?
- For each test file: which critical function(s) does it test, and which scenario categories are missing?
- Return a list of 10-15 test files with gaps identified per file

**Agent 3 — Untested Critical Code, Test Waste & Effectiveness:**
Three-pronged search:
- **Untested critical code**: Find business logic, complex functions, and high-risk paths with no corresponding tests. Focus on code where a bug would cause data corruption, financial loss, security breach, or user-facing failure
- **Test waste & weak tests**: Find tests that consume maintenance effort without catching real bugs — tests on trivial getters/setters, tests that only verify mock wiring, tests that assert framework behavior, tests on simple data classes. Also find tests with weak assertions: `assertNotNull`/`assertDoesNotThrow` on functions that return specific values, tests where the return value is captured but never asserted, tests with more setup than assertion lines
- **Flakiness risks**: Flag tests with `sleep()`/`delay()` for synchronization, shared mutable state between tests (class-level or module-level variables), real network calls without mocking, wall-clock time dependencies (`new Date()`, `time.time()`) without clock injection, database tests without transaction rollback
- Return three separate lists: untested critical code (5-15 items), test waste and weak tests (5-10 items), flakiness risks (3-5 items)

After agents return, read the key files they identified to verify findings.

### 4. Analyze Findings

Load references as needed:

| Dimension | Reference | Load When |
|-----------|-----------|-----------|
| Test strategy | [test-strategy.md](test-strategy.md) — Priority tiers for what to test, happy/sad/edge case framework, test waste patterns, test pyramid assessment | Always |
| Test effectiveness | [test-effectiveness.md](test-effectiveness.md) — Mutation testing heuristics, property-based testing candidates, contract testing signals, flakiness risks, behavior vs implementation coupling, branch coverage gaps, concurrent code testing, error handling coverage, coverage inflation patterns, approval testing trade-offs | When tests exist and the question is whether they would actually catch bugs |

For specific topics in `test-effectiveness.md`, grep for section headers: `## Mutation`, `## Property-Based`, `## Contract Testing`, `## Test Isolation`, `## Behavior-Driven`, `## Branch and Condition`, `## Testing Concurrent`, `## Testing Error`, `## Test Effectiveness vs`, `## Approval`.

For each finding:
1. Classify: coverage gap, missing scenario, test waste, flakiness risk, or effectiveness concern
2. Cite the specific production code location and (if applicable) the test file
3. Assess severity using the definitions in [shared-quality-standards.md](../shared-quality-standards.md)
4. For coverage gaps: explain what could break and under what conditions
5. For test waste: explain why the test adds no value
6. Provide a specific recommendation (what test to write, or what test to remove)

### 5. Verify Findings

Apply the verification checklist from [shared-quality-standards.md](../shared-quality-standards.md). Additionally:
- For coverage gaps, confirm the production code is actually reachable and not dead code
- For missing scenarios, confirm the scenario is realistic — do not invent edge cases that cannot occur given the domain
- For test waste, confirm the test genuinely adds no value — a test that looks trivial may guard against a known regression

### 6. Write Report

Write to `.hand-offs/reviews/test-coverage/YYYY-MM-DD-HHMM.md`. Create `.hand-offs/reviews/test-coverage/` if it does not exist.

- **timestamp**: `YYYY-MM-DD-HHMM` (e.g., `2026-03-04-1430`)
- Example: `.hand-offs/reviews/test-coverage/2026-03-04-1430.md`

```markdown
# Test Review: <Scope>

> Reviewed: <date> | Scope: <files/modules reviewed> | Health: <Well tested | Gaps in critical paths | Significant coverage gaps>

## Critical Code Map

Summary of critical business logic, complex functions, and high-risk paths identified. For each, whether tests exist:

| Critical Code | Location | Tested? | Gaps |
|---------------|----------|---------|------|
| <description> | `path/to/file.py:42` | Partial | Missing sad path, edge cases |
| <description> | `path/to/file.py:100` | No | No tests |

## Findings

### Coverage Gaps

**[Severity] <Untested Critical Path>**
Location: `path/to/service.py:42`
Issue: <What critical logic is untested>
Risk: <What could break undetected — be specific about the failure scenario>
Fix: <Specific test cases to add, with scenario descriptions>

### Missing Scenarios

**[Severity] <Missing Happy/Sad/Edge Case>**
Production code: `path/to/service.py:42`
Test file: `tests/test_service.py:10`
Issue: <What scenario category is missing>
Risk: <What bug could slip through>
Fix: <Specific test case to add>

### Test Effectiveness

**[Severity] <Weak/Ineffective Test>**
Production code: `path/to/service.py:42`
Test file: `tests/test_service.py:10`
Issue: <Why this test would not catch a real bug — weak assertion, coverage inflation, implementation coupling>
Fix: <Specific stronger assertion or restructured test>

### Flakiness Risks

**[Severity] <Flakiness Pattern>**
Location: `tests/test_service.py:30`
Issue: <What makes this test non-deterministic — sleep, shared state, time dependency, network call>
Fix: <Specific fix — inject clock, use polling assertion, isolate state, mock network>

### Test Waste

**[Low] <Trivial/Useless Test>**
Location: `tests/test_models.py:15`
Issue: <Why this test adds no value>
Fix: Remove or replace with a meaningful behavioral test

<!-- Order findings by severity within each section: Critical -> High -> Medium -> Low -->
<!-- Omit sections with no findings -->

## Summary

| Category | Count |
|----------|-------|
| Coverage gaps (Critical/High) | N |
| Missing scenarios | N |
| Test effectiveness | N |
| Flakiness risks | N |
| Test waste | N |

**Top recommendations:**
1. <Highest impact test to add — what it covers and why>
2. <Second>
3. <Third>

**Overall assessment:** <Well tested | Gaps in critical paths | Significant coverage gaps>
```

## Edge Cases

- **No tests in codebase**: Report as a critical finding. Focus the report on the Critical Code Map — identify the highest-priority code to test first and recommend a starting point.
- **Codebase is mostly glue code** (thin wrappers, config, routing): Testing glue has low value. Focus on the few places where business logic exists and flag if those are tested. Don't manufacture findings.
- **Very high test coverage already**: Focus on scenario completeness (happy/sad/edge) rather than coverage gaps. Good coverage does not mean good tests — look for missing edge cases and false-confidence tests. Load `test-effectiveness.md` to evaluate test effectiveness.
- **Test framework is unusual or custom**: Note it but review the tests on their merits — the principles apply regardless of framework.
