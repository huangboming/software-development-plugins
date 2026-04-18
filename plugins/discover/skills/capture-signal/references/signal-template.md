# Signal Record Template

```markdown
# Signal: [Short Name]

**Date observed:** [when the observation occurred — not when it was captured]
**Date captured:** [today's date]
**Source:** [who or what — specific enough to trace back: "user interview with <persona>", "support ticket #1234", "Mixpanel funnel report Q1", "competitor X blog post"]
**Source type:** [user-feedback | data-anomaly | competitor-move | support-pattern | market-signal | dev-observation | user-research]
**Confidence:** [observed — firsthand or primary data | reported — secondhand, credible source | inferred — pattern across weak signals | speculative — untested hypothesis]

## Observation

[What was actually observed. Facts only — no interpretation, no proposed solutions. One to three sentences. If the user provided a verbatim quote, include it in quotation marks.]

## Interpretation

[What this might mean for the product. Clearly separated from the observation. Why does it matter? Who is affected? What is the cost of inaction? Optional — leave blank if the signal speaks for itself.]

## Hypothesis

[If this signal originated as an idea ("we should build X"), capture the proposed solution here and reframe above as the observation that prompted it. Otherwise leave blank.]

## Related Signals

[Links to other signal files on the same theme, if any. Otherwise "None yet."]

## Tags

[Comma-separated tags for later synthesis grouping. Example: onboarding, activation, new-user]
```

## Field Guidance

### Source type definitions

| Source type | When to use |
|-------------|-------------|
| user-feedback | Direct input from users or customers — interviews, surveys, reviews, in-app feedback |
| data-anomaly | Unexpected pattern in analytics, metrics, or monitoring — drop-offs, spikes, trend breaks |
| competitor-move | Competitor launched a feature, changed pricing, entered a segment, or shifted messaging |
| support-pattern | Recurring theme in support tickets, bug reports, or escalations |
| market-signal | Industry trend, analyst report, regulatory shift, or technology change |
| dev-observation | Something a developer noticed during build — edge case users hit, architectural constraint surfacing as UX friction |
| user-research | Finding from a formal research activity — usability test, diary study, concept test |

### Confidence calibration

| Level | What it means | Example |
|-------|---------------|---------|
| observed | You or your team directly witnessed it, or it comes from primary data | Watched a user fail the onboarding flow in a usability test |
| reported | Credible secondhand source — you trust the reporter but didn't witness it | Sales rep relays that 3 prospects asked for SSO in demos this month |
| inferred | Pattern you assembled from multiple weak signals — plausible but not directly evidenced | Support tickets about "confusing settings" + low settings-page engagement + 2 churn interviews mentioning configuration → inference that settings UX is a retention risk |
| speculative | An idea or hunch with no backing evidence yet — captured to avoid losing it, but needs validation | "I think we should add dark mode" with no user data behind it |

### Slug naming

Derive `<slug>` from the short name: lowercase, kebab-case, 2-5 words. Example: "Onboarding drop-off at step 3" → `onboarding-drop-off-step-3`.

If a file with the same slug already exists, append the capture date: `<slug>-YYYY-MM-DD`. If still taken, add a numeric tiebreak: `<slug>-YYYY-MM-DD-2`.
