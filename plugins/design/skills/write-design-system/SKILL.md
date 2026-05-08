---
name: write-design-system
description: "Create or maintain design system documentation — tokens, visual conventions, component patterns. Triggers: 'design system', 'design tokens', 'color palette', 'typography scale', 'UI feels inconsistent', 'visual style'."
---

# Write Design System

## Process

1. Pick a workflow from the table below.
2. Read the corresponding workflow file in `workflows/`.
3. Follow it end to end. Every workflow finishes by generating the preview (see [Output](#output)) and presenting both files.

| Situation | Workflow |
|---|---|
| `DESIGN.md` already exists at the project root | [workflows/update.md](workflows/update.md) |
| User names a public reference product (Linear, Vercel, Stripe, etc.) | [workflows/reference.md](workflows/reference.md) |
| New project, little or no frontend code | [workflows/create.md](workflows/create.md) |
| Existing project with scattered or informal styling | [workflows/establish.md](workflows/establish.md) |
| Existing project with well-defined theme/token files | [workflows/document.md](workflows/document.md) |

If intent is unclear, ask: "Is this a new project where we're defining the visual direction, do you have a reference product in mind to adapt, or does the codebase already have UI code?"

## Output

The canonical output is `DESIGN.md` at the project root — sibling to `AGENTS.md` / `CLAUDE.md`. Format adapts the [Stitch DESIGN.md format](https://stitch.withgoogle.com/docs/design-md/format/).

After drafting, generate the visual preview:

```bash
uv run --script ${CLAUDE_PLUGIN_ROOT}/skills/write-design-system/scripts/generate-preview.py DESIGN.md
```

Emits `DESIGN-preview.html` next to `DESIGN.md`. Present both files.

## Reference

- [references/design-system-template.md](references/design-system-template.md) — output template for `DESIGN.md`: concrete values, per-variant recipes, do's and don'ts, Agent Prompt Guide. Read before drafting in any workflow.

## Gotchas

- **`DESIGN.md` lives at project root, not in `docs/` or `.claude/`** — placing it elsewhere breaks the Stitch auto-discovery convention.
- **Regenerate the preview after any token change** — `DESIGN-preview.html` is a static render. Stale previews mislead stakeholders.
- **Don't fabricate tokens in the Document workflow** — every token must trace to a specific file. Inferring "reasonable" values silently invents a system that doesn't exist.
- **Component recipes spell out every property per variant** — bg, text, padding, radius, border, shadow, hover, focus. Abstract guidance ("use the primary color") does not reproduce across generations.

## Edge cases

- **Aesthetic preference conflicts with accessibility** — accessibility wins. Propose the closest accessible alternative and explain the constraint.
- **User wants a specific component library** — align token names and values with the library's theming API.
- **No frontend code and no preferences** — make opinionated recommendations based on product type and explain reasoning.
- **Multiple styling approaches in codebase** (e.g., Tailwind + CSS modules) — document both, note which is used where.
- **User only wants part of the system** (e.g., "just colors") — deliver what's requested; flag dependencies.

This skill produces a reference document — it does not modify codebase styling or configuration files.
