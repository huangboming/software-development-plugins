---
name: create-design-md
description: "Create or migrate root `DESIGN.md` using the DESIGN.md format. Triggers: '/create-design-md', 'create DESIGN.md', 'write DESIGN.md', 'migrate DESIGN.md', 'update DESIGN.md format'."
---

Create or migrate only the root `DESIGN.md` artifact. Read implementation files as evidence when useful, but do not edit app code, CSS, Tailwind/theme config, token JSON, Figma exports, or any file other than `DESIGN.md`.

## Reference

- `references/template.md` — strict DESIGN.md skeleton, minimum token set, section order, and compliance checklist. Read before creating or migrating `DESIGN.md`.

## Process

1. **Locate root `DESIGN.md`.** It must live at the project root, sibling to `AGENTS.md` / `CLAUDE.md` / `README.md`; never `docs/`, `.claude/`, or `.product/`.
2. **Classify the source.** Use audit mode when UI/theme/token files exist; otherwise use greenfield mode from product docs or user-provided brand direction. If greenfield context is insufficient, ask this compact intake: product name/audience, desired personality, light/dark preference, existing colors/fonts, UI density, dislikes/constraints.
3. **Handle existing files safely.** If `DESIGN.md` exists, assess compliance first. If already compliant, report that and offer targeted edits. If non-compliant, present a migration plan and wait for approval before rewriting; preserve usable content in standard sections.
4. **Read the template.** Follow `references/template.md` exactly: YAML frontmatter, one optional H1, then all 8 standard `##` sections in order.
5. **Write or migrate `DESIGN.md`.** Make the source explicit in `## Overview`: audited from named files, or proposed greenfield from named inputs. In audit mode, token/component choices must trace to files; in greenfield mode, label them as proposed.
6. **Run the compliance checklist** from the template before finishing.

## Hard constraints

- Require YAML frontmatter with `version: alpha`, `name`, and token groups for `colors`, `typography`, `rounded`, `spacing`, and `components`.
- Use only standard body sections: `Overview`, `Colors`, `Typography`, `Layout`, `Elevation & Depth`, `Shapes`, `Components`, `Do's and Don'ts`.
- Always generate all 8 sections, even when a section states that a style mechanism is intentionally not used.
- Use semantic flat color tokens as the required minimum; add palette ramps only when useful or audited.
- Verify WCAG AA for key foreground/background pairings: 4.5:1 normal text, 3:1 large text and UI components.
