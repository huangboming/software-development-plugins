# Responsive Patterns

Breakpoint reflow, collapse, hide, and swap patterns for page-level design. Use this at the responsive step of the workflow — per major region of the page, commit to a reflow rule at each breakpoint.

LLMs default to "it's responsive" with no explicit reflow rules. That's a hope, not a design. A responsive strategy is a set of per-region decisions: what stacks, what collapses, what disappears, what gets replaced entirely.

## Contents

1. [Breakpoint commitments](#breakpoint-commitments)
2. [Reflow patterns](#reflow-patterns)
3. [Per-region reflow rules](#per-region-reflow-rules)
4. [Touch-vs-pointer affordances](#touch-vs-pointer-affordances)
5. [Common failure modes](#common-failure-modes)

## Breakpoint commitments

Commit to a breakpoint set in the artifact. Default to a four-stop set (matches Tailwind / most design systems). If the design system you're composing from uses different stops, use those instead — but state them.

| Name | Width | Typical device | Primary design target |
|---|---|---|---|
| sm | 0–639 px | Phone portrait | Mobile-first: core content and primary CTA |
| md | 640–767 px | Phone landscape / small tablet | Same as sm with more horizontal room |
| lg | 768–1023 px | Tablet / small laptop | Two-column layouts start appearing |
| xl | 1024–1279 px | Laptop / desktop | Three-column layouts, persistent nav |
| 2xl | 1280+ px | Wide desktop | Content-width caps to prevent over-long lines |

**Mobile-first vs desktop-first** — commit to one and apply it consistently. Mobile-first is the default for most public-facing pages; desktop-first can be right for dense internal tools where mobile is rare.

**Orientation** — for tablets, specify whether portrait vs landscape triggers a layout change (usually yes for split-view designs).

**Content-width cap** — long lines at 2xl are a readability failure; specify a max content width (typically 1280-1440 px for page body, 640-720 px for article reading column).

## Reflow patterns

The five canonical patterns for moving from wide to narrow. Per region of the page, pick one.

### Stack

Multi-column becomes single-column, top-to-bottom. Column order matters — usually main content stacks above sidebar, but sometimes the reverse (e.g., product images above reviews on a PDP).

**Use when:** two or three equal-weight columns exist on desktop and content order is stable.

**Specify:** the stacking order explicitly. "Left column above right column" is not the same as "right above left."

### Collapse

Multi-item horizontal becomes a single affordance (hamburger, dropdown, accordion). User taps to expand.

**Use when:** horizontal real estate is tight (mobile nav, filter bars, toolbars).

**Specify:** the collapsed affordance (icon + label, or icon-only), the expanded presentation (full-screen menu, dropdown, bottom sheet), the close/back affordance.

### Hide

Region is not shown at smaller breakpoints. The information is either non-critical or surfaced elsewhere.

**Use when:** the region is redundant on mobile (decorative sidebar, marketing rail) or a lower-priority convenience (secondary nav, "recently viewed" trail).

**Specify:** where the user can reach the hidden content if they need it. Hidden-and-unreachable is a bug.

### Swap

Replace the component with a different component optimized for the breakpoint (e.g., table → cards; tabs → dropdown; hover-menu → full-screen overlay).

**Use when:** the desktop component doesn't degrade well to narrow (tables, dense data grids, hover-reliant menus).

**Specify:** both components are named; the content mapping is 1:1 so the user loses nothing.

### Resize

Same component, different dimensions. Font scales, image resizes, padding tightens.

**Use when:** the component is fundamentally viewport-agnostic (most text blocks, most media) and only needs proportional adjustment.

**Specify:** fluid (CSS `clamp`, viewport units) vs stepped (fixed values per breakpoint). Fluid is lower-maintenance; stepped is more predictable.

## Per-region reflow rules

Apply one reflow pattern per region, per breakpoint. The table below is a default starting set by region; override per page.

| Region | sm (phone) | md | lg (tablet) | xl (desktop) | 2xl |
|---|---|---|---|---|---|
| Primary nav | Collapse (hamburger) | Collapse | Hide hamburger, show inline | Inline | Inline, content-capped |
| Page header / hero | Stack | Stack | Side-by-side OK | Side-by-side | Content-capped |
| Content + sidebar | Stack (content first) | Stack | Side-by-side | Side-by-side | Side-by-side, capped |
| Data table | Swap to cards | Swap to cards | Horizontal-scroll table | Full table | Full table |
| Filter bar | Collapse (filter button → bottom sheet) | Collapse | Inline with overflow | Inline | Inline |
| Form (single column) | Stack | Stack | Stack, centered | Stack, centered, capped | Same |
| Form (multi-column) | Stack | Stack | 2-col | 2-col or 3-col | Same |
| Wizard step indicator | Compact (numbers only) | Compact | Full (numbers + labels) | Full | Full |
| Dashboard tile grid | 1 col | 1 col | 2 col | 3-4 col | 4 col, capped |
| List row with many columns | Swap to card | Swap to card | Subset of columns | All columns | All columns |
| Sticky CTA | Sticky bottom bar | Sticky bottom bar | Inline, plus sticky at footer | Inline only | Inline only |
| Modal | Full-screen | Full-screen | Centered dialog | Centered dialog | Centered dialog |
| Side panel | Bottom sheet | Bottom sheet | Side panel (full height) | Side panel | Side panel |
| Mega menu | Hide (collapse into hamburger) | Hide | Full-screen overlay | Dropdown panel | Dropdown panel |
| Article body | Resize (single col) | Resize | Single col, wider | Single col + TOC sidebar | Same, capped |

## Touch-vs-pointer affordances

Reflow patterns are only half the story; input device matters too.

| Affordance | Pointer (lg+) | Touch (sm-md) |
|---|---|---|
| Hover | Allowed for reveals, tooltips | Never — replace with always-on or focus-revealed |
| Context menu | Right-click OK | Long-press (and must be discoverable) |
| Target size | ≥24×24 px OK | ≥44×44 px hard minimum |
| Cursor changes | Meaningful (pointer on buttons, text on inputs) | N/A but don't rely on it |
| Tooltips | Hover-triggered | Tap-triggered, dismissible |
| Drag | Native drag API | Touch equivalent needed (long-press + drag) or alternative |

**Hover-reveal is a mobile bug.** Any affordance that only appears on hover must have a parallel trigger for touch users (focus, always-on, long-press).

**Touch target minimums are non-negotiable.** 44×44 px minimum for primary actions (Apple HIG, WCAG 2.5.5 AAA recommends 44). 24×24 px is the new AA minimum (WCAG 2.2 SC 2.5.8). Spacing between adjacent targets matters — touch errors compound when buttons are cramped.

## Common failure modes

Surface these as blockers if present in the design; many are subtle enough to slip past review.

- **No stated reflow rules.** "It's responsive" is not a design. Per region, name the pattern.
- **Hidden content with no reachable path.** If you hide a region on mobile, say where the user can get to the content.
- **Hover-dependent affordances.** Any `:hover` behavior without a focus or touch parallel excludes touch and keyboard users.
- **Tables forced into mobile without reflow.** Horizontal scroll on a 20-column table is unusable — swap to cards.
- **Sticky elements eating the viewport.** On mobile, a sticky top nav + sticky bottom CTA + sticky toolbar leaves almost no content visible. Pick one sticky, not three.
- **Form input types that trigger wrong keyboards.** `type="email"`, `type="tel"`, `inputmode="numeric"` — not optional polish.
- **Touch targets under 44×44 px.** Close buttons, toggle switches, and text links are the repeat offenders.
- **Autofocus on mobile.** Auto-focusing an input on page load pops up the keyboard and shoves content out of view. Usually a bug.
- **Viewport meta missing or wrong.** `<meta name="viewport" content="width=device-width, initial-scale=1">` is the baseline; `user-scalable=no` is an a11y failure.
- **Breakpoints mismatched to device classes.** E.g., placing the nav-collapse breakpoint at 900 px instead of the design system's stop creates inconsistency across the product.
- **No landscape-vs-portrait consideration for tablets.** A tablet in landscape is closer to a laptop than a phone; the default should often match laptop.
- **CSS-only dark mode with no user override.** `prefers-color-scheme` is table stakes; user override is the usability requirement.
