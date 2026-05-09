---
name: guard-boundary
description: "Guard encapsulation boundaries against the Parnas (information hiding) and Ousterhout (interface depth) tests. Triggers: 'guard boundary', 'check encapsulation', 'find leaked internals', 'check module boundaries', 'is my code well encapsulated'."
---

Audit boundaries (modules, classes, functions, cross-module imports) in the user's scope (default: `git diff --name-only HEAD` + staged). Skip generated/vendored/test files.

## Two essential principles

Every boundary violation is a failure of one of these.

### 1. Parnas test — what does this hide?

For each module/class, ask: **what one design decision does it hide?** If the answer is *"nothing"*, *"the same thing as another module"*, or *"a sequence of process steps"* — the boundary is in the wrong place.

Common failures:
- Mixed concerns (HTTP + domain + persistence in one file)
- Multi-responsibility class (methods cluster into groups touching disjoint state)
- Behavior in the wrong place (data class + service that only operates on its fields; method accessing 3+ fields of another object)
- Temporal decomposition (modules named after process steps, sharing the same data structure)

### 2. Ousterhout depth test — is the interface simpler than the implementation?

For each module's public surface, ask: **does the caller have to understand the implementation to use it?** If yes — module is shallow.

Common failures:
- Over-exposed module (exports many items, few used externally)
- Implementation-shaped names (`queryDatabaseForUser` instead of `findUser`)
- Leaky types crossing boundaries (ORM models, framework types in domain signatures)
- Reaching into another module's internals (importing `_private` paths)
- Pass-through methods that add no depth

## One mechanical auto-fix

**Barrel re-exports** (`export * from`, `from .x import *`, `pub use x::*`) → replace with explicit named exports of items actually consumed externally. Apply directly.

## Output

Group findings as `[clear]` (mechanical, apply directly) and `[judgment]` (architectural, present and wait for approval). For each judgment finding, state the impact (which modules need updating) before recommending.

In languages with compiler-enforced encapsulation (Rust, Go), focus on design-level violations — the compiler already catches visibility ones.
