# Assumption Test Plan Template

```markdown
# Assumption Test: [Short Name]

**Date designed:** [today's date]
**Status:** designed
**Source:** `.product/discover/opportunities/tree-<slug>.md` → Sub-Outcome N → Solution [name]
(or `.product/discover/opportunities/<slug>.md` when testing a framing-level assumption)

## Assumption

[One sentence. The specific load-bearing claim to test — not the category.]

**Type:** [desirability | viability | feasibility | usability]
**Risk before test:** [low | medium | high]

## Hypothesis

[Testable, directional, falsifiable. "If we [stimulus], then [specific measurable behavior]" — phrased so the result can disconfirm, not just confirm.]

## Method

**[fake door | smoke test | landing page | concierge / Wizard of Oz | interactive prototype | expert review | data mining / cohort backcast | pricing probe | technical spike | analog teardown]**

[1–2 sentences on why this method fits this assumption type. Name the specific behavior the method surfaces and why it is a credible proxy for the claim.]

## Setup

[What gets built or prepared before the test starts. Include the stimulus (ad copy, page, script, prototype screens, spike scope). Enough detail that someone else could reproduce it.]

## Participants / Traffic

- **Segment:** [who — mirrors the Who of the source opportunity where possible]
- **Recruitment / traffic source:** [how they reach the test]
- **Target sample size:** [N] — [one-line rationale; see method-specific sizing guidance in `methods-catalog.md`]

## Success Criterion

[A single quantitative bar. "≥ X% click through", "≥ N of M complete the task unaided", "conversion ≥ X% over M sessions". Pre-committed — written before the test runs so the result cannot be reinterpreted after the fact.]

## Kill Criterion

[A single quantitative bar where the test falsifies the assumption. Should be a meaningfully different outcome from the success bar — a "meh" result between the two is an inconclusive zone, which is fine to acknowledge.]

## Timebox

[Target duration and stop date. Tests without a timebox become cancellations of the roadmap rather than learning events.]

## Cost / Effort

[T-shirt size: XS / S / M / L. One line on the largest cost component — engineering, design, ad spend, researcher time.]

## Threats to Validity

- [What confound could produce a false positive? e.g., novelty effect, self-selected traffic, incentive contamination.]
- [What confound could produce a false negative? e.g., unfamiliar stimulus, sample too small, wrong segment reached.]

## Next Steps After Result

- **If success:** [what the next action is — typically: flip source opportunity Status to `validated`, route to `prioritize` or `slice-mvp`.]
- **If kill:** [what the next action is — typically: drop the solution branch, reopen `map-opportunities` for the sub-outcome, or re-frame at a higher level.]
- **If inconclusive:** [what the next action is — typically: redesign with a tighter stimulus or larger sample, not a re-run with the same setup.]
```

## Field Guidance

### Assumption — specificity test

Copy the specific claim, not the category. The type label goes in its own field. If the assumption reads as a category only, rewrite it as the behavioral claim the category is about.

| Weak (category or vague) | Strong (specific claim) |
|--------------------------|--------------------------|
| Desirability | B2B admins will click into a wizard from the settings page even though they normally prefer full manual control |
| Feasibility | We can detect inherited-but-no-longer-applicable settings from our current config schema without a migration |
| Users will love it | Trial users who hit the aha screen in session 1 return within 7 days at ≥ 2x the rate of users who do not |

### Assumption type — lens

Four types. Picking the wrong type leads to picking the wrong method.

| Type | The claim is about | Example |
|------|--------------------|---------|
| desirability | The user wants the outcome badly enough to change behavior | "Admins will accept a wizard-led onboarding over manual setup" |
| viability | The business economics support shipping | "At $20/mo, attach rate on the new tier covers its support cost" |
| feasibility | The team can build it with available tools and time | "We can auto-detect inherited settings without a schema migration" |
| usability | The user can use it successfully once shipped | "A first-time admin completes setup in one session without docs" |

### Hypothesis — falsifiability test

Rewrite the hypothesis until a bystander can name an observation that would disconfirm it. If no observation would change your mind, the hypothesis is a belief, not a hypothesis.

| Weak (not falsifiable) | Strong (falsifiable) |
|------------------------|----------------------|
| Users will like the wizard | ≥ 15% of settings-page visitors click "Try the setup assistant" within 14 days |
| The new tier will sell | ≥ 10 self-serve signups to the new tier in a 2-week window at the posted price |
| We can build it quickly | A 3-day spike produces a working prototype for the inheritance-detection step |

### Success / Kill — pre-committed bars

Both bars are written before the test starts. Writing them after is rationalization, not validation.

- Success bar ≠ "did it work". It is a threshold that, if met, lets the team act. Anchor to a decision: "if ≥ X, we commit; if < X, we do not."
- Kill bar ≠ "did it fail". It is the threshold below which the team commits to dropping or redesigning the solution. Gaps between the two create an honest inconclusive zone.
- Prefer absolute numbers over relative ones when sample sizes are small. "≥ 8 of 20 users complete the task" is auditable; "40% completion" sounds similar but loses the denominator at a glance.

### Risk before test — calibration

Matches the risk field in `tree-template.md` from `map-opportunities`.

| Level | Meaning |
|-------|---------|
| low | Direct evidence already exists (signals, research, prior shipped feature). Usually no separate test needed. |
| medium | Plausible from analogous cases but not directly tested here |
| high | Novel, load-bearing, no direct evidence |

`test-assumption` prioritizes `high` first, then `medium`.

### Timebox — sizing

Default timeboxes per method are in `methods-catalog.md`. Exceed a default only with a named reason (recorded in the plan body).

### Slug naming

Derive the slug from the assumption itself, not the source tree. Kebab-case, 2–5 words. Examples:

- "Admins accept a wizard" → `admins-accept-wizard.md`
- "We can auto-detect inherited settings" → `detect-inherited-settings.md`
- "New tier converts at posted price" → `new-tier-price-conversion.md`

If a test for the same assumption already exists, append the date: `<slug>-YYYY-MM-DD.md` (the old file stays as a historical record).

### Status field lifecycle

Written by this skill as `designed`. Downstream is manual (no skill automates execution yet).

| Status | Set by |
|--------|--------|
| designed | `test-assumption` (this skill) |
| running | manual, when the test starts |
| passed | manual, when result clears the success bar |
| killed | manual, when result falls below the kill bar |
| inconclusive | manual, when result lands between bars |
| abandoned | manual, when the test was never run |

When a test `passes`, the *source opportunity's* Status may flip to `validated` — that update happens in the source opportunity file, not here.

## Quality Check

Run before writing the plan file. Correct any violation in place; if a violation cannot be corrected without input the user has not yet provided, pause and ask before writing.

- Assumption is a specific behavioral claim, not a category label.
- Hypothesis names an observation that would disconfirm it.
- Method's primary use (per `methods-catalog.md`) matches the assumption type.
- Success and kill criteria are separate, quantitative, and pre-committed.
- Timebox is set and not open-ended.
- Next-steps-on-result are named for each of success, kill, and inconclusive.
