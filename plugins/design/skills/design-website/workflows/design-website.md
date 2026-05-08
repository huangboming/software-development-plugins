# Workflow: Design a Website (Website-Level)

End-to-end procedure for producing a website-design artifact. Steps are ordered; each step produces an input the next step depends on. Skip a step only when there is a clear reason it does not apply (called out per step). The 10-step process overview lives in `SKILL.md` § Process — this file provides per-step depth.

## Step 1: Ingest upstream context

Read whatever upstream `.product/` artifacts exist. They define the *why* and the *who*; do not invent these.

Look for, in this order:

| Artifact | Where | Use for |
|---|---|---|
| Opportunity brief | `.product/discover/opportunities/<slug>.md` | Who / Pain / What Good Looks Like / Non-Goals |
| Slice / MVP scope | `.product/define/slices/<slug>.md` | What's in / out for v1 |
| PRD | `.product/define/specs/<feature>/v<N>.md` | Functional scope and success metrics |
| User research | `.product/discover/research/*.md` | Personas, JTBDs |

When found, summarize back to the user in 3-5 lines what you're treating as fixed input from each artifact. Let them correct the summary before proceeding.

If the user corrects the summary, update the fixed inputs accordingly and continue to Step 2. If a correction invalidates a previously elicited input (e.g., the site type changes), return to the affected step before proceeding.

When **no upstream artifacts exist**, proceed to Step 2 with no fixed inputs and elicit everything inline.

## Step 2: Elicit missing strategy

Strategy inputs (user, business goal, scope) gate every later step. Do not invent personas, JTBDs, or business outcomes when the user has not provided them — stop and elicit instead.

Use the `AskUserQuestion` tool. Ask only what's missing after Step 1. Never ask more than 4 questions in a single turn; bundle related ones.

**Required strategy inputs (gate the design), in priority order:**

1. **Site type** — pick from the 8 in `references/site-type-patterns.md`, or "hybrid: <primary> + <secondary>." If unclear, present 2-3 most-likely types with one-sentence framing each.
2. **Primary users** — 2-4 personas or roles. Single-sentence description each.
3. **Top user JTBDs** — 3-5 jobs, ordered by frequency or importance. Phrase as "When …, I want to …, so I can …" or accept user's own phrasing.
4. **Primary business outcome** — *one* metric (conversion, signups, engagement, retention, deflection, etc.). Push back if the user names three.
5. **Constraints** — tech stack, framework/CMS, performance budget, SEO/SSR requirements, localization, accessibility tier, timeline.

**Asking strategy when more than 4 inputs are missing:** ask inputs 1-4 in turn 1, then return for input 5 (constraints) in turn 2 after receiving those answers. Constraints can be elicited later because they shape implementation, not page inventory.

**Stop and ask when:** an input above is missing or contradicted by upstream context. **Proceed without asking when:** upstream artifacts cover the input cleanly.

## Step 3: Commit site type

Open `references/site-type-patterns.md` for the chosen type. Read the entry end-to-end — audience, JTBDs, canonical inventory, dominant nav, common flows, gotchas.

State the commitment back to the user in one line:

> "Designing as a **<site type>** site. Canonical inventory and nav paradigm will follow that pattern, adapted to the JTBDs above."

If the user pushes back, return to Step 2.

## Step 4: Derive page inventory

For each JTBD from Step 2, work backward from "user goal achieved" to "user entry point" and name the pages required to bridge them. Then merge with the canonical inventory from Step 3.

For each page, capture:

- **Name** — short, user-facing.
- **URL** — slug; use `:param` for dynamic templates.
- **Purpose (JTBD it serves)** — one sentence tied to a JTBD or the business outcome.
- **Content type** — `static` / `dynamic template` / `app view` / `external`.
- **Auth** — `public` / `authed` / `role-gated`.
- **Owner template** — name of the template that renders it (one template per row of dynamic content).

**Apply rule 2 from `rules/ia-principles.md`:** if a page has no JTBD, cut it; if a JTBD has no page, add one. **Apply rule 3:** if a page has three jobs, split it.

Render the inventory as the page-inventory table from `assets/template-website-design.md`.

## Step 5: Commit nav paradigm

Pick one paradigm from `rules/ia-principles.md` rule 4. Justify in one sentence against the JTBDs and site type.

Map every page in the inventory to a nav region:

- **Primary nav** — top-level discovery. Cap at 4-7 items.
- **Utility nav** — search, login, CTA, notifications, locale switcher.
- **Footer** — full sitemap, legal, secondary nav.
- **Side / contextual nav** — only if the chosen paradigm uses side nav.

A page that doesn't fit a region is a sign it shouldn't exist or belongs deeper in the hierarchy. Cut or nest it.

Render the nav model with the `flowchart LR` subgraph pattern from `references/sitemap-mermaid-patterns.md` § Navigation model pattern.

## Step 6: Walk top 3-5 flows

Pick 3-5 flows, one per top JTBD. Cap at 5; more is a sign the site is doing too many things (rule 7).

For each flow, write:

- **Title:** "Who → what → success condition."
- **Trigger:** how the user enters this flow (search, deep link, in-product CTA, email).
- **Mermaid diagram:** `flowchart LR` for linear, `flowchart TD` with decision diamonds for branching, `sequenceDiagram` for interaction-heavy flows. Patterns in `references/sitemap-mermaid-patterns.md` § Cross-page user flow patterns.

If a flow requires invented intermediate pages not in the inventory, the IA is missing something — return to Step 4 and add the page.

## Step 7: Enumerate edge pages

Open `references/edge-pages-checklist.md` and walk every category. For each row, decide:

- **Include** — add it to the page inventory.
- **Exclude with reason** — record the justification in the artifact's Edge Pages section.

The quick include/exclude matrix at the bottom of the checklist gives defaults per site type — start there, then override per site specifics.

Re-render the page inventory and the sitemap diagram with the included edge pages.

## Step 8: Assemble & write artifact

Fill `assets/template-website-design.md` (in this skill) into a new file at:

```
.product/design/websites/<slug>.md
```

`<slug>` is kebab-case derived from the site name (e.g., "Acme Marketing Site" → `acme-marketing-site`). Create the `.product/design/websites/` directory if it does not exist.

Section-by-section:

1. **Strategy preamble** — paste from Step 2 inputs.
2. **Site type & nav paradigm** — paste Step 3 commitment + Step 5 nav model.
3. **Sitemap** — `flowchart TD` with the page inventory from Steps 4 + 7.
4. **Page inventory table** — the table from Step 4 (with edge pages from Step 7 merged in).
5. **URL / route shape** — table or `flowchart TD`. Use a markdown table when the route tree has ≤15 routes with no nested sub-paths; use a `flowchart TD` when there are >15 routes or multi-level nesting that a table would flatten. Do not render both formats for the same content.
6. **Cross-page user flows** — diagrams from Step 6, one subsection per flow.
7. **Edge pages** — table from Step 7.
8. **Design principles for this site** — 3-7 site-specific opinionated calls a reviewer can test against.
9. **Open questions** — every assumption you had to make, every input the user deferred, every excluded edge page that might be wrong. Numbered.
10. **Hand-offs** — populated from the template's hand-offs table; adjust to the project's actual next steps.

## Step 9: Self-check against rules

Before delivering, walk `rules/ia-principles.md` end-to-end and confirm each rule is satisfied. For any deliberate violation, add a numbered entry to Open Questions explaining the trade-off.

Specific checks (these are the failures that show up most):

- Does every page in the inventory map to a stated JTBD or business outcome?
- Is the nav paradigm one choice, not two?
- Are 404, 500, Privacy, Terms in the inventory?
- Are 3-5 flows walked end-to-end (not 0, not 10)?
- Is the primary business outcome a single metric?
- Are non-goals (visual design, page-level layout, feature tech specs) explicitly named?

## Step 10: Multi-axis review

Before delivering, offer the user a parallel multi-axis review. Do **not** launch reviewers without confirmation.

Use the `AskUserQuestion` tool with this exact prompt shape:

```
The website design is drafted at .product/design/websites/<slug>.md.

Run a parallel review with the design:website-design-reviewer agent? Each
axis focuses on a different concern:

- A) coverage — every JTBD has at least one page; every page has a JTBD; top
     flows are walked; required edge pages present; no scope creep into surface plane
- B) ia-quality — site type fits JTBDs; nav paradigm is one choice and survives
     the top flows; page hierarchy reflects user mental models; growth-resilient
- C) risk — accessibility statement / legal pages required for jurisdiction
     present; auth-gated routes have all paired states; localization handled if
     in scope; SEO / SSR / performance constraints reflected in the inventory

Reply with: "all" (recommended) · a subset like "A, C" · or "skip" for a
self-review against ia-principles.md instead.
```

Then branch:

- **User selects one or more axes** → launch the `design:website-design-reviewer` agent *in parallel*, one `Task` call per selected axis. Each call must pass (1) the absolute artifact path, (2) the single axis name (`coverage`, `ia-quality`, or `risk`), and (3) the site type from the strategy preamble. Do not bundle multiple axes into one invocation — the reviewer is scoped to one axis per run so findings stay focused. Wait for all parallel reviewers to return before reconciling.
- **User replies "skip"** → walk `rules/ia-principles.md` end-to-end and report any rule the artifact does not satisfy, using a `**Finding:** <one sentence>` / `**Fix:** <one concrete action>` format.

Reconcile reviewer output:

1. **Merge and dedupe** — collapse findings that different axes raised about the same line (rare but possible; keep the clearest wording)
2. **Group by severity** — Critical → Major → Minor, preserving the axis tag on each finding
3. **Present to the user** — show the consolidated list with the verdict from each axis. For each Critical and Major finding, show the proposed fix inline
4. **Apply agreed fixes** — edit the artifact directly for fixes the user accepts; skip or park fixes the user declines. Then deliver.

## Edge cases

- **Cold start, no upstream `.product/` artifacts** — Skip Step 1, do all elicitation in Step 2. Save the elicited strategy as a callout in the artifact's preamble so future iterations can reference it.
- **User explicitly defers persona work ("I'll figure out the personas later")** — Treat "user who deferred persona work" as a single stand-in persona; this is the only case where stand-ins are permitted. Flag every page whose JTBD depends on a specific, unstated persona in Open Questions. Do not fabricate persona details (name, role, or goal) not stated by the user.
- **Hybrid site (e.g., marketing + SaaS app)** — Pick the primary type and design its IA fully. Treat the secondary surface as an Open Question with a hand-off note: "Secondary surface (`<type>`) deserves its own design-website artifact; see future v2."
- **Existing site being redesigned** — Add a Step 1.5: read the current site's nav and top routes (use `mcp__chrome-devtools__navigate_page` if available, or ask the user to paste them in). Treat the current IA as evidence, not a constraint.
- **Internal tool with no public surface** — Skip cookie banner, accessibility statement (verify with user — many internal tools still require it), and most marketing edge pages. Use the internal-tool entry in `references/site-type-patterns.md`.
- **User pushes for visual design (colors, fonts, components)** — Stop and hand off to `harness:write-design-system`. Do not stretch into surface-plane work (rule 9).
- **User pushes for single-page layout (wireframes, component composition)** — Hand off to `design:design-page` (sibling skill). Note the dependency in Open Questions if the page design is not yet drafted.
- **Site has >25 pages** — Split the sitemap into multiple diagrams (one per top-level section) and cross-link them. The page inventory stays in a single table.
