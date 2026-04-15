---
name: write-design-system
description: "Create or maintain design system documentation — tokens, visual conventions, component patterns. Triggers: 'design system', 'design tokens', 'color palette', 'typography scale', 'UI feels inconsistent', 'visual style'."
---

# Write Design System

## Process

1. Pick a workflow from the table below.
2. Read the corresponding workflow file in `workflows/`.
3. Follow the workflow's steps end to end — each one terminates by generating the preview (see [Output](#output)) and presenting both files.

### Pick a Workflow

| Situation | Workflow |
|---|---|
| `DESIGN.md` already exists at the project root | **Update** — [workflows/update.md](workflows/update.md) |
| User names a public reference product (Linear, Vercel, Stripe, etc.) | **Reference** — [workflows/reference.md](workflows/reference.md) |
| New project, little or no frontend code | **Create** — [workflows/create.md](workflows/create.md) |
| Existing project with scattered or informal styling | **Establish** — [workflows/establish.md](workflows/establish.md) |
| Existing project with well-defined theme/token files | **Document** — [workflows/document.md](workflows/document.md) |

If intent is unclear, ask: "Is this a new project where we're defining the visual direction, do you have a reference product in mind to adapt, or does the codebase already have UI code?"

## Output

The canonical output is `DESIGN.md` at the project root — a sibling to `AGENTS.md` / `CLAUDE.md`. This convention (introduced by Google Stitch and adopted by Cursor, Copilot, and other AI coding tools) ensures any agent automatically picks it up. Format adapts the [Stitch DESIGN.md format](https://stitch.withgoogle.com/docs/design-md/format/) and the conventions of [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md).

After drafting `DESIGN.md`, generate the visual preview catalog:

```bash
uv run --script ${CLAUDE_PLUGIN_ROOT}/skills/write-design-system/scripts/generate-preview.py DESIGN.md
```

This emits `DESIGN-preview.html` next to `DESIGN.md` — a self-contained file showing color swatches, type scale, spacing, and radius tokens with a light/dark surface toggle. Open it in a browser to verify the system before sharing with stakeholders. Present both `DESIGN.md` and `DESIGN-preview.html` to the user.

## References

### Workflows

Read the one matched in [Pick a Workflow](#pick-a-workflow) above. Each workflow is self-contained and references the guides and examples below as needed.

- [workflows/create.md](workflows/create.md) — Multi-round design consultation followed by token derivation and drafting. Read when starting from scratch on a new project.
- [workflows/establish.md](workflows/establish.md) — Codebase audit, consultation informed by findings, token consolidation. Read when an existing project has inconsistent or informal styling.
- [workflows/document.md](workflows/document.md) — Extract existing tokens and patterns from a well-structured codebase. Read when the project already has a clear design system in code.
- [workflows/reference.md](workflows/reference.md) — Adapt a known public design system by deltas. Read when the user has a clear reference product in mind.
- [workflows/update.md](workflows/update.md) — Revise specific sections of an existing `DESIGN.md`. Read when `DESIGN.md` already exists at the project root.

### Guides

- [discovery-guide.md](references/discovery-guide.md) — Five-track discovery framework with question banks, Aaker's brand personality dimensions, vibe-to-tokens heuristics, and product type matrix. Read during the consultation phase of Create and Establish.
- [token-derivation-guide.md](references/token-derivation-guide.md) — Systematic token derivation: color (3-layer architecture), typography (modular scales), spacing, radius, shadows, motion, and the shadcn reference token set. Read when generating or proposing token values.
- [design-system-template.md](references/design-system-template.md) — Output template for the `DESIGN.md` document. Concrete values, evocative names, per-variant recipes, do's and don'ts, Agent Prompt Guide. Read when drafting.

### Examples

Concrete reference `DESIGN.md` files showing the expected prose voice, recipe density, and section thickness. **Read at least one before drafting** — pick the one whose product type roughly matches the user's. All are MIT-licensed adaptations from [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md).

| File | Archetype | Best for |
|---|---|---|
| [examples/linear.md](references/examples/linear.md) | Dense, dark, technical, achromatic + indigo accent | Developer tools, dashboards, dark B2B |
| [examples/vercel.md](references/examples/vercel.md) | Clean, light, restrained, monochrome | Marketing sites, infrastructure, minimalist light UIs |
| [examples/stripe.md](references/examples/stripe.md) | Chromatic gradients + fintech polish, weight-300 elegance | Fintech, API products, brand-forward marketing |
| [examples/notion.md](references/examples/notion.md) | Warm minimalism, serif headings, soft surfaces | Productivity, content, writing-oriented products |
| [examples/apple.md](references/examples/apple.md) | Premium spacious editorial, SF Pro, full-bleed imagery | Hardware, consumer, brand sites with negative space |
| [examples/spotify.md](references/examples/spotify.md) | Vibrant green on dark, bold type, media-driven | Consumer media, entertainment, content-rich UIs |

## Gotchas

- **`DESIGN.md` lives at the project root, not in `docs/` or `.claude/`** — the Stitch convention relies on agents finding it beside `AGENTS.md` / `CLAUDE.md`. Placing it elsewhere breaks auto-discovery.
- **Regenerate the preview after any token change** — `DESIGN-preview.html` is a static render, not a live view. Stale previews mislead stakeholders reviewing the document.
- **Read at least one file from `references/examples/` before drafting** — the examples set the expected prose voice and recipe density. Skipping this step produces generic, abstract output that doesn't reproduce reliably.
- **Don't fabricate token values in the Document workflow** — every token must trace to a specific file in the codebase. Inferring "reasonable" values silently invents a system that doesn't exist.
- **Component recipes must spell out every property per variant** — bg, text, padding, radius, border, shadow, font, hover, focus. Abstract guidance ("use the primary color") does not reproduce across generations; concrete recipes do.

## Edge Cases

If the user's aesthetic preferences conflict with accessibility requirements:
  → Accessibility wins. Propose the closest accessible alternative and explain the constraint.

If the user wants to use a specific component library:
  → Align token names and values with the library's theming API. Note how to configure the tokens.

If the project has no frontend code and the user has no strong preferences:
  → Make opinionated recommendations based on product type defaults from [discovery-guide.md](references/discovery-guide.md). Explain the reasoning.

If the codebase uses multiple styling approaches (e.g., Tailwind + CSS modules):
  → Document both. Note which is used where. Recommend consolidation if appropriate.

If the user only wants part of the design system (e.g., "just colors"):
  → Deliver what's requested. Note dependencies: "the color palette pairs with typography choices — want me to cover that too?"

This skill produces a reference document — it does not modify codebase styling or configuration files.
