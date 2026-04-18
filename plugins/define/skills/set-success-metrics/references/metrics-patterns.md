# Metrics Patterns

Catalog of metric patterns — north-star candidates by product shape, guardrail categories, vanity-to-outcome rewrites, and instrumentation planning guidance. Read in Step 2 for north-star shortlisting and in Step 3 for guardrail selection.

## North-star candidates by product shape

The north-star measures whether the user's job got done better. Shape-match it to the kind of value the slice is delivering.

| Slice shape | North-star candidates (pick one) |
|---|---|
| **New workflow / activation** | Time-to-first-value (median minutes from signup to first completed job). Activation rate (% of new users completing the core job in first N days). |
| **Retention / habit formation** | % of users completing the job in N of the last M weeks (e.g. "3 of 4"). D28 retention for segment X. Session-gap median (inverse of return rate). |
| **Workflow replacement** (replacing a manual or external process) | Substitution rate (% of the job done through the product vs. through the old path). Median time saved per completion, measured against the workaround baseline. |
| **Efficiency / throughput** | Jobs completed per active user per week. Tasks per session at quality ≥ Q. |
| **Self-serve conversion** | % of users completing the upgrade or configuration unaided (no support ticket opened within 48h of attempt). |
| **Trust / correctness** | Rate of user-corrected outputs (inverse — lower is better). % of sessions with zero recorded errors AND a completed job. |
| **Revenue-adjacent** | Revenue per active user, expansion rate, or seat-activation rate — but only if the slice is load-bearing on revenue. For most slices, a leading-indicator outcome metric is sharper. |

If two candidates are tied, prefer the one closer to the user's own experience of the job — a metric the user could feel is sharper than a metric only the team can see.

## Output vs outcome — the rewrite table

Output metrics are easy to measure and easy to game. Rewrite each into the outcome it proxies.

| Output (vanity) | Outcome (rewrite) |
|---|---|
| Sign-ups | D7 activation — % of signups who complete the core job within 7 days |
| Page views on the dashboard | Weekly reports exported per active manager, segment X |
| CSV download count | Managers exporting ≥ 1 report in 3 consecutive weeks |
| Feature adoption rate | Task completion — % of users who finish the job the feature supports |
| Time on page | Jobs completed per session at quality ≥ Q |
| Total users | Weekly active users completing the core job |
| Button clicks | % of sessions where the click led to a completed job |
| Demos booked | Demos that convert to a first completed job within N days |

The pattern: outputs count actions; outcomes count jobs done. When stuck, ask "what would the user tell their manager they accomplished?" — the answer is closer to an outcome.

## Guardrail categories

Guardrails protect the north-star from false wins. Pull from these categories, picking only the ones where regression would invalidate the gain.

- **Performance** — p95 or p99 latency on the core flow, time-to-interactive, largest-contentful-paint on entry pages. Pick when the slice touches a user-perceptible render or response path.
- **Reliability** — error rate per 1000 sessions, crash-free session rate, successful-request ratio for critical calls. Pick when the slice adds new failure surface.
- **Retention** — D7 or D28 retention, weekly-active-to-monthly-active ratio. Pick when the slice could juice activation at the cost of people bouncing later.
- **Support load** — tickets per 1000 active users touching the feature, self-serve deflection rate, CSAT for related queries. Pick when the slice introduces new interaction patterns.
- **Unit economics** — cost per job (infra + vendor), margin per active user, cost-of-goods per unit outcome. Pick when the slice shifts cost structure (new API, new model call, new storage shape).
- **Safety / quality** — error-of-record rate, hallucination rate (for LLM output), data-loss rate. Pick when correctness is load-bearing on trust.
- **Equity across segments** — variance in north-star across segments that should be served equally. Pick when the slice could improve the aggregate by worsening a segment.

Apply the **false-win test** (defined in `metrics-template.md`) to each candidate before keeping it.

## Common guardrail thresholds — starting points

Treat as defaults to adjust, not commitments. The right threshold comes from the current baseline plus the team's risk appetite; these are starting points when no baseline exists.

| Guardrail | Starting threshold |
|---|---|
| p95 latency on an existing flow | No regression beyond +10% vs current baseline |
| Error rate on a critical call | No regression beyond +20% relative (e.g., 0.5% → 0.6% max) |
| D28 retention | No regression beyond −2 percentage points vs control segment |
| Support ticket rate | No regression beyond +15% tickets/1000 active users |
| Cost per job | No regression beyond +20% vs prior month |

Numbers adjust with team risk tolerance; what is non-negotiable is that each threshold is stated as a number plus a segment plus a window.

## Instrumentation planning

For each metric, one of three states:

- **Measurable today.** Event + storage already exist. Name the source; no blocker.
- **Partially measurable.** Source exists but needs a new view, join, or derived field. Name the work and the owner. Can usually land in parallel with the slice build.
- **Not measurable.** Source event or field does not exist. The PRD must include the instrumentation work as a scope item, or the launch ships blind on this metric.

The common trap is marking a metric `Measurable today` based on "the event fires" without checking that segment, window, and numerator/denominator are all computable from the current schema. Verify the full formula is computable, not just that a log line exists.

If the team is asked to pick between "launch blind on the right metric" vs "launch sighted on a weaker proxy", pick the right metric and delay the launch — a slice that cannot prove its hypothesis is not shipping, it is hoping.

## Anti-patterns

Avoid these failure modes — each one looks like rigor but isn't.

- **Metric inflation.** Listing eight guardrails so the team can always point to "one that moved". Three to five is enough.
- **Fuzzy denominators.** "% of users" without naming the denominator (all users? active users? touched-the-feature users?). Denominators drive the number more than numerators — pin them.
- **Leading indicators dressed as north-stars.** "Button clicks" is not an outcome even if the slice is about button clicks. Ask what the click is supposed to *lead to*, measure that.
- **Moving targets.** Targets that get re-set post-hoc to match the observed result. Commit the target in writing before launch. If it was wrong, write a note about why, do not silently replace it.
- **Owner-by-committee.** "The team" owning a metric means no one reads it. Name a person. If the metric spans teams, name the accountable one — not the list.
- **Baseline by intuition.** A baseline inferred from memory ("I think it's around 30%") is treated as a real number downstream. Mark it `TBD` if it was not measured; don't dress intuition as data.
