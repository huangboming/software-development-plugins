---
name: write-prd
description: "Write feature-level PRDs — one per capability, versioned. For alignment first, use grill-me. For product-wide definition, use write-product-md. Triggers: '/write-prd', 'write a PRD', 'write a feature PRD', 'spec out this feature', 'I need a PRD for...', 'document requirements from code'."
---

# PRD Writer

Write feature-level PRDs at `.product/define/specs/<feature-name>/v<N>.md` — one per capability, versioned. For product-wide definition, use `write-product-md`.

If alignment is shaky, run `grill-me` first using the template below as the decision tree.

## Process

1. **Locate the file.** Target is `.product/define/specs/<feature-name>/v<N>.md`. New feature → `v1.md`. Significant revision → next version with a `Supersedes:` link. Otherwise edit in place. Read prior versions and any framed opportunity in `.product/discover/opportunities/`; flag inconsistencies with the inputs you were given.
2. **Draft against the template** using the aligned context (typically from a prior `grill-me` session). If inputs are insufficient, stop and run `grill-me`. Do not invent. Set `Last updated` to today.
3. **Review against the quality bar; revise; present.**

## Template

````markdown
# <Feature Name>

> Last updated: <YYYY-MM-DD>
> Version: v<N> *(Supersedes: [v<N-1>](./<previous-version>.md) — omit for v1)*

## Problem

<1–2 sentences. Name the specific persona and the specific pain, not the solution.>

## Non-goals

- <Capability someone might assume is in scope but isn't, with a one-line reason.>

## User stories

### US-1: <Story Title>

**As a** <specific role>, **I want** <capability — what the user does, not how it's built>, **So that** <benefit — real value to the user>.

- [ ] Given <precondition>, when <action>, then <expected result>
- [ ] Given <precondition>, when <action>, then <expected result>

*Notes (optional): edge cases, dependencies, NFRs, or a mermaid flow if the journey is non-trivial.*

## Success metrics *(omit if no metric is meaningful for this feature)*

| Metric | Definition | Target |
|--------|------------|--------|
| <metric> | <how it's measured> | <target value> |
````

## Quality bar

- Problem statement names a specific persona and a specific pain — not generic "users need X".
- Non-goals would genuinely surprise a first-time reader (e.g., "Real-time collaboration — single-user for v1; revisit Q3"), not throwaways ("not building a mobile app").
- Every success metric has a definition and a target. If a baseline must be measured post-launch, write `TBD — measure baseline before launch` inline (this is deferred data, not an alignment gap).
- Each acceptance criterion is independently testable — passes or fails unambiguously.
- Zero implementation details — no technologies, architecture, or system internals. PRDs capture *what* and *why* from the user's perspective.
- If user stories exceed ~10, the feature is too broad — recommend splitting into sub-features.
- If inputs contradict or are missing, stop and run `grill-me` — do not paper over with placeholders.
