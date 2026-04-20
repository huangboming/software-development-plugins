# Information Architecture Principles

Hard rules for every website-design artifact this skill produces. These exist because the default LLM response to "design a website" produces a generic 7-page template (Home / About / Services / Blog / Contact / Pricing / FAQ) regardless of context. Each rule below blocks one of those default failures.

Apply on every run. Surface any deliberate violation in the artifact's Open Questions section.

## 1. Commit to a site type before drafting the sitemap

Pick one site type from `references/site-type-patterns.md` before writing any pages into the inventory. Site type determines the canonical page set, the nav paradigm, and which edge pages apply. Drafting the sitemap first locks you into a generic shape.

When the user names a site that fits two types equally (e.g., marketing + SaaS), pick the *primary* and treat the secondary as a separate surface. Do not blend them.

## 2. Derive the page inventory from user JTBDs, not from a template

For every page, name the JTBD it serves. If a page does not map to a stated user job or a stated business outcome, cut it. Conversely, if a JTBD has no page or flow that delivers it, add the missing page.

The first pass should start from "what's the shortest path from each persona's entry point to their goal?" — not from "what pages do sites usually have?"

## 3. One page = one primary job

If a page serves three different user jobs, split it. If ten pages answer variants of the same question, consolidate them. A page should have a single answer to "what is this page for?"

When a page legitimately has secondary jobs (e.g., a PDP also handles related-products and reviews), call them out explicitly so they're not weighted equally with the primary job.

## 4. Commit to one navigation paradigm

Pick exactly one: top nav · side nav · hybrid top + side · search-first · command-palette-primary. Mixing paradigms (e.g., top nav AND a permanent left side nav AND a floating menu) leaks cognitive load and signals indecision.

State the choice in the artifact's nav section with a one-sentence justification. Mega menus are a top-nav variant, not a separate paradigm.

## 5. Treat every page as a potential landing page

Most users do not enter through the home page — they arrive on deep links from search, social, email, or in-product help. Every page must answer:

- Where am I? (page title and breadcrumb-equivalent)
- What can I do here? (primary action)
- Where else can I go? (related navigation)

For marketing and content sites in particular, design the long-tail page (PDP, blog post, docs guide) as carefully as the home page.

## 6. Edge pages are first-class IA, not afterthoughts

Walk `references/edge-pages-checklist.md` and decide *include* or *exclude with reason* for each category. At minimum every site needs: 404, 500, privacy policy, terms of service. Most public sites also need cookie consent and an accessibility statement.

If you exclude an edge page, justify it in Open Questions so a reviewer can challenge the call.

## 7. Walk the top 3-5 user flows end-to-end

The sitemap shows structure; flows reveal whether the structure works. Pick the 3-5 highest-leverage journeys (one per top JTBD) and walk each from entry point to success condition as a mermaid diagram. If a flow can't be drawn without invented intermediate pages, the IA is missing something — fix the IA, not the flow.

Cap at 5 flows. More than that is a sign the site is doing too many things and IA needs decomposition.

## 8. Name the one business outcome the site optimizes for

Demand a single primary metric: trial-to-paid conversion, qualified demos, weekly active users, support-ticket deflection, etc. Multiple metrics in tension produce IA that serves none of them well.

Secondary metrics are fine as guardrails, but the primary one drives nav placement and CTA priority.

## 9. Stay in scope: structure, not surface

This skill produces *structure-plane* artifacts (Garrett's planes 1-3): user/business strategy, content scope, IA. It does NOT design:

- Visual design — tokens, color, typography, spacing (handed off to `harness:write-design-system`)
- Single-page layouts and component composition (handed off to a future `design-page` sibling skill)
- Feature-level technical architecture (handed off to `design:design-spec`)
- Copywriting or content (out of marketplace scope)

If the user asks for any of the above, surface the right hand-off and continue with what's in scope. Do not stretch into surface-plane work.

## 10. Design for growth

Every IA must accommodate plausible new content without restructuring. Before finalizing, ask: "What happens when we add a new product, a new section, or a new locale?" If the answer is "we re-architect the nav," the current IA is brittle — surface it as an Open Question or revise.

Brittleness shows up as: hard-coded nav order, sections that depend on exactly N children, top-level slots reserved for marketing campaigns.
