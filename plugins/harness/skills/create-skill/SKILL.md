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

Before any skill-creation or iteration task, read both files in `rules/`:

1. `rules/core-principles.md` — concise, push-off-defaults, degrees-of-freedom, avoid-railroading
2. `rules/authoring.md` — frontmatter, imperative form, exclusions, no-duplication, reference-every-file

## Common Tasks

| Task | Workflow |
|------|----------|
| Create a new skill from scratch | `workflows/create-new-skill.md` |
| Iterate on an existing skill after real use | `workflows/iterate-on-skill.md` |
| Classify new content (rule vs. workflow vs. reference) | `workflows/iterate-on-skill.md` (Step 3) |
| Package a finished skill for distribution | `workflows/create-new-skill.md` → Step 5 |
| **Other / unlisted task** | Default to `workflows/create-new-skill.md`, jumping to the relevant step |

Workflows link to the per-topic references below as needed.

## Reference Index

Consult these based on the sub-problem at hand:

- `references/skill-anatomy.md` — Folder structure, file types, and when to split `references/` into `rules/` + `workflows/` + `references/`.
- `references/progressive-disclosure.md` — Three-level loading system and general guidelines.
- `references/progressive-disclosure-patterns.md` — Three worked patterns for slicing a large skill across files.
- `references/context-engineering.md` — Strategies for allocating content across SKILL.md, references, scripts, assets.
- `references/writing-effective-instructions.md` — Prompt engineering playbook for SKILL.md body (imperative form, examples, edge cases, anti-patterns).
- `references/workflow-patterns.md` — Sequential, conditional, decision-loop, and self-correction patterns for multi-step processes.
- `references/output-patterns.md` — Template, example, structured-data, and argument patterns.
- `references/common-patterns.md` — Gotchas section, first-run configuration, persistent data across sessions.

## Scripts

- `scripts/init_skill.py <skill-name> --path <output-directory>` — Generate a new skill template with frontmatter and example directories.
- `scripts/package_skill.py <path/to/skill-folder> [output-directory]` — Validate and package a skill into a distributable `.skill` file.
- `scripts/quick_validate.py` — Standalone structural validation (used by `package_skill.py`; can be run directly).

## Gotchas

- **Unreferenced files are invisible** — A file in `references/`, `rules/`, or `workflows/` that isn't named in SKILL.md (or in a workflow that loads it) will never be read. Add an index entry with *what* and *when*.
- **Splitting too early hurts more than it helps** — For small skills, a flat `references/` is fine. Split into `rules/` + `workflows/` only when a flat directory starts mixing content shapes or Claude loads the wrong file.
- **Returning to the same skill mid-session doesn't re-trigger routing** — On follow-up tasks in the same conversation, Claude may skip re-reading SKILL.md and act on stale context. If a new task arrives, re-enter through SKILL.md and re-route.
