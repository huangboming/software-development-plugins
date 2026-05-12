# Developer Guidelines

## Overview

A Claude Code plugin marketplace. Six plugins (`define`, `design`, `build`, `ship`, `harness`, `misc`) cover the software product loop, each shipping skills (auto-invoked playbooks) and agents (task-scoped subagents).

## Commands

| Task | Command |
|---|---|
| Validate a plugin | `claude plugin validate plugins/<name>` |

## Code Quality

- Skills live at `plugins/<plugin>/skills/<skill-name>/SKILL.md`. Agents at `plugins/<plugin>/agents/<agent>.md`.
- A skill's `description` frontmatter is the auto-invocation signal — list concrete trigger phrases users would actually say.
- No H1 title in `SKILL.md`. The `name` frontmatter already identifies the skill — a `# Title` line right after frontmatter is duplicate ceremony. Start the body with prose or the first `##` section.
- Naming: `write-*` for generators, `guard-*` / `review-*` for quality checks, concrete verbs (`create-*`, `tag-*`, `cleanup-*`) for operations.
- Canonical reference for authoring skills: [`plugins/harness/skills/create-skill/SKILL.md`](plugins/harness/skills/create-skill/SKILL.md).

## Versioning

Each plugin tracks its own `version` in `plugins/<plugin>/.claude-plugin/plugin.json`. Bump on any user-visible behavior change — new skill, renamed skill/agent, changed trigger phrases, removed artifact. Versions are independent per plugin; never share or reuse across plugins.

## Commit

Conventional Commits, scoped by plugin: `feat(define): …`, `refactor(ship): …`, `chore: …` for cross-cutting changes.

## Pull Requests

Title ≤72 chars, conventional-commit style. Body sections: **Summary** · **Problem** · **Proposed Solution** · **Key Changes**.

## Gotchas / Don'ts

- The filesystem and `.claude-plugin/marketplace.json` must move together in one commit. A plugin directory present on disk but missing from the manifest is invisible to Claude Code; an orphaned manifest entry can break loading for every plugin listed after it.
- After any structural change (new/renamed/removed skill, agent, or plugin; manifest edit), run `claude plugin validate plugins/<name>` and read the output — do not assume success.
- Renames are the most common source of silent breakage. When renaming a plugin: rename on disk → update `plugin.json` `name` → update both `name` and `source` in `marketplace.json` → bump `version` → validate.
- Don't add unknown top-level keys to `marketplace.json` or `plugin.json` — unrecognized fields are ignored at best, rejected at worst.
