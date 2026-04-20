---
name: design-website
description: "Design the site-wide structure (sitemap, page inventory, navigation/IA, cross-page user flows) for a web product — site structure only, not page layouts or visual design. Produces a markdown artifact with mermaid diagrams at .product/design/websites/<slug>.md. Hands off page-level layout to design:design-page, visual tokens to harness:write-design-system, and feature tech specs to design:design-spec. Triggers: '/design-website', 'design the website structure', 'design the structure of [website]', 'figure out the structure for [site]', 'design the IA', 'redesign the website structure', 'redesign the IA', 'plan the pages for [product]', 'plan out the pages for [site]', 'lay out the website', 'sitemap for [site]', 'information architecture for [product]', 'map out the pages and navigation for [site]', 'website IA', 'landing site structure', 'structure for our e-commerce site', 'what pages does an online store need', 'what pages should [site] have', 'figure out the pages for [site]', 'how should the pages of [site] connect', 'now I need the website structure', 'I have a PRD, help me design the website'."
---

# Design Website

Produce a website-level design artifact: sitemap, page inventory tied to user JTBDs, a committed navigation paradigm, the top 3-5 cross-page user flows, and an enumerated set of edge pages. The artifact lives at `.product/design/websites/<slug>.md` and feeds page-level design, feature specs, and implementation.

This skill stops at *structure*. It does not design page layouts, visual tokens, or feature tech specs — those have their own skills (see [Hand-offs](#hand-offs)).

## Process

```
Step 1: Ingest upstream context     → Read .product/ artifacts if present
Step 2: Elicit missing strategy     → AskUserQuestion for what's missing
Step 3: Commit site type            → Pick one from site-type-patterns.md
Step 4: Derive page inventory       → JTBD-first, not template-first
Step 5: Commit nav paradigm         → One choice, justified
Step 6: Walk top 3-5 flows          → Mermaid each end-to-end
Step 7: Enumerate edge pages        → Walk edge-pages-checklist.md
Step 8: Assemble & write artifact   → Fill template-website-design.md
Step 9: Self-check against rules    → Walk ia-principles.md
Step 10: Multi-axis review (opt-in) → Confirm with user, then launch reviewers
```

Steps 1-9 are detailed in [`workflows/design-website.md`](workflows/design-website.md). Step 10 lives in this file (see [Step 10: Multi-axis review](#step-10-multi-axis-review)). Apply `rules/ia-principles.md` per the per-step citations in the workflow (Steps 4, 5, 6, 7) and as a final gate at Step 9.

## Bundled resources

Rules, workflow, references, and asset bundled with this skill. Each entry says *what* it covers and *when* to read it.

**Rules**
- [`rules/ia-principles.md`](rules/ia-principles.md) — 10 hard rules that push the design off generic LLM defaults (commit a site type, derive from JTBDs, one nav paradigm, edge pages first-class, etc.). **Read once at Step 1**; the workflow cites specific rules at Steps 4, 5, 6, and 7; walk all 10 as a final gate at Step 9.

**Workflows**
- [`workflows/design-website.md`](workflows/design-website.md) — step-by-step procedure for Steps 1-9 with stop conditions, branches, and edge cases. **Read at Step 1** and follow through Step 9.

**References**
- [`references/site-type-patterns.md`](references/site-type-patterns.md) — the 8 site types (marketing, SaaS, e-commerce, content, docs, portfolio, community, internal tool) with canonical page inventory, dominant nav paradigm, common flows, and type-specific gotchas per type. **Read at Step 3** when the site type is committed; consult sections at Steps 4-6 when drafting inventory, nav, and flows.
- [`references/sitemap-mermaid-patterns.md`](references/sitemap-mermaid-patterns.md) — mermaid templates for sitemaps (`flowchart TD`), nav models (`flowchart LR` with subgraphs), user flows (`flowchart` and `sequenceDiagram`), and URL/route trees. **Read at Steps 5-6 and 8** when drawing diagrams. § Worked examples contains 5 annotated patterns (marketing sitemap, SaaS app sitemap, top SaaS flow, e-commerce conversion flow, docs nav model) — consult these before producing any new diagram.
- [`references/edge-pages-checklist.md`](references/edge-pages-checklist.md) — catalog of edge pages by category (errors, auth, empty states, confirmations, system state, legal, localization) with an include/exclude matrix per site type. **Read at Step 7** to enumerate edge pages.

**Assets**
- [`assets/template-website-design.md`](assets/template-website-design.md) — the output artifact template. Strategy preamble, site-type/nav commitment, sitemap, page inventory table, route shape, flows, edge pages, design principles, open questions, hand-offs, changelog. **Use at Step 8** as the file scaffold.

## Hard constraints

Rules in `rules/ia-principles.md` apply on every run; do not relax without the user's explicit instruction. The one orchestration constraint specific to this skill (not in the rules file): **Confirm before delegating** — Step 10 spawns review subagents; always ask the user and wait for confirmation before launching. When asked for surface-plane work (visual design, page layouts, feature tech specs), route to the [Hand-offs](#hand-offs) table and continue with structure-plane work.

## Step 10: Multi-axis review

Steps 1-9 conclude with the artifact written at `.product/design/websites/<slug>.md`. Before delivering, offer the user a parallel multi-axis review using the `design:website-design-reviewer` subagent (axes: `coverage`, `ia-quality`, `risk`). Do **not** launch reviewers without confirmation. Use the `AskUserQuestion` prompt, branching logic, and reconciliation steps in [`workflows/design-website.md`](workflows/design-website.md) § Step 10.

## Output location

Write the artifact to:

```
.product/design/websites/<slug>.md
```

`<slug>` is kebab-case derived from the site name (e.g., "Acme Marketing Site" → `acme-marketing-site`). Create the `.product/design/websites/` directory if it does not exist.

## Hand-offs

After delivery, route the user to the right next-step skill based on what they want to do:

| User wants to… | Skill |
|---|---|
| Design a single page's UI/UX (layout, components, states) | `design:design-page` |
| Define visual design system (tokens, typography, components) | `harness:write-design-system` |
| Spec a feature's backend/frontend architecture | `design:design-spec` |
| Scaffold the implementation | `build:scaffold-project` |
| Decide what to build first within the new IA | `define:slice-mvp` |
| Capture additional product signals from this design | `discover:capture-signal` |

## Edge cases & gotchas

Procedural edges (cold start, hybrid sites, redesigns, oversized sites, deferred personas, surface-plane requests) are handled in [`workflows/design-website.md`](workflows/design-website.md) § Edge cases at the level of detail those steps need. Skill-level operational notes:

- **Mermaid renderers vary** — Stick to the diagram types in `references/sitemap-mermaid-patterns.md` (`flowchart`, `sequenceDiagram`, `stateDiagram-v2`); avoid newer types not yet supported by common viewers.
- **`.product/` directory may not exist** — Some repos do not yet have it. Create the full `.product/design/websites/` path on first write rather than failing.
- **User wants to write the artifact under a different path** — Honor the override but record the chosen path in the changelog row so subsequent iterations can find it.
