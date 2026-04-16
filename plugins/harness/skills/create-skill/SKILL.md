---
name: create-skill
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
license: Complete terms in LICENSE.txt
---

# Skill Creator

Navigation center for creating and iterating on skills. This file routes to rules, workflows, and references rather than holding the material itself. Read the file named for the task at hand; everything else loads on demand.

## What a Skill Is

A skill is a modular package — a required `SKILL.md` plus optional `scripts/`, `references/`, `assets/` (and, for larger skills, `rules/` and `workflows/`) — that transforms Claude from a general-purpose agent into a specialized one for a specific domain.

For the full anatomy and loading model, see `references/skill-anatomy.md` and `references/progressive-disclosure.md`.

## Always Read

Before any skill-creation or iteration task, read all six files below:

1. `rules/core-principles.md` — concise, push-off-defaults, degrees-of-freedom, avoid-railroading
2. `rules/authoring.md` — frontmatter, imperative form, exclusions, no-duplication, reference-every-file
3. `rules/context-engineering.md` — context allocation strategies, signal-to-noise tests, anti-patterns
4. `references/skill-anatomy.md` — folder structure, file types, and when to split into `rules/` + `workflows/` + `references/`
5. `references/progressive-disclosure.md` — three-level loading system; governs what goes in SKILL.md vs. references
6. `references/writing-effective-instructions.md` — imperative form, examples, edge cases, anti-patterns for SKILL.md body

## Hard Constraints

- **Confirm before delegating.** Before launching `skill-reviewer` agents (Step 5 of `workflows/create-new-skill.md`), present the axis options to the user and wait for their selection. Do not auto-launch reviews without confirmation.

## Common Tasks

| Task | Workflow |
|------|----------|
| Create a new skill from scratch | `workflows/create-new-skill.md` |
| Iterate on an existing skill after real use | `workflows/iterate-on-skill.md` |
| Classify new content (rule vs. workflow vs. reference) | `workflows/iterate-on-skill.md` (Step 3) |
| Review a skill for quality issues | `workflows/create-new-skill.md` → Step 5 |
| Package a finished skill for distribution | `workflows/create-new-skill.md` → Step 7 |
| **Other / unlisted task** | Default to `workflows/create-new-skill.md`, jumping to the relevant step |

Workflows link to the per-topic references below as needed.

## Reference Index

Files marked **(always read)** are loaded above. The rest load on demand from workflows:

- `rules/core-principles.md` — **(always read)** Concise, push-off-defaults, degrees-of-freedom, avoid-railroading.
- `rules/authoring.md` — **(always read)** Frontmatter, imperative form, exclusions, no-duplication, reference-every-file.
- `rules/context-engineering.md` — **(always read)** Context allocation strategies, signal-to-noise tests, anti-patterns.
- `references/skill-anatomy.md` — **(always read)** Folder structure, file types, and when to split `references/` into `rules/` + `workflows/` + `references/`.
- `references/progressive-disclosure.md` — **(always read)** Three-level loading system and general guidelines.
- `references/writing-effective-instructions.md` — **(always read)** Prompt engineering playbook for SKILL.md body (imperative form, examples, edge cases, anti-patterns).
- `references/output-patterns.md` — Read when the skill produces structured output (templates, schemas, examples).
- `references/progressive-disclosure-patterns.md` — Read when slicing a large skill across multiple files.
- `references/workflow-patterns.md` — Read when the skill has multi-step procedures (sequential, conditional, loops).
- `references/common-patterns.md` — Read when adding gotchas, first-run configuration, or persistent data across sessions.

## Scripts

- `scripts/init_skill.py <skill-name> --path <output-directory>` — Generate a new skill template with frontmatter and example directories.
- `scripts/package_skill.py <path/to/skill-folder> [output-directory]` — Validate and package a skill into a distributable `.skill` file.
- `scripts/quick_validate.py` — Standalone structural validation (used by `package_skill.py`; can be run directly).

## Gotchas

- **Unreferenced files are invisible** — A file in `references/`, `rules/`, or `workflows/` that isn't named in SKILL.md (or in a workflow that loads it) will never be read. Add an index entry with *what* and *when*.
- **Never mix content shapes in one directory** — Imperative constraints go in `rules/`, ordered procedures in `workflows/`, descriptive material in `references/`. Not every skill needs all three, but when a content type is present, it goes in the matching directory.
- **Returning to the same skill mid-session doesn't re-trigger routing** — On follow-up tasks in the same conversation, Claude may skip re-reading SKILL.md and act on stale context. If a new task arrives, re-enter through SKILL.md and re-route.
