# Framed Opportunity Template

```markdown
# Opportunity: [Short Name]

**Date framed:** [today's date]
**Status:** framed
**Confidence:** [strong | moderate | emerging | speculative]

## Who

[The specific user, role, or behavioral segment affected. Not "users" — a segment narrow enough that a reader can picture one.]

## Pain

[What they experience — observable behavior, measurable cost, or reported friction. The symptom, not the hypothesized cause.]

## Why Now

[What changed that makes this surface now: market shift, growth stage, competitor move, internal data trend, regulatory change. Distinguishes a live opportunity from a "someday" problem.]

## Cost of Inaction

[What breaks, stays broken, or compounds if we do nothing. Churn, lost deals, support load, opportunity cost, risk exposure.]

## What Good Looks Like

[The outcome — how the affected user's situation changes. An end state, not a feature. Keeps the opportunity open for multiple solution shapes.]

## Hypothesis

[Only present when this opportunity was framed from a stated solution. Record the user's original framing verbatim so downstream reviewers can trace the inversion. Omit this section entirely when the framing started from a problem.]

## Non-Goals

[What this opportunity explicitly is NOT: adjacent problems, edge cases, deferred segments. Optional but valuable for scope discipline downstream.]

## Evidence

- `.product/discover/signals/<slug>.md` — one line on what this signal contributes
- `.product/discover/research/synthesis-<slug>.md` — theme name this draws on

## Related Opportunities

[Links to other opportunity files on adjacent or overlapping problems. Otherwise "None yet."]
```

## Field Guidance

### Who — specificity test

Substitute "everyone" for the Who. If the sentence still reads as sensible, narrow further. A good Who lets a reader picture a specific person.

| Weak | Strong |
|------|--------|
| Users who struggle with settings | B2B admins inheriting a configuration from a predecessor |
| New customers | Trial users in their first session who haven't connected a data source |
| Power users | Analysts running the same report weekly against rotating date ranges |

### Pain — observability test

Describe what a bystander would see or measure. If the pain can only be inferred from an imagined internal state, you are describing a hypothesis, not a pain — strengthen it with an observable anchor or lower confidence.

| Weak (hypothesis) | Strong (observable) |
|-------------------|---------------------|
| Users feel overwhelmed | 68% of trial users abandon during onboarding step 4; session recordings show repeated scrolling between docs and the product |
| Settings are confusing | Support receives 12 tickets/week about the same three settings fields; Mixpanel shows avg 4:30 on the settings page before save |

### What Good Looks Like — outcome, not solution

Describe the change in the user's situation. If the sentence names a feature, uses "we build/add/ship", or describes a UI, it is solution-shaped — rewrite to the end state.

| Weak (solution) | Strong (outcome) |
|-----------------|------------------|
| We add a config wizard | A new admin reaches a working configuration in under 10 minutes, without needing support |
| Build a dashboard for X | Analysts see their weekly metrics without constructing the query |
| Users can access the new API | Partners integrate in under a day instead of the current two-week average |

Keeping the outcome solution-agnostic is what lets `map-opportunities` generate multiple competing solution shapes downstream.

### Confidence calibration

| Level | Criteria |
|-------|----------|
| strong | Multiple independent sources converge: a synthesis theme marked `strong`, plus 2+ grounding signals, or primary research with diverse sources |
| moderate | One synthesis theme of `moderate` strength, or 2+ signals from similar contexts (same channel, same segment) |
| emerging | One strong signal, or an `emerging` theme — pattern plausible but thinly evidenced |
| speculative | Framed from hypothesis or intuition — no direct observation yet; captured to reserve the problem space but flagged for validation |

Default to the lower of two adjacent levels when in doubt. Underrating confidence triggers healthy validation downstream; overrating skips it.

### Why Now — valid triggers

Accept any of: a data trend that changed in the last 1–2 quarters, a competitor move, a market or regulatory shift, an internal strategy change, a threshold crossed (user count, deal size, error rate), a dependency becoming available or removed.

Reject "we keep hearing about it" without a timing anchor — that is why *at all*, not why *now*. If nothing has changed, say so in the field and mark confidence one level lower.

### Non-Goals — when to fill

Fill Non-Goals when the problem sits near an adjacent problem that readers will conflate. Leave blank when the scope is already tight. Examples of useful non-goals:

- "Enterprise SSO configuration — same surface, different user, tracked separately"
- "Mobile onboarding — same problem class, excluded until web is stable"

### Slug naming

Derive `<slug>` from the pain or Who, not the solution: lowercase, kebab-case, 2–5 words. Examples:

- "New admins inherit a broken configuration" → `new-admin-config-inheritance`
- "Analysts re-author the same weekly report" → `weekly-report-reauthoring`

If a file with the same slug exists, append the framing date: `<slug>-YYYY-MM-DD`. If still taken, add a numeric tiebreak.

### Status field lifecycle

Written by this skill as `framed`. Downstream skills update it:

| Status | Set by |
|--------|--------|
| framed | `frame-problem` (this skill) |
| validated | `test-assumption` after a successful assumption test |
| prioritized | `prioritize` (in `define`) |
| scoped | `slice-mvp` or `write-prd` (in `define`) |
| shipped | manual, after launch |
| archived | manual, when abandoned — record reason in the file |

Do not invent new statuses — downstream skills filter on these values.

## Classification Examples

### Splitting a too-broad theme

```
User: "Frame the 'onboarding friction' theme."

Agent: "That theme covers two distinct problems in the synthesis:
       (1) new trial users abandoning before connecting a data source, and
       (2) invited team members skipping the tour and getting stuck later.
       Different Whos, different pains. Frame them separately?"
```

The test for "too broad" is a failed specificity test on Who, Pain, or both: if two different Whos (or two different pains for the same Who) are plausible readings of the same theme, split it before framing.

### Reframing user-directed solution framing

When a user insists on framing from a solution after reframing was offered, the file still gets written, but the shape changes:

```
User: "Just frame the wizard opportunity, I know what I want."

→ Hypothesis: "Build a configuration wizard for new admins."
  Who: (best inference from context) B2B admins inheriting a configuration
  Pain: (best inference, or "Not determined" if no signal available)
  Confidence: speculative
  Body note: "Framing is user-directed from a stated solution;
              underlying problem is inferred."
```

The Hypothesis field preserves the user's original framing verbatim, so a downstream reviewer can see how the opportunity was derived and decide whether the inferred problem is load-bearing.

