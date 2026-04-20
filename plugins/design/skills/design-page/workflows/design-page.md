# Workflow: Design a Page (Page-Level)

End-to-end procedure for producing a page-design artifact. Steps are ordered; each step produces an input the next step depends on. Skip a step only when there is a clear reason it does not apply (called out per step). The 10-step process overview lives in `SKILL.md` § Process — this file provides per-step depth.

## Step 1: Ingest upstream context

Read whatever upstream `.product/` artifacts exist. They define *where this page sits* and *who it serves*; do not invent these.

Look for, in this order:

| Artifact | Where | Use for |
|---|---|---|
| Website design | `.product/design/websites/<slug>.md` | Page's role in the site IA, entry/exit paths, nav paradigm, canonical inventory |
| Design system | `.product/design-system/*` or user-named path | Component composition, tokens (do not redefine) |
| PRD / feature spec | `.product/define/specs/<feature>/v<N>.md` | Functional scope, success metrics |
| User stories | `.product/define/stories/<feature>/*.md` | Specific user-observable behaviors the page must support |
| Opportunity brief | `.product/discover/opportunities/<slug>.md` | Who / Pain / What Good Looks Like (if the page is opportunity-driven) |

When found, summarize back to the user in 3-5 lines what you're treating as fixed input from each artifact. Let them correct the summary before proceeding.

If the user corrects the summary, update the fixed inputs accordingly. If a correction invalidates a later-step input (e.g., page goal changes), return to the affected step. If the user does not correct the summary (acknowledges, approves, or stays silent past the next message), treat it as accepted and proceed to Step 2 without further confirmation.

When **no upstream artifacts exist**, proceed to Step 2 with no fixed inputs and elicit everything inline.

## Step 2: Elicit missing strategy

Strategy inputs (page goal, audience/JTBD, archetype) gate every later step. Do not invent any of these when the user has not provided them — stop and elicit instead.

Use the `AskUserQuestion` tool. Ask only what's missing after Step 1. Never ask more than 4 questions in a single turn; bundle related ones.

**Required inputs (gate the design), in priority order:**

1. **Page name + URL** — what this page is called and where it lives (e.g., "Pricing page at `/pricing`").
2. **Page goal** — exactly one primary outcome (see `rules/page-design-principles.md` rule 1). If the user names three, push back and ask for the *one* that matters most.
3. **Primary audience + entry point** — who lands here, from where, with what intent.
4. **Archetype** — pick from the 8 in `references/page-archetype-patterns.md`. If unclear, present the 2-3 most-likely with one-sentence framing each. Archetype is higher priority than JTBD detail and responsive strategy because it locks in mandatory states, above-the-fold ranking, and per-archetype a11y gotchas that downstream steps depend on.
5. **Top JTBD(s) for this page** — 1-3 jobs the page exists to serve. Rule of thumb: if the user names more than three, the page is doing too much and should be split.
6. **Design system status** — exists / doesn't exist yet / exists but incomplete. Affects component composition step.
7. **Responsive strategy** — mobile-first / desktop-first. Defaults to mobile-first for public-facing, desktop-first for internal tools.

**Ask inputs 1-4 in turn 1; ask inputs 5-7 in turn 2 only if still missing after turn 1.** Upstream artifacts may already cover 5-7 (e.g., a PRD names JTBDs; website-design constraints imply responsive strategy); check before asking.

**Stop and ask when:** an input above is missing or contradicted by upstream context. **Proceed without asking when:** upstream artifacts cover the input cleanly (e.g., the website design already names the page's role; the PRD states the goal).

## Step 3: Commit archetype

Open `references/page-archetype-patterns.md` for the chosen archetype. Read the entry end-to-end — above-the-fold ranking, mandatory states, canonical interactions, a11y gotchas, LLM failure modes.

State the commitment back to the user in one line:

> "Designing as a **<archetype>** page. Canonical composition and mandatory states will follow that pattern, adapted to the page goal and JTBD above."

If the user pushes back (e.g., "it's actually a hybrid landing + form"), return to Step 2 and commit a *primary* archetype with the secondary as a region (per rule 2 in `rules/page-design-principles.md`).

## Step 4: Rank above-the-fold elements

Draft the top 3-5 elements that will live above the fold, in strict rank order. Apply rule 3 from `rules/page-design-principles.md`: primary CTA must appear in the ranked set; flat "everything is important" rankings are a blocker.

For each ranked element, capture:

- **Rank position** (1-5)
- **Element** (hero, headline, CTA, metric tile, first row of list, etc.)
- **Purpose** (why this element is at this rank against the page goal)
- **Desktop placement** (top-left, top-centered, full-width)
- **Mobile placement** (same, sticky bottom, stacked lower, hidden)

Then commit the primary CTA explicitly (rule 4): label, visual weight, placement, mobile behavior, disabled-state rendering. If the page legitimately has no primary CTA (pure informational reading, e.g., an article), state that — and reconfirm the page goal.

## Step 5: Draft the wireframe

Pull the matching pattern from `references/wireframe-ascii-patterns.md` for the chosen archetype. Paste the desktop and mobile variants. Adapt:

- Replace the sample elements with the actual top-5 ranking from Step 4.
- Inline-annotate state markers (`{loading}`, `{empty}`, `{denied}`) at the regions where states matter.
- Inline-annotate interactions (e.g., `// sticky bottom on mobile`, `// disabled when empty`) where they're not obvious from the wireframe alone.

Do not aim for pixel-accuracy. The wireframe is a structural commitment — component inventory and hierarchy — not a visual draft.

If the page does not fit any archetype's wireframe cleanly, that's a signal to re-examine the archetype commitment (Step 3) or split the page (it may be doing two jobs).

## Step 6: Specify component composition

Walk every region of the wireframe. For each component used:

- **Design system exists and has the component** — name the design-system component and the variant used. Do not redefine tokens or styles — that's the design system's job.
- **Design system exists but is missing the component** — add an entry to the **"Components needed but not in the design system"** bullet block in the artifact (template § 6, last block) with: component name, one-sentence description, and the note "recommend adding via `harness:write-design-system`". Do not invent inline.
- **No design system exists** — name the component as you'd name it (e.g., "inline-validation-toast") and describe it **structurally only**: purpose, the region it lives in, its states. Omit token values (no exact colors, typography sizes, spacing). Surface the full list of page-local components in Open Questions and note it should feed `harness:write-design-system`.

Render as the component composition table from `assets/template-page-design.md`. Structural naming is always correct; visual token values belong in the design system.

## Step 7: Enumerate states per region

Walk `references/state-catalog.md` mandatory baseline and the archetype-conditional matrix. For each data-driven region of the page (from Step 5 wireframe):

- List the mandatory states that apply to this region.
- For each, specify: how it renders (visual/content), what interactions are available, and any `aria-live` or `aria-busy` treatment.
- Decide conditional states (partial, offline, rate-limited, read-only) per region: *include* / *exclude with reason*.

Render as one state table per region in the artifact (template § 7).

**Do not:** conflate empty-first-run with empty-filtered — they are distinct states (per `references/state-catalog.md`). **Do not:** design only the happy path — that's a blocker per rule 6.

## Step 8: Specify interactions, responsive behavior, and a11y

These three concerns are intertwined but have distinct outputs. Work them in order — 8a → 8b → 8c — so later sub-steps can reference decisions made in earlier ones.

### Step 8a: Interactions (rule 10)

For each element in the top-5 ranking and each interactive region, specify trigger, response, affordance, keyboard equivalent. For multi-step interactions (menu open→select, async form validation, modal open→close), draft a mermaid `stateDiagram-v2`.

**Default when an element has no keyboard equivalent:** write "not keyboard-reachable — flag in Open Questions." Do not omit the row; the gap is itself a finding. Most "no keyboard equivalent" cases are really a design mistake — reconsider whether the element should be there in that form.

### Step 8b: Responsive behavior (rule 7)

Walk `references/responsive-patterns.md`. For each region, commit to a reflow pattern (stack / collapse / hide / swap / resize) per breakpoint. Note touch affordances explicitly — hover-reveal is a blocker on mobile.

**Default when a region has a single-state layout that does not reflow** (e.g., a full-width hero that stays full-width at every breakpoint): write "no reflow: full-width at all breakpoints." A declared no-reflow is a valid commitment; an omitted row is not.

### Step 8c: Accessibility (rule 8)

Walk `references/a11y-checklist.md` baseline + per-archetype gotchas. Declare in the artifact: WCAG tier, heading outline, landmark regions, focus order (first 5-10 tab stops), contrast commitments, target sizes, motion policy, `aria-live` regions, and the screen-reader narrative.

**Default when contrast ratios are unknowable because the design system doesn't exist yet:** write "contrast TBD — flag in Open Questions; minimum WCAG AA required at implementation." This keeps the a11y commitment explicit even when exact values are deferred.

## Step 9: Enumerate edge cases and assemble

**Edge cases (rule 9):** walk the archetype-specific edges from `references/page-archetype-patterns.md` plus the cross-archetype baseline (404/403 landing, offline, slow network, JS disabled, third-party block, rate-limited, stale auth). For each, decide *handle* / *defer with reason*.

**Assemble the artifact:** fill `assets/template-page-design.md` into a new file at:

```
.product/design/pages/<slug>.md
```

`<slug>` is kebab-case derived from the page name (e.g., "Pricing page" → `pricing`, "Customer dashboard" → `customer-dashboard`). Create the `.product/design/pages/` directory if it does not exist.

Section-by-section, fill from the steps above:

1. **Page goal** — Step 2 input 2.
2. **Audience & JTBD** — Step 2 inputs 3-4.
3. **Archetype commitment** — Step 3.
4. **Above-the-fold hierarchy** — Step 4.
5. **Wireframe** — Step 5.
6. **Component composition** — Step 6.
7. **State catalog** — Step 7.
8. **Interactions** — Step 8.
9. **Responsive behavior** — Step 8.
10. **Accessibility** — Step 8.
11. **Edge cases** — Step 9.
12. **Metrics & events** — inherit from PRD/website-design if present; name the primary success event at minimum.
13. **Open questions** — every input the user deferred, every component flagged for addition, every state excluded with reason.
14. **Hand-offs** — from the template's hand-offs table.

**Self-check against `rules/page-design-principles.md`:** walk all 10 rules end-to-end. For any deliberate violation, add a numbered Open Question explaining the trade-off. The failures that show up most:

- Does the page have exactly ONE primary goal?
- Is the archetype committed, and does the wireframe match the canonical pattern?
- Are 3-5 elements ranked above the fold (not flat, not 10)?
- Is the primary CTA named with label + visual weight + placement?
- Does every region have a state catalog, not just the happy path?
- Is a responsive strategy committed per region (not "it's responsive")?
- Are a11y commitments in the artifact (not punted to implementation)?
- Are edge cases enumerated per archetype?

## Step 10: Multi-axis review

Steps 1-9 conclude with the artifact written at `.product/design/pages/<slug>.md`. Before delivering, offer the user a parallel multi-axis review. Do **not** launch reviewers without confirmation.

Use the `AskUserQuestion` tool with this exact prompt shape:

```
The page design is drafted at .product/design/pages/<slug>.md.

Run a parallel review with the design:page-design-reviewer agent? Each
axis focuses on a different concern:

- A) completeness — every section populated; primary CTA named; state catalog
     covers mandatory baseline; a11y commitments declared; no scope creep into
     visual tokens / IA / feature tech spec
- B) ux-quality — archetype fits the page goal; above-the-fold ranking is crisp
     (3-5, not flat); states are first-class; interactions specified; responsive
     strategy per region; hover/touch parity
- C) risk — a11y baseline (WCAG AA) holds; edges enumerated per archetype;
     destructive actions safely placed; no single-device assumptions;
     performance budget stated if performance is a constraint

Reply with: "all" (recommended) · a subset like "A, C" · or "skip" for a
self-review against page-design-principles.md instead.
```

Then branch:

- **User selects one or more axes** → launch the `design:page-design-reviewer` agent *in parallel*, one `Task` call per selected axis. Each call must pass (1) the absolute artifact path, (2) the single axis name (`completeness`, `ux-quality`, or `risk`), and (3) the archetype from the artifact's commitment section. Do not bundle multiple axes into one invocation — the reviewer is scoped to one axis per run so findings stay focused. Wait for all parallel reviewers to return before reconciling.
- **User replies "skip"** → walk `rules/page-design-principles.md` end-to-end and report any rule the artifact does not satisfy, using a `**Finding:** <one sentence>` / `**Fix:** <one concrete action>` format.
- **User replies with something other than a valid axis letter or "skip"** (e.g., "not now," "later," a question about the axes) → answer the question if asked, otherwise treat as "skip" and proceed with the self-review branch. Do not stall waiting for a differently-phrased answer.

Reconcile reviewer output:

1. **Merge and dedupe** — collapse findings that different axes raised about the same region
2. **Group by severity** — Critical → Major → Minor, preserving the axis tag on each finding
3. **Present to the user** — show the consolidated list with the verdict from each axis. For each Critical and Major finding, show the proposed fix inline
4. **Apply agreed fixes** — edit the artifact directly for fixes the user accepts; skip or park fixes the user declines. Then deliver.

## Edge cases

- **Cold start, no upstream `.product/` artifacts** — Skip Step 1, do all elicitation in Step 2. Save the elicited strategy as a callout in the artifact's preamble so future iterations can reference it.

- **No design system exists yet** — In Step 6, name components as you'd name them (page-local naming). In Open Questions, flag the full list of page-local components that should be promoted to the design system. Surface the hand-off to `harness:write-design-system`.

- **Redesign of an existing page** — Add a Step 1.5: read the current implementation. Preferred method: `mcp__chrome-devtools__navigate_page` if available, which captures the rendered page. If that tool is not available, read the current implementation source directly using `Read` + `Grep` against the HTML / component / template files. Either way, note in the artifact's Changelog which input method was used so future iterations understand the evidence base. Treat the current design as evidence, not a constraint — call out what's being changed and why.

- **Page doesn't fit any archetype cleanly** — First, re-examine whether the page is doing two jobs (split it). If the answer is genuinely "this is a hybrid," pick the primary archetype (tied to the page goal) and design the secondary as a region within it. Do not design two parallel archetypes on the same page.

- **Page is too large to design in one artifact** — Split into multiple pages at the IA layer (this is upstream work, belongs in `design:design-website`). If the user insists it's one page, design the ONE primary job and surface the rest as Open Questions or deferred-to-v2.

- **User pushes for visual design (colors, fonts, exact pixel values)** — Stop and hand off to `harness:write-design-system`. Do not stretch into surface-plane work (rule 5).

- **User pushes for backend/feature architecture** — Hand off to `design:design-spec`. The page design names what needs to exist; the feature spec decides how it's built.

- **User asks for microcopy (exact headline text, CTA labels as marketing copy)** — Draft placeholder-quality labels only. Real copy requires a copywriter / stakeholder and usually iterates post-design. Flag in Open Questions.

- **Archetype is "empty/error"** — This is the simplest archetype but the one most often under-designed. Walk `references/page-archetype-patterns.md` § 8 carefully and resist the temptation to skip state enumeration because "there's nothing here."

- **Archetype is "settings" and the product has many settings sections** — Design the *settings shell* (nav, search-within-settings, save behavior, destructive actions zone) as one page design. Individual settings sections are separate page designs if they have material complexity; otherwise document them inline in the shell artifact.

- **User wants live prototype review** — Out of scope for this skill. Suggest spawning `mcp__chrome-devtools__navigate_page` against a built prototype, or hand off to an implementation step.

- **Mermaid renderers vary** — When drawing interaction state diagrams in the artifact, stick to `flowchart`, `sequenceDiagram`, and `stateDiagram-v2` (supported broadly); avoid newer diagram types.

- **`.product/` directory may not exist** — Some repos do not yet have it. Create the full `.product/design/pages/` path on first write rather than failing.

- **User wants the artifact at a different path** — Honor the override but record the chosen path in the artifact's Changelog row so subsequent iterations can find it.

- **Design system path is non-standard** — If the design system lives somewhere other than `.product/design-system/`, accept a user-supplied path and cite it in the artifact's Related artifacts header.

- **Page is part of a feature being designed in parallel** — If the user is also running `design:design-spec` for the same feature, the two artifacts are peers (structure vs tech); cross-link them in the Related artifacts header.
