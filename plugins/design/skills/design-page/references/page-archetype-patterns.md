# Page Archetype Patterns

Canonical above-the-fold composition, mandatory states, core interactions, and archetype-specific a11y gotchas — by archetype. Archetype is the single biggest variable in page-level design; commit to one before drafting layout.

Every design must adapt the default shape to the specific page goal, audience, and JTBD captured in the artifact's preamble. The patterns below are starting points that block the generic-three-section-stack default, not templates to copy verbatim.

## Contents

1. [Choosing an archetype](#choosing-an-archetype)
2. [Landing](#1-landing)
3. [Dashboard](#2-dashboard)
4. [Form](#3-form)
5. [List + detail](#4-list--detail)
6. [Article / content](#5-article--content)
7. [Wizard / multi-step](#6-wizard--multi-step)
8. [Settings](#7-settings)
9. [Empty / error](#8-empty--error)
10. [Hybrid pages](#hybrid-pages)

## Choosing an archetype

Pick exactly one **primary** archetype. Use this matrix when the choice isn't obvious:

| If the page's primary goal is... | Archetype |
|---|---|
| Convert a cold or warm visitor to a next step (sign up, demo, buy, subscribe) | Landing |
| Surface in-progress work, metrics, or next actions for an authenticated user | Dashboard |
| Capture user input that gets submitted as a unit (contact, checkout, account creation) | Form |
| Browse a collection and drill into one item | List + detail |
| Read a single long-form unit of content (blog post, docs guide, news article) | Article |
| Walk the user through a multi-step process they cannot complete in one view | Wizard |
| Let a user configure account, workspace, or app preferences | Settings |
| Represent the absence of content, permission, or connectivity | Empty / error |

Adjacent: when the answer is "two of the above are equally important," the page is probably doing too much — split it or demote one goal to secondary and design under the primary archetype.

---

## 1. Landing

**Page goal.** Convince a visitor to take the primary CTA (sign up, request demo, buy, subscribe). The visitor typically arrived from search, ads, social, or a deep link — they may have never seen this product before.

**Canonical above-the-fold ranking (top 5).**

1. Value proposition (one sentence, scannable in <3 seconds)
2. Primary CTA (solid high-contrast button, specific label — not "Learn More")
3. Supporting visual or product screenshot (not a decorative photo)
4. Proof anchor (logo strip, one testimonial quote, or a single headline metric)
5. Secondary CTA (text link or ghost button — "See how it works" / "Pricing")

Everything else scrolls: features, social proof, deep product explanations, FAQ, footer.

**Mandatory states.**

- Happy path (above the fold renders fully)
- JS disabled (value prop + CTA must still work; no JS-only hero)
- Slow network (visual placeholder, not layout shift; content-first render order)
- Third-party block (analytics, chat widget, video embed fails silently without breaking the page)
- Logged-in variant (if the site has auth — usually a "Go to app" CTA instead of "Sign up")

**Canonical interactions.**

- Primary CTA → form modal or destination page (specify which, and loading state)
- Hover on supporting visual → ideally no interaction; resist parallax and auto-playing video
- Scroll → fade-in or reveal animations allowed if motion-reduced alternative is provided
- Sticky nav on scroll (common; specify breakpoint behavior)

**Archetype-specific a11y gotchas.**

- Hero video or animation must respect `prefers-reduced-motion`. Provide a static poster image fallback.
- Primary CTA must be focusable and reachable via Tab within the first 3-5 tab stops (not buried after a decorative sub-nav).
- Value prop must be a real `<h1>`, not a styled `<div>` — screen readers and SEO both depend on it.
- Autoplaying carousels are a known a11y failure; if used, expose pause/prev/next controls and auto-pause on focus or `prefers-reduced-motion`.

**Common LLM failure modes to avoid.**

- Hero + three feature tiles + testimonials + FAQ + CTA, copy-pasted regardless of audience.
- Generic stock phrases in the value prop ("Empower your team to...", "The all-in-one platform for...").
- Two co-equal primary CTAs ("Sign up free" AND "Book a demo" at the same visual weight) that cancel each other out.
- Feature lists that describe the product instead of the user's outcome.

---

## 2. Dashboard

**Page goal.** Orient an authenticated user to their in-progress work and route them to their next action within seconds. The user returns here repeatedly — optimize for recognition, not novelty.

**Canonical above-the-fold ranking (top 5).**

1. Identity / context strip (workspace name, current view, active filters if any)
2. Primary next-action surface (resume in-progress work, or "what to do next" tile)
3. Key metrics or status (1-3 numbers; not a wall of charts)
4. Recent activity or queue (a short list, not an infinite feed)
5. Global search / command palette entry (always visible, even if collapsed into a shortcut)

Everything else (settings links, secondary metrics, marketing nudges) is below the fold.

**Mandatory states.**

- Populated (the default after a few uses)
- First-run / zero-data (new user has no activity yet — empty states are load-bearing)
- Partial data (some widgets loaded, some still fetching)
- Degraded (one or more data sources failed; show partial data + inline error, not full-page crash)
- Permission-subset (user has some roles but not others — gated widgets show locked state, not blank)
- Offline (last-known data with clear staleness indicator)

**Canonical interactions.**

- Card click → detail view (specify: same-tab navigation, modal, or side panel)
- Metric click → drill-down view or filter applied
- Keyboard shortcut surface (Cmd-K or /) opens command palette; specify the discoverability affordance
- Filter changes → URL updates so the view is shareable/reloadable
- Inline actions on activity items (mark done, dismiss, assign) — specify trigger, response, and undo

**Archetype-specific a11y gotchas.**

- Heading hierarchy is critical — the page usually has nested regions; use `<section>` with accessible names, not bare `<div>`.
- Charts/graphs must have a non-visual alternative (aria-label, summary text, or a data table toggle).
- Skeleton loaders need `aria-busy` so screen readers don't announce placeholders as content.
- Keyboard users must be able to reach every interactive card without 30 tab stops — group related actions under `role="group"` with a single tab stop + arrow-key nav.

**Common LLM failure modes to avoid.**

- A wall of 12 chart widgets that tries to be useful to everyone and serves no one.
- Welcome banners and feature tours permanently occupying above-the-fold after week one.
- Activity feeds that default to infinite scroll with no anchor, so the user never feels "done."
- No zero-state design (new user sees an empty dashboard and bounces).

---

## 3. Form

**Page goal.** Capture user input with minimum friction and submit it as a unit. Every field is a friction point; every error is an abandonment risk.

**Canonical above-the-fold ranking (top 5).**

1. Page title + one-sentence explanation of what will happen on submit
2. First field (focused on load, with clear label)
3. Progress indicator (if multi-step — otherwise skip)
4. Primary submit CTA (visible even when fields are tall — usually sticky on mobile)
5. Trust / reassurance anchor (privacy note, security badge, time-to-complete estimate) when the ask is sensitive (payment, PII)

Field groups, secondary options, and help text fill the middle.

**Mandatory states.**

- Empty (fresh load)
- In-progress (fields partially filled; validation not yet triggered)
- Field-level validation error (inline, per field, with focus management)
- Field-level success (if applicable — uniqueness check, email verification)
- Submitting (button disabled, spinner, no double-submit)
- Server error on submit (form retains values; error message specific)
- Success / thank-you (either in-page replacement or redirect — specify)
- Auto-save conflict (if auto-save is used — user edits on two tabs)
- Permission / plan limit hit (if the action is gated)

**Canonical interactions.**

- Field focus → label animates (if floating) or help text appears
- Field blur → validate; on error, show inline, link error to field via `aria-describedby`
- Submit → disable button, show spinner, prevent double-submit, restore on error
- Tab order strictly top-to-bottom, left-to-right; no traps
- Enter key submits on single-field forms; is disabled on multi-line fields

**Archetype-specific a11y gotchas.**

- Every input needs a visible `<label>`, not just placeholder text. Placeholders disappear on focus; labels do not.
- Error messages must be announced via `aria-live="polite"` or linked via `aria-describedby` on the field.
- Required fields must be marked with both visual `*` and `aria-required="true"` / native `required`.
- Do not rely on color alone for error state — combine color + icon + text.
- Do not auto-advance focus on input completion (e.g., SMS code) unless clearly signaled; it traps screen-reader users.
- Autocomplete attributes (`autocomplete="email"`, `autocomplete="postal-code"`) are an a11y and usability requirement for known field types, not a polish item.

**Common LLM failure modes to avoid.**

- Asking for every field "just in case" instead of the minimum required set.
- Placeholders masquerading as labels.
- Submit button at the bottom of a long form with no sticky duplicate (mobile-killer).
- Generic "Something went wrong" error instead of field-specific guidance.
- No distinct server-error vs. validation-error state.

---

## 4. List + detail

**Page goal.** Let the user scan a collection, narrow it by filter/search/sort, and drill into one item — then return to the same scroll position with state preserved.

**Canonical above-the-fold ranking (top 5).**

1. Search / filter bar (primary navigation for this archetype)
2. Sort + view-mode toggles (list / grid / compact)
3. First row(s) of the collection (at least 3-5 items visible)
4. Primary action on each item (click-through; hover-reveal actions are risky on touch)
5. Pagination or load-more anchor (set expectation: total count visible)

Detail view is a separate concern — specify whether it is a navigation (same-tab), a modal, a side-panel, or a split-view.

**Mandatory states.**

- Populated (default)
- Empty (no items yet — first-run CTA)
- Filtered-to-empty (user's filter returned zero — distinct from "no data yet"; offer "clear filters")
- Loading (initial fetch + incremental page fetch — distinguish skeleton from spinner)
- Partial-data / failed fetch (show what loaded + inline retry)
- Permission-subset (some rows are visible, some locked — indicate)
- Selected / multi-select (if bulk actions exist)
- Detail pane: loading · not-found · permission-denied · success

**Canonical interactions.**

- Filter change → URL updates → reloadable/shareable; scroll position maintained
- Row click → detail (specify: navigation vs modal vs side panel); back preserves scroll
- Hover row → subtle affordance (background tint, not drastic shift); touch devices get always-on affordances
- Keyboard navigation: up/down arrow moves selection, Enter opens detail, Esc closes modal/panel
- Bulk select (if supported): shift-click range, Cmd/Ctrl-click toggle, checkbox column

**Archetype-specific a11y gotchas.**

- Tables must use `<table>` with `<th scope>` for screen readers; "fake tables" in `<div>` lose semantics unless ARIA roles are wired correctly.
- Large lists need virtual scrolling for performance, but virtualization breaks "find in page"; provide a search or jump-to input.
- Sort changes must announce the new order via `aria-live`.
- Hover-only actions fail for keyboard and touch users; make item actions focus-revealed too.
- Side-panel or modal detail views must trap focus while open and restore focus on close.

**Common LLM failure modes to avoid.**

- Infinite scroll with no URL state, so reloading loses position.
- Treating filtered-empty and no-data-yet as the same empty state.
- Drop-down menus of sort/filter with no applied-filter chips (user forgets what's filtered).
- Hover-only action buttons that are invisible to keyboard and touch users.

---

## 5. Article / content

**Page goal.** Deliver one long-form unit of content (blog post, docs guide, news article, case study) in a reading-optimized layout, and route the finished reader to the next meaningful action.

**Canonical above-the-fold ranking (top 5).**

1. Headline (real `<h1>`, legible and scannable)
2. Byline + publication date + reading time
3. Hero visual or lede (one, not a carousel)
4. First paragraph (the lede — weighted as important as the headline)
5. Table of contents (for pieces >1500 words) or "In this article" anchor block

Subheads (`<h2>`, `<h3>`), pull quotes, code blocks, figures, and related-content modules fill the body.

**Mandatory states.**

- Fully rendered (the default)
- JS disabled (content must still be readable — print view should also work)
- Paywall (soft / metered / hard — if applicable)
- Subscriber vs. non-subscriber view
- Draft / unpublished (if CMS surfaces a preview state)
- Comments loading / disabled / moderated (if comments exist)
- Related-content failed to load (article still readable)

**Canonical interactions.**

- Scroll → reading progress indicator (optional); TOC highlights current section
- Anchor link click → smooth scroll, URL updates
- Code block → copy-to-clipboard button with confirmation
- Image / figure click → lightbox (optional; specify behavior)
- Share → prepopulated tweet/email intent (do not use custom popup modal)

**Archetype-specific a11y gotchas.**

- Reading line length: aim for 60-80 characters per line; wider than that hurts low-vision readers.
- Heading hierarchy must be strict: one `<h1>`, subsections `<h2>`, then `<h3>`. Don't skip levels for styling.
- Code blocks need a visible copy button with `aria-label`, not only hover-revealed.
- Figures need real `<figcaption>`, not inline prose below.
- Dark-mode / light-mode toggle must persist in `prefers-color-scheme` first, user override second.
- For long pieces, provide a skip-link to main content that bypasses nav + TOC.

**Common LLM failure modes to avoid.**

- Sidebar ads or related-content rails that break reading flow without clear separation.
- Auto-playing video embeds that hijack scroll.
- Pop-up newsletter modal appearing before the user has read anything.
- Reading-progress bar that overlaps with the headline at the top.
- TOC that becomes stale if anchors are renamed — use auto-generated TOC tied to headings.

---

## 6. Wizard / multi-step

**Page goal.** Walk a user through a process with clear state, clear progress, and safe recovery from mid-flow exits. Used for onboarding, checkout, complex configuration, and anything that cannot be completed in one view.

**Canonical above-the-fold ranking (top 5).**

1. Step indicator (e.g., "Step 2 of 4: Billing") — must be accurate and clickable for completed steps
2. Current step heading and one-sentence explanation
3. Field or input for the current step (focused on entry)
4. Primary action (Continue / Next) + Back action
5. Exit / save-and-come-back affordance

Summary / sidebar is often to the right on desktop and collapsible/hidden on mobile.

**Mandatory states.**

- Step 1 fresh start (no prior data)
- Mid-flow resume (user left, returned — specify how state is reconstituted: URL params, server-side session, local storage)
- Validation failure (per step, before allowing Next)
- Back to a completed step (must preserve entered data; editing may invalidate downstream steps — specify)
- Abandoned mid-flow (user closes tab — what happens to partial data? auto-save? 24h expiry?)
- Final submit (distinguished from intermediate Continue — often "Confirm and pay" / "Finish")
- Post-completion (success view + what-happens-next)
- Error at final submit (retain all prior steps; show error near the action)

**Canonical interactions.**

- Back → preserves forward-step data so the user can return without re-entering
- Next → validates current step, transitions to next, updates step indicator, updates URL (e.g., `?step=2` or `/wizard/step-2`) for reload/share
- Step indicator click on a completed step → jumps back (allowed); on a future step → disabled (not allowed)
- Exit mid-flow → confirmation dialog if data would be lost
- Keyboard: Enter advances on single-field steps; on multi-field steps, Enter in the last field advances

**Archetype-specific a11y gotchas.**

- Step indicator must be exposed as a list with `aria-current="step"` on the current step.
- Focus must move to the new step's heading on transition (users otherwise lose their place).
- Progress announcement via `aria-live` on step change.
- Do not trap users on a step if they need to fix an earlier step — always allow back navigation.
- Time-limited steps (session timeouts) must warn before expiry and allow extension.

**Common LLM failure modes to avoid.**

- No URL-based step state, so reload restarts the flow.
- Vague progress indicator (dots without labels).
- Data loss on back navigation.
- Re-asking for info the user already provided earlier in the flow.
- No distinct "final submit" vs. intermediate "next" — user fears accidentally charging their card.

---

## 7. Settings

**Page goal.** Let an authenticated user configure account, workspace, or app preferences. Settings are read rarely, edited rarely, and searched often — they are the "control panel" of the product.

**Canonical above-the-fold ranking (top 5).**

1. Settings nav (tree, tabs, or side list — pick one, usually side on desktop)
2. Current section heading + one-sentence explanation
3. Primary setting cluster (usually the most-edited field — e.g., display name, notification preferences)
4. Save / confirm action (if explicit saves are used — specify inline vs bottom sticky)
5. Search within settings (if >10 sections — required)

Destructive actions (delete account, leave workspace, reset data) go in a visually-demoted, color-coded region at the bottom — never above the fold.

**Mandatory states.**

- Unsaved changes (dirty form — warn before navigation away)
- Saving / saved (per-field inline or global bottom bar)
- Save failed (field-level or global; specify retry)
- Permission-gated section (some settings visible only to owners/admins — show disabled state, not absent)
- Plan-gated section (feature requires upgrade — show locked state with upgrade path)
- Destructive action confirmation (multi-step: button → modal → type-to-confirm for irreversibles like "delete account")
- Read-only state (for non-owner members viewing owner-only settings)

**Canonical interactions.**

- Inline edit vs explicit save — commit to one model per form (do not mix)
- Toggle change → optimistic update → rollback on error with clear message
- Destructive action → typed confirmation (e.g., "type DELETE") for anything irreversible
- Section nav click → URL updates; deep-linkable settings pages
- Search within settings → fuzzy match across labels and help text

**Archetype-specific a11y gotchas.**

- Settings nav must be reachable in 1-2 tab stops; collapsible sections need ARIA disclosure semantics.
- Toggle switches must have a visible label and announce state ("Notifications, on" / "Notifications, off"), not just "toggle."
- Destructive action confirmations must not rely on color alone (red button) — include an icon + explicit verb.
- Feedback on save (toast) must be announced via `aria-live`.
- Form groups must use `<fieldset>` + `<legend>` where multiple related inputs share context.

**Common LLM failure modes to avoid.**

- A single scrolling mega-form of every setting the product has.
- Destructive actions above the fold or next to benign saves.
- Plan-gated features hidden entirely (user discovers only by accident) vs shown-with-upgrade (clear path).
- Save affordance that is inconsistent across sections (some inline, some explicit, some auto-save — pick one).

---

## 8. Empty / error

**Page goal.** Represent the absence of content, permission, or connectivity in a way that (a) tells the user what happened, (b) offers a next action, (c) preserves trust. These pages are often designed last and show it.

**Canonical above-the-fold ranking (top 5 — tight; these pages are short by design).**

1. One-line plain-language headline ("Nothing here yet" / "You don't have access" / "We couldn't load this")
2. One or two sentences of context (why, and whether it's temporary)
3. Primary action (the most useful next step — "Create your first project," "Request access," "Retry," "Go home")
4. Secondary action or link (help docs, status page, support)
5. Illustration or icon (optional; do not let visuals out-weigh the message)

Footer nav should be present on public-facing error pages; the site's global nav should still work.

**Mandatory states — these ARE the states.**

- First-run empty (no data yet — user is new)
- Filtered-to-empty (user's filter/search returned zero — distinct from "no data")
- Permission-denied (403 / plan-required / workspace-scoped lack of access)
- Not-found (404 — the URL does not resolve)
- Server error (500 — something broke on our end)
- Rate-limited / throttled (user or their IP hit a limit)
- Offline / network failure (client-side connectivity)
- Maintenance (planned downtime)

Each of these is a distinct page or page-state; conflating them confuses users and breaks SEO (404 should return 404, not 200).

**Canonical interactions.**

- Primary action → the likeliest useful destination (for 404: home or search; for 403: request access flow; for 500: retry + status page; for empty: create first record)
- Retry (on 500 / network error) → re-attempt the original request, not a page reload
- Help link → targeted help page, not a generic contact form
- No animation or wait states — users are already frustrated; keep it instant

**Archetype-specific a11y gotchas.**

- Headline must be a real `<h1>` with the human error summary, even if a numeric code is shown.
- Status codes (404, 500) must not be the most prominent element — humans need the explanation first.
- Primary action button must be reachable via the first 1-2 tab stops.
- Do not use auto-redirect after a countdown — users on screen readers may not finish reading before redirect.
- For offline: provide a cached fallback when possible (service worker) rather than a blank state.

**Common LLM failure modes to avoid.**

- Generic "Oops! Something went wrong" without explaining what or what to do next.
- Humor or cute illustrations on a server-error page where the user just lost their work.
- A 404 page with no search and no link home — a dead end.
- Conflating filtered-to-empty with no-data-yet — users see "Create your first" when they just applied a filter.
- Returning HTTP 200 on a 404 page (breaks SEO and monitoring).

---

## Hybrid pages

Many real pages combine archetypes. Common combinations and how to handle them:

| Combination | Approach |
|---|---|
| Landing + form (e.g., "Request demo" landing with inline form) | Primary archetype is Landing; the form is a region inside it. Apply landing a11y/states to the page; apply form a11y/states to the form region only. |
| Dashboard + list+detail (dashboard whose primary widget is a list) | Primary archetype is Dashboard; the main widget adopts list+detail patterns internally. |
| List + wizard (list of items, each with an inline multi-step edit) | Primary archetype is List+detail; the edit flow is a wizard inside a side-panel or modal. |
| Article + form (long-form content + subscribe form) | Primary archetype is Article; the form is a demoted CTA region, not the page's primary goal. |
| Settings + wizard (onboarding into settings) | Primary archetype is Wizard during onboarding; transitions to Settings after completion. |

**Rule:** name a primary archetype and apply its canonical composition and mandatory states to the page. Secondary regions inherit the primary's a11y baseline + their own region-specific gotchas. Do not design two parallel archetypes on the same page — that means the page is doing two jobs and should be split.
