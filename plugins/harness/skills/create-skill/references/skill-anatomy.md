# Skill Anatomy

The non-derivable conventions for skill folder shape and frontmatter. Read on every authoring task.

## Folder layout

```
skill-name/
├── SKILL.md              required
├── rules/                imperative constraints — "you must do X"
├── workflows/            ordered procedures — "step 1, then 2, then 3"
├── references/           descriptive material — "X happens because Y"
├── scripts/              executable code (Python, Bash, etc.)
└── assets/               output templates, fonts, images
```

Not every skill needs every directory.

## SKILL.md frontmatter

Exactly two required fields:

```yaml
---
name: skill-name              # hyphen-case identifier, matches the directory name
description: One imperative sentence stating what the skill does or produces, plus concrete trigger phrases users would actually say.
---
```

Optional: `license: …` referencing a `LICENSE.txt` in the skill directory.

The `description` is the **trigger mechanism** — Claude reads it to decide whether to load the body. All "when to use" information goes here, not in the body. A `## When to Use This Skill` section inside the body is invisible to routing.

## Loading model (progressive disclosure)

Three tiers, paid in this order:

1. **Frontmatter** — loaded for every skill in the marketplace, every session. Cheapest tier; only `name` and `description` go here.
2. **SKILL.md body** — loaded when the skill triggers. Should contain only what's needed every time the skill fires.
3. **Bundled resources** (`rules/`, `workflows/`, `references/`) — loaded on demand from the body. Each file gets one index entry in SKILL.md naming *what* it contains and *when* to read it.

Scripts and assets cost zero context — they're executed or copied into output without being read into the window.
