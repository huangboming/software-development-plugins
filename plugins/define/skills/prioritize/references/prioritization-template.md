# Prioritization Template

```markdown
# <Scope> — Prioritization

> Last updated: <date>
> Participants: <who was involved in scoring>
> Framework: <RICE | ICE | MoSCoW | Value vs Effort | WSJF>

## Context

- **Target outcome:** <What OKR, goal, or metric are we prioritizing toward?>
- **Time window:** <What period do Reach/Impact estimates cover? e.g., "per quarter">
- **Capacity:** <How much can the team build? e.g., "~6 engineer-weeks this sprint">
- **Scope:** <What is included in this prioritization? e.g., "All unstarted items in the search improvements epic">

## Prioritized Opportunities

<!-- Use the scoring table for your chosen framework. Delete the others. -->

### RICE

| Rank | Item | Reach | Impact | Confidence | Effort | Score | Rationale |
|------|------|-------|--------|------------|--------|-------|-----------|
| 1 | <item> | <number/period> | <Massive/High/Medium/Low/Minimal> | <100%/80%/50%/20%> | <person-months> | <score> | <one sentence: why this ranks here> |

### ICE

| Rank | Item | Impact | Confidence | Ease | Score | Rationale |
|------|------|--------|------------|------|-------|-----------|
| 1 | <item> | <1-10> | <1-10> | <1-10> | <score> | <one sentence: why this ranks here> |

### MoSCoW

#### Must Have

| Item | Rationale |
|------|-----------|
| <item> | <why this is non-negotiable for this time box> |

#### Should Have

| Item | Rationale |
|------|-----------|
| <item> | <why this is important but not fatal to omit> |

#### Could Have

| Item | Rationale |
|------|-----------|
| <item> | <why this is nice-to-have> |

### Value vs Effort

| Rank | Item | Value | Effort | Quadrant | Rationale |
|------|------|-------|--------|----------|-----------|
| 1 | <item> | <1-10 or Low/High> | <1-10 or Low/High> | <Quick Win / Big Bet / Fill-In / Money Pit> | <one sentence> |

### WSJF

| Rank | Item | User-Business Value | Time Criticality | RR/OE | Cost of Delay | Job Size | WSJF | Rationale |
|------|------|---------------------|------------------|-------|---------------|----------|------|-----------|
| 1 | <item> | <1-20> | <1-20> | <1-20> | <sum> | <1-20> | <score> | <one sentence> |

---

## Cut Line

> Items above this line are committed for <time box>. Items below are stretch goals or next-cycle candidates.

| Status | Items |
|--------|-------|
| **Committed** | <item 1>, <item 2>, ... |
| **Stretch** | <item 3>, <item 4>, ... |
| **Next cycle** | <item 5>, ... |

## Excluded Items

| Item | Why Excluded | Revisit Trigger |
|------|-------------|-----------------|
| <item> | <one sentence reason> | <what would change this decision> |

## Assumptions

- <Key assumption behind the scoring — what must be true for these rankings to hold>
- <Another assumption>

## Open Questions

- [ ] <Unresolved question that could change priorities if answered>
```

### Usage Notes

- Delete framework-specific scoring tables that are not used — only one framework table should remain.
- The Cut Line section is optional but strongly recommended when capacity is constrained.
- Every excluded item should have a revisit trigger — this prevents relitigating the same decisions.
- Assumptions should focus on the most impactful uncertainties. If an assumption is wrong, which scores would change?
- For MoSCoW, there is no composite score — the ranking within each category is determined by dot voting or team consensus, documented in the Rationale column.
- Won't Have items from MoSCoW go in the Excluded Items table.
