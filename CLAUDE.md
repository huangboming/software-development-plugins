# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A **Claude Code plugin marketplace** — a collection of 8 plugins (`define`, `design`, `build`, `verify`, `ship`, `docs`, `harness`, `misc`) that guide agents through the software product lifecycle. There is no application code to run; authored artifacts are Markdown skills and agents consumed by Claude Code itself.

## Repository layout

- `.claude-plugin/marketplace.json` — root marketplace manifest registering each plugin (name + source path).
- `plugins/<plugin>/.claude-plugin/plugin.json` — per-plugin manifest.
- `plugins/<plugin>/skills/<skill-name>/SKILL.md` — one skill per directory; may include `references/` (loaded on demand) and `scripts/` (executed by the skill).
- `plugins/<plugin>/agents/<agent>.md` — one agent per file, invoked via the `Task` tool.
- `.claude/hooks/validate-plugins.py` — `Stop` hook that runs `claude plugin validate` on every plugin listed in `marketplace.json`. Runs automatically at end of turn.
- `settings/` — standalone artifacts (example `settings.json`, `user-CLAUDE.md`) not wired into runtime; reference material only.

## Validation

Validate a single plugin:

```bash
claude plugin validate plugins/<plugin>
```
