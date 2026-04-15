# Discovery Document Guide

Section-by-section guidance for writing each part of the discovery document. Read this before drafting.

## Table of Contents

1. [Document Structure](#document-structure)
2. [Executive Summary](#1-executive-summary)
3. [Problem Statement](#2-problem-statement)
4. [Business Context](#3-business-context)
5. [User Personas](#4-user-personas)
6. [Jobs to be Done](#5-jobs-to-be-done)
7. [User Journey Map](#6-user-journey-map)
8. [Competitive Landscape](#7-competitive-landscape)
9. [Opportunities & Recommendations](#8-opportunities--recommendations)
10. [Open Questions & Risks](#9-open-questions--risks)
11. [Next Steps](#10-next-steps)
12. [Quality Checklist](#quality-checklist)

---

## Document Structure

The sections form a progressive narrative chain — each builds on the previous:

```
Problem → Personas → JTBD → Journey → Competition → Opportunities → Next Steps
```

Maintain this chain. Every opportunity should trace back to a persona need, a JTBD gap, or a competitive white space.

---

## 1. Executive Summary

One paragraph (3-5 sentences) that answers:
- What problem did we investigate?
- Who experiences it?
- What did we learn?
- Where is the biggest opportunity?

Write this LAST, after all other sections are complete.

**Good example:**
> Marketing managers at mid-market SaaS companies spend 3+ hours weekly compiling performance data from fragmented tools, often making decisions on stale data. Our research identified 4 direct competitors — none of which solve the cross-platform attribution problem. The biggest opportunity is a unified dashboard with automated cross-channel attribution, targeting the 68% of mid-market teams still using spreadsheets.

**Bad example:**
> We think there's a market opportunity for a dashboard product. We looked at some competitors and talked to potential users.

---

## 2. Problem Statement

Solution-free. Specific. Measurable where possible.

**Formula:** [Who] experiences [what problem] when [circumstance], which results in [consequence].

| Weak | Strong |
|------|--------|
| "Teams need better collaboration tools" | "Remote engineering teams of 10-50 lose an average of 4 hours/week to context-switching between Slack threads, Jira tickets, and code reviews because there is no unified view of what's in progress" |
| "Users want a faster experience" | "E-commerce shoppers abandon carts 34% more often when checkout takes more than 3 steps, costing mid-tier retailers an estimated $2M/year in lost revenue" |

Include:
- The specific persona(s) affected
- Observable behavior or measurable impact
- The circumstance that triggers the pain
- What they do today (the workaround)

---

## 3. Business Context

Explain why this problem is worth solving NOW. Cover:

- **Strategic alignment** — how this connects to business goals or strategy
- **Market timing** — why now (trends, regulatory changes, competitive pressure, technology shifts)
- **Opportunity size** — rough sizing (TAM/SAM/SOM if available, or qualitative signals like "growing segment")
- **Cost of inaction** — what happens if this is not addressed

Keep this section brief (5-10 sentences). If the business context is speculative, label assumptions explicitly.

---

## 4. User Personas

Write 2-4 personas representing distinct behavioral segments (not job titles). Every detail must serve a design decision — cut anything decorative.

### Persona Template

```markdown
### [Name] — The [Archetype Label]

**Role**: [Job title, company type, team size]
**Experience**: [Relevant background that shapes their perspective]

> "[Representative quote that captures their worldview]"

**Goals**
- [What success looks like for them — 2-3 items]

**Frustrations**
- [What blocks them or causes friction — 2-3 items]

**Behaviors**
- [How they currently solve the problem, tools they use, decision-making patterns — 2-3 items]

**Context**
- [Environment, constraints, team dynamics that affect how they'd adopt a solution — 1-2 items]
```

### Persona Quality Criteria

- Every persona has a distinct primary goal that differs from the others
- Frustrations are specific and observable, not generic ("frustrated with slow tools")
- Behaviors describe what they DO, not what they want
- The representative quote sounds like something a real person would say in an interview
- Demographics are included only when they affect product decisions
- If derived from codebase analysis (not real interviews), label them as **hypothesized personas** and note the evidence source

---

## 5. Jobs to be Done

Use the Christensen/Moesta format for JTBD statements:

```
When [situation/trigger], I want to [motivation/action], so I can [expected outcome].
```

### Structure

For each persona, write 1-3 JTBD statements covering:
- **Core functional job** — the practical task
- **Emotional job** — how they want to feel (or avoid feeling)
- **Social job** (if applicable) — how they want to be perceived

### JTBD Quality Criteria

| Good | Bad |
|------|-----|
| Solution-free — describes the job, not a tool | Mentions a specific product or feature |
| Includes the situational trigger ("when...") | Generic and context-free |
| Stable over time — this job existed before the product | Tied to current technology |
| Specific outcome, not vague aspiration | "...so I can be more productive" |

### Example

**Persona: Sarah, Scaling Startup CTO**

- **Functional:** When I'm reviewing a pull request from a team I no longer work with daily, I want to quickly assess whether it follows our architecture patterns, so I can approve or flag issues without reading every line.
- **Emotional:** When a production incident happens at 2 AM, I want to trust that the on-call engineer has enough context to resolve it, so I can avoid the dread of being the single point of failure.
- **Social:** When presenting the technical roadmap to the board, I want to show clear progress metrics tied to business outcomes, so I can be seen as a strategic leader, not just a "tech person."

---

## 6. User Journey Map

Map the CURRENT state — how users solve the problem today, without the product. Use domain-specific stages, not generic funnels.

### Format: Table-Per-Stage

For each stage, capture five dimensions:

```markdown
### Stage: [Stage Name]

| Dimension | Details |
|-----------|---------|
| **Actions** | What the user does (observable behavior) |
| **Thoughts** | What questions or considerations arise |
| **Emotions** | Confidence, frustration, confusion, relief (be specific) |
| **Pain points** | Friction, blockers, workarounds, time waste |
| **Opportunities** | Where a product could intervene to improve the experience |
```

### Journey Map Quality Criteria

- 4-7 stages (fewer if the problem is simple, more if the workflow is complex)
- Stages are named for what the user does, not product features
- Pain points describe observable friction, not vague dissatisfaction
- Opportunities are solution-agnostic (describe what should improve, not how)
- At least one stage captures the "moment of highest frustration" — this is often where the biggest opportunity exists
- If derived from codebase analysis, label stages as **inferred from code** and note which code paths informed them

---

## 7. Competitive Landscape

Combine strategic positioning with a targeted feature comparison.

### 7a. Strategic Positioning

Describe a 2x2 positioning map using two dimensions most relevant to the target personas. Place each competitor and describe the white space.

```markdown
**Positioning dimensions:** [Dimension A] (x-axis) vs [Dimension B] (y-axis)

| Competitor | [Dim A] | [Dim B] | Position |
|-----------|---------|---------|----------|
| Competitor 1 | High | Low | [Brief positioning note] |
| Competitor 2 | Low | High | [Brief positioning note] |
| ...         | ...     | ...     | ...      |

**White space:** [Where no competitor is strong — this is the opportunity zone]
```

Choose dimensions that differentiate meaningfully. Avoid generic axes like "quality" or "features."

### 7b. Competitor Profiles

For each key competitor (3-5 max):
- **What they do well** — core strength and why customers choose them
- **Where they fall short** — gaps relative to target users' JTBD
- **Strategic direction** — where they appear heading (recent launches, hiring signals, messaging shifts)

### 7c. Feature Comparison

Compare the 8-12 capabilities that matter most to the target personas. Use a clear rating system.

```markdown
| Capability | Competitor A | Competitor B | Competitor C | Opportunity |
|-----------|-------------|-------------|-------------|-------------|
| Feature 1 | Full | Partial | None | ... |
| Feature 2 | None | Full | Full | ... |
```

### 7d. Key Takeaways

- What is table stakes (every competitor has it)?
- Where is the differentiation opportunity?
- What unmet needs are competitors ignoring?

---

## 8. Opportunities & Recommendations

Synthesize findings into prioritized opportunities. Each opportunity must trace back to evidence from the previous sections.

### Opportunity Template

```markdown
### Opportunity: [Name]

**Evidence:** [Which personas, JTBD, journey pain points, or competitive gaps support this]
**Impact:** [High/Medium/Low — who benefits and how much]
**Feasibility:** [High/Medium/Low — rough sense of effort]
**Priority:** [Recommended priority based on impact x feasibility]

[1-3 sentence description of the opportunity]
```

List 3-7 opportunities, ordered by priority. For each, make the evidence chain explicit — this is what separates actionable recommendations from opinions.

---

## 9. Open Questions & Risks

### Open Questions

Unanswered questions that need further investigation. For each:
- State the question
- Explain why it matters (what decision it blocks)
- Suggest how to answer it (interview, experiment, data analysis)

### Risks

Known risks to pursuing the identified opportunities. For each:
- State the risk
- Assess likelihood and impact
- Suggest a mitigation or how to learn more

---

## 10. Next Steps

Concrete, actionable next steps. Each should have:
- A clear action ("Conduct 5 user interviews with mid-market CTOs")
- Purpose ("Validate persona assumptions and refine JTBD")
- Suggested sequence or dependency

Avoid vague statements like "explore this further" or "do more research." If more research is needed, specify what questions it should answer.

---

## Quality Checklist

Review the complete document against these criteria before presenting:

### Narrative Chain
- [ ] Problem statement is solution-free and specific
- [ ] Every persona has distinct goals that differ from the others
- [ ] JTBD statements include situational triggers and specific outcomes
- [ ] Journey map shows current state, not idealized future
- [ ] Competitive analysis connects gaps back to user needs
- [ ] Every opportunity traces to evidence from personas, JTBD, journey, or competition

### Evidence & Honesty
- [ ] Claims are grounded in research, data, or codebase evidence
- [ ] Assumptions are labeled explicitly ("assumed based on..." or "hypothesized")
- [ ] Codebase-derived insights are distinguished from real user research
- [ ] Open questions capture genuine unknowns, not rhetorical filler
- [ ] Confidence levels are indicated where findings are uncertain

### Actionability
- [ ] Executive summary can be read standalone in under 60 seconds
- [ ] Opportunities are prioritized, not just listed
- [ ] Next steps are concrete actions, not vague directions
- [ ] The document is scannable — headings, tables, bullet points over prose walls

### Completeness
- [ ] All sections present (Executive Summary through Next Steps)
- [ ] 2-4 personas covering distinct behavioral segments
- [ ] JTBD for each persona covering functional + emotional dimensions
- [ ] Journey map with 4-7 domain-specific stages
- [ ] 3-5 competitors analyzed with positioning + feature comparison
- [ ] 3-7 prioritized opportunities
