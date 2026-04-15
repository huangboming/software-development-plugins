# Changelog Writing Guide

## Writing for Contributors

Write for developers and contributors. Use precise language, reference PR/issue numbers, and start each entry with an imperative verb.

| Principle | Example |
|-----------|---------|
| Imperative verb start | "Add CSV export endpoint for reports (#342)" |
| Include references | "Fix token refresh race condition (fixes #891)" |
| Note API/behavior changes | "Change `GET /users` to require `Authorization` header" |
| State before/after for breaking changes | "Rename `user.fullName` to `user.displayName` in API response" |

## Categorization Rules

### Category Definitions

| Category | Contains | Example Entry |
|----------|----------|---------------|
| Breaking Changes | Behavior incompatible with prior version; requires user action | "The `--format` flag now defaults to JSON instead of plain text" |
| Added | New features or capabilities | "Add bulk import for user accounts" |
| Changed | Modified existing behavior (non-breaking) | "Improve error messages for form validation" |
| Fixed | Bug corrections | "Fix pagination returning duplicate results on page boundaries" |
| Deprecated | Features marked for future removal | "Deprecate XML export; use CSV or JSON instead. Removal planned for v4.0" |
| Removed | Deleted features or capabilities | "Remove legacy v1 API endpoints" |
| Security | Vulnerability patches | "Patch stored XSS vulnerability in comment rendering" |
| Performance | Measurable speed or resource improvements | "Reduce memory usage by 40% for large file uploads" |

### Inferring Categories from Non-Conventional Commits

When commit messages lack type prefixes, infer from content:

| Signal in Commit Message | Likely Category |
|--------------------------|----------------|
| "add", "new", "introduce", "support", "implement" | Added |
| "change", "update", "modify", "adjust", "improve" | Changed |
| "fix", "resolve", "correct", "patch", "handle" | Fixed |
| "remove", "delete", "drop", "clean up" | Removed |
| "deprecate", "phase out" | Deprecated |
| "security", "CVE", "vulnerability", "XSS", "injection" | Security |
| "perf", "speed", "fast", "optimize", "cache", "reduce memory" | Performance |
| "breaking", "rename API", "remove endpoint", "change default" | Breaking Changes |

When ambiguous, default to Changed. Flag uncertain categorizations for user review.

### Conventional Commit Type Mapping

| Commit Type | Category |
|-------------|----------|
| `feat:` / `feat!:` | Added (Breaking if `!` or `BREAKING CHANGE` footer) |
| `fix:` | Fixed |
| `perf:` | Performance |
| `refactor:` | Changed (omit unless behavior changed) |
| `docs:` | Include if notable to contributors |
| `chore:` / `ci:` / `build:` / `test:` | Include selectively |
| `BREAKING CHANGE:` footer | Breaking Changes (regardless of type prefix) |

## Breaking Changes

Breaking changes require special treatment:

1. List first, before all other categories
2. Include migration guidance: what the user must do to adapt
3. State before/after behavior when applicable

**Example:**

> **Breaking:** The `--output` flag now defaults to `json` instead of `text`.
>
> **Migration:** If your scripts parse plain-text output, add `--output text` to preserve the previous behavior.

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| "Various bug fixes and performance improvements" | Cannot determine if a specific issue was addressed | Name each fix specifically |
| "Merge PR #234 from dev/feature-auth" | Git noise, not human communication | Write a human summary of the change |
| "Improvements and enhancements" | Empty calories — says nothing | Remove or replace with specifics |
| Burying breaking changes mid-list | Users miss critical action items | Always list breaking changes first |

## Quality Checklist

- [ ] Follows Keep a Changelog structure
- [ ] Each entry starts with an imperative verb
- [ ] PR/issue references included where available
- [ ] Breaking changes documented with before/after behavior
- [ ] Entries are specific and complete (not just commit subjects)
- [ ] Internal-only changes (refactors, CI, tests) included selectively and only when meaningful to contributors
- [ ] Empty categories omitted
