# Synthesis Document Template

```markdown
# Synthesis: [Topic]

**Date:** [today's date]
**Method:** [affinity-mapping | thematic-analysis]
**Sources:** [list each input — interview transcripts, survey results, usability observations, diary entries, etc., with participant count or sample size]

## Summary

[2-3 sentence overview: what the research covered, what the strongest patterns were, and what surprised you.]

## Themes

### Theme 1: [Theme Name]

**Strength:** [strong — multiple independent sources converge | moderate — clear pattern but limited sources | emerging — early signal, needs more evidence]

**Insight:** [One sentence: what this theme means for the product or user. Not a solution — a distilled understanding.]

**Evidence:**
- [Verbatim quote or specific observation] — *Source: [participant/data source]*
- [Verbatim quote or specific observation] — *Source: [participant/data source]*
- [Verbatim quote or specific observation] — *Source: [participant/data source]*

### Theme 2: [Theme Name]

...

## Contradictions and Tensions

[Observations that don't fit neatly into themes, or themes that contradict each other. These are often the most valuable findings — they reveal nuance and prevent premature convergence.]

## Gaps

[What the research did NOT cover. Questions that remain unanswered. Areas where evidence is thin. Flags for future research.]

## Grounding Signals

[Links to related signals in `.product/discover/signals/` that this research validates, refutes, or extends. If no related signals exist, note "None linked."]
```

## Field Guidance

### Theme strength calibration

| Strength | Criteria | Implication |
|----------|----------|-------------|
| strong | 3+ independent sources converge on the same pattern; consistent across segments | High confidence — ready to feed into `frame-problem` |
| moderate | Clear pattern from 2+ sources, but limited diversity (e.g., all from same user segment) | Worth acting on, but note the scope limitation |
| emerging | 1-2 mentions, or a pattern the synthesizer inferred across weak signals | Capture it, but flag for validation before building on it |

### Slug naming

Derive `<slug>` from the topic: lowercase, kebab-case, 2-5 words. Prefix with `synthesis-`. Example: "Onboarding friction points" → `synthesis-onboarding-friction`.

### Evidence quality

Prefer verbatim quotes over paraphrases — they carry more signal and are harder to unconsciously reinterpret. When paraphrasing is necessary (e.g., quantitative survey data), note that it is a paraphrase.

Minimum evidence per theme: 2 observations from independent sources. A theme supported by a single observation is an anecdote, not a pattern — capture it under Contradictions and Tensions or downgrade to `emerging`.
