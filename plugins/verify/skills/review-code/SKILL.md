---
name: review-code
description: "Review, audit, or evaluate backend code. Triggers: 'review code', 'review architecture', 'review logic', 'review maintainability', 'review tests', 'security audit', 'find code smells', 'check test coverage', 'check backward compatibility'."
---

# Review Code

## Arguments

Parse from the user's request:

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| mode | no | ask user | `architecture`, `logic`, `maintainability`, or `test` |
| scope | no | full project | Files, modules, or directories to review |
| focus | no | all dimensions | Specific dimension within a mode (e.g., "security", "coupling", "SOLID") |

**Parsing examples:**

- "review code" → mode: ask user
- "review the architecture of src/orders/" → mode: architecture, scope: src/orders/
- "find code smells in the API layer" → mode: maintainability, scope: API layer files
- "security audit" → mode: logic, focus: security
- "check backward compatibility" → mode: architecture, focus: backward compatibility
- "review tests" → mode: test

## Process

1. Parse arguments from the user's request
2. If mode is not specified, ask the user which mode to run
3. Read the workflow for the selected mode (see [Workflows](#workflows))
4. For multiple modes, run sequentially: architecture → logic → maintainability → test

## Workflows

Read the workflow file for the selected mode:

- **Architecture** — [references/architecture/workflow.md](references/architecture/workflow.md): structural soundness, layering, coupling, resilience, backward compatibility. Read when reviewing architecture, coupling, scalability, or system design.
- **Logic** — [references/logic/workflow.md](references/logic/workflow.md): correctness, API design, database usage, security, performance. Read when reviewing correctness, logic, APIs, security, or databases.
- **Maintainability** — [references/maintainability/workflow.md](references/maintainability/workflow.md): code smells, SOLID violations, naming, dead code. Read when reviewing code quality, maintainability, smells, SOLID, or naming.
- **Test** — [references/test/workflow.md](references/test/workflow.md): test coverage adequacy, scenario completeness, test waste. Read when reviewing test coverage, quality, or strategy.

All workflows use [references/shared-quality-standards.md](references/shared-quality-standards.md) for finding format, severity definitions, verification checklist, and report standards. Read before writing any report.

## Escalation

If the codebase type is unclear (library vs service vs CLI):
→ Check framework dependencies, entry points, and directory conventions
→ If still unclear, ask the user before proceeding

If a potential issue might be intentional design:
→ Flag as "Potential — verify intent" rather than a definitive finding

If the codebase is too large to review fully:
→ Prioritize hot spots (high complexity, high change frequency, high coupling)
→ State which areas were reviewed and which were skipped

## Edge Cases

- **Very small codebase** (< 10 source files): Focus on what to monitor as it grows.
- **No clear architectural pattern**: Report as a finding.
- **Multiple modes requested**: Ask whether the user wants a combined or separate reports.
- **No tests in codebase**: Flag as critical in test mode.
- **Library or CLI** (no endpoints): Skip API-specific checks; focus on public interface, error handling, correctness.
