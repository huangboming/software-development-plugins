# Design System Template

Template for `DESIGN.md` at the project root. This document is **agent-facing prompt context** — written to be read by AI coding agents that generate UI. Optimize accordingly:

- **Concrete values, not abstract guidance.** "Background `#08090a`" beats "use a dark surface."
- **Evocative aliases paired with systematic names.** *Marketing Black* / *Brand Indigo* anchor an LLM more than `primary-600`.
- **Per-variant component recipes.** Spell out every property — bg, text, padding, radius, border, shadow, font, hover, focus. Recipes reproduce reliably; abstract guidance doesn't.
- **Explicit Do's and Don'ts.** Don'ts are how you preserve identity across generations.
- **Ready-to-paste agent prompts.** The Agent Prompt Guide is what makes this doc executable.

Omit any section that doesn't apply.

````markdown
# Design System

> Last updated: <YYYY-MM-DD>

## 1. Visual Theme & Atmosphere

<2-3 paragraphs of evocative prose grounded in discovery findings or codebase audit — never generic filler. Describe: the canvas (light/dark, warm/cool, the *feeling* of the surface), the typographic voice (what type does at scale, what weights carry meaning), the role of color (chromatic or achromatic, how restrained), and the structural moves (borders, shadows, spacing rhythm) that distinguish this system from a generic theme.>

<Fold rationale for the major design choices into this prose — the tensions and priorities driving the system.>

### Key Characteristics

<6-10 non-negotiable signature elements. Each one line, concrete, value-bearing — the "if you only follow ten rules, follow these" anchors.>

- <e.g. Inter Variable with `"cv01", "ss03"` enabled globally>
- <e.g. Brand indigo `#5e6ad2` reserved for primary CTAs only — never decoration, never background>
- <e.g. 4px base spacing — most padding lands on 8/12/16, never 5/10/15>
- <e.g. Borders are 1px semi-transparent white `rgba(255,255,255,0.08)`, never solid dark colors>
- <e.g. Three weights total: 400 (read), 510 (emphasize), 590 (announce)>

## 2. Color

### Primitive Palette

<Raw color values — source of truth. Components MUST NOT reference primitives directly; they go through semantic tokens (next subsection).>

#### Brand
| Token | Value | Notes |
|-------|-------|-------|
| brand-50 | #<hex> | Lightest tint |
| brand-100 | #<hex> | Hover backgrounds |
| brand-500 | #<hex> | Mid-tone |
| brand-600 | #<hex> | **Default brand** — primary actions |
| brand-700 | #<hex> | Hover state |
| brand-900 | #<hex> | Dark backgrounds |

<Repeat for neutral/gray (always required) and any accent palettes.>

#### Status
| Token | Value | Notes |
|-------|-------|-------|
| error | #<hex> | Errors, destructive actions |
| success | #<hex> | Confirmations |
| warning | #<hex> | Caution |
| info | #<hex> | Informational |

### Semantic Tokens

<The layer components reference. Each token gets an evocative name + role description so an agent knows *when* to use it.>

#### Surfaces
- **Page Canvas** (`background` → `<hex>` light / `<hex>` dark) — Page background, the canvas content emerges from.
- **Card Surface** (`card` → `<hex>` / `<hex>`) — Default card and panel background.
- **Popover Surface** (`popover` → `<hex>` / `<hex>`) — Dropdowns, popovers, command palettes.
- **Muted Surface** (`muted` → `<hex>` / `<hex>`) — Disabled fields, code blocks, inert regions.

#### Text
- **Primary Text** (`foreground` → `<hex>` / `<hex>`) — Default text. Prefer near-black/near-white over pure black/white to avoid harshness.
- **Muted Text** (`muted-foreground` → `<hex>` / `<hex>`) — Secondary copy, metadata, helper text.

#### Actions
- **Brand Action** (`primary` → `<hex>` / `<hex>`) — Primary CTAs and active states. Reserved for interactivity — never decorative.
- **Brand Action Text** (`primary-foreground` → `<hex>` / `<hex>`) — Text on brand action surfaces.
- **Accent** (`accent` → `<hex>` / `<hex>`) — Hover states, selected items.
- **Destructive** (`destructive` → `<hex>` / `<hex>`) — Delete, danger, irreversible actions.

#### Structural
- **Border** (`border` → `<hex>` / `<hex>`) — Default 1px borders, dividers.
- **Focus Ring** (`ring` → `<hex>` / `<hex>`) — Keyboard focus indicator.

### Accessibility

<Verify every key text/background pairing. WCAG AA: 4.5:1 normal text, 3:1 large text (18px+ or 14px bold) and UI components.>

| Foreground | Background | Ratio | Pass |
|------------|------------|-------|------|
| foreground | background | <ratio> | AA |
| primary-foreground | primary | <ratio> | AA |
| muted-foreground | muted | <ratio> | AA |
| destructive-foreground | destructive | <ratio> | AA |

## 3. Typography

### Font Families
| Role | Family | Fallback Stack |
|------|--------|----------------|
| Body | <family> | <system fallback> |
| Display | <family or same as body> | <fallback> |
| Code | <monospace family> | <fallback> |

<OpenType features if essential to identity (e.g., `"cv01", "ss03"`, `"tnum"`). Note global vs scoped.>

### Type Scale

Scale ratio: <ratio> (<name>) from <base>px base.

| Token | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| display-lg | <px> | <wt> | <lh> | Hero headlines |
| heading-lg | <px> | <wt> | <lh> | Page titles |
| heading-md | <px> | <wt> | <lh> | Card headers |
| body-lg | <px> | <wt> | <lh> | Lead paragraphs |
| body-md | <px> | <wt> | <lh> | Default body |
| body-sm | <px> | <wt> | <lh> | Captions, metadata |
| label | <px> | <wt> | <lh> | Form labels, badges |
| code | <px> | <wt> | <lh> | Code blocks |

### Principles

<2-4 bullets stating typographic moves unique to this system.>

- <e.g. 510 is the signature UI weight — between regular 400 and medium 500>
- <e.g. Letter-spacing tightens at display sizes (-1.6px at 48px+, normal below 24px)>
- <e.g. Three weights only: 400 (read), 510 (emphasize), 590 (announce). No bold.>

## 4. Component Recipes

<Concrete per-variant recipes. Spell out every property. Recipes reproduce reliably; abstract guidance doesn't.>

### Buttons

**Primary**
- Background: `<token>` (`<hex>`)
- Text: `<token>` (`<hex>`)
- Padding: `<v> <h>`
- Radius: `<value>`
- Border: `<value or none>`
- Font: `<size> <weight>`
- Hover: `<change>`
- Active: `<change>`
- Focus: `<ring treatment>`
- Disabled: `<change>`
- Use: <when — primary CTAs, form submission>

**Secondary** — same shape as Primary. Use: secondary actions paired with primary.
**Ghost** — transparent background, `foreground` text, hover lifts to `accent`. Use: toolbar, contextual, low-emphasis actions.
**Destructive** — `destructive` background, `destructive-foreground` text. Use: delete, irreversible actions.

### Inputs

**Text Input**
- Background: `<token>`
- Text: `<token>`
- Border: `<value>`
- Padding: `<v> <h>`
- Radius: `<value>`
- Font: `<size> <weight>`
- Focus: `<ring treatment>`
- Error: `<border + helper text treatment>`
- Disabled: `<treatment>`

### Cards

**Default Card**
- Background: `<token>`
- Border: `<value>`
- Radius: `<value>`
- Padding: `<value>`
- Shadow: `<value>`
- Hover: `<change if interactive>`

### Interactive States

| State | Treatment |
|-------|-----------|
| Hover | <description> |
| Focus | typically 2px ring in `ring` color |
| Active | <description> |
| Disabled | typically `muted-foreground` text on `muted`, opacity .6 |
| Loading | <description> |
| Error | <description> |

## 5. Layout

### Spacing Scale

Base unit: <N>px

| Token | Value | Usage |
|-------|-------|-------|
| space-1 | <N>px | Hairline gap, icon-to-label |
| space-2 | <N>px | Intra-component padding |
| space-3 | <N>px | Form input padding |
| space-4 | <N>px | Default content padding |
| space-6 | <N>px | Card gaps, section breaks |
| space-8 | <N>px | Major section separation |

### Whitespace Philosophy

<1-2 sentences stating how this system uses (or doesn't use) empty space. e.g., "Darkness as space — the near-black canvas IS the whitespace, content emerges from it." Or "Massive vertical padding (80px+) communicates that the product has nothing to prove.">

### Grid & Container
- Max content width: <N>px
- Content padding: `<token>`
- <Grid system if applicable: 12-col, 8-col, fluid>

### Border Radius

Default: <N>px — <one-line rationale tied to personality>

| Token | Value | Usage |
|-------|-------|-------|
| radius-sm | <N>px | Subtle softening |
| radius-md | <N>px | Default — buttons, inputs |
| radius-lg | <N>px | Cards, modals, panels |
| radius-full | 9999px | Pills, badges, avatars |

## 6. Elevation

| Token | Treatment | Usage |
|-------|-----------|-------|
| shadow-sm | `<css>` | Cards at rest |
| shadow-md | `<css>` | Dropdowns, raised elements |
| shadow-lg | `<css>` | Modals, dialogs |
| focus | `<css>` | Keyboard focus on interactive elements |

**Shadow philosophy**: <1-2 sentences. e.g., "On dark surfaces, traditional shadows are nearly invisible — depth is communicated via background luminance steps and semi-transparent white borders, not shadow darkness." Or "Multi-layer stacks: one layer for the border, one for ambient softness, one for distance.">

## 7. Do's and Don'ts

<Concrete rules tied to specific values. Don'ts in particular preserve identity across generations.>

### Do
- <e.g. Use `foreground` (#f7f8f8) for primary text — never pure white>
- <e.g. Apply `radius-md` (4px) to all interactive elements consistently>
- <e.g. Reserve brand indigo (#5e6ad2) for primary CTAs and active states only>
- <e.g. Use semantic tokens — components reference `card`/`popover`/`muted`, not primitives>
- <e.g. Verify every text/background pairing meets WCAG AA>

### Don't
- <e.g. Don't use pure white #ffffff as primary text — harsh on dark backgrounds>
- <e.g. Don't apply brand indigo decoratively — it signals interactivity, never decoration>
- <e.g. Don't introduce additional accent hues — system is single-accent by design>
- <e.g. Don't use weight 700 (bold) — maximum weight is 590>
- <e.g. Don't use traditional CSS borders on dark surfaces — use semi-transparent white instead>

## 8. Agent Prompt Guide

### Quick Color Reference

<One-screen cheat sheet of most-used tokens for fast lookup.>

- Page background: `<token>` (`<hex>`)
- Card background: `<token>` (`<hex>`)
- Primary text: `<token>` (`<hex>`)
- Muted text: `<token>` (`<hex>`)
- Primary action: `<token>` (`<hex>`)
- Hover/accent: `<token>` (`<hex>`)
- Border: `<token>` (`<hex>`)
- Focus ring: `<token>` (`<hex>`)
- Destructive: `<token>` (`<hex>`)

### Example Component Prompts

<5-8 ready-to-paste prompts referencing specific tokens, not abstract guidance.>

- "Hero section: `<bg>` background. Headline at <type spec> in `<text>`. Subtitle at <type spec> in `<muted>`. Primary CTA using <button recipe inline>, secondary CTA using <ghost recipe inline>."
- "Card: `<card bg>`, `<border>` 1px border, `<radius>`, `<shadow>`. Title at <heading spec>, body at <body spec> in `<muted>`."
- "Form input: `<input bg>`, `<input border>`, `<radius>`, `<padding>`. Focus: `<ring>`. Label above at <label spec>."
- "Navigation: `<header bg>` sticky header, links at <link spec>, hover lifts to `<accent>`. CTA right using <primary recipe>."
- "Modal: `<popover bg>`, `<radius-lg>`, `<shadow-lg>`. Backdrop: `<overlay>`. Close is icon-only ghost."
- "Status pill: `<bg tint>`, `<status text>`, 9999px radius, `<padding>`, `<font>`."

### Iteration Guide

<5-7 numbered, scannable rules an agent must follow on every request. Compact enough to re-paste in context as a system reminder.>

1. <e.g. All interactive elements use `radius-md` — no exceptions>
2. <e.g. Brand color is for primary actions only — never decorative, never background>
3. <e.g. Surfaces always use semantic tokens (background/card/popover/muted), never primitives>
4. <e.g. Three weights total: 400/510/590 — no other weights>
5. <e.g. Borders: 1px semi-transparent white on dark, 1px solid `border` on light>
6. <e.g. Always include focus rings on interactive elements — 2px in `ring`>
7. <e.g. Verify every text/background pairing meets WCAG AA before shipping>
````
