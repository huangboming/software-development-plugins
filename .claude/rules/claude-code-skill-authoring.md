---
paths:
  - "plugins/**/skills/**/SKILL.md"
  - "**/skills/**/references/**/*.md"
---

# Claude Code Skill Authoring

One skill per directory at `plugins/<plugin>/skills/<skill-name>/SKILL.md`. Optional siblings: `references/` (loaded on demand), `scripts/` (executed by the skill), `assets/` (static files).

## Frontmatter

Required: `name`, `description`. Optional: `model`, `license`.

- `name` — lowercase-kebab-case, matches the directory name.
- `description` — the auto-invocation signal. Claude routes to the skill by matching user intent against this text. Treat it as search-indexable, not marketing copy.

## Writing the description

- Open with one imperative sentence stating what the skill produces or does. No filler, no "This skill...".
- Follow with an explicit `Triggers:` list of quoted phrases a user would actually say, plus the slash-command form.
- Cover at least three phrasings. Phrases not in `description` won't fire the skill.
- Example: `"Generate product-level or feature-level PRDs. Triggers: 'write a PRD', 'create a product spec', 'spec out this feature', '/write-prd'."`

## Keep SKILL.md concise

- SKILL.md loads into every matching session. Every line costs context tokens.
- Treat the body as a router: state the process in a few steps, link to references/workflows for depth.
- Push templates, long examples, edge-case catalogs, and domain reference material into `references/<topic>.md`. In SKILL.md, name each file with *what* it covers and *when* to read it.
- Unreferenced files in `references/` are invisible — Claude only reads what SKILL.md advertises.

## Choose the right degree of freedom

Match enforcement to task fragility:

- **Prose instructions** — judgment-heavy tasks with many valid outputs (PRD drafting, architecture review).
- **Numbered steps / pseudocode** — procedures where order and completeness matter (release cutting, migration workflows).
- **Fixed scripts** — deterministic operations where creativity is a bug (template scaffolding, structural validation).

Prefer less freedom when in doubt. Over-specifying a judgment task narrows the model; under-specifying a mechanical task lets it drift.

## Naming prefixes

Pick the prefix that matches user intent, not implementation:

- `write-` — generates an artifact (`write-prd`, `write-readme`, `write-changelog`).
- `guard-` — enforces quality on existing code (`guard-test`, `guard-boundary`).
- `review-` — audits or evaluates (`review-code`, `review-backlog`).
- `create-` — concrete lifecycle operation producing a thing (`create-pr`, `create-hook`).
- `tag-`, `cleanup-`, `intake-` — other concrete verbs. One skill per verb.

Prefix predictability is how users discover skills via trigger phrases — match the house style when adding new skills.

## Content shape separation

Always separate bundled content by shape: imperative constraints in `rules/`, ordered procedures in `workflows/`, descriptive material in `references/`. Not every skill needs all three directories, but when a content type is present, it goes in the matching directory. Never mix content shapes in a single directory.


## Never

- Never duplicate a skill's procedure inside a wrapping agent — the agent should delegate via its `skills:` field.
- Never put session-specific or ephemeral content in SKILL.md. Decaying guidance belongs in `references/` or gets deleted.
- Never use emojis in frontmatter or body unless the user explicitly asks.
- Never list a reference file in SKILL.md that doesn't exist, and never leave an existing `references/` file unlisted.
