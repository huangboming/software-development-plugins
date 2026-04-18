---
name: capture-signal
description: "Capture a raw product signal — an observation from users, data, competitors, or development — and write it to .product/discover/signals/. Forces idea-shaped inputs to reframe as the underlying observation before recording. Triggers: 'capture signal', 'new signal', 'I noticed that', 'I heard from a user', 'competitor just', 'the data shows', 'capture this observation', '/capture-signal'."
---

# Capture Signal

Capture a product-relevant observation and write it to `.product/discover/signals/<slug>.md`. Separate what was **observed** from what should be **built** — reframe idea-shaped inputs into the underlying observation before recording.

## References

- [references/signal-template.md](references/signal-template.md) — Template for signal records and field guidance (source types, confidence calibration, slug naming). Read before writing a signal record.

## Process

Four steps: classify the input, reframe if idea-shaped, structure the signal, write and confirm.

### 1. Classify Input

Read the user's input. Route by shape:

- **Observation-shaped** ("users are dropping off at step 3", "competitor X launched Y") → skip to step 3.
- **Idea-shaped** ("we should add dark mode", "let's build an API for X") → proceed to step 2.
- **Batch** (multiple signals) → process each individually through steps 1–4, present a summary table at the end.

### 2. Reframe Ideas into Observations

1. Acknowledge the idea.
2. Ask one reframing question: "What prompted this? Did you observe something — user feedback, a data point, a competitor move, something during development?"
3. If the user provides an observation → use that as the signal, note the proposed solution in the Hypothesis field.
4. If no backing observation exists → capture with confidence `speculative` and Hypothesis filled in.

Limit reframing to **one round**. If the user says "just capture it," respect that and proceed with what exists.

**Reframing example:**

```
User: "We should add dark mode."

Agent: "Got it — dark mode. What prompted this? Did you hear from users,
       see data, or notice something during development?"

User: "Three users mentioned eye strain in our last feedback survey."

→ Observation: "Three users reported eye strain in Q1 feedback survey."
  Hypothesis: "Dark mode to reduce eye strain."
  Confidence: reported
```

### 3. Structure the Signal

Read [signal-template.md](references/signal-template.md) for the template and field guidance. Fill the template fields:

- **Observation** — facts only, no interpretation or solutions.
- **Interpretation** — clearly separated, optional.
- **Confidence** — calibrated per the guide; default to `reported` or `inferred` for secondhand input, `speculative` for ideas without evidence.
- **Tags** — 2–4 terms for later synthesis grouping.

### 4. Write and Confirm

1. Create `.product/discover/signals/` if it does not exist.
2. Write the signal at `.product/discover/signals/<slug>.md`.
3. Present a summary and ask the user to confirm or correct.

**Examples by signal type:**

Data anomaly:
```
Captured: **Onboarding drop-off at step 3**
- Observation: Mixpanel funnel shows 34% of new users abandon at email
  verification — up from 22% last quarter.
- Source: data-anomaly, observed
- Tags: onboarding, activation, new-user
```

Competitor move:
```
Captured: **Competitor X launches collaborative editing**
- Observation: Competitor X announced real-time collaborative editing
  in their Apr 2026 release. Two prospects mentioned it in sales calls.
- Source: competitor-move, reported
- Tags: collaboration, competitive-pressure, editor
```

Reframed idea (speculative):
```
Captured: **API for third-party integrations**
- Observation: (none — untested hypothesis)
- Hypothesis: "Build a public API so partners can integrate."
- Source: dev-observation, speculative
- Tags: api, integrations, platform
```

For batch captures, present a summary table:

```
| # | Signal | Source Type | Confidence | Tags |
|---|--------|-------------|------------|------|
```

## Edge Cases

If the user provides a **mix of signals and issues** (bugs, refactors, perf):
  → Capture product signals here. Route engineering issues to `capture-issue` in the `build` plugin. Surface the routing decision explicitly.

If a signal **overlaps with an existing signal** in `.product/discover/signals/`:
  → Surface the existing signal. Ask whether to merge or keep separate. Separate signals on the same theme are valid — synthesis groups them later.

If the observation is **too vague** ("users seem unhappy"):
  → Ask one grounding question: "What specifically did you see or hear?" If still vague, capture with confidence `inferred` and note the gap in Interpretation.

If the user says **"just capture it, don't ask questions"**:
  → Write the signal with what is available. Set confidence based on evidence strength. Skip reframing.

## Gotchas

- **Keep Observation and Hypothesis separate** — if Observation contains a proposed feature, downstream synthesis treats it as evidence when it is not. Observation holds facts; Hypothesis holds the idea.
- **Default confidence to `reported` or lower** — most secondhand input is `reported` or `inferred`. Reserve `observed` for firsthand data. Underrating confidence triggers healthy validation; overrating skips it.
- **Watch for orphaned signals** — signals create value only when they feed into synthesis. If `.product/discover/signals/` grows while `opportunities/` stays empty, flag the imbalance.
