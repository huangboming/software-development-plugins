# Triage Guide

## Elicitation Questions

Ask only what is missing. If the user's input already covers an area, skip it.

### Minimum viable intake (must know before writing)

1. **What** — What is being requested? (the need, not the solution)
2. **Who** — Who experiences this problem or has this need?
3. **Source** — Where did this come from? (customer, stakeholder, observation, etc.)

### Deepen understanding (ask if not obvious)

4. **Why now** — What changed? Is there urgency or a trigger event?
5. **Impact** — How many users/customers are affected? How severely?
6. **Current workaround** — What do people do today? (reveals pain intensity)

### Limit question volume

- First round: 2-4 questions max
- Follow-up rounds: 1-2 questions
- Stop asking when the minimum viable intake is covered. Remaining unknowns go into the assessment (clarity = partial/vague) or Raw Notes.

## Duplicate Detection

### What to check

| Location | What to look for |
|----------|-----------------|
| `.product/backlog/backlog.md` | Active items with similar scope or overlapping user need |
| `.product/prd/` | Existing PRDs that address the same problem space or feature area |
| `.product/research/` | Discovery documents covering the same user segment or problem |
| `.product/intakes/` | Prior intake records for the same or similar requirement |

### How to check

1. Read each file/directory that exists. Skip any that don't exist.
2. Compare by **problem and user need**, not by surface wording. "Faster search" and "search results take too long" are the same need.
3. Record findings in the Duplicate & Overlap Check table — both matches and no-matches.

### When overlap is found

Do not silently deduplicate. Report the overlap and describe how the new requirement relates:

- **Exact duplicate:** Same need, same scope → flag it, note the existing item, ask if user wants to reinforce priority or add new evidence
- **Partial overlap:** Related but different scope → note the relationship, capture the new requirement separately
- **Superset/subset:** New requirement contains or is contained by an existing item → flag it, ask if the scope should expand or if this is a separate increment

## Assessment Calibration

### Category decision tree

```
Is this something the product cannot do at all today?
  → Yes: new-capability
  → No: Does the product do it but poorly or incompletely?
    → Yes: Is the issue causing user pain/failure?
      → Yes: pain-point
      → No: enhancement
    → No: Is this driven by legal/regulatory/policy?
      → Yes: compliance
      → No: Is this infrastructure that enables future work?
        → Yes: technical-enabler
        → No: Re-examine — it should fit one of the above
```

### Clarity levels

| Level | Meaning | What this signals |
|-------|---------|-------------------|
| clear | Problem, users, and scope are well-defined. Could write a feature PRD from this. | Ready for backlog |
| partial | Problem is understood but scope or user details need work. | May need brief follow-up before backlog |
| vague | Problem is fuzzy, users are unclear, or the need is speculative. | Likely needs discovery (research-users) first |

### Size estimation heuristics

These are rough heuristics, not commitments. The goal is order-of-magnitude, not precision.

| Signal | Points toward |
|--------|--------------|
| Touches one component, one team | small |
| Has a clear existing pattern to follow | small |
| Needs UI + backend + data model changes | medium |
| Requires design iteration or user testing | medium |
| New domain concept or entity | medium-large |
| Needs new infrastructure or third-party integration | large |
| Cross-team coordination required | large |
| "We've never done anything like this" | large |

## Batch Intake

When the user provides multiple requirements at once (e.g., "here are 5 things from the retro"):

1. Process each item individually through the full intake flow
2. Write separate intake records for each
3. After all are captured, present a summary table:

```markdown
| # | Intake | Category | Size | Clarity | Overlaps |
|---|--------|----------|------|---------|----------|
| 1 | ... | ... | ... | ... | ... |
```

4. Ask if any need correction before finalizing
