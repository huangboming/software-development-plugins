# Backend Architecture — Template & Guide

## Document Template

Use this structure for `docs/development/system/architecture.md`. Adapt based on what the codebase contains — omit inapplicable sections, add sections for significant concerns not listed.

```markdown
# Architecture

> Last updated: <date>

## System Overview

What the system does, its primary responsibilities, and the architectural
style (monolith, modular monolith, microservices, etc.).

## System Context

How this system fits into its broader environment:
- External consumers and how they interact (REST, gRPC, events, CLI)
- External dependencies (databases, third-party APIs, message brokers, auth
  providers) and where each is accessed in the code
- Public interfaces and contracts (endpoints, message schemas, shared types)

Include a Mermaid flowchart or block diagram. Use standard diagram types
(flowchart, block-beta), not C4Context.

## Tech Stack & Infrastructure

Languages, frameworks, runtime. Key libraries and their roles. Infrastructure
(databases, caches, queues) and how they're provisioned. Build tooling and
package management.

## Core Architecture & Components

Architectural style and how the codebase is organized around it. List major
components with responsibilities, mapped to codebase locations
(e.g., `Order Processing → src/domain/orders/`).

Include a Mermaid component diagram if it clarifies module relationships.

## Data Flow

How data moves through the system for primary use cases — request lifecycle,
event pipeline, or transformation chain. Include Mermaid diagrams for
non-trivial flows.

## Design Patterns

Patterns in use (repository, event sourcing, CQRS, middleware pipeline, etc.).
For each: where it's implemented and why it was chosen.

## Configuration & Environment

How the system is configured (env vars, config files, feature flags) and key
options that affect behavior.
```

## Exploration Guide

When creating from scratch, prioritize these areas during deep exploration:

- **Entry points and request/event lifecycle** — understanding how requests enter and flow through the system anchors every other section
- **Module boundaries and inter-module dependencies** — reveals the actual architecture vs. what directory names suggest
- **External system integrations** (databases, APIs, queues) — these are the hardest parts to reconstruct from code alone and the most valuable to document
- **Public interfaces and contracts** — what other teams/services depend on; changes here have the widest blast radius
- **Configuration and environment handling** — often scattered and poorly documented; worth surfacing early
- **Recurring structural patterns** (e.g., repository pattern, middleware pipeline) — recognizing these helps developers predict where new code should go

## Quality Checklist

- [ ] Architectural claims are grounded in concrete code (specific files or directories)
- [ ] Module descriptions are one sentence each, not paragraphs
- [ ] Mermaid diagrams included for non-trivial data flows and component relationships
- [ ] Mermaid node labels use actual line breaks, never `\n` escape sequences
- [ ] Concrete path examples (e.g., "`api/routes.py` → `services/order.py` → `repos/order_repo.py`") instead of abstract layer names
- [ ] Written for a developer with zero project context
- [ ] Intentional design decisions distinguished from emergent patterns

## Edge Cases

- **Monorepo with multiple services**: One architecture.md per service, or top-level with cross-references. Ask the user.
- **Very small project** (< 10 source files): Keep proportionally brief. Skip sections like "System Context" or "Design Patterns" if not warranted.
- **No clear architectural pattern**: Document actual structure honestly. Note this as an observation rather than imposing a pattern.
