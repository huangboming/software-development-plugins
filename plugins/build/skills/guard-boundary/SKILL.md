---
name: guard-boundary
description: "Guard encapsulation boundaries — detect over-exposed APIs, leaked internals, mixed responsibilities, and implementation-shaped interfaces. Auto-fixes clear violations (unused exports, barrel re-exports, import path fixes) and reports architectural issues with recommendations. Triggers: 'guard boundary', 'guard boundaries', 'check encapsulation', 'guard my boundaries', 'are my modules well encapsulated', 'check API exposure', 'find leaked internals', 'encapsulation check', 'check module boundaries', 'is my code well encapsulated'."
---

# Guard Boundary

## Arguments

Parse from the user's request:

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| scope | no | changed files | Files, directories, or modules to guard |
| focus | no | all | Boundary level filter: `module`, `class`, `function`, `cross-boundary`, or `all` |

**Parsing examples:**

- "check encapsulation" → scope: changed files, focus: all
- "guard my boundaries in src/billing/" → scope: src/billing/, focus: all
- "check API exposure of this module" → scope: current module, focus: module
- "find leaked internals" → scope: changed files, focus: cross-boundary
- "are my classes well encapsulated" → scope: changed files, focus: class

## References

- [references/boundary-violation-catalog.md](references/boundary-violation-catalog.md) — 21 violation patterns organized by boundary level (module, class, function, cross-boundary), each with concrete detection signals, confidence rules, and auto-fix/recommendation actions. Read at the start of Step 3 before analyzing code. Contains worked examples for key violations — use them to calibrate detection and output quality.

## Process

1. Determine scope
2. Map boundaries
3. Analyze boundaries
4. Present plan
5. Apply changes
6. Verify

### Step 1: Determine Scope

Resolve target files:

- **Explicit paths** — use what the user specified
- **"changed files"** (default) — `git diff --name-only HEAD` and `git diff --name-only --staged`, filtered to source files
- **Directory/module** — glob for source files, excluding generated/vendored files

Skip auto-generated files (protobuf, OpenAPI codegen, migrations), vendored code, config files, and test files (boundary analysis targets production code structure).

If no changed files and no scope specified → ask what to guard.
If scope resolves to >20 source files → ask: "That's N files. Focus on the most exposed modules, or work through all?"

### Step 2: Map Boundaries

Build a boundary map before analyzing violations. For each module in scope:

1. **Identify module boundaries** — determine what constitutes a module in this codebase: directories with `__init__.py`, packages with `index.ts`/`mod.rs`, namespace directories, or explicit package boundaries. Use the project's existing conventions, not a theoretical ideal.
2. **Catalog public surface** — list every exported/public function, class, type, and constant. Count them.
3. **Trace dependencies** — for each module, record what it imports and from where. Note which imported items are public API vs internal.
4. **Map class responsibilities** — for each class with 5+ methods, list its methods and which instance fields each method reads/writes.

Scale mapping depth to the `focus` argument. For `function` focus, catalog public signatures and parameter lists — skip detailed module dependency tracing. For `class` focus, include module boundaries for context but skip cross-boundary dependency chains. For `all`, map comprehensively.

**Worked example:**

```
Module: src/orders/
  Public (3): OrderService, Order, OrderStatus
  Internal (3): _calculate_tax(), _validate_items(), OrderRepository
  Imported by: src/billing/ (OrderService, Order), src/shipping/ (Order, OrderStatus)

Module: src/billing/
  Public (2): BillingService, Invoice
  Internal (2): _apply_discount(), TaxEngine
  Imported by: src/api/ (BillingService, Invoice)
  Imports: src/orders/ (Order, OrderService)
```

### Step 3: Analyze Boundaries

Read [references/boundary-violation-catalog.md](references/boundary-violation-catalog.md). Using the boundary map from Step 2, evaluate the code against the catalog's four levels, applying only the levels matching the `focus` argument (or all if `all`).

Record each finding using this format:

```
<file>:<lines>
  <ID> <Name> [<confidence>] — <target symbol>
    Evidence: <specific signals detected, with numbers>
    <Auto-fix|Recommendation>: <concrete action>
```

**Worked example:**

```
src/orders/service.py:L15-280
  2.1 God class [judgment] — OrderService
    Evidence: 12 public methods in 3 clusters sharing <20% instance state.
    Recommendation: Split into OrderLifecycle, OrderPricing, OrderNotifier.

src/orders/__init__.py:L1-8
  1.3 Barrel re-export [clear]
    Evidence: `from .service import *` re-exports 15 items, 3 consumed externally.
    Auto-fix: Replace with explicit named exports.

src/billing/engine.py:L20
  4.5 Law of Demeter [judgment] — calculate_order_total()
    Evidence: Navigates order.customer.address.region (depth 3).
    Recommendation: Add Order.shipping_region property.
```

### Step 4: Present Plan

Group findings into two sections — auto-fixable (clear) and architectural (judgment). Include impact assessment for judgment items.

```
## Boundary Guard Plan

### Auto-Fix (Clear)

#### src/orders/__init__.py
- [clear] FIX barrel re-export (L1-8) — replace `import *` with 3 explicit named exports

### Recommendations (Judgment)

#### src/orders/service.py
- [judgment] SPLIT OrderService (L15-280) — god class, 3 responsibility clusters
  Impact: consumed by 2 modules. Requires import updates in src/billing/, src/api/.

#### src/billing/engine.py
- [judgment] MOVE calculate_order_total (L20) — feature envy, 4 Order fields, 0 own fields

**Total: 1 auto-fix | 2 recommendations**
```

Ask: "Apply the auto-fix now? I'll walk through recommendations one by one."

### Step 5: Apply Changes

**Order of operations:**

1. **Apply clear auto-fixes** following the catalog's transform ordering (cross-boundary → module → function)
2. **Walk through judgment findings** one by one, ordered by impact (highest first):
   - Show the current code and the violation
   - Explain the impact and blast radius (what else would need to change)
   - Present the recommended approach
   - Wait for the user's decision: apply, skip, or modify the approach

For auto-fixes, verify after each change that imports and references still resolve correctly.

For architectural recommendations, if the user approves:
- Perform the refactoring (split class, move method, redesign interface)
- Update all affected imports and references
- Preserve all existing behavior — boundary improvements must not change what the code does

### Step 6: Verify

1. **Run linter/formatter** — if the project has one configured, run on changed files
2. **Run tests** — execute the test suite on affected modules
3. **Check results** — if tests fail, investigate whether the refactoring introduced a regression or exposed a pre-existing issue
4. **Summarize** using this template:

```
## Boundary Guard Summary

- **Auto-fixes applied:** N — brief list of what changed
- **Recommendations applied:** N of M — brief list
- **Recommendations skipped:** N — reasons for each
- **Modules affected:** list of module paths
- **Issues discovered:** regressions or pre-existing issues found during verification
```

## Escalation

If the user's intent is ambiguous (boundary check vs. code review vs. refactoring):
→ Ask: "Are you looking for a boundary analysis, a general code review, or help with a specific refactoring?"

If module boundaries are unclear (monorepo with unclear ownership):
→ Ask: "I can't determine the module boundaries in this area. Can you tell me what constitutes a module here?"

If a fix would cascade across 3+ modules:
→ Report the violation and blast radius. Ask: "This fix would touch N modules. Want me to draft the full refactoring plan, or just document the violation for now?"

If the codebase has no clear module structure (flat directory):
→ Note: "No module boundaries detected — analysis limited to class and function levels." Skip levels 1 and 4.

## Edge Cases

- **No violations found** — report the code as well-bounded at the analyzed levels.
- **Single-file scope** — skip module-level and cross-boundary analysis, focus on class and function levels.
- **Language with compiler-enforced encapsulation** (Rust, Go) — focus on design-level violations (god classes, mixed concerns, interface design) rather than visibility violations the compiler already catches.
- **Framework conventions override principles** — some frameworks require public methods for dependency injection, serialization, or routing. Treat framework-required public surface as intentional. Only flag public items that aren't required by the framework.
- **Data transfer objects at system boundaries** — API request/response types, serialization models, and protocol buffers are expected to be behavior-free data structures. Do not flag these as "data bags" (2.3) or "anemic models" (2.4).
- **Test files in scope** — skip them. Encapsulation analysis targets production code structure.
