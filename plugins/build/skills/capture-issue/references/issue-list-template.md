# Issue List Template

The rolling list at `.product/build/issues/issues.md` is the index over per-issue records. It exists so issues are discoverable without reading every file in the directory.

```markdown
# Build Issues

> Last updated: <date>

## Open

| ID | Category | Summary | Severity | Size | Status | Added |
|----|----------|---------|----------|------|--------|-------|
| <slug> | <bug / refactor / tech-debt / perf-internal> | <one-line summary> | <blocker / high / medium / low / n/a> | <small / medium / large> | <New / Triaged / In Progress> | <date> |

## Resolved

| ID | Category | Summary | Resolution | Closed |
|----|----------|---------|------------|--------|
| <slug> | <category> | <summary> | <fixed / won't-fix / duplicate / obsolete> | <date> |
```

## Usage Notes

- **ID** is the filename slug without the `.md` extension. This makes the record file one click away from the list.
- **Open** section is the working inventory. Sort by severity (blocker → low), then by added date.
- **Resolved** serves as a decision record. Move rows here rather than deleting them.
- Keep `Summary` to one line. Detail lives in the per-issue record.
- Bump `Last updated` on every mutation — add, update, or status change. A stale date makes the list untrustworthy.

## Status Lifecycle

```
New → Triaged → In Progress → Resolved
 │
 └→ Resolved (won't-fix / duplicate / obsolete)
```

- **New:** Just captured. May need reproduction or scoping before pickup.
- **Triaged:** Enough context to prioritize — severity confirmed, size estimated, owner identifiable.
- **In Progress:** Actively being worked.
- **Resolved:** Closed out. Always record a resolution reason:
  - `fixed` — code change landed.
  - `won't-fix` — explicit decision not to address.
  - `duplicate` — consolidated into another issue (link in the record).
  - `obsolete` — the surrounding code or behavior no longer exists.
