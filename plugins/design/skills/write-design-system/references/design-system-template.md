# Design System Template

Template for `DESIGN.md` at the project root. This document is **agent-facing prompt context** — written to be read by AI coding agents that generate UI. Optimize accordingly:

- **Concrete values, not abstract guidance.** "Background `#08090a`" beats "use a dark surface."
- **Evocative, memorable token names.** *Marketing Black* / *Brand Indigo* anchor an LLM's reasoning more than `primary-600`. Pair the systematic name with a memorable alias.
- **Per-variant component recipes.** Spell out every property (bg, text, padding, radius, border, shadow, font, hover, focus). Recipes reproduce reliably; abstract guidance doesn't.
- **Explicit Do's and Don'ts.** Don'ts are how you preserve identity across hundreds of generations.
- **Ready-to-paste agent prompts.** The Agent Prompt Guide section is what makes this doc executable.

**Structure note**: components are placed early (right after Typography) so an agent generating UI hits them in reading order. Border Radius lives inside Layout; Motion and Design Principles are local extensions.

Omit any section that doesn't apply to the project.

```markdown
# Design System

> Last updated: <date>

## 1. Visual Theme & Atmosphere

<2-3 paragraphs of evocative prose. Describe the *feel* — what mood the UI conveys, what philosophy drives the choices, what tensions or signature moves define it. This prose is what lets an LLM make borderline judgement calls about whether a generated UI "fits" the system. Ground it in the discovery findings or codebase audit — not generic filler.>

<Talk about: the canvas (light/dark, warm/cool, the *feeling* of the surface), the typographic voice (what the type does at scale, what weights carry meaning), the role of color (chromatic or achromatic, how restrained the palette is), and the structural moves (borders, shadows, spacing rhythm) that make this system distinguishable from a generic theme.>

### Key Characteristics

<6-10 non-negotiable signature elements that must be preserved in all generated UI. Each is a single line, concrete, value-bearing. These are the "if you only follow ten rules, follow these" anchors.>

- <e.g. Inter Variable with `"cv01", "ss03"` enabled globally — geometric alternates>
- <e.g. Brand indigo `#5e6ad2` reserved for primary CTAs only — never decoration, never background>
- <e.g. 4px base spacing — most padding lands on 8/12/16, never 5/10/15>
- <e.g. Borders are 1px semi-transparent white `rgba(255,255,255,0.08)`, never solid dark colors>
- <e.g. Three weights total: 400 (read), 510 (emphasize), 590 (announce)>

## 2. Design Principles

<3-5 principles that anchor visual decisions. Each principle is one sentence stating a priority with brief rationale tied to product context.>

- **Clarity over decoration** — users are under time pressure; every visual element serves comprehension
- **Calm confidence** — the product handles sensitive data; the UI should feel trustworthy and precise
- **Consistent density** — information-dense screens maintain uniform spacing to reduce cognitive load

## 3. Color Palette & Roles

### Primitive Palette

<Raw color values — the source of truth. Components MUST NOT reference primitives directly; they go through semantic tokens (next subsection). Build full scales for any chromatic family used in the system.>

#### Brand
| Token | Value | Notes |
|-------|-------|-------|
| brand-50 | #<hex> | Lightest tint — backgrounds |
| brand-100 | #<hex> | Hover backgrounds |
| brand-200 | #<hex> | Active backgrounds |
| brand-300 | #<hex> | Borders, decorative |
| brand-400 | #<hex> | Icons, secondary elements |
| brand-500 | #<hex> | Mid-tone |
| brand-600 | #<hex> | **Default brand** — primary actions |
| brand-700 | #<hex> | Hover state |
| brand-800 | #<hex> | Active state |
| brand-900 | #<hex> | Dark backgrounds |
| brand-950 | #<hex> | Darkest shade |

<Repeat for neutral/gray (always required) and any accent/secondary palettes.>

#### Status
| Token | Value | Notes |
|-------|-------|-------|
| error | #<hex> | Errors, destructive actions |
| success | #<hex> | Success states, confirmations |
| warning | #<hex> | Warning states, caution |
| info | #<hex> | Informational states |

### Roles (Semantic Tokens)

<This is the layer components actually reference. Each token gets an evocative name + role description so an agent knows *when* to use it. Pair the systematic name with a memorable alias to make the doc more anchored.>

#### Surfaces
- **Page Canvas** (`background` → `<hex>` light / `<hex>` dark) — The deepest surface. Page background, the canvas content emerges from.
- **Card Surface** (`card` → `<hex>` / `<hex>`) — Slightly elevated containers. Default card and panel background.
- **Popover Surface** (`popover` → `<hex>` / `<hex>`) — Floating elements: dropdowns, popovers, command palettes.
- **Muted Surface** (`muted` → `<hex>` / `<hex>`) — Subtle grouping, disabled fields, code blocks, inert regions.

#### Text
- **Primary Text** (`foreground` → `<hex>` / `<hex>`) — Default text color. Prefer near-black/near-white over pure black/white to avoid harshness.
- **Muted Text** (`muted-foreground` → `<hex>` / `<hex>`) — Secondary copy, metadata, helper text.

#### Actions
- **Brand Action** (`primary` → `<hex>` / `<hex>`) — Primary CTAs and active states. Reserved for interactivity — never decorative.
- **Brand Action Text** (`primary-foreground` → `<hex>` / `<hex>`) — Text on brand action surfaces.
- **Accent** (`accent` → `<hex>` / `<hex>`) — Hover states, emphasis, selected items.
- **Destructive** (`destructive` → `<hex>` / `<hex>`) — Delete, danger, irreversible actions.

#### Structural
- **Border Default** (`border` → `<hex>` / `<hex>`) — Default 1px borders, dividers.
- **Input Border** (`input` → `<hex>` / `<hex>`) — Form field borders.
- **Focus Ring** (`ring` → `<hex>` / `<hex>`) — Keyboard focus indicator.

### Accessibility

<Verify all key text/background pairings at derivation time. WCAG AA minimum: 4.5:1 normal text, 3:1 large text (18px+ or 14px bold), 3:1 UI components.>

| Foreground | Background | Ratio | Pass |
|------------|------------|-------|------|
| foreground | background | <ratio> | AA |
| primary-foreground | primary | <ratio> | AA |
| muted-foreground | muted | <ratio> | AA |
| destructive-foreground | destructive | <ratio> | AA |

## 4. Typography Rules

### Font Families
| Role | Family | Fallback Stack |
|------|--------|----------------|
| Body | <family> | <system fallback> |
| Display | <family or same as body> | <fallback> |
| Code | <monospace family> | <fallback> |

<OpenType features if any are essential to the system's identity (e.g., `"cv01", "ss03"`, `"liga"`, `"tnum"`). Note them as global vs scoped.>

### Type Scale

Scale ratio: <ratio> (<name>) from <base>px base.

| Token | Size | Weight | Line Height | Letter Spacing | Usage |
|-------|------|--------|-------------|----------------|-------|
| display-lg | <px> (<rem>) | <wt> | <lh> | <ls> | Hero headlines |
| display-md | <px> (<rem>) | <wt> | <lh> | <ls> | Section headers |
| heading-lg | <px> (<rem>) | <wt> | <lh> | <ls> | Page titles |
| heading-md | <px> (<rem>) | <wt> | <lh> | <ls> | Card headers |
| heading-sm | <px> (<rem>) | <wt> | <lh> | <ls> | Sub-headings |
| body-lg | <px> (<rem>) | <wt> | <lh> | normal | Lead paragraphs |
| body-md | <px> (<rem>) | <wt> | <lh> | normal | Default body |
| body-sm | <px> (<rem>) | <wt> | <lh> | normal | Captions, metadata |
| label-lg | <px> (<rem>) | <wt> | <lh> | normal | Form labels |
| label-sm | <px> (<rem>) | <wt> | <lh> | normal | Helper text, badges |
| code | <px> (<rem>) | <wt> | <lh> | normal | Code blocks |

### Principles

<2-4 bullets stating typographic moves unique to this system — the things that make the type feel like *this* system.>

- <e.g. 510 is the signature weight for UI text — between regular 400 and medium 500>
- <e.g. Letter-spacing tightens at display sizes (-1.6px at 48px+, normal below 24px)>
- <e.g. Three weights only: 400 (read), 510 (emphasize), 590 (announce). No bold.>

## 5. Component Recipes

<Concrete per-variant recipes. Spell out every property — bg, text, padding, radius, border, shadow, font, hover, focus. Agents reproduce recipes far more reliably than abstract guidance. Components live this early in the document so an agent generating UI hits them right after the type and color anchors. Add variants as the system needs them.>

### Buttons

**Primary Button**
- Background: `<token>` (`<hex>`)
- Text: `<token>` (`<hex>`)
- Padding: `<vertical> <horizontal>`
- Radius: `<value>`
- Border: `<value or none>`
- Font: `<size> <weight> <family>`
- Hover: `<change>`
- Active: `<change>`
- Focus: `<focus ring treatment>`
- Disabled: `<change>`
- Use: <when to use — primary CTAs, form submission, etc.>

**Secondary Button**
- Background: ...
- Text: ...
- <same shape as Primary>
- Use: <secondary actions paired with primary>

**Ghost Button**
- Background: transparent or near-transparent
- Text: ...
- <same shape>
- Use: <toolbar, contextual, low-emphasis actions>

**Destructive Button**
- Background: `destructive`
- Text: `destructive-foreground`
- <same shape>
- Use: <delete, irreversible actions>

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
- Use: <standard text entry>

<Add other input types as needed: textarea, select, search, number, etc.>

### Cards

**Default Card**
- Background: `<token>`
- Border: `<value>`
- Radius: `<value>`
- Padding: `<value>`
- Shadow: `<value>`
- Hover: `<change if interactive>`
- Use: <containers for grouped content>

<Add featured/elevated/image card variants if the system distinguishes them.>

### Badges & Pills

**Status Pill**
- Background: ...
- Text: ...
- Padding: ...
- Radius: 9999px
- Font: ...
- Use: ...

### Navigation

<Recipe or bullet list. Cover: header surface, link styling, active/hover states, CTA placement, mobile collapse trigger.>

### Interactive States

| State | Visual Treatment |
|-------|-----------------|
| Hover | <description> |
| Focus | <typically a 2px ring in `ring` color> |
| Active | <description> |
| Disabled | <typically `muted-foreground` text on `muted` background, opacity .6> |
| Loading | <description> |
| Error | <description> |

## 6. Layout Principles

### Spacing Scale

Base unit: <N>px

| Token | Value | Usage |
|-------|-------|-------|
| space-1 | <N>px | Hairline gap, icon-to-label |
| space-2 | <N>px | Intra-component padding |
| space-3 | <N>px | Form input padding |
| space-4 | <N>px | Default content padding |
| space-5 | <N>px | Component gaps within sections |
| space-6 | <N>px | Card gaps, nav item height |
| space-7 | <N>px | Section dividers |
| space-8 | <N>px | Content section margins |
| space-9 | <N>px | Major section separation |
| space-10 | <N>px | Page section breaks |

### Whitespace Philosophy

<1-2 sentences stating how this system uses (or doesn't use) empty space. e.g., "Darkness as space — the near-black canvas IS the whitespace, content emerges from it." Or "Gallery emptiness — massive vertical padding (80px+) communicates that the product has nothing to prove.">

### Grid & Container
- Max content width: <N>px
- Content padding: <token>
- <Grid system if applicable: 12-col, 8-col, fluid, etc.>

### Border Radius

Default: <N>px — <one-line rationale tied to personality>

| Token | Value | Usage |
|-------|-------|-------|
| radius-none | 0px | Sharp elements |
| radius-sm | <N>px | Subtle softening |
| radius-md | <N>px | Default — buttons, inputs, most components |
| radius-lg | <N>px | Cards, modals, panels |
| radius-xl | <N>px | Large featured panels |
| radius-full | 9999px | Pills, badges, avatars |

## 7. Depth & Elevation

<Each level gets a treatment recipe and a use case. For dark systems, note that elevation often comes from background luminance shifts rather than shadows.>

| Token | Treatment | Usage |
|-------|-----------|-------|
| shadow-none | none | Flat elements |
| shadow-sm | `<css>` | Cards at rest, subtle depth |
| shadow-md | `<css>` | Dropdowns, raised elements |
| shadow-lg | `<css>` | Modals, dialogs |
| shadow-xl | `<css>` | Floating alerts, toasts |
| focus | `<css>` | Keyboard focus on interactive elements |

**Shadow philosophy**: <1-2 sentences. e.g., "On dark surfaces, traditional shadows are nearly invisible — depth is communicated via background luminance steps and semi-transparent white borders, not shadow darkness." Or "Multi-layer shadow stacks: each layer has a job — one for the border, one for ambient softness, one for distance.">

## 8. Motion

### Duration
| Token | Value | Usage |
|-------|-------|-------|
| duration-fast | <N>ms | Toggles, micro-interactions |
| duration-normal | <N>ms | Most UI transitions |
| duration-slow | <N>ms | Panels, modals, drawers |

### Easing
| Token | Value | Usage |
|-------|-------|-------|
| easing-standard | <value> | Most movements |
| easing-enter | <value> | Elements appearing |
| easing-exit | <value> | Elements disappearing |

**Reduced motion**: when `prefers-reduced-motion: reduce` is active, all durations collapse to 0ms.

## 9. Responsive Behavior

### Breakpoints

| Token | Width | Target | Key Changes |
|-------|-------|--------|-------------|
| sm | <N>px | Mobile landscape | Single column, compact padding |
| md | <N>px | Tablet | Two-column grids begin |
| lg | <N>px | Desktop | Full layout, expanded padding |
| xl | <N>px | Wide desktop | Generous margins |

### Touch Targets
- Minimum 44x44px for any interactive element
- <Other rules specific to this system>

### Collapsing Strategy
- <Display sizes scaling: e.g., "72px → 48px → 32px on mobile, tracking adjusts proportionally">
- <Navigation collapse: e.g., "horizontal links → hamburger at md">
- <Grid collapse: e.g., "3-column → 2-column → 1-column at sm">
- <Section spacing: e.g., "80px+ → 48px on mobile">

## 10. Do's and Don'ts

<Concrete rules tied to specific values, not principles. These are the guardrails that preserve identity across many generations. Don'ts in particular are how you keep an agent on-system.>

### Do
- <e.g. Use `foreground` (#f7f8f8) for primary text — never pure white>
- <e.g. Apply `radius-md` (4px) to all interactive elements consistently>
- <e.g. Reserve brand indigo (#5e6ad2) for primary CTAs and active states only>
- <e.g. Use semantic tokens — components reference `card`/`popover`/`muted`, not primitives>
- <e.g. Verify every text/background pairing meets WCAG AA>

### Don't
- <e.g. Don't use pure white #ffffff as primary text — it's harsh on dark backgrounds>
- <e.g. Don't apply brand indigo decoratively — it signals interactivity, never decoration>
- <e.g. Don't introduce additional accent hues — the system is single-accent by design>
- <e.g. Don't use weight 700 (bold) — maximum weight is 590>
- <e.g. Don't use traditional CSS borders on dark surfaces — use semi-transparent white instead>
- <e.g. Don't skip OpenType features — they're identity, not decoration>

## 11. Agent Prompt Guide

### Quick Color Reference

<One-screen cheat sheet of the most-used tokens for fast lookup. An agent should be able to glance at this and immediately grab the right value.>

- Page background: `<token>` (`<hex>`)
- Card background: `<token>` (`<hex>`)
- Primary text: `<token>` (`<hex>`)
- Muted text: `<token>` (`<hex>`)
- Primary action: `<token>` (`<hex>`)
- Hover/accent: `<token>` (`<hex>`)
- Border default: `<token>` (`<hex>`)
- Focus ring: `<token>` (`<hex>`)
- Destructive: `<token>` (`<hex>`)

### Example Component Prompts

<5-8 ready-to-paste prompts that demonstrate how to invoke the system. Each prompt should reference specific tokens and values, not abstract guidance. These are the prompts a developer would copy into "build me a hero section like X.">

- "Create a hero section: `<bg>` background. Headline at <type spec> in `<text token>`. Subtitle at <type spec> in `<muted token>`. Primary CTA using <button recipe inline>, secondary CTA using <ghost recipe inline>."
- "Design a card: `<card bg>` background, `<border>` 1px border, `<radius>` radius, `<shadow>`. Title at <heading spec>, body at <body spec> in `<muted text>`."
- "Build a form input: `<input bg>` background, `<input border>`, `<radius>`, `<padding>`. Focus state: `<ring treatment>`. Label above at <label spec>."
- "Create navigation: `<header bg>` sticky header, links at <link spec> in `<text>`, hover lifts to `<accent>`. CTA on the right using <primary recipe>."
- "Design a modal: `<popover bg>`, `<radius-lg>`, `<shadow-lg>`. Backdrop: `<overlay color>`. Close button is icon-only ghost variant."
- "Build a status pill: `<bg tint>` background, `<status text>`, 9999px radius, <padding>, <font spec>."

### Iteration Guide

<5-8 numbered, scannable rules an agent must follow on every request. Compact enough to re-paste in context as a system reminder.>

1. <e.g. All interactive elements use `radius-md` — no exceptions on buttons, inputs, or cards>
2. <e.g. Brand color is for primary actions only — never decorative, never background>
3. <e.g. Surfaces always use semantic tokens (background/card/popover/muted), never primitives directly>
4. <e.g. Three weights total: 400 (read), 510 (emphasize), 590 (announce) — no other weights>
5. <e.g. Borders are 1px semi-transparent white on dark, 1px solid `border` token on light>
6. <e.g. Always include focus rings on interactive elements — 2px in `ring` color>
7. <e.g. Verify every text/background pairing meets WCAG AA before shipping>
```
