# Document Workflow

Extract and document an existing well-structured design system from the codebase.

## Steps

1. Extract tokens and patterns
2. Draft `DESIGN.md`
3. Generate preview, verify, and present

## Step 1: Extract

Explore the codebase for design system artifacts:

- **Token sources** — Theme files, CSS custom properties, Tailwind config, styled-components themes, design token JSON/YAML files.
- **Color tokens** — Primitive palette values and semantic mappings. Note light/dark mode handling.
- **Typography** — Font families, size scale, weight usage, line heights.
- **Spacing** — Base unit and scale values.
- **Layout** — Breakpoints, grid system, container widths.
- **Border radius** — Default value and variants.
- **Shadows** — Elevation scale.
- **Motion** — Duration and easing values, reduced-motion support.
- **Component patterns** — Recurring styling conventions (button variants, card treatments, form styles, interactive states).

Ground every finding in specific file paths.

## Step 2: Draft

Read [design-system-template.md](../references/design-system-template.md). Then read at least one file from [examples/](../references/examples/) to internalize prose voice and recipe density — pick the example whose aesthetic matches the codebase (the table in [SKILL.md](../SKILL.md#examples) shows which fits which archetype).

Create `DESIGN.md` at the project root following the template. Key drafting moves:

1. **Visual Theme & Atmosphere** — 2-3 paragraphs of evocative prose describing the *feel* of the existing system. Ground it in what you observed in the codebase (canvas, typographic voice, color restraint, structural moves). Add a "Key Characteristics" bullet list of 6-10 signature elements actually present in the code.
2. **Design Principles** — 3-5 principles inferred from the codebase patterns.
3. **Core token sections** — fill each section with extracted values. Reference source files. Pair systematic token names with evocative aliases where the codebase uses them.
4. **Component Recipes** — per-variant recipes documenting what actually exists in the components. Spell out every property (bg, text, padding, radius, border, shadow, font, hover, focus).
5. **Do's and Don'ts** — concrete rules tied to specific values, inferred from patterns the codebase consistently follows or avoids.
6. **Agent Prompt Guide** — quick color reference, 5-8 example component prompts that demonstrate the actual system, numbered Iteration Guide.
7. Omit template sections that don't apply.
8. Set "Last updated" to today's date.

## Step 3: Generate Preview, Verify, and Present

Generate the visual preview (see [SKILL.md → Output](../SKILL.md#output) for the command).

Verify against this checklist:

- Every documented token is traceable to a specific file in the codebase.
- No fabricated values — only document what actually exists.
- Token names match what the codebase uses.
- Dark mode mappings documented if present.
- `DESIGN-preview.html` renders the extracted colors and type scale.

Present `DESIGN.md` and `DESIGN-preview.html` together. Ask if any sections need clarification or expansion.
