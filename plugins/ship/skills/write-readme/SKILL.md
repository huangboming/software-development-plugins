---
name: write-readme
description: "Write, generate, or update a README for a project or library. Triggers: 'write a README', 'create a README', 'generate a README', 'update the README', 'document this project', '/write-readme'."
---

# README Writer

A README is for **users**, not maintainers. Front-load what they need to act; link out for everything else.

## Type — pick before drafting

- **Project** (deployed app, service, CLI): What it does → screenshot/demo → install → run → configure.
- **Library** (installed as dependency): Tagline → install → minimal example → API summary → links.
- **Monorepo:** project-style root, library-style per package. If ambiguous, ask.

## Workflow

1. If `README.md` exists and is non-trivial (≥20 lines), **update** — preserve voice, structure, and ordering; edit in place.
2. Otherwise **generate** from the codebase: manifests, entry points, scripts, public API surface.
3. Verify every command and path you write actually exists.

## Hard rules

- No architecture, internals, or contributor docs in a README. If asked, link to `docs/` instead.
- Never invent badges, install commands, or examples that aren't grounded in the repo.
- If the project has no code yet, write a minimal README (name, one-line goal, "Coming Soon") and stop.
