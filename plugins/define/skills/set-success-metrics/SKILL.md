---
name: set-success-metrics
description: "Turn a committed slice's success signals into locked metric definitions (north-star + guardrails) and write them to .product/define/metrics/<slug>.md — runs after slice-mvp and before write-prd. Slash command: /set-success-metrics. Forces outcome metrics over vanity output metrics, demands a definition, data source, baseline, target, timeframe, and owner per metric, and runs an instrumentation gate — if a metric cannot be computed today, the work needed to measure it is named before launch. Reads .product/define/slices/<slug>.md when present; falls back to .product/discover/opportunities/<slug>.md for standalone use. Feeds write-prd. Not for filling the metrics section of a PRD already in progress — use write-prd for that. Not for retrospective metric reviews (measure plugin), not for deciding what to build (prioritize), and not for scoping what to ship (slice-mvp). Triggers: '/set-success-metrics', 'set success metrics', 'set metrics for this slice', 'commit metrics for this slice', 'define success metrics', 'set launch criteria', 'define OKRs for this feature', 'what does success look like for this', 'north-star metric', 'guardrail metrics', 'what metrics matter', 'how do we measure success', 'how will we know this worked', 'define KPIs for this', 'metrics before PRD', 'instrument this slice', 'turn signals into metrics'."
---

# Set Success Metrics

Define the north-star and guardrail metrics for a committed slice and write them to `.product/define/metrics/<slug>.md`. The doc commits a measurable definition of success — outcome metrics with formula, data source, baseline, target, timeframe, and owner — *before* the PRD is drafted, so the spec is written against what the team will be held to.

This skill defines the metrics. It does not run experiments (that is `test-assumption`), does not draft the spec (that is `write-prd`), and does not review post-launch numbers (that is the `measure` plugin).

## References

- [references/metrics-template.md](references/metrics-template.md) — Template, field guidance, slug naming, status lifecycle, quality check, rewording test for targets, false-win test for guardrails, summary format, and edge case handling. Read at the start of Step 4 (before writing) and again after writing (quality check and self-review). Also contains the edge case playbook — consult when any condition in the Edge Cases pointer at the bottom of SKILL.md matches.
- [references/metrics-patterns.md](references/metrics-patterns.md) — North-star candidates by slice shape, vanity-to-outcome rewrite table, guardrail categories with selection test, common guardrail threshold starting points, instrumentation planning, anti-patterns catalog. Read in Step 2 (north-star shortlisting) and Step 3 (guardrail selection).

## Process

Four steps: gather input, pick the north-star, pick guardrails, specify and write.

### 1. Gather input

Identify what the metrics are for:

- **User names a slug** → read `.product/define/slices/<slug>.md` and the source opportunity at `.product/discover/opportunities/<slug>.md`.
- **User says "set metrics" without specifying** → list slice files in `.product/define/slices/*.md` with Status `drafted` and no sibling metrics file in `.product/define/metrics/`. Ask which. If zero candidates exist, ask whether to run against an opportunity instead, or route to `slice-mvp` first. If the user declines both, state that `set-success-metrics` requires either a slice or an opportunity file as input and stop.
- **User points directly to an opportunity (no slice exists)** → see Edge Cases below. Default behavior is to offer routing to `slice-mvp` first, since metrics pinned to an unsliced opportunity tend to drift when scope is later narrowed.

Read the slice's Hypothesis, Load-bearing risk, User and job, and Signals fields in full. The Signals field in the slice is an intent — this skill turns it into a committed metric definition.

### 2. Pick the north-star metric

The north-star measures whether the user's job got done better — not whether the feature was used. Shape-match it to the slice.

1. Read the slice's Hypothesis and User + job fields.
2. Consult the **"North-star candidates by product shape"** table in `metrics-patterns.md` and shortlist 2–3 candidates.
3. Apply the **output-vs-outcome rewrite**: for each candidate, check the rewrite table in `metrics-patterns.md`. If the candidate is an output dressed as an outcome, rewrite it.
4. Present the top 2 candidates with a one-line rationale each and ask the user to confirm.
   - If the user is uncertain, apply the tiebreaker: pick the candidate closer to the user's felt experience of the job and state the reason.
   - If both candidates are genuinely equidistant on outcome-proximity and measurability, surface them both with a one-sentence consequence for each and ask the user to decide. If the user still cannot decide after one round, proceed with the candidate that is measurable today and record the choice in the doc's Open Questions field.

### 3. Pick guardrails

Guardrails protect the north-star from false wins. Pick 3–5.

1. Walk the **guardrail categories** in `metrics-patterns.md`: performance, reliability, retention, support load, unit economics, safety/quality, equity across segments.
2. Apply the **false-win test** (from `metrics-template.md`) to each candidate. Keep only the ones where the answer is yes. If no baseline exists, use the **Common guardrail thresholds** table in `metrics-patterns.md` as a starting point and adjust with the user.
3. Keep 3–5. If none pass the false-win test, state that explicitly in the doc with one sentence on why.

### 4. Specify and write

Execute the following in order:

1. For each metric (north-star and each guardrail), fill every field as specified in the template in `metrics-template.md`.
2. Fill the **Instrumentation gate** table. Honestly classify each metric as `Yes / Partially / No` on measurability today. For anything less than `Yes`, name the instrumentation work and the owner. See the "Instrumentation planning" section of `metrics-patterns.md` for the common trap (marking `Yes` when only a log line exists but the full formula is not computable).
3. Fill the **Anti-vanity check**: name one tempting output metric that was rejected and why. If nothing was tempting, the north-star likely was not debated enough — go back to Step 2. Consult the **Anti-patterns** section of `metrics-patterns.md` for common failure modes (metric inflation, fuzzy denominators, moving targets).
4. If any required field is blocked on input the user has not provided (baseline value, instrumentation owner, data source the team uses), pause. State the specific blocker and ask before proceeding, rather than writing placeholder numbers that read as real.
5. Run the **quality check** from `metrics-template.md` against the drafted fields. Apply the rewording test to targets and the false-win test to guardrails. Fix violations in place.
6. Create `.product/define/metrics/` if it does not exist.
7. Write the metrics doc at `.product/define/metrics/<slug>.md` with Status `drafted`. Slug naming is in `metrics-template.md` (reuse the slice's slug).
8. Append a `Metrics:` link to the source slice file pointing at the new metrics doc. Do not change the slice's Status — that transitions when `write-prd` consumes both.
9. Present the summary using the **Summary format** section of `metrics-template.md` and ask the user to confirm or correct. Apply corrections in place, re-run the quality check on changed fields, and re-present only what changed. If after one correction round a field still fails the quality check and the user cannot or will not resolve it, write the file with the field marked `[INCOMPLETE — reason]` and state what is needed before `write-prd` can consume the metrics doc.

## Edge Cases

For edge cases (incomplete slice signals, opportunity-only input, unmeasurable baseline, instrumentation gaps, guardrail overflow, contested targets, pre-existing metrics doc, hypothesis-free slices), see the **Edge case playbook** section of `metrics-template.md`.
