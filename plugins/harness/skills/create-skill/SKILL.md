---
name: create-skill
description: "Create or update a Claude Code skill. Triggers: 'create a skill', 'write a skill', 'add a skill for...', 'turn this into a skill', '/create-skill'."
---

# Skill Creator

## Always read first

Before any skill-creation task, read both:

- `rules/core-principles.md` — radical minimalism, decay-vs-read test, write-skill purity, signal-to-noise tests, degrees of freedom.
- `references/skill-anatomy.md` — folder shape, frontmatter contract, loading model.

## Process

Follow `workflows/create-new-skill.md` end-to-end. Skip steps only when they manifestly don't apply (e.g., skipping init when iterating on an existing skill).

## Scripts

- `scripts/init_skill.py <skill-name> --path <output-directory>` — Generate a skill template with frontmatter and example directories.
- `scripts/package_skill.py <path/to/skill-folder> [output-directory]` — Validate and package a skill into a distributable `.skill` archive. Auto-runs `quick_validate.py`.
- `scripts/quick_validate.py <path/to/skill-folder>` — Standalone structural validator.

## Gotchas

- **Unreferenced files are invisible** — every file in `rules/`, `workflows/`, `references/`, `scripts/`, `assets/` must have an index entry in SKILL.md or in a workflow that loads it.
- **Never mix content shapes in one directory** — imperatives in `rules/`, ordered procedures in `workflows/`, descriptive material in `references/`.
- **Returning to a skill mid-session doesn't re-trigger routing** — if a new task arrives in the same conversation, re-read SKILL.md before acting; otherwise Claude may run on stale context.
