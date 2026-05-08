---
name: simplify-code
description: "Simplify code in a user-specified scope. Triggers: 'simplify this code', 'clean up this module', 'reduce complexity', 'remove dead code', 'clean up this file'."
---

# Simplify Code

Simplify code in the user's scope (default: `git diff --name-only HEAD` + staged). If scope is unclear, ask.

## Two essential rules

### 1. Clear vs. judgment

Every change is either **clear** or **judgment**:

- **Clear** — mechanical and behavior-preserving (unused imports, magic numbers → constants, deep nesting → guard clauses, commented-out code). Apply directly.
- **Judgment** — could change observable behavior, requires codebase-wide search, or has multiple valid forms (delete a possibly-unused function, extract method, deduplicate). Present before applying.

When in doubt → judgment. In critical paths (auth, payments, data integrity) → judgment regardless.

### 2. Order

Within each file: **dead code first, then complexity reduction**.

Within each pass: process **bottom-up** (last line first) to preserve line numbers across edits.

## Output

Present a plan grouped by file with `[clear]` / `[judgment]` tags. Apply clear changes silently; walk through judgment changes one at a time.

After applying: run the project's linter/formatter on changed files if one exists.
