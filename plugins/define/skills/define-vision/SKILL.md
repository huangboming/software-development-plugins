---
name: define-vision
description: "Create or update a product vision document with ranked product principles. The aspirational 3–10yr companion to define-product (present-tense product definition) and feature PRDs. Triggers: '/define-vision', 'write a product vision', 'create product vision', 'define our vision', 'draft a vision', 'product vision document', 'where is our product going', 'product principles', 'what do we stand for'. NOT for describing the product today — use define-product for that."
---

# Product Vision Writer

## References

- [references/cagan-canon-and-writing.md](references/cagan-canon-and-writing.md) — Knowledge spine. Cagan's 10 principles, distinctions from mission/strategy/NSM/OKRs, timeframe and ownership, the default 6-section scaffold, section-by-section writing guide with weak/strong examples, and the full quality checklist derived from 8 named failure modes. Read before drafting (Step 3) and during review (Step 5).
- [references/principles-guide.md](references/principles-guide.md) — Companion guide for Section 6 (Product Principles). Conflict-resolution test, position+rationale writing pattern, eBay canonical example, ranking and count rules, elicitation questions. Read when drafting Section 6 and when reviewing principles.
- [references/alternative-scaffolds.md](references/alternative-scaffolds.md) — Slack 6-section memo, Linear 3-act manifesto, Amazon Working Backwards PR+FAQ. Each with mini-template and when-to-pick guidance. Read only when the user declines the default scaffold.

## Process

Writing a product vision involves these steps:

1. Confirm scope and ownership
2. Select input workflow (conversational or research-synthesis)
3. Gather context
4. Select scaffold (default or alternative)
5. Draft vision.md
6. Review against quality checklist, revise until it passes
7. Present to the user

### Step 1: Confirm Scope and Ownership

Before gathering any content, verify two things:

1. **Product-level, not team-level.** Product vision is a leadership artifact covering the full product, not a single feature area. If the user asks for "a vision for my team" or "a vision for this feature," stop and explain — this skill produces a product-wide vision owned by a product leader (CPO, VP Product, founder). Suggest alternatives:
   - For present-tense product definition: use `define-product`
   - For feature-scoped direction: use `write-prd`
   - For team-level goals: defer to a future OKR skill (not yet built)
2. **Ownership.** Ask: "Who owns this vision — CPO, VP Product, founder, or is it still TBD?" Record the name (or "TBD") in the front matter. If the user is not the owner, confirm the owner has delegated authorship.

If either check fails, pause and resolve with the user before proceeding.

### Step 2: Select Input Workflow

Determine which workflow applies based on available inputs:

| User situation | Workflow |
|---|---|
| User describes an idea, concept, or rough aspiration with no existing artifacts | **Conversational Elicitation** (Step 3a) |
| `.product/discover/research/*.md` exists from a prior `prepare-user-research` run | **Synthesis from Research** (Step 3b) |
| Both of the above | Start with Step 3b, fill gaps with Step 3a questions. |

If the user has nothing — no research, no developed idea — proceed with Conversational Elicitation but add a prominent warning banner to the draft (see Step 5).

### Step 3a: Conversational Elicitation

Ask clarifying questions in rounds of 3–5, prioritized by what blocks progress most. Use conflict-shaped questions to surface real trade-offs, not platitudes.

**Round 1 — Core direction:**

| Area | Ask About |
|---|---|
| Customer | Who specifically is this product for? Name a role, a context, a specific user type. |
| Future moment | What does a day in this customer's life look like when the vision is realized? What changed for them? |
| Insight | What do you believe about this customer or this market that most competitors do not? |
| Timeframe | Software (2–5 years) or hardware (5–10 years)? |

**Round 2 — Rejection and principles:**

| Area | Ask About |
|---|---|
| Rejection | Name 2–3 things this product explicitly rejects becoming. Which markets, which framings, which features? |
| Recurring arguments | When your team argues about what to build, what is the argument usually about? (Surfaces latent principles.) |
| Recent rejection | Name a feature request you rejected recently — and why. (Surfaces rationale for a principle.) |

Ask further rounds only if the problem, customer, insight, or rejection areas remain unclear. Proceed to Step 4 when these four are answerable.

### Step 3b: Synthesis from Research

1. Read every file in `.product/discover/research/`. Extract:
   - Personas → raw material for Section 2 (Who We're Building For)
   - Jobs to be Done → raw material for Section 1 (The Future We're Creating)
   - Competitive gaps and unmet needs → raw material for Section 3 (The Insight)
   - Competitive positioning → raw material for Section 4 (What This Is Not)
2. Present a 1-paragraph summary of what was extracted and ask the user to confirm or correct before drafting.
3. Ask 2–4 targeted questions for the sections the research cannot answer — typically the insight (Section 3), rejection (Section 4), timeframe, and principles (Section 6).
4. Proceed to Step 4.

### Step 4: Select Scaffold

Ask the user: **"What shape should the vision take?"** Present four options:

1. **Default 6-section** (recommended for first-time vision) — a practical scaffold informed by Cagan's principles. Read `cagan-canon-and-writing.md` Section 5 for the layout.
2. **Slack 6-section memo** — internal persuasive narrative, ~3,000 words. Read `alternative-scaffolds.md`.
3. **Linear 3-act manifesto** — public-facing narrative with named antagonists. Read `alternative-scaffolds.md`.
4. **Amazon Working Backwards PR+FAQ** — shortest format, discipline-forcing. Read `alternative-scaffolds.md`.

If the user has no preference, use the default. Do not push alternatives unnecessarily.

### Step 5: Draft vision.md

1. Read [references/cagan-canon-and-writing.md](references/cagan-canon-and-writing.md). This file contains the section-by-section writing guide, the weak/strong examples for each section, and the failure-mode checklist.
2. Read [references/principles-guide.md](references/principles-guide.md) before drafting Section 6 (Product Principles).
3. If using an alternative scaffold, read [references/alternative-scaffolds.md](references/alternative-scaffolds.md) and use the selected structure.
4. Create the output file at `.product/define/vision.md`. Create the `.product/define/` directory if it does not exist.
5. Write the front matter:
   ```markdown
   > **Owner:** [name or "TBD"]
   > **Status:** Draft
   > **Last updated:** [today's date]
   > **Next review:** [today + 2 years]
   > **Timeframe:** [3 years / 5 years / 10 years]
   > **Distribution:** [one-line note on how this will be evangelized]
   ```
6. **If the user provided no research and only minimal conversational input:** Add a prominent warning banner immediately after the front matter:
   ```markdown
   > **⚠️ Drafted without grounding.** This vision was written from conversational
   > input alone — no user research. Validate against real customer evidence
   > before sharing beyond the authoring session. Consider running
   > `prepare-user-research` first and revising.
   ```
7. Draft each section per the writing guide in `cagan-canon-and-writing.md`. Use the weak/strong examples as calibration.
8. Draft Section 6 (Product Principles) per `principles-guide.md`. Elicit principles using the conflict-shaped questions if the user has not already provided them.

### Step 6: Review and Revise

Review the draft against the quality checklist in `cagan-canon-and-writing.md` Section 7. Do not present a draft that fails the checklist.

For each of the 8 failure modes, verify the draft passes:

- FM-1 (not a mission statement)
- FM-2 (not aspirational vagueness — not copy-pasteable to a competitor)
- FM-3 (no roadmap, no features, no dates)
- FM-4 (customer-outcome framing, not company-position)
- FM-5 (distribution note is present)
- FM-6 (product-level, not team-level; owner named)
- FM-7 (ambitious enough to require a leap of faith)
- FM-8 (not a strategy in disguise)

For principles: verify each passes the conflict-resolution test per `principles-guide.md`. Revise any that are platitudes.

If the draft fails any item, revise and re-check. Iterate internally until the draft passes every check. Only then proceed to Step 7.

### Step 7: Present to the User

1. Summarize what was written:
   - Which scaffold was used
   - Which sections drew from research vs. user input
   - Any sections where the draft required assumptions (flag these)
2. Note any unresolved items — e.g., owner TBD, missing principles, placeholder review date
3. Link to `.product/define/vision.md`
4. Ask: "What feels wrong? What's missing?" — not "does this look good?" (the latter produces hollow approvals)

## Edge Cases

If the user asks for a **team-level or feature-level vision**:
  → Stop. Explain that product vision is a leadership artifact owned by a product leader and covers the full product. Suggest `write-prd` for feature-level direction.

If the user asks to **update an existing vision** at `.product/define/vision.md`:
  → Read the existing file. Ask what is changing and why. Preserve sections that are not changing. Update `Last updated` to today and push `Next review` forward if significant revisions were made. Do not fork versions — vision is a living document.

If the user wants to **write vision without research or a developed idea**:
  → Proceed with Conversational Elicitation. Add the grounding warning banner per Step 5 item 6. Warn verbally as well: "This vision will be aspirational without evidence. Consider running `prepare-user-research` first for a stronger foundation."

If the user supplies **a mission statement and calls it a vision**:
  → Explain the distinction using the Vision vs. Mission table in `cagan-canon-and-writing.md` Section 3. Ask whether to (a) convert it to a proper vision (requires real drafting), (b) keep it as a mission and write a vision separately, or (c) abort.

If `.product/discover/research/*.md` exists but is **older than 12 months**:
  → Flag that the research may be stale. Ask whether to refresh research first (run `prepare-user-research`) or proceed with stale data. Note the staleness in the vision front matter if proceeding.

If the user wants the vision **at a non-default path**:
  → Accept but warn: downstream skills (`define-product`, `write-prd`, `prioritize`, etc.) expect the default path `.product/define/vision.md`. If the user insists, document the custom path in a CLAUDE.md or project-level note.

If the user cannot produce **any real conflicts** when eliciting principles:
  → This signals either (a) the product is too new to have principles or (b) the user is not close enough to product decisions. Suggest deferring Section 6 with a placeholder ("TBD — will draft after first quarter of shipping") rather than filling it with platitudes.

If the generated draft **fails the quality checklist after 3 revision attempts**:
  → Stop and present the failing items to the user. Ask which constraint to relax or what input is missing. Do not keep iterating silently.
