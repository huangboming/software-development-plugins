# Simplification Catalog

Pattern categories, confidence rules, and transform ordering for code simplification.

## Transform Ordering

Apply changes in this order within each file:

| Order | Category | Rationale |
|-------|----------|-----------|
| 1 | Dispensables | Removing dead code reduces noise and may eliminate false positives in subsequent categories |
| 2 | Complexity reduction | Refactoring is easier and less error-prone in clean code |

Within each category, process changes bottom-up (last line first) to preserve line numbers for subsequent edits.

## Confidence Rules

Every transform is classified as **clear** (apply without asking) or **judgment** (present to user for approval).

**Default to clear when:**
- The transform is mechanical (find-and-delete, direct substitution)
- Behavior is provably preserved (e.g., removing unreachable code)
- The pattern has no caveats or the caveats don't apply

**Default to judgment when:**
- The transform could change observable behavior
- Codebase-wide search is needed to confirm safety (e.g., deleting a function that might have external callers)
- Multiple valid transforms exist (e.g., how to split a long method)
- The pattern appears consistently across the codebase (may be intentional)

**Override to judgment** any normally-clear transform if:
- The file is in a critical path (payments, auth, data pipeline)
- The surrounding code suggests the "redundant" code may be intentional

## Category 1: Dispensables

Remove code that shouldn't be there. Generally the safest transforms.

| Pattern | Confidence | Caveat |
|---------|------------|--------|
| Unused imports | Clear | Python imports may have side effects. TypeScript type-only imports may be needed for declaration files. |
| Unreachable code | Clear | Verify guard condition is truly always-false, not just usually-false. |
| Vestigial functions/classes | Judgment | Requires codebase-wide search to confirm no callers. Check exports and dynamic references. |
| Dead feature toggles | Judgment | Confirm the flag is not toggled dynamically or via environment variables. |
| Redundant conditionals | Clear | `if x: return True else: return False` → `return x` and similar boolean-wrapping patterns. |
| Unnecessary wrapping | Judgment | Wrapper may exist for API stability, testing seams, or planned extension. |
| Over-defensive code | Judgment | Verify the value truly cannot be null/invalid by tracing all callers. |
| Commented-out code | Clear | Version control preserves history. |
| Obvious comments | Clear | Comments that restate what the code already says. |
| Outdated comments | Judgment | Verify the code is correct and the comment is wrong, not vice versa. |
| Zombie TODOs | Judgment | Check referenced issue/ticket is actually resolved before removing. |

## Category 2: Complexity Reduction

Make existing code simpler. These require more judgment about boundaries and naming.

| Pattern | Confidence | Key Decision Criteria |
|---------|------------|----------------------|
| Deep nesting → guard clauses | Clear | Apply at > 3 indentation levels. Invert conditions, return/continue early. |
| Long method → extract function | Judgment | Apply at > 30-40 LOC with identifiable blocks. Extracted function should have ≤ 3 parameters. Name after purpose, not implementation. |
| Complex conditionals → named booleans | Clear | Apply at > 2 clauses in a compound condition. |
| Magic numbers/strings → named constants | Clear | Any literal in logic without an explanatory name. Place constant at module/class level. |
| Long parameter list → parameter object | Judgment | Apply at > 4 parameters. Requires identifying right grouping and updating all callers. |
| Boolean blindness → named args/enums | Judgment | Boolean params unclear at call site. Requires updating all callers. |
| Duplicate logic → shared helper | Judgment | Extract at ≥ 3 occurrences, or 2 that are clearly the same responsibility. Verify blocks are truly identical, not superficially similar. |
| If/elif chain → lookup table | Clear | Only when cases are pure value mappings with no logic per branch. |

### Method Extraction Guidance

Method extraction is the highest-judgment transform. When boundaries are ambiguous:

- Comments labeling sections are natural extraction points
- Variables used only within a contiguous block indicate a candidate
- If the extracted function would need > 3 parameters, the boundary is wrong — look for a different split
- Present 2 options with trade-offs when the split is genuinely ambiguous
