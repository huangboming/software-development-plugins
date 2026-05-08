# Establish Workflow

Audit an existing project with inconsistent styling, consult on intended direction, and propose a unified design system to refactor toward.

## Steps

1. Audit the codebase
2. Present findings
3. Run discovery consultation
4. Derive token values with consolidation notes
5. Draft `DESIGN.md`
6. Generate preview, verify, and present

## Step 1: Audit the Codebase

Use the `explorer` agent to inventory existing visual patterns:

- **Colors** — Scan CSS, theme files, Tailwind config, styled-components for all color values. Count distinct values per category (e.g., "15 distinct grays, 8 blues, 4 reds").
- **Typography** — List font families, sizes, weights, and line heights in use. Count distinct combinations.
- **Spacing** — Catalog padding, margin, and gap values. Identify whether a base unit exists or values are arbitrary.
- **Border radius** — List all radius values and which components use them.
- **Shadows** — List distinct shadow values.
- **Component patterns** — Note recurring button styles, card treatments, form input conventions, hover/focus states.

Score inconsistencies by visibility and frequency — not all inconsistencies matter equally.

## Step 2: Present Findings

Summarize the audit for the user:

- Total distinct values per category (colors, spacing, fonts, radii).
- The most-used values (likely intentional).
- Clear inconsistencies (e.g., "7 different grays where 3-4 would suffice").
- What's working well (patterns that are already consistent).
- Accessibility violations if found (contrast failures, missing focus states).

## Step 3: Discovery Consultation

Run the same multiple-choice consultation rounds as the Create workflow, but informed by audit results. Add a track of audit-driven questions using audit findings to populate the options.

Key differences from Create:

- Present audit findings as keep/replace choices (Q18) — users react to concrete options.
- Ask which frequently-used colors are intentional brand choices vs. drift (Q19).
- Ask which existing components or pages are the "gold standard" (Q20 — open-ended).

## Step 4: Derive Token Values

Follow the same derivation process as Create, with one addition:

For each proposed token, note which existing values it replaces or consolidates. Example: "primary-600 (#2563eb) consolidates the 4 blues currently in use: #2563eb, #2564ec, #3b82f6, #1d4ed8."

Anchor proposals in what the codebase already uses — consolidate rather than replace wholesale. Propose changes only where the audit revealed clear problems.

## Step 5: Draft

Read [design-system-template.md](../references/design-system-template.md). Create `DESIGN.md` at the project root following it. Key drafting moves:

1. **Visual Theme & Atmosphere** — 2-3 paragraphs of evocative prose grounded in both discovery findings and the audit. Describe how this system relates to the existing codebase. Add a "Key Characteristics" bullet list of 6-10 signature elements.
2. **Design Principles** — 3-5 principles with rationale tied to both discovery and audit findings.
3. **Core token sections** (Color, Typography, Spacing, Radius, Elevation, Motion) — fill every section with specific values. For each token, note which existing values it maps to or replaces. Pair systematic names with evocative aliases where they help.
4. **Component Recipes** — per-variant recipes with every property spelled out. Where existing components are kept, document their actual current state; where they're being consolidated, document the target.
5. **Do's and Don'ts** — concrete rules tied to specific values. Include don'ts for the legacy patterns being phased out.
6. **Agent Prompt Guide** — quick color reference, 5-8 example component prompts, numbered Iteration Guide.
7. Set "Last updated" to today's date.

## Step 6: Generate Preview, Verify, and Present

Generate the visual preview (see [SKILL.md → Output](../SKILL.md#output) for the command).

Apply the [Create workflow's verification checklist](create.md#step-4-generate-preview-verify-and-present), plus these establish-specific items:

- Every proposed token has a clear mapping to existing values it replaces.
- Consolidation choices are explained (why these 4 blues become 1).
- The system preserves patterns the user said are working well.

Present `DESIGN.md` and `DESIGN-preview.html` together. Highlight the key changes from the current state and ask for feedback.
