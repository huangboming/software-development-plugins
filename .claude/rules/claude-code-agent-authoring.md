---
paths:
  - "plugins/**/agents/*.md"
---

# Claude Code Agent Authoring

One agent per file at `plugins/<plugin>/agents/<agent-name>.md`. The file body is the system prompt the agent runs with when invoked via the `Task` tool.

## Frontmatter

Required: `name`, `description`, `tools`, `model`.
Conditional: `skills` — include when the agent wraps an existing skill.

- `name` — lowercase-kebab-case, matches the filename.
- `description` — one or two sentences stating what the agent does and when to invoke it. Claude uses this to route Task calls, same role as a skill's `description`.
- `tools` — comma-separated, accurate subset. List only tools the agent actually needs. No wildcards.
- `model` — pick by role, not by default:
  - `opus` — judgment-heavy work (architecture review, ambiguous research, writing that requires taste).
  - `sonnet` — structured execution (doc generation, spec-driven review, synthesis).
  - `haiku` — mechanical transforms, classification, short lookups.
- `skills` — a single reference like `docs:write-api` when the agent's whole job is to execute that skill.

## Two agent shapes

**Skill-wrapping agent** (has `skills:`). The body states role, constraints, and escalation rules — *not* the procedure. The procedure lives in the referenced skill; duplicating it here causes the two to drift. Keep the body short.

**Self-contained agent** (no `skills:`). The body holds the full system prompt: identity, procedure, stopping conditions, output format. Use this shape when the agent does not map 1:1 onto a skill (researchers, specialists making a judgment call, general-purpose roles).

## System prompt content

- Lead with identity and responsibilities in a few short lines — not a character sheet.
- State hard constraints explicitly: resource budgets, stopping conditions, forbidden actions.
- State escalation rules — when to hand back to the caller rather than guessing.
- Define the output shape when the caller needs to parse or re-use it.

## Tool list discipline

The `tools` list is a capability contract. Adding a tool "just in case" expands the agent's blast radius every time it runs. Audit the list against the procedure: if a tool isn't named in the body or the referenced skill, remove it.

## Never

- Never list tools the agent won't use.
- Never duplicate the procedure of a referenced skill inside the agent body.
- Never set `model: opus` for mechanical work, or `haiku` for work that needs judgment. Match model cost to task complexity.
- Never write a multi-page character sheet before the actual instructions. Role framing should be a few lines, not a page.
