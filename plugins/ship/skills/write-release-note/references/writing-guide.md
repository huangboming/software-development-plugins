# Release Notes Writing Guide

## Writing for End Users

Lead with user benefit, not implementation. Use "you" language. Group by product area when there are 5+ changes, otherwise group by category.

| Principle | Example |
|-----------|---------|
| Name the user impact | "You can now export reports as CSV" |
| Quantify when possible | "Search results load 3x faster" |
| Explain breaking changes plainly | "The `/api/v1/users` endpoint now requires an API key. Update your integration by March 30." |
| Skip internal details | Omit class names, file paths, function names |

### Translating Commits to User-Facing Entries

| Commit Message | User-Facing Entry |
|---|---|
| "Fix NPE in TokenRefreshService.java:234" | "Fixed a crash that could occur when your session expired during file upload" |
| "Add Redis caching for dashboard queries" | "Dashboard pages now load up to 3x faster for returning users" |
| "Refactor payment module error handling" | "Improved reliability of payment processing during high traffic" |
| "Bump lodash from 4.17.15 to 4.17.21" | "Addressed a security vulnerability in a third-party dependency" |
| "feat: add CSV export to reports" | "You can now export any report as a CSV file" |
| "fix(auth): handle expired OAuth tokens gracefully" | "Fixed an issue where some users were unexpectedly logged out" |

## Writing Executive Summaries

Write for leadership. Lead with business outcomes. 3-5 bullet points maximum. No version numbers, no technical terms.

**Example:**

> This release focuses on performance and reliability:
> - Dashboard load times reduced by 60%, addressing the top customer complaint from Q4
> - Payment processing is now resilient to provider outages, eliminating the recurring weekend incidents
> - CSV export enables the sales team's requested workflow for bulk reporting

## Categorization Rules

### Category Definitions

| Category | Contains | Example Entry |
|----------|----------|---------------|
| Breaking Changes | Behavior incompatible with prior version; requires user action | "The `--format` flag now defaults to JSON instead of plain text" |
| Added | New features or capabilities | "You can now export reports as CSV" |
| Changed | Modified existing behavior (non-breaking) | "Improved error messages during checkout" |
| Fixed | Bug corrections | "Fixed a crash when uploading large files" |
| Deprecated | Features marked for future removal | "XML export is deprecated — use CSV or JSON instead. Removal planned for v4.0" |
| Removed | Deleted features or capabilities | "Removed legacy v1 API endpoints" |
| Security | Vulnerability patches | "Addressed a security vulnerability in session handling" |
| Performance | Measurable speed or resource improvements | "Dashboard pages now load up to 3x faster" |

### Inferring Categories from Commits

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
| `refactor:` | Omit unless behavior changed |
| `docs:` / `chore:` / `ci:` / `build:` / `test:` | Omit from release notes |
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
| "Various bug fixes and performance improvements" | Users cannot determine if their issue was addressed | Name each fix specifically |
| "Fixed NullPointerException in UserAuthMiddleware" | Internal jargon meaningless to users | Translate to user-visible impact |
| "Updated API endpoint behavior" | No context on what changed | State what changed, who is affected, required action |
| "Improvements and enhancements" | Empty calories — says nothing | Remove or replace with specifics |
| Burying breaking changes mid-list | Users miss critical action items | Always list breaking changes first |

## Quality Checklists

### User-Facing Release Notes

- [ ] Release overview frames the theme in 1-2 sentences
- [ ] Highlights (top 3-5 changes) appear before the detailed list
- [ ] Breaking changes listed first with migration guidance
- [ ] Every entry describes user impact, not implementation
- [ ] No internal jargon (class names, file paths, function names)
- [ ] No vague catch-alls ("various bug fixes", "minor improvements")
- [ ] Each entry is specific enough that a user can tell if their issue was addressed
- [ ] Changes grouped logically (by product area when 5+ changes, by category otherwise)
- [ ] Empty categories omitted
- [ ] Date is set

### Executive Summary

- [ ] 3-5 bullet points maximum
- [ ] Each bullet maps a change to a business outcome
- [ ] No version numbers or technical terminology
- [ ] Framed around customer/business impact, not feature list
