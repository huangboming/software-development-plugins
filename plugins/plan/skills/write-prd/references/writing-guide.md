# PRD Writing Guide

## Working Backwards: Start with the Customer

Every PRD begins with the problem, not the solution. Before writing anything else, answer:

1. **Who** has this problem? (specific persona, not "users")
2. **What** is painful about their current situation?
3. **Why** does solving it matter now?

The problem statement is the most important section. If it doesn't resonate, nothing else matters.

### Problem Statement Examples

**Weak:**
> We need a dashboard to display analytics data.

**Strong:**
> Marketing managers spend 2+ hours each Monday manually pulling data from three different tools to build their weekly performance report. They often miss trends because the data is stale by the time they compile it.

**Why the strong version works:** It names the persona (marketing manager), quantifies the pain (2+ hours), describes the current workaround (manual pulling from three tools), and explains why it matters (missed trends).

## Perspective

Write everything from the **user's or product manager's perspective**. Describe *what* users need and *why*, never *how* the system implements it.

- Describe behavior in terms of what the user sees, does, and experiences.
- Frame non-functional requirements as user expectations ("search results appear within 2 seconds"), not engineering specs ("use Redis caching with 100ms TTL").
- Frame dependencies as product-level relationships ("requires the notifications feature"), not technical integrations ("calls the notification microservice via gRPC").

If any sentence references a specific technology, database, API endpoint, or architectural pattern, rewrite it in user/business terms.

## Writing SMART Success Metrics

Every metric must be:

- **Specific** — what exactly is measured
- **Measurable** — how to measure it (tool, query, method)
- **Achievable** — realistic given constraints
- **Relevant** — tied to the problem statement
- **Time-bound** — by when

| Quality | Example |
|---------|---------|
| Weak | "Improve user satisfaction" |
| Strong | "Increase task completion rate from 62% to 80% within 3 months of launch, measured via analytics" |

If a baseline isn't known yet, write "TBD — measure before launch" rather than guessing.

## Non-Goals: Preventing Scope Creep

Non-goals are not "things we don't want." They are **things someone might reasonably expect to be in scope, but aren't.** Each non-goal should include a brief reason.

**Weak:**
> - Not building a mobile app

**Strong:**
> - **Real-time collaboration** — initial version is single-user; we'll evaluate collaboration based on adoption data in Q3
> - **Custom report builder** — we'll ship pre-built report templates first and assess demand for customization

**Guiding question:** "If I showed this PRD to a new engineer, what would they assume is included that actually isn't?"

## Persona Writing

Personas bridge the gap between abstract "users" and real people with specific problems.

**Keep personas lightweight** — 3-4 lines, not multi-page documents. Focus on what's relevant to *this* product:

| Field | What to Include | What to Skip |
|-------|----------------|--------------|
| Role | Job title or function | Demographics, age, hobbies |
| Context | When/where they hit this problem | General work description |
| Pain point | Their specific frustration today | Vague "needs" |
| Success | What "done" looks like for them | Aspirational vision |

## User Stories

Use specific roles, user-perspective capabilities, and real business value:

| Component | Weak | Strong |
|-----------|------|--------|
| Role | "As a **user**" | "As a **paying subscriber**" |
| Capability | "I want a date picker component" | "I want to filter orders by date" |
| Benefit | "So that I can use the feature" | "So that I can find recent transactions quickly" |

**Full example — weak:**

> **As a** user, **I want** a search bar, **So that** I can search.

**Full example — strong:**

> **As a** hiring manager, **I want** to search candidates by skill and years of experience, **So that** I can quickly build a shortlist for open roles.

## Acceptance Criteria

Write in Given/When/Then format. Each criterion should be independently verifiable and describe what the user observes.

**Example — weak:**

> - [ ] The system validates the input correctly

**Example — strong:**

> - [ ] Given a logged-in recruiter, when they enter "Python" in the skill filter and "3+" in the experience field, then only candidates matching both criteria appear in the results
> - [ ] Given a logged-in recruiter, when they search with no matching candidates, then a message "No candidates match your filters" appears with a suggestion to broaden the search

Cover these categories after the happy path:

- **Empty states** — no data, first-time use
- **Boundary values** — max length, zero, negative
- **Error conditions** — invalid input, unavailable service, permission denied
- **Concurrent/conflicting actions** — two users editing the same item

## Mermaid Flowcharts

Include a flowchart when the feature involves multiple decision points, multi-step user journeys, or state transitions visible to the user.

Focus on what the user experiences. Exclude internal system steps (queue processing, database writes, cache invalidation) unless they produce user-visible effects.

Example:
```
flowchart TD
    A[User opens form] --> B{Logged in?}
    B -->|Yes| C[Show form]
    B -->|No| D[Redirect to login]
    C --> E[User submits]
    E --> F{Input valid?}
    F -->|Yes| G[Show confirmation]
    F -->|No| H[Show error messages]
    H --> C
```

## Risks & Mitigations

Good risk analysis surfaces what could derail the initiative. Focus on risks specific to *this* product, not generic risks.

**Categories to consider:**

- **User adoption** — will users actually switch from their current workflow?
- **Dependencies** — are we blocked by another team's work?
- **Complexity** — is the scope larger than it appears?
- **Data** — do we have the data we need, or are we assuming it exists?
- **Timing** — are there deadlines, compliance dates, or market windows?

**Weak:**
> Risk: Project might be delayed. Mitigation: Add more engineers.

**Strong:**
> Risk: Payment provider API has a 3-week integration timeline that could delay launch. Mitigation: Begin integration in week 1; have fallback provider identified.

## Feature Prioritization

When listing features in a product-level PRD, use three tiers:

| Priority | Meaning | Decision Rule |
|----------|---------|---------------|
| Must-have | Launch is blocked without this | Users cannot accomplish the core task without it |
| Should-have | Significantly improves the experience | Users can work around it, but it's painful |
| Nice-to-have | Polishes the experience | Adds delight but doesn't affect core value |

## Quality Checklist

### Product-Level PRD

- [ ] Problem statement names a specific persona and a specific pain
- [ ] Product vision is one sentence, customer-centric
- [ ] Goals describe outcomes, not outputs (no "build X" or "implement Y")
- [ ] Non-goals would surprise someone who didn't write this PRD
- [ ] At least one persona is defined with role, context, pain point, and success criteria
- [ ] Features are prioritized (must-have / should-have / nice-to-have)
- [ ] Success metrics are SMART — each has definition, baseline, target, timeframe
- [ ] Risks are specific to this initiative, not generic project risks
- [ ] No implementation details — no technologies, architecture, or system internals
- [ ] Open questions capture genuine unknowns, not rhetorical questions

### Feature-Level PRD

- [ ] Problem statement ties back to the parent PRD's problem (if applicable)
- [ ] Goals are specific to this feature, not the whole product
- [ ] Non-goals prevent feature scope creep
- [ ] User stories use specific roles, capabilities, and real benefits
- [ ] Capabilities describe user intent, not implementation details
- [ ] Benefits state actual business/user value
- [ ] Acceptance criteria are in Given/When/Then format and independently testable
- [ ] Happy path and key edge cases are covered
- [ ] Mermaid flowchart included for multi-step or branching flows
- [ ] Success metrics are feature-specific and measurable
- [ ] Non-functional requirements framed as user expectations
- [ ] Glossary defines all domain-specific terms in plain language
- [ ] No implementation details leaked — no technologies, architecture, or system internals
- [ ] Stories within a feature are cohesive — they belong together
- [ ] Document is understandable by an engineer with no prior context
