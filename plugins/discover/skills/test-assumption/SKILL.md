---
name: test-assumption
description: "Write a test plan for the riskiest assumption behind a framed opportunity or candidate solution to .product/discover/assumptions/. Operates on an already-identified assumption — run map-opportunities first to surface solution-level assumptions. Selects a method (fake door, smoke test, concierge / Wizard of Oz, prototype experiment, pricing probe, technical spike) that fits the assumption type, and commits pre-written success and kill criteria. Designs the test only — does not run it. Triggers: 'test an assumption', 'test the assumption', 'design a test for', 'design an experiment', 'what is the riskiest assumption', 'de-risk this idea', 'validate before we build', 'validate this assumption', 'should we build this', 'before we commit to building', 'fake door test', 'smoke test', 'concierge test', 'wizard of oz test', 'prototype experiment', 'test card', 'experiment card', 'learning card', 'run a discovery experiment', '/test-assumption'."
---

# Test Assumption

Design a test for the single riskiest assumption behind a framed opportunity or a candidate solution, and write the test plan to `.product/discover/assumptions/<slug>.md`. The plan commits a method, a hypothesis, and pre-written success and kill criteria *before* the test runs — so the result cannot be reinterpreted after the fact.

This skill designs the test. It does not run it. The output is a plan.

## References

- [references/test-plan-template.md](references/test-plan-template.md) — Template for the test plan and field guidance (assumption specificity, type lens, hypothesis falsifiability, success/kill calibration, timebox defaults, slug naming, status lifecycle). Read before writing a plan.
- [references/methods-catalog.md](references/methods-catalog.md) — Catalog of test methods with what-it-tests, what-to-measure, sample sizing, default timebox, and gotchas. Read when selecting a method or when a chosen method feels like a poor fit for the assumption.

## Process

Four steps: gather input, select the assumption, design the test, write and confirm.

### 1. Gather Input

Identify which assumption to test. Four input shapes:

- **User points to a tree** (`tree-<slug>.md` or slug) → read it, list every solution with its key assumption and risk, then proceed to step 2.
- **User points to a framed opportunity with no tree** → the assumption under test is usually on the framing itself (Confidence `speculative` or `emerging`, or a shaky Why Now). Offer to test the framing, or route to `map-opportunities` first to surface solution-level assumptions. If the user prefers framing-level, treat the opportunity's load-bearing claim as the assumption and continue.
- **User names an assumption inline** → use it. Skip the ranking step in step 2; go directly to classifying type.
- **User says "test an assumption" without specifying** → list candidates from `.product/discover/opportunities/`: solutions marked `high` risk in any `tree-*.md`, then `medium` risk. If zero candidates exist, offer to run `map-opportunities` first.

### 2. Select the Riskiest Assumption

Skip this step if the user named an assumption inline.

Rank candidates by risk-to-decision, not by interest:

- Eliminate `low`-risk assumptions — they do not need a separate test. If a user insists on testing one, proceed but flag in the plan body that this is likely duplicate validation.
- Among `high` and `medium`, prefer the one whose failure would most change the decision: "if this assumption is wrong, do we stop building?" An assumption whose result would not change the plan is not worth testing.
- Prefer assumptions whose method is feasible now (method needs a surface that exists, a segment reachable today, or data already captured). When a high-risk assumption has no feasible live method, first check `methods-catalog.md` for an access-free substitute — analog teardown or data mining require no surface, no participants, no build. If one applies, pivot to it. If none applies, surface the binding constraint by name ("this fake door needs a settings page that does not yet exist") and recommend building the minimum stimulus first before designing the test.

When more than one assumption is a strong candidate, surface the top two or three and ask the user to pick one. One test plan per invocation — bundling tests across assumptions dilutes each.

If the selected assumption is **category-shaped** (just "desirability" or "feasibility"), rewrite it as the specific behavioral claim before continuing. See `test-plan-template.md` for the specificity test.

### 3. Design the Test

Four fields carry the design. Fill them in this order so each constrains the next.

**Type.** Classify the assumption as desirability, viability, feasibility, or usability. The type narrows method selection — see the selection table in `methods-catalog.md`. If the assumption spans two types (e.g., desirability *and* usability), split it into two assumptions. Sequence the desirability or viability sub-claim first — those are decision-gates for whether to build; usability and feasibility are only worth testing once the decision to build is live. Record the deferred sub-claim in the plan's Next Steps section as "deferred pending result". If the user pushes to combine both into one test, decline once and explain that a combined result cannot clearly falsify either sub-claim; then offer the sequenced design above.

**Hypothesis.** Rewrite the assumption as a falsifiable, directional statement: "If we [stimulus], then [specific measurable behavior] in [segment] within [timebox]." A bystander should be able to name an observation that would disconfirm it. If no observation would change your mind, the hypothesis is a belief — see the falsifiability examples in `test-plan-template.md`.

**Method.** Pick from `methods-catalog.md`. Let the assumption type drive primary selection, then check the method's preconditions (sample access, build cost, surface availability). If the primary method is infeasible, use the secondary list — do not force-fit the method to the tool on hand.

**Success and kill criteria.** Write both as single quantitative bars *before* the test runs. The success bar is the threshold that, if met, lets the team act. The kill bar is the threshold below which the team commits to dropping or redesigning the solution. Leave an honest inconclusive zone between them rather than using a single decision line that rationalizes the middle.

Then fill the remaining fields — setup, sample, timebox, cost, threats to validity, next steps — following `test-plan-template.md`. Timebox defaults by method are in `methods-catalog.md`; deviate only with a named reason.

### 4. Write and Confirm

Before writing, run the quality check in `test-plan-template.md` against the plan and correct any violation in place. If a violation cannot be corrected without input the user has not yet provided — e.g., the hypothesis cannot be made falsifiable without naming the segment, or no quantitative success bar can be set without a baseline — pause. State which field is blocked and what information is needed, and ask before writing the file.

Then:

1. Create `.product/discover/assumptions/` if it does not exist.
2. Write the plan at `.product/discover/assumptions/<slug>.md` with Status `designed`. Slug naming is in `test-plan-template.md`.
3. Present a summary and ask the user to confirm or correct. If the user requests corrections, apply them in place, re-run the quality check on the changed fields, and re-present only what changed.

**Summary example:**

```
Test designed: **admins-accept-wizard**
- Source: .product/discover/opportunities/tree-new-admin-config-inheritance.md → Sub-Outcome 1 → Solution: "Guided wizard with per-setting recommendation"
- Assumption (desirability, high risk): B2B admins will click into a wizard from the settings page even though they normally prefer full manual control
- Method: fake door on the settings page
- Success: ≥ 15% of settings-page visitors click "Try the setup assistant" in 14 days (N ≥ 600 visitors)
- Kill: < 5% click-through at the same N
- Timebox: 14 days active
- File: .product/discover/assumptions/admins-accept-wizard.md

Next: run the test (this skill designs only). When the result lands, update Status in the plan file and in the source opportunity, then route to prioritize (in define) or slice-mvp.
```

## Edge Cases

If the **source tree has no `high`-risk assumption** (only `medium` and `low`):
  → Offer to test the highest `medium`-risk assumption, or route to `prioritize` (in `define`) if confidence is already strong enough. Do not synthesize a high-risk assumption to justify a test — a test without a risk is theatre.

If the **source opportunity is marked `speculative`** and the user wants to test a solution-level assumption:
  → Pause. A `speculative` opportunity has a load-bearing assumption upstream of any solution (often "this pain exists at meaningful frequency"). Offer to test the framing-level assumption first — a passing solution test on a wrong opportunity is wasted effort.

If **no method in the catalog fits** (the user's constraint set rules every method out — no traffic, no surface, no participants, no build capacity):
  → Do not write a plan. Reply with (1) one sentence naming the binding constraint, (2) two options as bullets — "Option A: build the minimum stimulus — [what that would be for this assumption]; Option B: switch to analog teardown or data mining — [what that would look like for this assumption]" — and (3) a direct question: "Which would you like to pursue, or should we hold this test until the constraint is lifted?"

If the user **wants the test plan to confirm a decision already made** ("we're building the wizard, write the test"):
  → The plan still gets written, but reframe the test so a kill bar would change the decision. If the user refuses to accept any kill bar ("we're building it either way"), write the plan with a body note ("Test is confirmatory; result will not change build decision") and flag that the test is running for learning, not gating — so downstream readers do not misread it as de-risking.

If an **existing test plan exists** for the same assumption:
  → Read it first. Ask whether to:
  - **Supersede** — rename the old to `<slug>-YYYY-MM-DD.md` and write a new plan at `<slug>.md`. Use when the prior test was abandoned or superseded by a stronger method.
  - **Record result and close** — if the prior test finished, ask for the result (pass / kill / inconclusive) and update the file's Status rather than designing a new test.
  - **Design a variant** — use a new slug (e.g., add a method or segment qualifier) and link to the prior plan in the body.

## Gotchas

- **Confirm the test is decision-gating before selecting a method.** Ask: "if this result lands below the kill bar, does the team stop?" If the answer is no, flag in the plan body that the test is observational, not gating, and shrink scope to match. A full fake door for a non-gating assumption wastes engineering time.
- **Passing a desirability test does not validate usability, and vice versa.** Users who click a fake door have not completed a task; users who complete a prototype task have not sought it out. Pair methods when both claims are load-bearing — do not let a pass on one infer the other.
