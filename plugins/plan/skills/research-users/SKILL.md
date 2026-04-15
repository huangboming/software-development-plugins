---
name: research-users
description: "Produce a discovery document with personas, JTBD, journey maps, and competitive analysis. Triggers: 'user research', 'product discovery', 'competitive analysis', 'who are our users', 'research the market', 'prepare for PRD', '/research-users'."
---

# User Research

## References

- [references/discovery-document-guide.md](references/discovery-document-guide.md) — Section-by-section writing guidance with templates, examples, and quality checklist for the discovery document. Read before drafting (Step 4).

## Process

Discovery research involves these steps:

1. Determine entry point
2. Gather context
3. Research the market
4. Write the discovery document
5. Review and present

### Step 1: Determine Entry Point

- User describes a product idea, feature concept, or problem space → **Idea-First** (Step 2a)
- User points to an existing codebase, module, or running product → **Code-First** (Step 2b)
- User provides both an idea AND an existing codebase → **Combined** (Step 2a then 2b)
- If ambiguous, ask: "Should I research this from your product idea, or also reverse-engineer insights from existing code?"

Determine a short slug name for this research (e.g., "analytics-dashboard", "auth-flow"). This becomes the output filename.

### Step 2a: Gather Context — Idea-First

#### Initial Understanding

1. Read what the user has provided.
2. Restate the core idea in one sentence to confirm understanding.

#### Clarifying Questions

Ask 3-5 questions in the first round, prioritized by what blocks progress most:

| Area | Ask About |
|------|-----------|
| Problem | What specific pain exists? Who experiences it? What do they do today? |
| Users | Who are the distinct user types? How do their needs differ? |
| Market | Who are the known competitors? What market segment? |
| Scope | What's the boundary of this research? Full product or specific feature? |
| Context | Is there existing data, user feedback, or prior research to build on? |

Ask follow-up rounds (2-3 questions each) until the problem, target users, and market space are clear enough to research. Remaining unknowns become research objectives.

Proceed to Step 3.

### Step 2b: Gather Context — Code-First

Use the `design:explorer` agent or explore directly:

1. Ask which part of the codebase to analyze, or identify the boundary from the directory/module the user points to.
2. Read entry points (routes, CLI commands, main files) to identify user-facing capabilities.
3. Examine data models and schemas to infer the domain entities users interact with.
4. Read tests (especially integration/e2e tests) — test names and scenarios reveal intended user workflows.
5. Check for existing documentation, README, or comments that describe the intended audience.

From the code, extract:
- **Inferred personas** — distinct user roles visible in auth/permissions, UI flows, or API namespaces
- **Inferred workflows** — end-to-end user flows traceable through routes → controllers → services
- **Inferred pain points** — complex workarounds, TODOs, error-handling density suggesting fragile user paths
- **Feature inventory** — what capabilities exist today

Label all code-derived findings as **"inferred from codebase"** — these are hypotheses, not validated research.

If running the combined approach, merge codebase findings with the idea context from Step 2a. Use code evidence to ground or challenge the user's stated assumptions.

Proceed to Step 3.

### Step 3: Research the Market

Use web search to research:

1. **Competitors** — search for products solving the same or adjacent problems. Identify 3-5 direct competitors and note indirect alternatives (spreadsheets, manual processes, in-house tools).
2. **Market context** — trends, growth signals, regulatory changes, technology shifts relevant to the problem space.
3. **User insights** — published case studies, survey data, forum discussions (Reddit, HN, Stack Overflow, industry forums) where target users describe their pain points in their own words.

For each competitor found:
- Note their core value proposition, target segment, and pricing model
- Identify strengths, weaknesses, and apparent strategic direction
- Check review sites (G2, Capterra, Product Hunt) for recurring user complaints — these are unmet needs

Organize findings before proceeding. Do not draft the document until research is complete.

### Step 4: Write the Discovery Document

Read [references/discovery-document-guide.md](references/discovery-document-guide.md) for section-by-section writing guidance, templates, and examples.

1. Create the output directory if needed: `.product/research/`
2. Write the document at `.product/research/<slug-name>.md`
3. Follow this document structure:

```
# Discovery: [Product/Feature Name]

**Date:** [today's date]
**Status:** Draft
**Author:** AI-assisted discovery

## Executive Summary
## Problem Statement
## Business Context
## User Personas
## Jobs to be Done
## User Journey Map
## Competitive Landscape
### Strategic Positioning
### Competitor Profiles
### Feature Comparison
### Key Takeaways
## Opportunities & Recommendations
## Open Questions & Risks
## Next Steps
```

4. Write the Executive Summary LAST — after all other sections are complete.
5. Maintain the narrative chain: every opportunity must trace back to evidence from personas, JTBD, journey, or competitive analysis.

#### Evidence Labeling

Distinguish the source of each finding:

| Label | Use when |
|-------|----------|
| **(researched)** | Grounded in online research with sources |
| **(reported by user)** | Based on information the user provided |
| **(inferred from codebase)** | Derived from code analysis |
| **(hypothesized)** | Reasonable inference without direct evidence |

### Step 5: Review and Present

1. Review the draft against the quality checklist in [references/discovery-document-guide.md](references/discovery-document-guide.md).
2. Verify specifically:
   - Problem statement is solution-free and names a specific persona
   - Every persona has distinct goals
   - JTBD statements include situational triggers ("when...") and specific outcomes
   - Journey map shows current state, not idealized future
   - Competitive analysis connects gaps to user needs
   - Every opportunity traces to evidence
   - Assumptions are labeled, not presented as facts
3. Fix any issues found before presenting.
4. Present the completed document to the user with a brief summary of key findings and top opportunities. Ask for feedback.

## Edge Cases

If the user provides only a vague idea ("something with AI for teams"):
  → Ask 2-3 grounding questions to establish the problem space before starting research. Do not research a space so broad the findings would be generic.

If no direct competitors exist:
  → Look for indirect competitors and alternative solutions (manual processes, spreadsheets, general-purpose tools). Every problem has a "current solution" even if it's doing nothing.

If the codebase has no tests, no documentation, and minimal structure:
  → Rely on entry points, route definitions, and data models. Flag low-confidence inferences. Recommend user interviews as a high-priority next step.

If research reveals the problem is already well-solved by competitors:
  → Do not suppress this finding. Present it honestly in the competitive analysis. Focus opportunities on underserved segments, unmet needs, or differentiation angles.

If the user wants to jump straight to solutions:
  → Explain that discovery research is deliberately solution-agnostic — it defines the problem space so solutions can be evaluated against real user needs. Suggest completing the discovery document first, then using `write-prd` or `design-spec` for solution definition.

If the scope is too broad (multiple distinct product areas):
  → Propose splitting into separate discovery documents, one per product area. Confirm with the user.

If the user provides existing research (surveys, interview notes, analytics):
  → Incorporate as primary evidence. Label the source. Use online research to fill gaps and triangulate, not to replace user-provided data.
