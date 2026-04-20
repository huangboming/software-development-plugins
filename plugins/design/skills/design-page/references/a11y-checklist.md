# Accessibility Checklist

Baseline a11y requirements for every page, plus archetype-specific gotchas. Use this at the a11y step of the workflow and again as a final gate before delivery.

A11y in the design artifact, not in the implementation ticket. By implementation, structural decisions (heading order, landmark choice, focus trap location) are locked — retrofitting them is expensive or impossible. Design it in.

Standard referenced: WCAG 2.2 Level AA as the minimum for all public-facing pages. Add AAA criteria where the user population warrants (screen-reader-primary users, government or healthcare products, accessibility-first brands).

## Contents

1. [Baseline checklist — every page](#baseline-checklist--every-page)
2. [Per-archetype gotchas](#per-archetype-gotchas)
3. [How to state a11y in the artifact](#how-to-state-a11y-in-the-artifact)

## Baseline checklist — every page

Walk these for every page. Items marked `must` are blockers; items marked `should` are strong preferences.

### Document structure

- `must` — Exactly one `<h1>` per page. Matches the page's headline or primary goal.
- `must` — Heading hierarchy is strict: `<h1>` → `<h2>` → `<h3>`. Do not skip levels for styling.
- `must` — Landmark regions: `<header>`, `<nav>`, `<main>`, `<footer>`. One `<main>` per page. Named `<nav>` regions via `aria-label` if more than one exists.
- `must` — Skip-to-main-content link as the first focusable element. Visible on focus.
- `should` — Page `<title>` reflects the page's headline and distinguishes this page from others.
- `should` — `lang` attribute on `<html>` matches the content language.

### Keyboard access

- `must` — Every interactive element is reachable via Tab in a logical order (top-to-bottom, left-to-right by default).
- `must` — Focus indicator is visible on every interactive element. `outline: none` without a replacement is a blocker.
- `must` — No keyboard traps. User can always Tab out of a region or Esc a modal.
- `must` — Enter activates buttons and submits forms; Space activates buttons and toggles.
- `should` — Skip-links for long regions (e.g., "Skip to main content," "Skip to search").
- `should` — Keyboard shortcuts (if used) are documented and do not conflict with native browser or assistive-tech shortcuts.

### Focus management

- `must` — When a modal opens, focus moves into the modal and traps inside until closed.
- `must` — When a modal closes, focus returns to the triggering element.
- `must` — When a page-level error is shown after form submit, focus moves to the error summary or first invalid field.
- `must` — In a wizard, focus moves to the new step's heading on step change.
- `should` — When dynamic content loads (infinite scroll, lazy sections), focus does not jump unexpectedly.

### Color and contrast

- `must` — Body text: contrast ratio ≥4.5:1 against its background (WCAG AA).
- `must` — Large text (≥18 px bold, ≥24 px regular): ≥3:1.
- `must` — Non-text UI (icons, borders essential for identifying controls): ≥3:1.
- `must` — Information is not conveyed by color alone (add icon, pattern, or text).
- `should` — AAA (≥7:1) for body text where feasible; this is the practical default for accessibility-first brands.
- `should` — Contrast holds in dark mode, hover, focus, and disabled states.

### Text and typography

- `must` — Text can be resized to 200% without loss of content or functionality.
- `must` — Users can zoom to 400% without horizontal scrolling at 320 px wide (mobile reflow).
- `should` — Line length for body text: 60-80 characters per line.
- `should` — Line height for body text: ≥1.5×. Paragraph spacing: ≥2× font size.
- `should` — Never use font-sizes below 14 px for secondary text; 16 px for primary body.

### Forms

- `must` — Every input has a visible `<label>` associated via `for`/`id`. Placeholder text is not a label.
- `must` — Required fields are marked with both visual `*` and `aria-required` / native `required`.
- `must` — Error messages are announced via `aria-live="polite"` or linked via `aria-describedby`.
- `must` — Errors are not conveyed by color alone — include icon + text.
- `must` — Autocomplete attributes (`autocomplete="email"`, `"postal-code"`, `"given-name"`) for known field types.
- `should` — Field-level validation on blur (not on every keystroke).
- `should` — Group related fields with `<fieldset>` + `<legend>`.

### Images and media

- `must` — Every `<img>` has `alt` text: descriptive for meaningful images, empty (`alt=""`) for decorative.
- `must` — Icons used as buttons have `aria-label`.
- `must` — Video has captions; audio has a transcript.
- `must` — Auto-playing media has pause/mute controls and respects `prefers-reduced-motion`.
- `should` — Complex images (charts, diagrams) have a longer description via `aria-describedby` or a linked data table.

### Motion and animation

- `must` — `prefers-reduced-motion` respected. Parallax, auto-scroll, and animated transitions have a reduced alternative.
- `must` — Animations do not flash >3× per second (photosensitive epilepsy risk).
- `should` — Essential animations are under 500 ms; decorative animations can be disabled entirely under reduced-motion.

### Touch and target size

- `must` — Minimum target size: 24×24 px (WCAG 2.2 SC 2.5.8). 44×44 px is the practical standard for primary touch actions.
- `must` — Adjacent targets have enough spacing to avoid mis-taps (≥8 px between targets; more for edge-of-screen).
- `should` — Primary actions ≥44×44 px on all breakpoints.

### Dynamic content

- `must` — Live regions (toasts, inline validation, chat messages) use `aria-live` appropriately (`polite` for non-urgent, `assertive` for errors).
- `must` — Loading states announced via `aria-busy`.
- `should` — Skeleton loaders have `aria-busy="true"` so they're not read as content.

### Identity and consistency

- `must` — Focus order matches visual order.
- `must` — Interactive elements that look alike behave alike across the page (consistent buttons, consistent links).
- `should` — Don't use custom ARIA roles when a native HTML element works (`<button>` over `<div role="button">`).

## Per-archetype gotchas

Baseline checklist applies to every archetype. These additional items apply where called out.

### Landing

- Hero video / animation must respect `prefers-reduced-motion`; provide static poster.
- Primary CTA reachable within first 3-5 tab stops.
- Value prop is a real `<h1>`, not a styled `<div>`.
- Autoplaying carousels expose prev/next/pause controls; auto-pause on focus.
- Marketing overlays (newsletter modal, cookie banner) must not trap focus before content is accessible.

### Dashboard

- Charts/graphs have non-visual alternative (aria-label summary, or data-table toggle).
- Card grids group related actions under `role="group"` with arrow-key nav (avoid 30 tab stops).
- Skeleton loaders use `aria-busy`.
- Command palette (Cmd-K) is discoverable — do not rely only on keyboard shortcut. Include visible affordance (search icon, "Press / to search" hint).
- First-run empty state uses actual heading and action, not just decoration.

### Form

- No placeholders-as-labels.
- Error messages linked via `aria-describedby`.
- Required fields: visual `*` + `aria-required`.
- No auto-advance focus on input completion (breaks screen readers).
- Multi-field forms group with `<fieldset>` + `<legend>` where related.
- Submit button shows loading state and is disabled during submit.
- Success redirect or inline message; focus moves to confirmation.

### List + detail

- `<table>` with `<th scope>` for tabular data; "fake tables" in `<div>` lose semantics unless full ARIA grid roles wire up correctly.
- Sort changes announced via `aria-live`.
- Virtual scrolling breaks "find in page" — provide search or jump-to.
- Row actions are focus-revealed, not only hover-revealed.
- Side-panel detail views trap focus while open; restore focus on close.
- Filter chips announce applied filters to screen readers.

### Article

- Reading line length 60-80 characters.
- Strict heading hierarchy; one `<h1>`.
- Code blocks have visible copy button with `aria-label`.
- Figures use real `<figcaption>`.
- Dark-mode toggle persists `prefers-color-scheme` first, user override second.
- Skip-link to main content past nav + TOC.
- Reading-progress indicator does not overlap with headline.

### Wizard

- Step indicator exposed as a list; `aria-current="step"` on current.
- Focus moves to new step's heading on transition.
- Progress announced via `aria-live` on step change.
- Back navigation always available.
- Session timeout warning before expiry with extension option.
- No data loss on back.

### Settings

- Settings nav reachable in 1-2 tab stops.
- Collapsible sections use ARIA disclosure (`aria-expanded`, `aria-controls`).
- Toggle switches announce state ("Notifications, on"), not just "toggle."
- Destructive actions: icon + color + explicit verb (not color alone).
- Save feedback announced via `aria-live`.
- `<fieldset>` + `<legend>` for related input groups.

### Empty / error

- Headline is a real `<h1>` with human-readable summary (not just "404").
- Status code is secondary, not primary.
- Primary action reachable in first 1-2 tab stops.
- No auto-redirect with countdown (screen-reader users may not finish reading).
- For offline: service-worker cached fallback preferred over blank.
- 404 pages return HTTP 404, not 200 (breaks SEO and monitoring).

## How to state a11y in the artifact

The template's Accessibility section (see `assets/template-page-design.md`) should explicitly state:

1. **WCAG tier:** AA (default) or AAA (where applicable).
2. **Heading hierarchy:** the outline. "h1: page title → h2: main sections → h3: subsections."
3. **Landmark regions:** which are used and how labeled.
4. **Focus order:** list the first 5-10 tab stops explicitly.
5. **Contrast commitments:** body text ratio, interactive element ratio, dark mode parity.
6. **Target sizes:** minimum px for touch targets on mobile.
7. **Motion policy:** what respects `prefers-reduced-motion` and what the reduced alternative is.
8. **Screen-reader flow:** how the page reads top-to-bottom (the narrative a screen reader produces).
9. **Dynamic region policy:** which regions are `aria-live` and at which priority.
10. **Known a11y trade-offs:** anything accepted below the baseline, with reason in Open Questions.

Do not leave a11y as a bullet list of compliance items. Design it as part of the structure.
