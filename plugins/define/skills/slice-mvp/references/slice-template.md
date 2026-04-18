# Slice Template

Template for the MVP slice document and field guidance. Read before writing a slice and during the self-review in SKILL.md Step 4.

## Template

```markdown
---
Status: drafted
Source opportunity: .product/discover/opportunities/<slug>.md
Slicing shape: <walking skeleton | vertical slice | concierge | wizard of oz | configuration-only | read-only | batch-before-real-time | other>
Sizing bar: <upper bound, e.g. "≤ 5 eng-weeks">
Last updated: <YYYY-MM-DD>
---

# MVP Slice: <human-readable title>

## Hypothesis

<One sentence: what the shipped slice will prove or deliver. Falsifiable — a reasonable reader could name a result that would contradict it.>

## Load-bearing risk

<One of: desirability, feasibility, viability. Reference the source opportunity's Confidence field or the tree's Risk field. One sentence on why this risk drives the slicing shape.>

## User and job

- **Segment:** <specific named segment, not "users">
- **Job:** <specific job-to-be-done, present tense>
- **Today's workaround:** <what they do now>

## Scope

### In (v1)

- <Concrete user-visible capability>
- <Concrete user-visible capability>

### Out (explicitly not v1)

- <Thing stakeholders would assume is in; include named pushback — e.g. "bulk import — sales will ask; not v1 because this slice tests pull from Monday reports first">

### Not now (v2+)

| Item | Unblock trigger |
|------|----------------|
| <thing> | <event or signal that activates this — outcome-shaped, not date-shaped> |

## Signals

- **Success:** <Quantitative. Threshold + sample size + window + segment. "≥ 40% of invited managers run the Monday report for 3 consecutive weeks, N ≥ 50">
- **Kill:** <Quantitative. Below this, roll back or re-scope or pivot. "< 15% run it even once, N ≥ 50">
- **Inconclusive zone:** <Between success and kill. Treated as "learn more before v2">

## Assumptions

- <What must be true for this slice to deliver value. Link to test plans in `.product/discover/assumptions/` if any.>

## Open questions

- [ ] <Unresolved item for the spec writer to resolve>
```

## Slug naming

Reuse the source opportunity's slug. If the slice represents a second cut of the same opportunity, append the cut descriptor:

- `weekly-report-reauthoring` → `weekly-report-reauthoring-marketers-only`

Lowercase, kebab-case, no dates in the filename (dates go in the Last updated field).

## Status lifecycle

| Status | Meaning |
|---|---|
| `drafted` | Written, not yet handed to `write-prd`. |
| `spec-drafted` | `write-prd` has consumed it and produced a PRD. Slice is now reference. |
| `shipped` | v1 is live. Awaiting success or kill signal result. |
| `superseded` | Replaced by a newer slice. Keep the file, mark the status. |

Do not delete superseded slices — they are the record of what was scoped out and why.

## Quality check

Before writing, verify the slice passes every item. Correct violations in place before presenting to the user.

- **Hypothesis is falsifiable.** A reasonable reader could name an observation that would contradict it. "Deliver value to users" is not falsifiable.
- **User is a named segment, not a persona archetype.** "Marketing managers at 50-200-person B2B companies" passes; "marketers" does not.
- **In list is user-observable.** Each item describes what the user can do, not what the team will build. "Export to CSV" passes; "CSV pipeline" does not.
- **Out list names the pushback.** Each Out item declares who will ask for it and why it is still Out. An empty Out list means the slice has not been scoped — it has been listed.
- **Not now items have triggers.** Each has an unblock signal ("when X passes Y"). Dates are not triggers — outcomes are.
- **Signals are quantitative and pre-written.** Both a threshold and a sample size or window. A signal that could be stated only after shipping is rationalization.
- **Inconclusive zone exists.** If success and kill thresholds touch, the middle gets interpreted to match what the team already wanted. Leave honest space.
- **Sizing bar is named.** Upper bound in eng-weeks, sprints, or calendar weeks. "Small" is not a bar.

### The rewording test for signals

Rephrase each signal as: "If we see [below kill bar], we will [specific action]." If the sentence ends with "we will investigate" or "we will think about it", the kill bar is not committing — rewrite until the action is concrete (roll back, re-scope, pivot, kill).

### The pushback test for Out items

For each Out item, ask: "which named stakeholder will push back, and what will they say?" If you cannot name them, the item is not contentious and does not need to be in Out. Move it to Not now or delete it.

## Summary format

After writing the file, present a summary in this format:

```
Slice drafted: <slug>
- Source: .product/discover/opportunities/<slug>.md (Status → sliced)
- Shape: <slicing shape> — <one-line narrowing>
- User + job: <segment>, <job>
- Load-bearing risk: <desirability | feasibility | viability> — <one-sentence rationale>
- In: <brief list>
- Out: <one representative item with pushback>
- Not now: <one representative item with trigger>
- Success: <threshold + sample size + window>
- Kill: <threshold + sample size + window>
- Sizing bar: <upper bound>
- File: .product/define/slices/<slug>.md

Next: write-prd builds the spec from this slice. When v1 ships, update Status in the slice file and in the source opportunity.
```

The summary is a decision record, not a full restatement. Keep each line to one piece of information.
