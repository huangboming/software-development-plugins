---
name: synthesize-research
description: "Synthesize raw qualitative research notes into structured themes and insights, and write a synthesis document to .product/discover/research/. Input must be qualitative data (transcripts, notes, observations, diary entries) — not quantitative metrics or analytics. Triggers: 'synthesize research', 'analyze interviews', 'analyze survey results', 'analyze usability test data', 'what patterns emerged from the research', 'research synthesis', 'find patterns in research', 'synthesize these notes', 'what are the themes', 'I ran the interviews now what', '/synthesize-research'."
---

# Synthesize Research

Turn raw research notes into structured themes and insights. Input is qualitative data (transcripts, observations, survey responses, diary entries). Output is a synthesis document written to `.product/discover/research/synthesis-<slug>.md`.

## References

- [references/synthesis-template.md](references/synthesis-template.md) — Template for synthesis documents and field guidance (theme strength calibration, evidence quality, slug naming). Read before writing a synthesis document.
- [references/analysis-methods.md](references/analysis-methods.md) — Affinity mapping and thematic analysis procedures, method selection guide, cross-method triangulation, and common failure modes. Read when choosing or executing an analysis method.

## Process

Four steps: gather inputs, analyze, structure themes, write and confirm.

### 1. Gather Inputs

Identify the raw research data. Three input shapes:

- **User provides notes directly** (pasted text, attached files) → use as-is.
- **User points to files** (paths to transcripts, survey exports) → read them.
- **User says "synthesize research" without specifying** → scan `.product/discover/research/` for unsynthesized prep documents and raw notes. If none found, ask what to synthesize. If the user cannot identify a source, explain that this skill requires raw qualitative data (transcripts, notes, survey responses) and suggest they paste data directly into the conversation.

**Single-source check:** If fewer than two sources are present, warn the user that synthesis from a single source produces anecdotes, not patterns. If the user agrees to proceed, add a note to the synthesis Summary stating evidence is insufficient to establish patterns. If the user declines, stop and ask them to provide additional sources before retrying.

### 2. Analyze

Read [analysis-methods.md](references/analysis-methods.md). Select a method using the Method Selection table, then follow the selected method's procedure. Extract atomic observations first, then group into themes. Target 3-8 themes. Watch for the failure modes described at the end of the reference.

### 3. Structure Themes

Read [synthesis-template.md](references/synthesis-template.md). Follow the template structure for each theme, including Contradictions and Tensions, Gaps, and Grounding Signals sections. Check `.product/discover/signals/` for related signals to link in Grounding Signals.

### 4. Write and Confirm

1. Create `.product/discover/research/` if it does not exist.
2. Write the synthesis at `.product/discover/research/synthesis-<slug>.md`.
3. Present a summary: theme count, strongest themes, key contradictions, and gaps. Ask the user to review.

**Summary example:**

```
Synthesized: **Onboarding friction** (5 interviews, 1 survey)
- 6 themes identified (3 strong, 2 moderate, 1 emerging)
- Strongest: "New users don't understand the value prop before being asked to configure"
- Key contradiction: Power users want more setup options; new users want less
- Gap: No data from mobile-only users
```

## Edge Cases

If the user provides **data that is already synthesized** (a report with themes, a summary doc):
  → This skill adds value only on raw data. Ask whether they want to re-synthesize from original sources, or whether `frame-problem` is the right next step.

If the input contains **a mix of research data and feature requests**:
  → Separate them. Synthesize the research data. Route feature requests to `capture-signal` with a note.

If themes are **too similar to the interview guide structure**:
  → The grouping is likely top-down. Re-examine the observations and regroup bottom-up. See the "Critical: bottom-up, not top-down" section in [analysis-methods.md](references/analysis-methods.md).

If the user wants to **synthesize incrementally** (new interviews added to an existing synthesis):
  → Read the existing synthesis. Code new observations against existing themes, but also look for new themes. Re-apply the strength calibration table in `synthesis-template.md` to every theme after coding new observations. Annotate new evidence with `[new — YYYY-MM-DD]` so the user can see what changed.