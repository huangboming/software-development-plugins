---
name: define-product
description: "Write or update .product/define/product.md — the present-tense product definition covering purpose, target users, value proposition, scope, and stage. The concrete companion to define-vision (3–10yr aspirational future) and feature PRDs (specific capabilities). Triggers: '/define-product', 'define what our product is today', 'product definition', 'product one-pager', 'what is our product', 'create product.md', 'describe our product', 'write a product overview', 'update product.md', 'refresh the product definition'. NOT for future vision, principles, or long-horizon direction — use define-vision for those."
---

# Product Definition Writer

Produce or update `.product/define/product.md` — the present-tense, concrete definition of what the product is today: purpose, target users, value proposition, scope, and stage. Explicitly no feature list (features live in opportunities → slices → feature PRDs) and no aspirational 3+yr framing (that belongs in `vision.md`).

## References

- [references/product-template.md](references/product-template.md) — Scaffold for the output document. Read at the start of Step 4 (drafting).
- [references/writing-guide.md](references/writing-guide.md) — Section-by-section quality calibration (weak/strong examples, boundary table with `define-vision`, quality checklist). Read at the start of Step 5 (review).

## Process

Writing a product definition involves these steps:

1. Confirm scope (product-wide, present tense)
2. Select input workflow (conversational, synthesis, or codebase)
3. Gather content
4. Draft product.md
5. Review against the quality checklist; revise until it passes
6. Present to the user

### Step 1: Confirm Scope

Before gathering content, verify three things:

1. **Product-wide, not feature-level.** `product.md` defines the product as a whole. If the user asks for a "product definition for the onboarding flow" or "what is our notifications system", stop — that's a feature-level concern. Suggest `write-prd` (feature-level) instead.
2. **Present tense, not future.** If the user is describing a 3–10yr vision, leap-of-faith ambition, or principles, stop — that's `define-vision`. Offer to run that skill instead, or to draft both as a pair (product.md grounds; vision.md projects).
3. **Resolve ambiguous scope.** If the user names a sub-system rather than the whole product (e.g., "define the product for our API platform"), ask one clarifying question — "Is the API platform the entire product, or a surface within a larger product?" — then apply the appropriate check. Do not proceed until the answer is unambiguous.

If any check fails, pause and resolve with the user before proceeding.

### Step 2: Select Input Workflow

Determine which workflow applies based on available inputs:

| User situation | Workflow |
|---|---|
| User describes a product idea or early concept with no existing artifacts | **Conversational Elicitation** (Step 3a) |
| `.product/define/vision.md` exists, or framed opportunities exist at `.product/discover/opportunities/`, or feature PRDs exist at `.product/define/specs/` | **Synthesis from Artifacts** (Step 3b) |
| The product already exists in code and the user wants to document what it *is* today | **Codebase Exploration** (Step 3c) |
| Multiple of the above apply | Use **3b (Synthesis)**. Within 3b, read artifacts in priority order: vision.md → opportunities → feature PRDs → research. Supplement with 1–3 targeted questions from 3a only for fields the artifacts don't cover. Add codebase exploration (3c) only if the artifacts contradict each other and the code is the tiebreaker. |

If a directory exists but is empty, treat it as absent. If you cannot determine which artifacts exist or are relevant, ask the user before selecting a workflow.

If `.product/define/product.md` already exists, treat this as an **update** — read the existing file first and ask the user what has changed. Preserve sections that are not changing. Bump `Last updated` to today. Do not version — `product.md` is a living doc.

### Step 3a: Conversational Elicitation

Ask clarifying questions in rounds of 3–5. Prioritize by what blocks progress. Use concrete, comparison-shaped questions — "who does this replace?" beats "what's the value?".

**Round 1 — Purpose and users:**

| Area | Ask About |
|---|---|
| User segment | Who specifically uses this today? Name a role, a team size, a tooling context. |
| Current workflow | What do they do *instead* right now — status quo, competitor, spreadsheet, DIY script? |
| Purpose | What can they do with this product that they couldn't do before? |
| Segment count | Are there 1, 2, 3, or 4 distinct target segments? How do their needs differ? |

**Round 2 — Positioning and scope:**

| Area | Ask About |
|---|---|
| Alternative named | When someone evaluates this, what's the thing they're comparing against? |
| Identity-shaping non-goals | What are 2–3 adjacent problems a reasonable person might assume this product solves — but it doesn't? |
| Product stage | Pre-launch, MVP, scaling, mature, or sunsetting? What pressure does that stage put on current decisions? |

Stop asking when the target segments, purpose, alternatives, and scope boundaries are clear. Remaining unknowns become Open Questions.

Proceed to Step 4.

### Step 3b: Synthesis from Artifacts

1. Read, in priority order, any of these that exist:
   - `.product/define/vision.md` — use as directional anchor for user archetype and purpose, but translate from future-tense to present-tense.
   - `.product/discover/opportunities/*.md` — framed opportunities reveal target segments and their pains concretely.
   - `.product/define/specs/<feature>/v*.md` — existing feature PRDs reveal what the product actually does.
   - `.product/discover/research/*.md` — synthesized research reveals segment characteristics.
2. Extract into raw material:
   - Personas and segment characteristics
   - Pain points and current workarounds (feeds Purpose and Value Proposition)
   - Scope boundaries stated or implied across artifacts
   - Any inconsistencies between vision's user archetype and what opportunities/PRDs actually serve — flag as Open Questions
3. Present a 4–6 bullet summary covering: inferred target segments, primary pain per segment, named alternative (or flag as unknown), and any cross-artifact inconsistencies found. Ask the user to confirm or correct each point before proceeding. A general "looks good" is not sufficient — prompt the user to address any flagged inconsistency explicitly.
4. Ask 1–3 targeted follow-up questions for anything the artifacts can't answer (typically: named alternative, product stage).

Proceed to Step 4.

### Step 3c: Codebase Exploration

Use when the product exists in code and the user wants to write down what it *is* today.

1. Ask the user for the repo root if not obvious.
2. Read entry points, primary user-facing routes, landing pages, and onboarding flows — these reveal the intended target user and positioning.
3. Read the top-level `README.md`, any marketing copy in the repo, and the first screen a new user sees. Contrast the stated positioning with what the code actually supports; flag drift as Open Questions.
4. Identify the 2–4 largest feature surfaces and infer the target segments from who those features serve.
5. Translate observations into present-tense product-level statements. Do not list features.
6. Present the extracted material to the user for validation before drafting.

Proceed to Step 4.

### Step 4: Draft product.md

1. Read [references/product-template.md](references/product-template.md).
2. Create or update `.product/define/product.md`. Create the `.product/define/` directory if it does not exist.
3. Write the front matter as specified in the template.
4. Draft each section following the template. Capture unresolved items in Open Questions and state assumptions explicitly.

### Step 5: Review and Revise

1. Read [references/writing-guide.md](references/writing-guide.md) in full.
2. Review the draft against its quality checklist. Revise anything that fails and iterate until the draft passes every check. Do not present a draft with known issues.

### Step 6: Present to the User

1. Summarize what was drafted:
   - Which sections drew from which inputs (vision, opportunities, conversation, code)
   - Any assumptions made to fill gaps
   - Which Open Questions remain
2. Link to `.product/define/product.md`.
3. Ask: "Which segment or section feels off?" — not "does this look good?" (the latter produces hollow approvals).
4. If the user approves without changes, confirm the file path and list any remaining Open Questions so the user knows what is unresolved. Do not probe further.

## Edge Cases

If `.product/define/vision.md` contradicts what the product actually does today:
  → Flag the contradiction. Ask whether (a) the vision has drifted and needs updating, or (b) the product has drifted from its vision and that's the real conversation. Draft `product.md` to reflect the present reality either way; do not paper over the gap.

If target segments keep multiplying past 4:
  → Stop listing and ask which 2–4 are *primary* — the segments whose needs shape product decisions. Move the rest to Open Questions as a breadth/positioning concern.

If the product has no named alternative (user says "nothing really" for Value Proposition):
  → Push back once — nearly every product competes with the status quo, a spreadsheet, or a manual process, even if no direct competitor exists. If the user still has no answer, that itself is a signal the value proposition is unclear; write "TBD — named alternative unknown" and add an Open Question.

If the user wants `product.md` at a non-default path:
  → Accept but warn: downstream skills (`define-vision`, `write-prd`, `prioritize`, etc.) expect `.product/define/product.md`. Document the custom path in a project CLAUDE.md if the user insists.

If the draft fails the quality checklist after 3 revision attempts:
  → Stop. Present the failing items to the user and ask which constraint to relax or what input is missing. Do not iterate silently.
