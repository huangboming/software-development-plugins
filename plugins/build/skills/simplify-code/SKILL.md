---
name: simplify-code
description: "Simplify code using a comprehensive pattern catalog, targeting user-specified scope. Triggers: 'simplify this code', 'clean up this module', 'reduce complexity', 'remove dead code', 'deep simplify', 'clean up this file'."
---

# Simplify Code

## Arguments

Parse from the user's request:

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| scope | no | changed files | Files, directories, or modules to simplify |
| focus | no | all | Category filter: `dispensables`, `complexity`, or `all` |

**Parsing examples:**

- "simplify this code" → scope: changed files, focus: all
- "clean up src/api/" → scope: src/api/, focus: all
- "remove dead code in the billing module" → scope: billing module, focus: dispensables
- "reduce complexity in this file" → scope: current file, focus: complexity

## References

- [references/simplification-catalog.md](references/simplification-catalog.md) — Pattern categories, confidence rules, and transform ordering. Read before analyzing code.

## Process

1. Determine scope
2. Load context
3. Analyze and classify
4. Present plan
5. Apply fixes
6. Verify and summarize

### Step 1: Determine Scope

Resolve target files:

- **Explicit paths** — use what the user specified
- **"changed files"** (default) — `git diff --name-only HEAD` and `git diff --name-only --staged`
- **Directory** — glob for source files, excluding generated/vendored files

Skip auto-generated files (protobuf, OpenAPI codegen, migrations) and minified/bundled files.

If no changed files and no scope specified, ask what to simplify.
If scope resolves to >20 files, ask: "That's N files. Focus on the most complex ones first, or work through all?"

### Step 2: Load Context

Load in parallel:

1. **Simplification catalog** — read [references/simplification-catalog.md](references/simplification-catalog.md).
2. **Target code** — read all files in scope.

### Step 3: Analyze and Classify

For each file, identify simplification opportunities using the catalog's pattern tables. For each opportunity:

1. **Name the pattern** from the catalog
2. **Note file and line(s)**
3. **Draft the transform**
4. **Assign confidence** per the catalog's rules: **clear** (mechanical, apply without asking) or **judgment** (may change behavior, present first). Default to judgment when uncertain.

### Step 4: Present Plan

Group findings by file, then by category:

```
## Simplification Plan

### path/to/file.py

- [clear] Remove unused import `foo` (L12)
- [judgment] Extract method from `process_order` (L67-120) — 54 LOC, 3 nesting levels

**Total: N changes across M files (X clear, Y need review)**
```

Ask: "Apply all clear changes? I'll show judgment calls individually."

### Step 5: Apply Fixes

Follow the catalog's transform ordering (dispensables → complexity). Within each category, process bottom-up (last line first) to preserve line numbers.

- **Clear** changes: apply directly
- **Judgment** changes: show before/after, explain trade-off, wait for approval

### Step 6: Verify and Summarize

1. **Verify** — if the project has a linter or formatter, run it on changed files. Suggest running tests.
2. **Summarize** — report files changed, changes applied/skipped by category, and per-file change descriptions.

## Escalation

If the user's intent is ambiguous (simplify vs. refactor vs. review):
→ Ask: "Are you looking for quick cleanup, deeper simplification, or a full code review?"

If a transform could change observable behavior:
→ Classify as **judgment** even if normally **clear**.

If a pattern appears consistently across the codebase:
→ Treat as intentional convention. Flag once as "Potential — verify intent."

## Edge Cases

- **No simplification opportunities** — report the file as clean.
- **Large function extraction is ambiguous** — present 2 options with trade-offs.
