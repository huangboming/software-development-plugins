---
name: write-spec
description: "Write a design-focused technical spec for a backend, frontend, or full-stack feature at .product/design/specs/<slug>.md. Mermaid diagrams (architecture, sequence, ER, state) and tables for shapes. Triggers: '/write-spec', 'write a tech spec', 'write a design spec', 'spec out [feature]', 'design the architecture for [feature]'."
---

# Write Spec

## Process

1. **Classify scope** — backend, frontend, or full-stack. State it in one line.
2. **Explore the codebase** — for non-trivial features, dispatch an `Explore` subagent to find similar features and patterns. Skip on greenfield.
3. **Write the artifact** — fill `assets/template-spec.md` at `.product/design/specs/<slug>.md`. `<slug>` is kebab-case from the feature name; create the directory if missing.

## Hard constraints

- **Design-first, code-light.** Shapes in tables (no DDL), architecture in `flowchart`, behavior in `sequenceDiagram` / `stateDiagram-v2` when non-trivial. Code snippets ≤10 lines, only when shape is otherwise ambiguous.
- **Skip sections that don't apply.** Every section after Context is conditional. Mark `N/A — reason` only when a reviewer might expect the section and you intentionally skipped it.
