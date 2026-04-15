# Token Derivation Guide

Systematic methods for translating discovery findings into specific token values. Covers color (3-layer architecture), typography (modular scales), spacing, border radius, elevation, and motion.

## Table of Contents

1. [Color System](#color-system)
2. [Typography System](#typography-system)
3. [Spacing System](#spacing-system)
4. [Border Radius](#border-radius)
5. [Elevation and Shadows](#elevation-and-shadows)
6. [Motion Tokens](#motion-tokens)
7. [Reference Token Set](#reference-token-set)

## Color System

### Three-Layer Architecture

Never collapse these layers. Components must reference semantic tokens, never primitives directly.

**Layer 1: Primitive Palette**

Raw color values named by hue + numeric scale (50-950, lighter = lower).

Derivation:

1. Start from the brand's primary hue. Designate it as the 500 or 600 level.
2. Generate lighter tints: increase HSL lightness, slightly reduce saturation.
3. Generate darker shades: decrease lightness, slightly increase saturation.
4. Maintain consistent saturation/lightness relationships across hues (blue-200 and green-200 should feel visually equivalent).

Build palettes for:

- Primary brand color (full 50-950 scale)
- 1-2 accent/secondary colors (full scales)
- Neutral/gray scale (full scale — the most-used palette)
- Semantic colors: red (error), green (success), amber (warning), blue (info)

If the primary brand color conflicts with a semantic color (e.g., brand is red), shift the semantic color to avoid confusion.

**The 60-30-10 rule:** 60% dominant neutral, 30% secondary/supporting, 10% accent. Applies to visual surface area, not token count.

**Layer 2: Semantic Tokens**

Names describe PURPOSE, not color. This layer enables dark mode and theming.

Core semantic tokens:

```
background / foreground              — page surface + primary text
card / card-foreground               — card surfaces
popover / popover-foreground         — dropdown/popover surfaces
primary / primary-foreground         — primary actions
secondary / secondary-foreground     — secondary actions
muted / muted-foreground             — disabled/inactive/subtle
accent / accent-foreground           — emphasis, hover states
destructive / destructive-foreground — danger, delete, error
border                               — borders and dividers
input                                — input field borders
ring                                 — focus ring
```

**Layer 3: Component Tokens (optional)**

Scoped to specific components, pointing to semantic tokens. Use only for exceptions — most components should use semantic tokens directly.

### Dark Mode Strategy

- Use dark gray (#0d1117 or #111827), not pure black — pure black creates harsh contrast.
- Desaturate light-mode colors slightly for dark surfaces.
- Replace shadows with surface lightness shifts — elevated surfaces are lighter, not shadowed.
- Every semantic token needs both a light and dark mapping.

### Contrast Verification

Verify at derivation time, not after:

- Normal text on background: 4.5:1 minimum (WCAG AA)
- Large text (18px+ or 14px bold): 3:1 minimum
- UI components and graphical objects: 3:1 minimum

Build a contrast matrix of all likely text/background pairings.

## Typography System

### Modular Scale Method

1. Start with base body size: **16px** (standard browser default).
2. Choose a ratio matching the product character:

| Ratio | Value | Best for |
|-------|-------|----------|
| Minor Second | 1.067 | Dense data apps, minimal UIs |
| Major Second | 1.125 | Long-form content, B2B SaaS |
| Minor Third | 1.200 | General-purpose products |
| Major Third | 1.250 | SaaS dashboards, consumer apps |
| Perfect Fourth | 1.333 | Landing pages, consumer apps |
| Perfect Fifth | 1.500 | Marketing, creative |
| Golden Ratio | 1.618 | Luxury, art-forward |

3. Generate the scale by multiplying/dividing the base by the ratio. Round to whole pixels or a 4px grid.

Example at Major Third (1.250) from 16px base:

```
body-sm:     10px  (16 / 1.25 / 1.25)
label-sm:    13px  (16 / 1.25)
body-md:     16px  (base)
heading-sm:  20px  (16 * 1.25)
heading-md:  25px  (16 * 1.25^2)
heading-lg:  31px  (16 * 1.25^3)
display-md:  39px  (16 * 1.25^4)
display-lg:  49px  (16 * 1.25^5)
```

### Semantic Type Roles

Assign purpose names, not size names:

```
display-lg     — hero headlines
display-md     — section headers
heading-lg     — page titles
heading-md     — card headers, section titles
heading-sm     — sub-headings
body-lg        — lead paragraphs
body-md        — default body text
body-sm        — captions, metadata
label-lg       — form labels
label-sm       — helper text, badges
code           — monospace content
```

### Line Height

- Body text: 1.5-1.6
- Headings: 1.1-1.3 (tighter at larger sizes)
- Dense data/tables: 1.2-1.4

### Font Weight

Establish 3-4 weights maximum:

- Regular (400): body text
- Medium (500): emphasis, labels
- Semibold (600): headings, buttons
- Bold (700): strong emphasis (use sparingly)

### Font Pairing

- One family is sufficient for most products.
- Two families maximum: display face for headings + body face for content.
- Three+ is almost never justified.

## Spacing System

### Base Unit

**4px** for dense UIs (B2B, developer tools, data-heavy).
**8px** for general-purpose and consumer apps.

### Scale

Standard progression from base unit:

```
space-1:   4px    — icon-to-label gap, hairline
space-2:   8px    — intra-component, button padding
space-3:  12px    — form input padding
space-4:  16px    — default content padding, card inner
space-5:  20px    — component gaps within sections
space-6:  24px    — card gaps, nav item height
space-7:  32px    — section dividers
space-8:  40px    — content section margins
space-9:  48px    — major section separation
space-10: 64px    — page section breaks
space-11: 80px    — hero sections
space-12: 96px+   — full-bleed section padding
```

Dense UIs: most usage clusters in space-1 through space-6.
Consumer/marketing: most usage clusters in space-4 through space-12.

## Border Radius

Pick ONE default and apply consistently. The default is one of the clearest personality signals.

```
none:   0px     — sharp, technical, data-heavy
sm:     2px     — subtle softening
md:     4px     — B2B neutral
lg:     8px     — approachable, modern SaaS
xl:     12px    — friendly, consumer
2xl:    16px    — playful, consumer apps
full:   9999px  — pill shapes (badges, tags, chips)
```

Using multiple different radii without systematic reason creates visual noise.

## Elevation and Shadows

Standard depth scale:

```
shadow-none  — flat, no elevation
shadow-sm    — cards at rest, subtle depth
shadow-md    — dropdowns, raised elements
shadow-lg    — modals, dialogs
shadow-xl    — highest elevation, alerts/toasts
```

Dark mode: replace shadows with surface lightness shifts. Elevated = lighter background, not shadowed.

## Motion Tokens

Define from day one — retrofitting `prefers-reduced-motion` across many components is painful.

### Duration

```
instant:     0ms     — reduced-motion fallback
fast:        100ms   — micro-interactions, toggles
normal:      200ms   — most UI transitions
slow:        300ms   — panels, drawers, modals
deliberate:  500ms   — page transitions, complex reveals
```

Developer tools: prefer fast (100-150ms). Consumer apps: allow expressive (200-500ms).

### Easing

```
standard:  cubic-bezier(0.2, 0, 0, 1)  — most movements
enter:     cubic-bezier(0, 0, 0.2, 1)   — elements appearing
exit:      cubic-bezier(0.4, 0, 1, 1)   — elements disappearing
linear:    linear                        — loaders, progress bars
```

### Reduced Motion

Always include `prefers-reduced-motion` support: set all durations to 0ms.

## Reference Token Set

The shadcn/ui CSS variable set covers 95% of web UI semantic token needs.

**Color pairs (each has foreground counterpart):**

background, card, popover, primary, secondary, muted, accent, destructive

**Standalone:**

border, input, ring

**Data visualization:**

chart-1 through chart-5

**Structural:**

radius (single base value)

The `--name / --name-foreground` pairing pattern ensures every surface has an accessible text counterpart at the semantic layer.
