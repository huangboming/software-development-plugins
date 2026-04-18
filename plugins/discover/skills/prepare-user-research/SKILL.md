---
name: prepare-user-research
description: "Produce prep artifacts for user research the PM will conduct: discussion guides, screeners, survey instruments, test plans, and debrief templates. Covers interviews, surveys, usability tests, concept tests, diary studies, and card sorts. Triggers: 'prepare research', 'research plan', 'discussion guide', 'interview guide', 'survey design', 'usability test plan', 'concept test', 'diary study', 'card sort', 'screener', 'I need to talk to users', 'prepare for user interviews', '/prepare-user-research'."
---

# Prepare User Research

Produce prep artifacts for research the PM will conduct themselves. Output is a single prep document written to `.product/discover/research/<slug>.md`. The agent produces plans, guides, and templates — it does not conduct research or synthesize findings.

## References

- [references/method-selection-guide.md](references/method-selection-guide.md) — Decision matrix for choosing a research method based on research questions. Read when the user hasn't specified a method or needs help choosing.
- [references/interview-prep.md](references/interview-prep.md) — Interview prep template, discussion guide structure, and question-writing gotchas. Read when preparing a discovery or evaluative interview.
- [references/survey-prep.md](references/survey-prep.md) — Survey instrument template, question design rules, and analysis plan structure. Read when preparing a survey or questionnaire.
- [references/usability-test-prep.md](references/usability-test-prep.md) — Usability test template, task scenario writing, and observation guide. Read when preparing a moderated or unmoderated usability test.
- [references/concept-test-prep.md](references/concept-test-prep.md) — Concept test template, stimulus design, and reaction interview guide. Read when testing a product concept before building.
- [references/diary-study-prep.md](references/diary-study-prep.md) — Diary study template, entry prompt design, and check-in schedule. Read when studying behavior over time.
- [references/card-sort-prep.md](references/card-sort-prep.md) — Card sort template, card list design, and analysis plan. Read when exploring information architecture or categorization.

## Arguments

Parse from the user's request:

| Argument | Required | Default | Description |
|---|---|---|---|
| topic | yes | — | The research subject: a problem space, feature, or user behavior |
| method | no | inferred from topic | One of: interview, survey, usability-test, concept-test, diary-study, card-sort |
| audience | no | inferred from topic | Who the research targets — a user segment or persona |

**Parsing examples:**

- "I need to interview users about onboarding" → topic: onboarding, method: interview
- "Prepare a survey about feature satisfaction for power users" → topic: feature satisfaction, method: survey, audience: power users
- "We want to understand how new users navigate the dashboard" → topic: dashboard navigation, method: inferred (usability-test or interview — ask)
- "Prepare research on why users churn" → topic: user churn, method: inferred — read [method-selection-guide.md](references/method-selection-guide.md)

## Process

Four steps: understand goals, select method, generate prep document, write and confirm.

### 1. Understand Research Goals

Identify the research questions, target participants, and method (if specified) from the user's input.

Check `.product/discover/signals/` for signals related to the topic. If relevant signals exist, reference them in the prep document's "Grounding signals" field to connect research back to observed evidence.

If the topic is too vague to select a method, ask one clarifying question: "What decision will this research inform?"

### 2. Select Method

If the user specified a method, use it. Otherwise, read [method-selection-guide.md](references/method-selection-guide.md) and recommend a method based on their research questions. Present the recommendation with a one-sentence rationale and confirm before proceeding.

If the user wants to combine methods (e.g., interviews followed by a survey), produce a separate prep document for each. Process each method through steps 2–4 independently.

### 3. Generate Prep Document

Read the method-specific reference for the selected method. Follow its template, adapting to the user's research goals, participants, and context. Pay close attention to the gotchas section in each reference — those capture the most common quality failures.

### 4. Write and Confirm

1. Create `.product/discover/research/` if it does not exist.
2. Write the prep document at `.product/discover/research/<method>-<topic>.md` (e.g., `interview-onboarding`, `survey-feature-satisfaction`, `usability-test-checkout`).
3. Present a summary and ask the user to review. Highlight any assumptions made about recruitment criteria, scope, or method choice.

## Examples

**User says:** "I want to understand why users drop off during onboarding."
→ Check `.product/discover/signals/` for onboarding-related signals. No method specified — read method-selection-guide. Research question is "why" (exploratory) → recommend **interview**. Read interview-prep.md. Write to `.product/discover/research/interview-onboarding-drop-off.md`.

**User says:** "Prepare a usability test for the new checkout flow."
→ Method specified: usability test. Read usability-test-prep.md. Write to `.product/discover/research/usability-test-checkout.md`.

**User says:** "I need to talk to users about our pricing — also want to survey a bigger sample."
→ Two methods requested. Produce two prep documents: `interview-pricing.md` (read interview-prep.md) and `survey-pricing.md` (read survey-prep.md). Process each independently.

## Edge Cases

If the user asks to **conduct the research** (run interviews, send surveys):
  → Clarify the boundary: this skill produces prep artifacts. Execution is the PM's job. Offer to help with synthesis afterward via `synthesize-research`.

If the user wants research on a topic with **no signals captured yet**:
  → Proceed without grounding signals. Note in the prep document that the research goals are not yet grounded in observed evidence, and suggest capturing signals first if appropriate.

If the user provides **existing research data** (interview transcripts, survey results):
  → Route to `synthesize-research` instead. This skill produces prep, not analysis.

If the user asks for a method **not covered** by the references (A/B test, focus group, contextual inquiry):
  → Use general knowledge to produce a prep document in a similar structure. Note that no method-specific reference was used.

## Gotchas

- **This skill produces prep, not findings.** If the output starts looking like a discovery document with personas and JTBD, stop — that's `synthesize-research` territory. Output is plans, guides, instruments, and templates.
- **One prep document per method.** If the user wants interviews + a survey, write two documents. Combining methods in one document makes each harder to use during execution.
- **Screeners and recruitment criteria are as important as the guide.** Talking to the wrong people with the right questions wastes more time than the reverse. Always include recruitment criteria and, for interviews/usability/concept tests, a screener.
