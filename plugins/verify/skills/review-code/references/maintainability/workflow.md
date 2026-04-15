# Maintainability Review Workflow

Review code for clean code violations, code smells, SOLID principle breaches, design anti-patterns, naming/readability issues, dead/unused/redundant code, useless tests, and useless comments.

## Process

1. Determine scope
2. Scan for hot spots
3. Review code
4. Analyze findings
5. Verify findings
6. Write report

### 1. Determine Scope

Ask the user (skip if already clear from context):
- Which files, modules, or directories to review? (or full project)
- Any specific concerns or areas of pain?
- Language/framework context if not obvious from the codebase

### 2. Scan for Hot Spots

Run the metrics scanner to identify files that warrant the closest attention:

```
uv run --script ${CLAUDE_PLUGIN_ROOT}/skills/review-code/scripts/code_metrics.py --repo <path>
```

This writes to `.hand-offs/code-metrics.md`. Use the hot spots (large files, long functions, high import counts, many parameters) to prioritize which files to review first.

Always run the script for fresh data, even if `.hand-offs/code-metrics.md` already exists.

### 3. Review Code

Launch 2-3 explorer agents in parallel:

**Agent 1 — Code Smells & Design:**
- Bloaters: long methods, large classes, long parameter lists, data clumps, primitive obsession
- Couplers: feature envy, inappropriate intimacy, message chains, middle man
- Change preventers: divergent change, shotgun surgery
- OOP abusers: refused bequest, temporary fields, anemic domain models
- Speculative generality (unused abstractions, single-implementor interfaces)
- Return a list of 5-15 files with one-line descriptions of the pattern found at each location

**Agent 2 — SOLID & Naming:**
- SRP violations: classes with multiple reasons to change, vague names ("Manager", "Handler")
- OCP violations: growing if/elif/switch chains for variants
- LSP violations: subclasses that override to no-op or raise
- ISP violations: fat interfaces, implementors with stub methods
- DIP violations: business logic directly instantiating infrastructure
- Naming: misleading names, inconsistent vocabulary, abbreviations, boolean blindness, magic numbers
- Return a list of 5-15 files with one-line descriptions of the pattern found at each location

**Agent 3 — Dispensables:**
- Dead/unused code: unused imports, unreachable code, vestigial features, dead feature toggles
- Redundant code: redundant conditionals, unnecessary wrapping, duplicate logic
- Test anti-patterns: tests without assertions, excessive mocking, implementation detail testing, happy-path-only coverage
- Comment anti-patterns: obvious comments, outdated comments, commented-out code, zombie TODOs
- Return a list of 5-15 files with one-line descriptions of the pattern found at each location

After agents return, read the key files they identified to verify findings.

### 4. Analyze Findings

Load the relevant reference for each dimension:

| Dimension | Reference | Load When |
|-----------|-----------|-----------|
| Code smells, SOLID, naming | [code-smells.md](code-smells.md) — Bloaters, OOP abusers, change preventers, couplers, SOLID violations, naming/readability patterns | Full review, or when structural/design issues found |
| Dead code, tests, comments | [dispensables.md](dispensables.md) — Dead/unused code, redundant code, test anti-patterns, comment anti-patterns | Full review, or when dispensable code found |

For each finding:
1. Name the pattern (use established names from the references)
2. Cite specific files and line numbers
3. Assess severity using the definitions in [shared-quality-standards.md](../shared-quality-standards.md)
4. Explain the concrete risk (not abstract theory)
5. Provide a specific, actionable recommendation

### 5. Verify Findings

Apply the verification checklist from [shared-quality-standards.md](../shared-quality-standards.md). Additionally:
- Flag pervasive patterns once with a representative example rather than listing every instance
- Verify that flagged patterns are genuine issues, not intentional conventions established across the codebase

### 6. Write Report

Write to `.hand-offs/reviews/maintainability/YYYY-MM-DD-HHMM.md`. Create `.hand-offs/reviews/maintainability/` if it does not exist.

- **timestamp**: `YYYY-MM-DD-HHMM` (e.g., `2026-03-04-1430`)
- Example: `.hand-offs/reviews/maintainability/2026-03-04-1430.md`

```markdown
# Maintainability Review: <Scope>

> Reviewed: <date> | Scope: <files/modules reviewed> | Health: <Clean | Mostly clean with issues | Needs cleanup>

## Metrics Summary

<Key numbers from code_metrics.py: file count, LOC, hot spots count>

## Findings

### Code Smells & Design

**[Severity] <Pattern Name>**
Location: `path/to/file.py:42`
Issue: <What the issue is, concretely>
Risk: <What can go wrong>
Fix: <Specific, actionable recommendation>

### SOLID Violations

<Same format per finding>

### Naming & Readability

<Same format per finding>

### Dead & Redundant Code

<Same format per finding>

### Test Quality

<Same format per finding>

### Comment Quality

<Same format per finding>

<!-- Order findings by severity within each section: Critical -> High -> Medium -> Low -->
<!-- Omit sections with no findings -->

## Summary

| Severity | Count |
|----------|-------|
| Critical | N |
| High | N |
| Medium | N |
| Low | N |

**Top recommendations:**
1. <Highest impact recommendation>
2. <Second>
3. <Third>

**Overall assessment:** <Clean | Mostly clean with issues | Needs cleanup>
```

## Edge Cases

- If the codebase has no tests, flag the absence as a critical finding rather than skipping the test quality dimension.
- If the code_metrics.py script reports no hot spots, review is still valuable — hot spots guide priority, but maintainability issues exist at any file size.
- If the codebase consistently uses an imperfect pattern throughout, flag the pattern once with a representative example rather than flagging every instance.
- Focus on structural and semantic issues, not style preferences (tabs vs spaces, brace placement).
