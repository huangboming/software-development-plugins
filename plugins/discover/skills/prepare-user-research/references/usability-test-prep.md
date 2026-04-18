# Usability Test Prep

Produces a prep document for a moderated or unmoderated usability test. Requires an interactive prototype or live product.

## Contents

1. [Prep Document Template](#prep-document-template) — Full template with task scenarios, observation guide, and debrief structure
2. [Gotchas](#gotchas) — Scenario leakage, task count limits, success criteria discipline

## Prep Document Template

```markdown
# Usability Test Prep: [Feature / Flow]

**Date:** [today]
**Method:** Usability test ([moderated | unmoderated])
**Estimated sessions:** [5–8 for moderated; 10–15 for unmoderated]
**Session length:** [30–45 min moderated; 15–20 min unmoderated]
**Prototype/product:** [link or description of what participants will interact with]

## Research Goals

1. [What usability questions we need to answer]
2. [...]

**Grounding signals:** [List any signals from .product/discover/signals/ that motivated this test]

## Recruitment Criteria

**Include:**
- [Behavioral criteria relevant to the feature being tested]
- [Experience level with the product or domain]

**Exclude:**
- [Who to screen out — e.g., internal employees, UX professionals]

## Task Scenarios

### Task 1: [Task Name]

**Scenario:** [Realistic context that motivates the task — a story, not an instruction. Does NOT name UI elements or reveal the path.]

> "You just received an email saying your subscription is about to renew. You want to change your plan before it renews."

**Success criteria:**
- [ ] Participant reaches [specific end state] without assistance
- [ ] Participant completes within [time limit, if applicable]

**Observation focus:** [What specific behaviors or reactions to watch for]

### Task 2: [Task Name]

**Scenario:** [...]

**Success criteria:**
- [ ] [...]

**Observation focus:** [...]

### Task 3: [Task Name]

[...]

## Pre-Test Questions

[2–3 questions before tasks begin, to understand baseline context]
- "Have you ever [relevant activity]? Tell me about the last time."
- [...]

## Post-Test Questions

[3–5 questions after all tasks, to capture overall impressions]
- "Which task felt most difficult? Why?"
- "Was anything confusing that you didn't mention during the tasks?"
- [...]

## Observation Guide (moderated)

| Task | Watch for | Notes column |
|---|---|---|
| Task 1 | [Specific UI elements, hesitation points, error paths] | |
| Task 2 | [...] | |

## Debrief Template

**Participant:** [ID]
**Date:** [session date]

| Task | Completed? | Time | Errors / Detours | Key Observations |
|---|---|---|---|---|
| Task 1 | [yes/no/partial] | [mm:ss] | [...] | [...] |
| Task 2 | [...] | [...] | [...] | [...] |

**Severity ratings for issues found:**
- Critical: [blocks task completion]
- Major: [causes significant delay or confusion]
- Minor: [noticeable friction but recoverable]

**Top issues:**
1. [...]
2. [...]
3. [...]
```

## Gotchas

- **Scenarios must never name UI elements or reveal the solution path.** "Click Settings, then go to Billing" is a walkthrough, not a test. The scenario provides motivation and context — the participant must figure out the path. Test the scenario by asking: "Could someone who has never seen this product understand what they need to accomplish?"
- **Limit to 4–6 tasks.** Each task takes longer than expected. Participant fatigue after ~30 minutes degrades signal quality. Prioritize the flows with the highest uncertainty.
- **Write success criteria before the test, not after.** Without predefined criteria, there's a temptation to rationalize partial completions as successes. Binary pass/fail per task forces honesty.
- **Include one "known easy" task first.** Starting with the hardest task intimidates participants and distorts think-aloud behavior. An easy win builds confidence for harder tasks.
- **For unmoderated tests, write scenarios that are fully self-contained.** There is no moderator to clarify. If the scenario requires context the participant doesn't have, the task data is unusable.
- **Separate task scenarios from moderator notes.** The participant sees (or hears) the scenario. The moderator sees the observation focus. Mixing them risks leaking hints.
