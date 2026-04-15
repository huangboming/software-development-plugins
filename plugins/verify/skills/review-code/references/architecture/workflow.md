# Architecture Review Workflow

Review system architecture for structural soundness, coupling health, layering violations, error handling, scalability readiness, and backward compatibility.

## Process

1. Establish context
2. Map the architecture
3. Analyze findings
4. Verify findings
5. Write report

### 1. Establish Context

Determine scope and quality priorities before examining code.

Ask the user (skip if already clear from context):
- What are the primary quality attributes this system prioritizes? (performance, availability, modifiability, security)
- Any specific architectural concerns or areas of pain?
- Is this a monolith, modular monolith, or microservices?

Run the inventory script to bootstrap understanding (always run for fresh data, even if `.hand-offs/architecture-inventory.md` already exists):

```
uv run --script ${CLAUDE_PLUGIN_ROOT}/skills/review-code/scripts/arch_inventory.py --repo <path>
```

Use the inventory output to inform agent charters in Step 2.

### 2. Map the Architecture

Launch 2-3 explorer agents in parallel:

**Agent 1 — Structure & Layering:**
- Map top-level directory structure and identify the architectural pattern (clean, hexagonal, onion, n-tier, or none)
- Identify layer boundaries and classify files into layers (domain, application, infrastructure)
- Check import direction: flag outward-pointing dependencies (inner layer -> outer layer)
- Identify public contracts: API schemas/specs, database schemas shared across services, event/message schemas
- Check for API versioning strategy (URL prefix, header-based, or none)
- Return a list of 5-10 key files with one-line descriptions of the pattern found in each

**Agent 2 — Dependencies & Coupling:**
- Map module/package dependencies and identify cycles
- Identify hub components (high fan-in AND fan-out)
- Check for shared database access across service boundaries (if multi-service)
- Look for distributed monolith signals (shared schemas, coordinated deployments)
- Return a list of 5-10 files with one-line descriptions of the concerning dependency pattern in each

**Agent 3 — Resilience & Scalability:**
- Examine error handling patterns: are errors typed, propagated explicitly, or silently swallowed?
- Check for circuit breakers, timeouts, retry logic on external calls
- Look for N+1 query patterns, synchronous call chains, stateful services
- Check for missing idempotency on mutation operations
- Return a list of 5-10 files with one-line descriptions of the concerning pattern in each

After agents return, read the key files they identified.

### 3. Analyze Findings

Load the relevant reference for each applicable dimension:

| Dimension | Reference | Load When |
|-----------|-----------|-----------|
| Anti-patterns | [anti-patterns.md](anti-patterns.md) — God Class, Brain Class, Anemic Domain Model, Circular Dependencies, Big Ball of Mud, Distributed Monolith, Leaky Abstraction | Full review, or when structural issues found |
| Coupling & metrics | [coupling-metrics.md](coupling-metrics.md) — Ca/Ce/Instability/Abstractness metrics, ADP/SDP/SAP principles, danger zones, hub node detection | Full review, or when dependency concerns found |
| Layering | [layering-patterns.md](layering-patterns.md) — Clean/Hexagonal/Onion/N-tier identification, layer definitions, import direction rules, violation patterns | Full review, or when layer violations found |
| Resilience & scalability | [resilience-patterns.md](resilience-patterns.md) — Error handling architecture, circuit breaker/retry/bulkhead/saga patterns, scalability anti-patterns | Full review, or when error/scalability concerns found |
| Backward compatibility | [backward-compatibility.md](backward-compatibility.md) — API contract evolution, database migration safety, event schema versioning, rolling deployment compatibility | Full review, or when contract/integration concerns found |
| Diagram templates | [mermaid-templates.md](mermaid-templates.md) — C4-style context, container, and sequence diagram templates | When writing the report (Step 5) |

For each finding:
1. Name the pattern or anti-pattern (use established names from the references)
2. Cite specific files and code locations
3. Assess severity using the definitions in [shared-quality-standards.md](../shared-quality-standards.md)
4. Explain the concrete risk — what breaks and under what conditions, not abstract theory

### 4. Verify Findings

Apply the verification checklist from [shared-quality-standards.md](../shared-quality-standards.md).

Additionally:
- Verify layer classifications by checking actual import statements, not just directory names
- Confirm dependency concerns by tracing real import chains in the cited files

### 5. Write Report

Write to `.hand-offs/reviews/architecture/YYYY-MM-DD-HHMM.md`. Create `.hand-offs/reviews/architecture/` if it does not exist.

- **timestamp**: `YYYY-MM-DD-HHMM` (e.g., `2026-03-04-1430`)
- Example: `.hand-offs/reviews/architecture/2026-03-04-1430.md`

```markdown
# Architecture Review: <Scope>

> Reviewed: <date> | Scope: <files/modules reviewed> | Style: <identified style> | Health: <Solid | Adequate with risks | Needs significant rework>

## Architecture Overview

- Identified architectural style (or lack thereof)
- System decomposition summary (modules, services, layers)
- Key quality attributes and how the architecture addresses them

## Architecture Diagrams

Include Mermaid diagrams adapted from `references/mermaid-templates.md`:
- C4-style system context diagram
- Container / service topology diagram
- 1-2 sequence diagrams for critical flows

## Findings

### <Dimension Name>

**[Severity] <Anti-Pattern/Issue Name>**
Location: `path/to/file.py:42`, `path/to/other.py:18`
Issue: <What the issue is, concretely>
Risk: <What can go wrong and under what conditions>
Fix: <Specific, actionable fix>

<!-- Repeat per finding, ordered by severity: Critical -> High -> Medium -> Low -->

## Summary

- Findings: <N> Critical, <N> High, <N> Medium, <N> Low
- **Top recommendations:**
  1. <Highest impact-to-effort recommendation>
  2. <Second>
  3. <Third>
- **Overall assessment:** <Solid | Adequate with risks | Needs significant rework>
```

## Edge Cases

- If the inventory script produces no signals (no frameworks, no infra), the project may be a library or CLI tool — adjust the review dimensions accordingly.
- If no clear architectural pattern is identifiable, report this as a finding (Big Ball of Mud tendency) rather than guessing at intent.
