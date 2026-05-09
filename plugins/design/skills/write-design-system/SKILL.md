---
name: write-design-system
description: "Create `DESIGN.md` — design tokens, component recipes, do's and don'ts. Triggers: 'design system', 'design tokens', 'color palette', 'typography scale', 'visual style'."
---

## Process

1. **Halt if `DESIGN.md` exists at the project root.** Tell the user: "DESIGN.md already exists. Edit it directly, or delete it to regenerate."
2. **Confirm inputs.** Need alignment output from `define:grill-me` or existing UI code to audit. If neither, halt and ask the user to run `/define:grill-me` first.
3. **Read [`references/template.md`](references/template.md).**
4. **Draft `DESIGN.md` at the project root.** Fill every section with concrete values, verifying WCAG AA (4.5:1 normal text, 3:1 large/UI) on every text/background pairing. If auditing existing UI code, anchor each token to what it consolidates (e.g., "primary-600 consolidates the 4 in-use blues").

## Hard constraints

- **`DESIGN.md` lives at the project root** — sibling to `AGENTS.md` / `CLAUDE.md` / `README.md`. Stitch auto-discovery convention. Never `docs/`, `.claude/`, or `.product/`.
- **Agent-facing prompt context, not human documentation.** Concrete hex values + per-variant recipes + explicit Don'ts. Abstract guidance ("use the primary color") doesn't reproduce across generations.
- **Don't fabricate tokens.** When auditing existing code, every documented token must trace to a specific file. Inferring "reasonable" values silently invents a system that doesn't exist.
