# Page Design Principles

Hard rules for every page-design artifact this skill produces. These exist because the default LLM response to "design a page" produces a generic three-section stack (hero + features + CTA) regardless of the page's purpose, audience, or place in the product. Each rule below blocks one of those default failures.

Apply on every run. Surface any deliberate violation in the artifact's Open Questions section.

**Severity tags.** Each rule below opens with a **Blocker** or **Required** tag. **Blocker** rules must be satisfied or the artifact fails the Step 9 self-check — deliver only with an Open Questions entry explaining the trade-off. **Required** rules are strong defaults that should be satisfied unless a specific context justifies deviation; document the justification.

## 1. Commit to ONE page goal before anything else

**Blocker.** A page has exactly one primary goal: convert · inform · enable-action · retain · recover. If the user names three, pick one and demote the rest to secondary. Multiple co-equal goals guarantee a flat page where everything is equally important and nothing stands out.

State the goal in a single sentence with a measurable outcome: "Get a cold visitor to request a demo," not "Educate users about the product." If the outcome isn't testable, it isn't a goal.

## 2. Commit to a page archetype before drafting layout

**Required.** Pick one archetype from `references/page-archetype-patterns.md`: landing · dashboard · form · list+detail · article · wizard · settings · empty-or-error. Archetype determines the canonical above-the-fold composition, the mandatory states, and the a11y gotchas. Drafting layout before committing an archetype locks you into a generic 3-column-stack template.

When the page plausibly fits two archetypes (e.g., a marketing landing page with a long-form article underneath), pick the *primary* (the one tied to the page goal) and design the secondary region inside it. Do not split into two archetypes in parallel.

## 3. Rank above-the-fold to exactly 3-5 elements

**Blocker.** The user sees the top of the page before scrolling — typically 600-800 px on desktop, 500-700 px on mobile. Rank the 3-5 elements that must live there, in strict order. Everything else scrolls. A flat "it's all important" top is indistinguishable from noise.

Primary CTA always appears in this ranked set. If it isn't in the top 5, either the CTA is weak or the ranking is wrong.

## 4. Name the primary CTA and its treatment explicitly

**Required.** Every page has exactly one primary CTA that serves the page goal. Name it in the artifact: its label, its visual weight ("solid high-contrast button"), its placement (above-the-fold, sticky on mobile, footer duplicate if scroll-heavy), and its state when disabled or unavailable.

Secondary CTAs are allowed but must be visually demoted (ghost button, text link, muted tone). Two visually-equal CTAs at the top = no CTA. If the page has no meaningful CTA (pure informational reading), state that explicitly — it forces you to reconsider whether the page has a goal.

## 5. Compose from the design system; never invent one-offs silently

**Required.** If a design system exists (`.product/design-system/*` or named by the user), compose every component from it. When a primitive is missing, say so explicitly and request its addition — do not invent a one-off inline.

If no design system exists yet, name the components you need (e.g., "card-with-icon," "segmented-control," "inline-validation"), but surface in Open Questions that these should either be added to `harness:write-design-system` work or remain page-local for now.

## 6. States are first-class, not bolted on

**Blocker.** For every data-driven region of the page, enumerate the full state catalog from `references/state-catalog.md` that applies: loading · empty · partial · error · success · disabled · permission-denied · offline · rate-limited · read-only. Design each mandatory state, not just the happy path.

The test: if a user sees this region with zero data, zero permissions, or a failed fetch, what do they see? If the answer is "I don't know," the design is incomplete. Roughly 40% of real page design is non-happy-path.

## 7. Commit to a responsive strategy before drafting layout

**Required.** Pick one: mobile-first · desktop-first. State the primary breakpoints (default: 640 / 768 / 1024 / 1280). For each breakpoint, declare the reflow rule (stack, collapse, hide, swap-component) for every major region of the page. Patterns live in `references/responsive-patterns.md`.

"It's responsive" without explicit reflow rules is not a design — it's a hope. Touch targets must be ≥44×44 px on the mobile viewport; state this as a hard constraint on any interactive element.

## 8. Accessibility in the artifact, not in the ticket

**Blocker.** For every page, declare in the artifact: color-contrast tier (AA minimum for body text, AAA where feasible), focus order, keyboard reachability of every interactive element, screen-reader flow (heading levels, landmark regions, aria-live for dynamic regions), reduced-motion handling, and minimum target sizes. Apply the per-archetype gotchas in `references/a11y-checklist.md`.

Do not defer a11y to the implementation — by then the structural decisions (heading order, landmark choice, focus trap location) are locked. A page design without a11y is not done.

## 9. Enumerate edge cases per archetype

**Required.** Walk the archetype-specific edge cases from `references/page-archetype-patterns.md` (e.g., landing: no-JS fallback, slow-network; dashboard: zero-records first-run, permission-subset; form: field-level validation, auto-save conflict). Decide *handle* / *defer with reason* for each. Do not hand-wave "we'll handle edge cases later."

The edges that recur across archetypes (404/403 landing, offline, slow third-party, JS disabled) should always appear in the artifact's Edge Cases section.

## 10. Specify interactions per primary element

**Required.** For every interactive element in the above-the-fold ranking (CTA, form field, filter, tab, menu, modal trigger), specify: the trigger (click · hover · focus · keyboard · swipe), the response (navigation · inline update · modal · toast · validation), the affordance (cursor · underline · color-shift), and the keyboard equivalent. "Button clicks and does the thing" is not a specification.

For multi-step interactions (menus, modals, inline forms with async validation), draw the interaction as a mermaid `stateDiagram-v2` in the artifact. The diagram surfaces missing states faster than prose.
