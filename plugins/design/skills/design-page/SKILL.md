---
name: design-page
description: "Design the UI/UX structure of a single page and produce a markdown artifact at .product/design/pages/<slug>.md covering archetype, above-the-fold hierarchy, wireframe, component composition, states, interactions, responsive behavior, and accessibility. Triggers: '/design-page', 'design a page', 'design the [page name] page', 'design the UI for [page]', 'design the UX for [page]', 'wireframe a page', 'mockup the [page name] page', 'sketch out the [page name] page', 'map out the [page name] page', 'design a landing page', 'design a dashboard', 'design a settings page', 'design an onboarding page', 'design the checkout page', 'design a pricing page', 'design an error page', 'page layout for [page]', 'lay out the [page name] page', 'UI design for [page]', 'UX design for [page]', 'page-level design', 'now design this page', 'I have the website structure help me design a page', 'I have a feature spec design the page', 'design a form page', 'design a list view', 'design an article page', 'design an onboarding wizard', 'I need to design a specific page'. Scope: structure + UX only — not visual tokens (hand off to harness:write-design-system), website IA (design:design-website, usually upstream), or feature tech specs (design:design-spec)."
---

# Design Page

Produce a page-level design artifact: one page goal, one committed archetype, a ranked above-the-fold set, an ASCII wireframe, component composition tied to the design system, a state catalog per region, interaction specs, a responsive strategy per region, and accessibility commitments. The artifact lives at `.product/design/pages/<slug>.md` and feeds the design system, feature tech specs, and implementation.

This skill stops at *structure and UX*. It does not design visual tokens, website IA, or feature tech specs — those have their own skills (see [Hand-offs](#hand-offs)).

## Process

```
Step 1: Ingest upstream context      → Read .product/ artifacts if present
Step 2: Elicit missing strategy      → AskUserQuestion for what's missing
Step 3: Commit archetype             → Pick one from page-archetype-patterns.md
Step 4: Rank above-the-fold          → 3-5 elements, primary CTA named
Step 5: Draft wireframe              → ASCII per archetype (desktop + mobile)
Step 6: Specify component composition → From design system; flag missing
Step 7: Enumerate states per region   → Walk state-catalog.md
Step 8: Interactions, responsive, a11y → Three intertwined specs
Step 9: Edge cases & assemble         → Fill template, self-check rules
Step 10: Multi-axis review            → Always offer; proceed if user declines
```

Steps 1-10 are detailed in [`workflows/design-page.md`](workflows/design-page.md). Apply `rules/page-design-principles.md` per the per-step citations in the workflow (Steps 2, 3, 4, 5, 6, 7, 8, 9) and as a final gate at Step 9.

## Bundled resources

Rules, workflow, references, and asset bundled with this skill. Each entry says *what* it covers and *when* to read it.

**Rules**
- [`rules/page-design-principles.md`](rules/page-design-principles.md) — 10 hard rules that prevent generic LLM defaults in page design (archetype commitment, state enumeration, responsive specificity, a11y in-artifact, and more). **Load once at Step 1** and keep in context through Step 9; the workflow cites specific rules per step and the final Step 9 gate walks all 10.

**Workflows**
- [`workflows/design-page.md`](workflows/design-page.md) — step-by-step procedure for Steps 1-9 with stop conditions, branches, and edge cases. **Read at Step 1** and follow through Step 9.

**References**
- [`references/page-archetype-patterns.md`](references/page-archetype-patterns.md) — the 8 archetypes (landing, dashboard, form, list+detail, article, wizard, settings, empty/error) with canonical above-the-fold composition, mandatory states, canonical interactions, a11y gotchas, and common LLM failure modes per archetype. **Read at Step 3** when the archetype is committed; consult sections at Steps 4, 5, 7 when drafting ranking, wireframe, and states; and Step 9 when enumerating archetype-specific edge cases.
- [`references/state-catalog.md`](references/state-catalog.md) — mandatory baseline states (loading/empty/error/success/disabled) and conditional states (partial/offline/permission-denied/rate-limited/read-only/saving/conflict/unsaved-changes/JS-disabled/slow-network) with per-archetype include/exclude matrix. **Read at Step 7** when enumerating states per region.
- [`references/responsive-patterns.md`](references/responsive-patterns.md) — breakpoint stops, reflow patterns (stack/collapse/hide/swap/resize), per-region defaults, touch-vs-pointer affordances, common failure modes. **Read at Step 8** when committing the responsive strategy.
- [`references/a11y-checklist.md`](references/a11y-checklist.md) — WCAG 2.2 AA baseline + per-archetype gotchas + how to state a11y in the artifact. **Read at Step 8** when drafting the a11y section and again as a final gate at Step 9.
- [`references/wireframe-ascii-patterns.md`](references/wireframe-ascii-patterns.md) — ASCII wireframe conventions and per-archetype desktop + mobile templates. **Read at Step 5** when drafting the wireframe.

**Assets**
- [`assets/template-page-design.md`](assets/template-page-design.md) — the output artifact template. Page goal, audience & JTBD, archetype commitment, above-the-fold hierarchy, wireframe, component composition, state catalog, interactions, responsive behavior, accessibility, edge cases, metrics & events, open questions, hand-offs, changelog. **Use at Step 9** as the file scaffold.

## Hard constraints

Rules in `rules/page-design-principles.md` apply on every run; do not relax without the user's explicit instruction. The one orchestration constraint specific to this skill (not in the rules file): **Confirm before delegating** — Step 10 spawns review subagents; always ask the user and wait for confirmation before launching. When the user's request contains *some* in-scope work plus out-of-scope concerns (visual tokens, website IA, feature tech specs, microcopy, implementation), route the out-of-scope parts to the [Hand-offs](#hand-offs) table and continue with the in-scope structure+UX work. When the request is *entirely* out of scope, route to the relevant hand-off and stop — do not produce a partial page-design artifact to justify the skill firing.

## Step 10: Multi-axis review

Steps 1-9 conclude with the artifact written at `.product/design/pages/<slug>.md`. Before delivering, offer the user a parallel multi-axis review using the `design:page-design-reviewer` subagent (axes: `completeness`, `ux-quality`, `risk`). Do **not** launch reviewers without confirmation. Use the `AskUserQuestion` prompt, branching logic, and reconciliation steps in [`workflows/design-page.md`](workflows/design-page.md) § Step 10.

## Output location

Write the artifact to:

```
.product/design/pages/<slug>.md
```

`<slug>` is kebab-case derived from the page name (e.g., "Pricing page" → `pricing`, "Customer dashboard" → `customer-dashboard`, "404 page" → `not-found`). Create the `.product/design/pages/` directory if it does not exist.

## Hand-offs

After delivery, route the user to the right next-step skill based on what they want to do:

| User wants to… | Skill |
|---|---|
| Define visual design system (tokens, typography, components) | `harness:write-design-system` |
| Spec a feature's backend/frontend architecture | `design:design-spec` |
| Design the website's structure/IA (usually upstream) | `design:design-website` |
| Scaffold the implementation | `build:scaffold-project` |

## Edge cases & gotchas

All procedural and operational edge cases are handled in [`workflows/design-page.md`](workflows/design-page.md) § Edge cases.
