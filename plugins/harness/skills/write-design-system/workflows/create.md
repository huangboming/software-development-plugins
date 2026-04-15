# Create Workflow

Design a complete design system from scratch for a new project through multi-round consultation.

## Steps

1. Run discovery consultation
2. Derive token values
3. Draft `DESIGN.md`
4. Generate preview, verify, and present

## Step 1: Discovery Consultation

Read [discovery-guide.md](../references/discovery-guide.md) for question banks, brand personality framework, and product type matrix.

Act as a design consultant. Present multiple-choice options for every question — users react to curated options far more easily than generating answers from scratch. Ask 2-4 questions per round, building on previous answers.

**Round structure:**

1. **Product context and audience** (Q1-Q5) — Product description (open-ended), user archetype, user mindset, voluntary vs required, session pattern.
2. **Brand personality and references** (Q6-Q8) — Product-as-person archetype, admired products (curated list, pick 2-3), word-pair selections.
3. **Content and interaction model** (Q9-Q11) — Content types (multi-select checklist), information density level, primary interaction mode.
4. **Technical constraints** (Q12-Q17) — Framework, styling approach, component library, dark mode, accessibility target, platforms.

Map responses to Aaker brand personality dimensions and the product type matrix to set initial design parameter ranges.

Transition to Step 2 when product context, brand personality, content model, and technical constraints are clear. Remaining unknowns become assumptions stated in the document's Design Principles section.

## Step 2: Derive Token Values

Read [token-derivation-guide.md](../references/token-derivation-guide.md) for derivation methods and reference token sets.

Translate discovery findings into specific token values:

1. **Color** — Select brand hue → assign as 500/600 → generate primitive palette (50-950) → assign semantic tokens (light + dark) → verify contrast (WCAG AA: 4.5:1 normal text, 3:1 large text).
2. **Typography** — Match product character to modular scale ratio → generate scale from 16px base → assign semantic type roles → select font families (1-2 maximum).
3. **Spacing** — Select base unit (4px for dense, 8px for standard) → generate scale → assign semantic names.
4. **Border radius** — Select single default value matching personality position.
5. **Elevation** — Define shadow depth scale (sm through xl) → plan dark mode strategy (surface lightness shifts).
6. **Motion** — Define duration and easing tokens → include `prefers-reduced-motion` fallback (all durations to 0ms).

Every recommendation needs a rationale tied to the discovery conversation.

## Step 3: Draft

Read [design-system-template.md](../references/design-system-template.md) for the output template. Then read at least one file from [examples/](../references/examples/) to internalize prose voice and recipe density — pick the example whose product type matches the user's (the table in [SKILL.md](../SKILL.md#examples) shows which fits which archetype).

Create `DESIGN.md` at the project root following the template. Key drafting moves:

1. **Visual Theme & Atmosphere** — 2-3 paragraphs of evocative prose grounded in discovery findings, then a "Key Characteristics" bullet list of 6-10 non-negotiable signature elements. This section is what lets an agent make borderline judgement calls — make it specific and value-bearing, not generic.
2. **Design Principles** — 3-5 principles with rationale tied to discovery findings.
3. **Core token sections** (Color, Typography, Spacing, Radius, Elevation, Motion) — fill every section with specific values. Pair systematic token names with evocative aliases where they help anchor the agent (e.g. *Brand Indigo*, *Marketing Black*).
4. **Component Recipes** — write per-variant recipes for buttons, inputs, cards, and any other components the system distinguishes. Spell out every property (bg, text, padding, radius, border, shadow, font, hover, focus). Recipes reproduce reliably; abstract guidance doesn't.
5. **Do's and Don'ts** — concrete rules tied to specific values. Don'ts in particular preserve identity across many generations (e.g. "Don't use pure white #ffffff — use foreground #f7f8f8").
6. **Agent Prompt Guide** — quick color reference cheat sheet, 5-8 ready-to-paste example component prompts, and a numbered Iteration Guide of 5-7 must-follow rules.
7. Set "Last updated" to today's date.

## Step 4: Generate Preview, Verify, and Present

Generate the visual preview (see [SKILL.md → Output](../SKILL.md#output) for the command).

Verify against this checklist before presenting:

- Every core token category (color, typography, spacing, radius, shadows, motion) has specific values.
- Color uses three layers (primitive → semantic → component).
- Semantic color tokens include both light and dark mappings.
- All text/background pairings meet WCAG AA contrast.
- Typography scale follows a consistent mathematical ratio.
- Spacing scale follows a consistent progression from a single base unit.
- Border radius uses one default applied consistently.
- Motion tokens include a `prefers-reduced-motion` fallback.
- **Visual Theme & Atmosphere** is concrete prose with specific values, not generic filler.
- **Key Characteristics** lists 6-10 non-negotiable signature elements.
- **Component Recipes** spell out every property per variant — no abstract guidance.
- **Do's and Don'ts** are concrete rules tied to values, not principles.
- **Agent Prompt Guide** has a quick color reference, 5+ example prompts, and an Iteration Guide.
- `DESIGN-preview.html` exists and renders the colors and type scale (open it to confirm).

Present `DESIGN.md` and `DESIGN-preview.html` together and ask for feedback.
