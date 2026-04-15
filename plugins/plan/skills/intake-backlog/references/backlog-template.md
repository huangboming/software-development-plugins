# Backlog Template

```markdown
# Product Backlog

> Last updated: <date>

## Active Items

| Item | Description | Source | Status | Added |
|------|-------------|--------|--------|-------|
| <short name> | <one sentence: what this is and why it matters> | <where it came from> | <New / Ready / In Progress> | <date> |

## Done

| Item | Description | Completed |
|------|-------------|-----------|
| <item> | <description> | <date> |

## Dropped

| Item | Description | Reason Dropped |
|------|-------------|----------------|
| <item> | <description> | <one sentence: why this was removed> |
```

### Usage Notes

- **Active Items** is the working inventory. Sort by status: `In Progress` first, then `Ready`, then `New`.
- **Done** and **Dropped** sections serve as decision records. Move items here rather than deleting them.
- Keep descriptions to one sentence. If more context is needed, link to a PRD or requirement doc.
- Source should be specific enough to trace back: "Customer feedback — 12 requests in Q1" is better than "feedback."
- When a backlog exceeds 30 active items, run a triage pass to prune — a backlog that large signals insufficient filtering upstream.

### Status Lifecycle

```
New → Ready → In Progress → Done
 │
 └→ Dropped
```

- **New:** Just captured. May need clarification before it can be scored.
- **Ready:** Enough context to score in a prioritization session.
- **In Progress:** Committed and actively being built.
- **Done:** Shipped.
- **Dropped:** Explicitly removed. Always include a reason.
