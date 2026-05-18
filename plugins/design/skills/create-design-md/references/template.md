# Strict DESIGN.md Template

Use this skeleton for root `DESIGN.md`. It is intentionally limited to the DESIGN.md format: YAML token frontmatter, one optional H1, and the 8 standard `##` sections in order.

````markdown
---
version: alpha
name: <Product or design system name>
description: <One sentence describing the visual system>
colors:
  primary: "#<hex>"
  on-primary: "#<hex>"
  secondary: "#<hex>"
  on-secondary: "#<hex>"
  tertiary: "#<hex>"
  neutral: "#<hex>"
  surface: "#<hex>"
  on-surface: "#<hex>"
  muted: "#<hex>"
  on-muted: "#<hex>"
  border: "#<hex>"
  ring: "#<hex>"
  error: "#<hex>"
  on-error: "#<hex>"
typography:
  headline-display:
    fontFamily: <Family name>
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: <Family name>
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-md:
    fontFamily: <Family name>
    fontSize: 28px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: -0.01em
  body-lg:
    fontFamily: <Family name>
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: <Family name>
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: <Family name>
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-lg:
    fontFamily: <Family name>
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: 0.01em
  label-md:
    fontFamily: <Family name>
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: 0.04em
  label-sm:
    fontFamily: <Family name>
    fontSize: 11px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: 0.06em
rounded:
  none: 0px
  sm: 4px
  md: 8px
  lg: 12px
  xl: 20px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
  button-secondary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-secondary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
  input-text:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
  card-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 24px
---

# <Product Name> Design System

## Overview

**Source:** <Audited from `path/to/file`, `path/to/theme`, and `path/to/component`; or proposed greenfield system based on product docs/user brand direction.>

<Describe the product personality, audience, visual tone, and the intent behind the token choices. State whether the system is audited or proposed.>

## Colors

<Describe the semantic color system. Use prose names paired with token names and hex values. Palette ramps may appear only if they exist in code or materially improve the system.>

- **Primary** (`primary`, `<hex>`): <role>
- **On Primary** (`on-primary`, `<hex>`): <role and contrast expectation>
- **Surface** (`surface`, `<hex>`): <role>
- **On Surface** (`on-surface`, `<hex>`): <role>
- **Error** (`error`, `<hex>`): <role>

Accessibility checks:

| Foreground | Background | Ratio | Pass |
|---|---|---:|---|
| `on-surface` | `surface` | <ratio> | AA |
| `on-primary` | `primary` | <ratio> | AA |
| `on-secondary` | `secondary` | <ratio> | AA |
| `on-error` | `error` | <ratio> | AA |

## Typography

<Describe font families, hierarchy, scale, weights, line heights, and any distinctive OpenType/variable-font choices. Every named level must match the YAML `typography` tokens.>

- **Display/headlines:** <usage>
- **Body:** <usage>
- **Labels:** <usage>

## Layout

<Describe spacing rhythm, density, containers, grids, and responsive behavior. Every spacing value should map to YAML `spacing` tokens unless it is a one-off layout constraint.>

- Base spacing rhythm: `<value>`
- Content width/container: `<value>`
- Density: <compact | balanced | spacious>

## Elevation & Depth

<Describe how hierarchy is conveyed: shadows, tonal layers, borders, blur, or explicitly flat/no-shadow treatment. If shadows are not tokenized in frontmatter, define them in prose with exact CSS values when used.>

## Shapes

<Describe the shape language and map it to YAML `rounded` tokens. State which radii apply to buttons, inputs, cards, modals, badges, and avatars.>

## Components

<Describe component recipes and states. The YAML `components` tokens are normative; prose explains usage, hover/focus/disabled/error treatment, borders, and shadows.>

### Buttons

- **Primary:** <background, text, radius, padding, height, hover, active, focus, disabled, and use case>
- **Secondary:** <same level of specificity>

### Inputs

- **Text input:** <background, text, border, radius, padding, height, focus, error, disabled>

### Cards

- **Default card:** <background, text, radius, padding, border/shadow, hover if interactive>

## Do's and Don'ts

### Do

- Do <specific rule tied to token/value>.
- Do verify every text/background pairing meets WCAG AA.
- Do use semantic tokens in components rather than raw hex values.

### Don't

- Don't <specific anti-pattern that would break the visual identity>.
- Don't introduce new accent hues without updating `colors` and component usage.
- Don't use palette ramps unless they are audited or intentionally needed.
````

## Concise format rules

- Frontmatter begins and ends with a line containing exactly `---`.
- Keep custom provenance out of frontmatter; put source labeling in `## Overview`.
- Required frontmatter keys: `version`, `name`, `colors`, `typography`, `rounded`, `spacing`, `components`.
- Color values are quoted SRGB hex strings like `"#1A1C1E"`.
- Dimensions use `px`, `em`, or `rem`; unitless line heights are allowed.
- Token references use `{path.to.token}` and must be quoted in YAML.
- Body headings use exactly one optional H1 and then these H2s in order: `Overview`, `Colors`, `Typography`, `Layout`, `Elevation & Depth`, `Shapes`, `Components`, `Do's and Don'ts`.
- Do not add non-standard H2 sections.
- Do not duplicate H2 section headings.

## Compliance checklist

Before finalizing `DESIGN.md`, verify:

- [ ] YAML frontmatter exists and parses.
- [ ] `version: alpha` and `name` are present.
- [ ] Required token groups are present: `colors`, `typography`, `rounded`, `spacing`, `components`.
- [ ] Required minimum semantic colors are present: `primary`, `on-primary`, `secondary`, `on-secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `muted`, `on-muted`, `border`, `ring`, `error`, `on-error`.
- [ ] Required typography tokens are present: `headline-display`, `headline-lg`, `headline-md`, `body-lg`, `body-md`, `body-sm`, `label-lg`, `label-md`, `label-sm`.
- [ ] Required rounded tokens are present: `none`, `sm`, `md`, `lg`, `xl`, `full`.
- [ ] Required spacing tokens are present: `xs`, `sm`, `md`, `lg`, `xl`.
- [ ] Required component tokens are present: `button-primary`, `button-primary-hover`, `button-secondary`, `input-text`, `card-default`.
- [ ] Color values are valid hex.
- [ ] Typography dimensions and line heights are valid.
- [ ] Component token references use valid `{path.to.token}` syntax.
- [ ] Body contains only the 8 standard H2 sections, in order, with no duplicates.
- [ ] `## Overview` explicitly labels the source as audited or proposed greenfield.
- [ ] Audited tokens/components cite source files; greenfield tokens do not claim to be audited.
- [ ] Key color pairings include WCAG AA ratios.
