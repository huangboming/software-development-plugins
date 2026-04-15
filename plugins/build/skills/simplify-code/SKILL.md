---
name: simplify-code
description: "Simplify code with project-aware checks — reads project guidelines, uses a comprehensive pattern catalog, and targets user-specified scope. Triggers: 'simplify this code', 'clean up this module', 'reduce complexity', 'remove dead code', 'enforce our code guidelines', 'deep simplify', 'simplify against guidelines', 'clean up this file'."
---

# Simplify Code

## Arguments

Parse from the user's request:

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| scope | no | changed files | Files, directories, or modules to simplify |
| focus | no | all | Category filter: `dispensables`, `complexity`, `guidelines`, or `all` |

**Parsing examples:**

- "simplify this code" → scope: changed files, focus: all
- "clean up src/api/" → scope: src/api/, focus: all
- "remove dead code in the billing module" → scope: billing module, focus: dispensables
- "reduce complexity in this file" → scope: current file, focus: complexity
- "enforce our code guidelines on changed files" → scope: changed files, focus: guidelines

## References

- [references/simplification-catalog.md](references/simplification-catalog.md) — Pattern categories, confidence rules, and transform ordering. Read before analyzing code.
- [references/guideline-integration.md](references/guideline-integration.md) — How to read and apply project code guidelines from `docs/development/code-guidelines/`. Read only when project guidelines exist and focus includes guidelines.

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

1. **Project guidelines** — check if `docs/development/code-guidelines/` exists. If found, read all `.md` files and load [references/guideline-integration.md](references/guideline-integration.md).
2. **Simplification catalog** — read [references/simplification-catalog.md](references/simplification-catalog.md).
3. **Target code** — read all files in scope.

If no guidelines exist and focus is `guidelines`, inform the user and run with generic patterns instead.

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

Follow the catalog's transform ordering (dispensables → complexity → guidelines). Within each category, process bottom-up (last line first) to preserve line numbers.

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
- **Guidelines contradict catalog** — project guidelines take precedence.
