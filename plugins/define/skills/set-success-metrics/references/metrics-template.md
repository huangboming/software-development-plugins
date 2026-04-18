# Metrics Template

Template for the success metrics document and field guidance. Read before writing metrics and during the self-review in SKILL.md Step 4.

## Template

```markdown
---
Status: drafted
Source slice: .product/define/slices/<slug>.md
Source opportunity: .product/discover/opportunities/<slug>.md
Last updated: <YYYY-MM-DD>
---

# Success Metrics: <human-readable title>

## North-star metric

- **Name:** <named outcome metric>
- **What it measures:** <the user outcome this captures, in user terms — one sentence>
- **Definition / formula:** <exact definition; for ratios, state numerator and denominator; name the time window and segment>
- **Data source:** <event name + system, e.g. "report_exported in Amplitude, users_v2 in Snowflake">
- **Current baseline:** <value + date measured, or "TBD — see Instrumentation gate">
- **Target:** <value + timeframe, e.g. "≥ 35% by end of 2026-Q3">
- **Owner:** <named person accountable for reading this metric and acting on it>

## Guardrails

List the 3–5 metrics whose regression would turn a north-star gain into a false win. Each follows the same field set.

### <guardrail name>

- **What it protects:** <one sentence — the property that must not regress>
- **Definition / formula:** <exact definition; name the segment and window>
- **Data source:** <event + system>
- **Current baseline:** <value + date, or "TBD">
- **Must-not-cross threshold:** <e.g. "p95 weekly-report render time ≤ 3.0s over any rolling 7-day window; breach triggers rollback discussion">
- **Owner:** <named person>

Repeat the section above per guardrail.

## Instrumentation gate

For each metric above, one row:

| Metric | Measurable today? | If not — what lands before launch | Owner |
|---|---|---|---|
| <north-star name> | Yes / Partially / No | <instrumentation work, or "n/a"> | <name> |
| <guardrail 1 name> | ... | ... | ... |

A `No` or `Partially` on the north-star blocks launch readiness — the PRD must include the instrumentation work.

## Anti-vanity check

Name one output metric that was tempting but was rejected in favor of the north-star, and one sentence on why. Keeps the team honest and makes the choice auditable.

- **Rejected:** <output metric, e.g. "weekly-report exports per week">
- **Why not:** <one sentence — usually "measures activity, not the job getting done better">

## Open questions

- [ ] <Unresolved item — baseline estimate, segment definition, instrumentation owner, etc.>
```

## Slug naming

Reuse the source slice's slug (which reuses the source opportunity's slug). If metrics are redefined for a second cut of the same slice, append the cut descriptor matching the slice file name.

Lowercase, kebab-case, no dates in the filename (dates go in the Last updated field).

## Status lifecycle

| Status | Meaning |
|---|---|
| `drafted` | Written, not yet consumed by `write-prd`. |
| `locked` | `write-prd` has consumed the metrics. Definition and thresholds are frozen for v1; baseline and target can still move only with a rationale note. |
| `active` | v1 has shipped and these metrics are being read. Observed values noted post-launch. |
| `superseded` | Replaced by a newer metrics doc. Keep the file; mark the status. |

Do not delete superseded metric docs — they are the record of what was measured and what was dropped.

## Quality check

Before writing, verify the doc passes every item. Correct violations in place before presenting to the user.

- **North-star is an outcome, not an output.** It measures whether the user's job got done better, not whether the feature was used. "% of managers who publish the Monday report on time for 3 consecutive weeks" passes; "Monday report page views" does not.
- **North-star is tied to the slice's hypothesis.** Re-read the slice's Hypothesis field. If the north-star does not directly test the hypothesis, rewrite one or the other until they agree.
- **Every metric has a formula.** A metric without a numerator, denominator, window, and segment is ambiguous and will be re-computed three different ways by three different people. Name each component.
- **Every metric has a named data source.** An event name and a system, not a department. "`report_exported` in Amplitude" passes; "the analytics team" does not.
- **Every metric has an owner.** A named person accountable for reading the number and acting. "PM" or "the team" does not pass — ownership diffuses.
- **Baseline is either measured or explicitly TBD.** A baseline copied from intuition looks real and corrupts the target. If no baseline exists, write `TBD — see Instrumentation gate` and list the work needed.
- **Target has a timeframe.** "≥ 35%" is a wish; "≥ 35% by end of 2026-Q3" is a commitment.
- **Guardrails protect the north-star, not the feature.** Each guardrail names a property whose regression would mean the north-star lied. A latency guardrail on a feature that is not latency-sensitive is decoration.
- **The instrumentation gate is honest.** If the north-star is `No — not measurable today`, the PRD must land the instrumentation before ship. Marking it `Yes` because "we'll add a query later" is how unmeasurable launches happen.
- **Anti-vanity rejection is named.** An empty Anti-vanity section means no tempting alternative was considered — the team likely did not push hard on the north-star definition.

### The rewording test for targets

Rephrase each target as: "If we reach [target] by [timeframe], we will [specific next decision]." If the sentence ends with "we will celebrate" or "we will keep going", the target is not load-bearing — rewrite it until the next decision is concrete (invest further, expand segment, close the initiative, cut loss).

### The false-win test for guardrails

For each guardrail, ask: "Could the north-star move the right direction while this metric regresses enough to turn the win sour?" If no, the guardrail is decoration — remove it. If yes, it stays.

## Summary format

After writing the file, present a summary in this format:

```
Metrics drafted: <slug>
- Source slice: .product/define/slices/<slug>.md (link added)
- North-star: <metric name> — <target> by <timeframe>
- Guardrails: <count>, e.g. <one representative, with threshold>
- Instrumentation gate: <all Yes | N Partially | N No — blocker: …>
- Owner (north-star): <name>
- File: .product/define/metrics/<slug>.md

Next: write-prd consumes this doc and the slice to draft the spec. When v1 ships, set Status to `active` and record observed values post-launch.
```

The summary is a decision record, not a full restatement. Keep each line to one piece of information.

## Edge case playbook

Handle these conditions as described. Each entry names the trigger and the response.

If the **slice has no Signals field filled in**, or signals are qualitative only:
  → Slicing was incomplete. Offer to route back to `slice-mvp` to commit signals before metrics. If the user wants to push through, treat this skill as the first place signals get pinned and stamp a one-line note in the slice's Signals field pointing to the metrics doc.

If **no slice exists** and the user points directly to an opportunity:
  → Offer to run `slice-mvp` first. If the user declines (e.g., the opportunity is already narrow and they want to stamp metrics early), proceed — read from the opportunity's Who / Pain / What-good-looks-like fields instead of the slice's Hypothesis. Note `Source slice: none (opportunity-only — add slice link when created)` in the frontmatter. Be stricter about the quality check: without a slice, the Hypothesis anchor is missing and metrics drift more easily.

If **no baseline can be measured** for the north-star:
  → Mark baseline `TBD` and list the baseline-measurement work in the Instrumentation gate. Do not invent a baseline. If the PM pushes for a placeholder number "so the target feels real," decline — placeholder baselines become real targets downstream.

If the **north-star requires instrumentation that does not yet exist** and the team wants to launch anyway:
  → Make the tradeoff explicit in the summary: "Launching sighted on the north-star requires <work>. Launching blind is an option — mark it in the PRD's Open Questions." Do not quietly downgrade to a weaker proxy to preserve the launch date.

If the user **wants more than 5 guardrails**:
  → Push back once. Ask which ones would actually trigger a rollback if breached — metrics that would not trigger a decision are not guardrails, they are dashboard items. If the user insists, write them but mark the non-rollback-triggering ones as `watch-only` in the doc so they do not clutter the launch gate.

If the **target value is contested** (product wants aggressive, eng wants conservative):
  → Write both. Record "Target: <aggressive>, floor: <conservative>" in the Target field with a one-sentence note on what triggers each. A single averaged number hides the disagreement without resolving it.

If **metrics already exist** for the same slice:
  → Read the existing doc first. Ask whether to:
  - **Supersede** — rename the old to `<slug>-YYYY-MM-DD.md`, set its Status to `superseded`, and write a new doc at `<slug>.md`. Use when the slice was re-sliced or the hypothesis changed.
  - **Iterate in place** — overwrite only if the doc is still `drafted` and `write-prd` has not yet consumed it. Once Status is `locked`, use supersede — do not edit a `locked` metrics doc in place. Edits-in-place destroy the audit trail of what was committed at PRD time.

If the slice is **hypothesis-free or its hypothesis is unfalsifiable**:
  → Metrics cannot save a slice whose hypothesis does not commit. Pause. Route back to `slice-mvp` to sharpen the hypothesis. Do not paper over by picking a metric that would move regardless of the slice's effect. If the user insists on proceeding, state that metrics without a falsifiable hypothesis cannot pass the quality check and will be flagged `[INCOMPLETE]` in the doc.
