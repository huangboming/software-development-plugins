# Intake Record Template

```markdown
# Intake: [Short Name]

**Date:** [today's date]
**Source:** [where this requirement came from]
**Source type:** [customer-feedback | stakeholder-request | support-ticket | market-signal | internal-observation | user-research | competitor-move | regulatory | other]
**Status:** Captured

## Requirement

[One paragraph: what is being requested or observed. State the need, not the solution. Include enough context that someone unfamiliar with the source can understand it.]

## Problem Context

[Why does this matter? What is the pain, gap, or opportunity? Who experiences it? What happens if we do nothing?]

## Duplicate & Overlap Check

| Checked Against | Findings |
|----------------|----------|
| Backlog (`docs/product/backlog/backlog.md`) | [No matches / Overlaps with: <item> — <how it relates>] |
| PRDs (`docs/product/prd/`) | [No matches / Related to: <prd> — <how it relates>] |
| Research (`docs/product/research/`) | [No matches / Covered in: <doc> — <how it relates>] |
| Intakes (`docs/product/intakes/`) | [No matches / Similar to: <intake> — <how it relates>] |

## Assessment

**Category:** [new-capability | enhancement | pain-point | compliance | technical-enabler]
**Rough size:** [small — days | medium — weeks | large — months]
**Clarity:** [clear — well-defined, can act on it | partial — needs more detail | vague — needs discovery]

## Raw Notes

[Optional. Verbatim quotes, links, screenshots, or supporting material from the source. Preserve original wording — do not interpret here.]
```

## Field Guidance

### Source type definitions

| Source type | When to use |
|-------------|-------------|
| customer-feedback | Direct feedback from users or customers (interviews, surveys, support conversations, reviews) |
| stakeholder-request | Request from internal stakeholders (executives, sales, partners) |
| support-ticket | Pattern emerging from support issues |
| market-signal | Market trends, analyst reports, industry shifts |
| internal-observation | Team-identified gap, tech debt surfacing as user pain, operational insight |
| user-research | Finding from a discovery document (`docs/product/research/`) |
| competitor-move | Competitor launched a feature, changed pricing, or shifted strategy |
| regulatory | Legal, compliance, or regulatory requirement |
| other | Anything not covered above — add a brief note |

### Category definitions

| Category | When to use |
|----------|-------------|
| new-capability | Something the product cannot do today at all |
| enhancement | Improving something the product already does |
| pain-point | Addressing a friction, failure, or frustration in current functionality |
| compliance | Legal, regulatory, or policy-driven requirement |
| technical-enabler | Infrastructure or platform work that unblocks future capabilities (not directly user-facing) |

### Rough size calibration

Size reflects end-to-end effort from spec through delivery, not just coding:

- **Small (days):** Isolated change, clear scope, minimal cross-cutting concerns
- **Medium (weeks):** Touches multiple components, needs design input, moderate testing
- **Large (months):** New system capability, architectural changes, cross-team coordination

When uncertain, round up. Optimistic sizing is a more common failure mode than pessimistic.
