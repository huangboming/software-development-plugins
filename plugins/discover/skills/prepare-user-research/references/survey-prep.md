# Survey Prep

Produces a prep document for a quantitative or mixed-methods survey instrument.

## Prep Document Template

```markdown
# Survey Prep: [Topic]

**Date:** [today]
**Method:** Survey ([exploratory | validation | satisfaction])
**Target responses:** [30 minimum for quantitative signal; 100+ for segmentation]
**Estimated completion time:** [target under 8 minutes]

## Research Goals

1. [What we want to quantify or validate]
2. [...]

**Grounding signals:** [List any signals from .product/discover/signals/ that motivated this research]

## Target Population

**Who should receive this survey:**
- [Behavioral definition of the audience]

**Segmentation variables:** [If comparing groups, list the segments]

## Distribution Plan

**Channel(s):** [in-app, email, social, panel, etc.]
**Incentive:** [if any]
**Timeline:** [open date → close date]
**Reminder cadence:** [if applicable]

## Survey Instrument

### Screener / Eligibility (if needed)

Q1. [Closed question to verify eligibility]
- [Option A]
- [Option B] → End survey

### Section 1: [Topic Name]

Q2. [Question text]
- Type: [single-select | multi-select | Likert 5-point | open-text | NPS | ranking]
- Options: [list if applicable]
- Required: [yes | no]
- Skip logic: [if any — e.g., "If Q2 = B, skip to Q5"]

Q3. [...]

### Section 2: [Topic Name]

Q4. [...]

### Closing

Q[N]. [Open-ended catch-all, optional] "Is there anything else you'd like to share about [topic]?"

## Analysis Plan

| Research goal | Key question(s) | Analysis approach |
|---|---|---|
| [Goal 1] | Q2, Q3 | [Frequency distribution / cross-tab by segment / ...] |
| [Goal 2] | Q5, Q6 | [...] |
```

## Gotchas

- **One concept per question.** "How satisfied are you with our pricing and billing?" is two questions fused. The respondent who loves pricing but hates billing can't answer accurately. Split them.
- **Anchor Likert scales with behavioral descriptions, not intensity words.** "Strongly agree / Agree / Neutral / Disagree / Strongly disagree" is ambiguous. "Every day / A few times a week / Once a week / Less than once a week / Never" is precise.
- **Front-load closed questions, end with open-text.** Open-text questions early cause drop-off. Place them at the end when the respondent is already committed.
- **Randomize option order for opinion questions.** Primacy bias means the first option gets selected more often. Randomize when options are not inherently ordered (not for Likert scales or numeric ranges).
- **Cap at 15–20 questions.** Every question past ~15 degrades response quality. Cut any question that doesn't map to a research goal in the analysis plan.
- **Write an analysis plan before the questions.** If you can't describe how a question's answers will be analyzed, the question shouldn't be there. The analysis plan prevents "nice to know" questions from inflating the instrument.
- **Avoid "how often do you..." without a time anchor.** "How often do you use feature X?" is ambiguous. "In the past 7 days, how many times did you use feature X?" is answerable.
