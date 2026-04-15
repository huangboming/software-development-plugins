# Dispensables: Dead Code, Useless Tests & Useless Comments

Detection catalog for code, tests, and comments that should be removed.

## Table of Contents

- [Dead & Unused Code](#dead--unused-code)
- [Redundant Code](#redundant-code)
- [Test Anti-Patterns](#test-anti-patterns)
- [Comment Anti-Patterns](#comment-anti-patterns)

---

## Dead & Unused Code

### Unused Imports

- **Detect**: Import statements with no reference in the file; IDE/linter warnings
- **Severity**: Low
- **Risk**: Noise; may pull in unnecessary dependencies; slows comprehension

### Unused Variables & Parameters

- **Detect**: Variables assigned but never read; function parameters never referenced in the body; caught exceptions assigned to variable but never used
- **Severity**: Low–Medium
- **Risk**: Misleads readers into thinking the value matters; may mask bugs

### Unreachable Code

- **Detect**: Code after unconditional `return`, `raise`, `break`, `continue`; branches guarded by always-false conditions; `else` after `if` that always returns
- **Severity**: Medium
- **Risk**: Developer intended it to run but it never does; hidden bugs

### Vestigial Code

- **Detect**: Functions/classes not called from anywhere in the codebase; feature flag code for flags long since resolved; migration code for one-time data transforms; backward-compatibility shims for deprecated APIs with no remaining callers
- **Severity**: Medium
- **Risk**: Maintenance burden; misleads into thinking the code is active; bloats codebase

### Dead Feature Toggles

- **Detect**: Feature flags that are always `true` or always `false` in config; toggle logic where both branches haven't been exercised in months
- **Severity**: Medium
- **Risk**: Complexity without benefit; stale branches may rot and break if accidentally enabled

---

## Redundant Code

### Redundant Conditionals

- **Detect**: `if x: return True else: return False` (should be `return x`); `if condition: x = True else: x = False`; double negation (`if not not x`)
- **Severity**: Low
- **Risk**: Noise; obscures intent

### Unnecessary Wrapping

- **Detect**: Function that just calls another function with the same arguments; class that wraps another class adding no behavior; try/except that just re-raises
- **Severity**: Low–Medium
- **Risk**: Indirection without value; more code to maintain

### Duplicate Logic

- **Detect**: Two or more code blocks with identical or near-identical logic; copy-paste with minor variations; same validation repeated in multiple places
- **Severity**: Medium–High
- **Risk**: Fix in one place, miss the other; inconsistency over time

### Over-Defensive Code

- **Detect**: Null checks on values that can never be null; type checks in strongly-typed code; validation of internal function inputs that are already validated upstream
- **Severity**: Low
- **Risk**: Noise; suggests lack of confidence in the codebase; may mask real issues

---

## Test Anti-Patterns

### Test That Tests Nothing

- **Detect**: Test with no assertions; test that only asserts `True`; test that asserts the mock returns what the mock was configured to return
- **Severity**: High
- **Risk**: False confidence; inflates coverage metrics while verifying nothing

### Testing Implementation Details

- **Detect**: Test asserts specific method calls on internal collaborators; test breaks when refactoring internals without changing behavior; test verifies the order of internal operations
- **Severity**: High
- **Risk**: Brittle tests that break on valid refactors; discourages improvement

### Excessive Mocking

- **Detect**: Test mocks > 3 dependencies; test mocks the class under test; mock configuration is longer than the test logic; mocks return mocks
- **Severity**: High
- **Risk**: Tests verify mock wiring, not behavior; refactoring breaks everything; false confidence

### Duplicate Production Logic

- **Detect**: Test reimplements the same calculation as production code to verify it; assertion duplicates the algorithm being tested
- **Severity**: Medium
- **Risk**: Same bug in test and production; test passes even when both are wrong

### Happy Path Only

- **Detect**: No tests for error cases, edge cases, or boundary conditions; all test inputs are "normal" values; no tests for empty/null/max inputs
- **Severity**: Medium
- **Risk**: Bugs hide in unhappy paths; error handling untested

### Flaky Tests

- **Detect**: Tests that use `sleep()`, depend on wall-clock time, rely on external services, depend on execution order, or use random data without seeds
- **Severity**: High
- **Risk**: Erode trust in test suite; team starts ignoring failures

### Overly Broad Tests

- **Detect**: Single test that asserts 10+ things; test name is vague ("test_it_works"); test covers multiple behaviors in one function
- **Severity**: Medium
- **Risk**: Hard to diagnose failures; unclear what's being verified

### Test-per-Method Mirroring

- **Detect**: Test file is a 1:1 mirror of source file; one test per method regardless of complexity; trivial getters/setters have dedicated tests
- **Severity**: Low–Medium
- **Risk**: Tests coupled to structure, not behavior; misses interaction bugs; wastes effort on trivial code

---

## Comment Anti-Patterns

### Obvious Comments

- **Detect**: Comment restates the code: `i += 1  # increment i`; comment describes what the function signature already says; doc comment that just repeats the function name
- **Severity**: Low
- **Risk**: Noise; readers learn to ignore comments

### Outdated Comments

- **Detect**: Comment describes behavior that no longer matches the code; references to renamed variables, deleted files, or removed features; TODO referencing resolved issues
- **Severity**: Medium–High
- **Risk**: Actively misleading; worse than no comment

### Commented-Out Code

- **Detect**: Blocks of code in comments; `// old implementation` followed by dead code; entire functions commented out
- **Severity**: Medium
- **Risk**: Clutters the file; version control already preserves history; readers wonder if it should be uncommented

### Journal Comments

- **Detect**: Comments tracking changes: `// Added by John, 2023-01-15`; `// Modified for ticket PROJ-123`; changelog at top of file
- **Severity**: Low
- **Risk**: Noise; duplicates git history; goes stale immediately

### Closing Brace Comments

- **Detect**: `} // end if`, `} // end for`, `} // end class Foo`
- **Severity**: Low
- **Risk**: Symptom of blocks that are too long; fix the length, not the symptom

### Mandated / Boilerplate Comments

- **Detect**: Every function has a docstring that adds no information beyond the signature; license headers copied into every file; `@param` tags that just restate parameter names
- **Severity**: Low
- **Risk**: Reduces signal-to-noise; real documentation gets lost in boilerplate

### Zombie TODOs

- **Detect**: `TODO` or `FIXME` comments older than 6 months (check git blame); TODO referencing completed tickets; TODO with no actionable description
- **Severity**: Medium
- **Risk**: False promises; clutters codebase; important TODOs get lost among stale ones
