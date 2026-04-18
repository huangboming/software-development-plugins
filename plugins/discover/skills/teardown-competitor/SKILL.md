---
name: teardown-competitor
description: "Produce a structured teardown of a competitor, market alternative, or indirect substitute (status quo, spreadsheet workflow, DIY script) and write it to .product/discover/research/teardown-<slug>.md. Picks a lens (job-to-be-done, pricing-and-packaging, positioning, gaps-and-frictions, technical) that matches the decision at hand, grounds every claim in a source, and commits a 'so what' — the implication for our framing or solution search. Feeds frame-problem (as evidence) and map-opportunities (as analog prompts). For cross-target synthesis across finished teardowns, use synthesize-research instead. Triggers: 'teardown a competitor', 'competitor teardown', 'tear down [competitor]', 'competitive analysis', 'competitive landscape', 'competitive landscape scan', 'study the competition', 'analyze the competition', 'what is [competitor] doing', 'how does [competitor] compare', 'benchmark against [competitor]', 'who are our competitors', 'what alternatives exist', 'landscape review', '/teardown-competitor'."
---

# Teardown Competitor

Teardown a competitor or alternative and write the structured result to `.product/discover/research/teardown-<slug>.md`. A teardown is not a feature parade — it extracts positioning insight grounded in verifiable sources and commits a "so what" that feeds `frame-problem` (as evidence) or `map-opportunities` (as analog prompts).

## References

- [references/teardown-template.md](references/teardown-template.md) — Template for the teardown and field guidance (sourcing discipline, observed-vs-inferred, confidence calibration, so-what test, slug naming, status lifecycle, quality check). Read before writing.
- [references/lenses.md](references/lenses.md) — The five lenses (job-to-be-done, pricing-and-packaging, positioning, gaps-and-frictions, technical) with what to capture, what questions each answers, and what to skip per lens. Read when selecting a lens or when a Findings section feels underspecified.

## Process

Four steps: gather input, scope the alternative set, pick a lens and draft, write and confirm.

### 1. Gather Input

Identify the target and the available material. Four input shapes:

- **User names a specific target** ("tear down Notion") → use as the seed. Confirm whether material is supplied (docs, reviews, screenshots) or whether the agent is expected to work from general knowledge and any web sources available. Note the source posture as a one-line prefix in the Target section (e.g., "Sources: user-supplied reviews + public pricing page" or "Sources: general knowledge only — no user-supplied material") and set `Confidence` per the calibration table in `teardown-template.md` accordingly.
- **User provides raw material** (URLs, pasted reviews, marketing copy) → structure from what they provided. Do not supplement with training-data claims unless explicitly asked; when you do, mark those claims `inferred` per `teardown-template.md`.
- **User says "competitive analysis" without naming a target** → ask what framed opportunity or problem space this feeds. Read any linked file in `.product/discover/opportunities/`, then surface 2–3 candidate alternatives — including at least one indirect (status quo, DIY, spreadsheet workflow) — before committing to one.
- **User asks for a market scan across multiple players** → this skill writes one file per target. Agree a shortlist (3–5 targets max). For ≤3 targets, run the skill sequentially in the same session. For 4–5 targets, state the planned order, confirm before starting the first teardown, and surface progress between files — batched runs of 4+ frequently lose user context mid-run. For cross-cut synthesis across finished teardowns, route to `synthesize-research` after the individual files exist.

### 2. Scope the Alternative Set

Before drafting, sanity-check the scope.

- **Is the named target the real alternative?** The most common miss is tearing down direct SaaS competitors while users actually live in Excel, email, or do nothing. If the user has a framed opportunity (`.product/discover/opportunities/<slug>.md`), read its Who and Pain — the "real alternative" is wherever that Pain is tolerated today. If the named target does not match the real alternative, state the mismatch in one sentence and ask whether to proceed with the named target, switch to the real alternative, or produce both.
- **Has at least one indirect alternative been considered?** If only direct SaaS competitors are listed, prompt once: "Status quo, DIY spreadsheets, or email workflows often set the real price ceiling. Should one of those be in the scan?" Accept `no` — record it in the body as a scoping choice, not an oversight.
- **Is the material current?** Competitor facts decay in months. Capture an access date on every timestampable source and set `Confidence` per the calibration table in `teardown-template.md`.

### 3. Pick a Lens and Draft

Default to **job-to-be-done** for discover-phase work — it is the most useful lens for informing framing and solution divergence. Use other lenses (pricing-and-packaging, positioning, gaps-and-frictions, technical) when the decision is narrower. See [references/lenses.md](references/lenses.md) for selection criteria and per-lens capture — filling every section with every lens produces a diffuse document.

Draft against the template. Two disciplines carry the draft:

- **Structure Findings by lens.** Write the Findings section using the "Capture" bullets for the selected lens in `references/lenses.md` as sub-headings, in the order listed. Apply the observed-vs-inferred sourcing discipline defined in `teardown-template.md` to every claim — unsourced claims that are not marked `inferred` are fabricated-evidence liabilities downstream.
- **Write the So What last.** The So What is load-bearing — if you cannot name an implication for our framing or solution search, the teardown was navel-gazing. See the So What test in `teardown-template.md`.

### 4. Write and Confirm

Before writing, run the quality check in `teardown-template.md` and correct violations in place. If a violation requires input the user has not supplied (e.g., the So What cannot be stated without knowing which framed opportunity this feeds), pause — state what is missing and ask before writing. Once the user supplies the missing input, resume by re-running the full quality check, then proceed to write.

Then:

1. Create `.product/discover/research/` if it does not exist.
2. Write the teardown at `.product/discover/research/teardown-<slug>.md` with Status `drafted`. Slug naming is in `teardown-template.md`.
3. Present a summary and ask the user to confirm or correct. If corrections land, apply them in place, re-check only the changed fields, and re-present only what changed.

**Summary example:**

```
Teardown drafted: **notion**
- Lens: job-to-be-done
- Primary job: shared knowledge capture for small teams starting from a blank page
- 3 cited sources, 2 inferred claims (marked)
- Confidence: moderate (primary + secondary sources, all within 4 months)
- So What: Notion's structure-as-you-go loop is the framing wedge for us — contrast, don't compete feature-for-feature.
- File: .product/discover/research/teardown-notion.md

Next: frame-problem (if this informs a new opportunity), map-opportunities (if this feeds an analog branch), or synthesize-research (to cross-cut with other teardowns).
```

## Edge Cases

If the user wants **one file per teardown across a 5+ target scan**:
  → Batches of 5+ lose signal fast — by file 4, reviewers skim. Offer to (1) shortlist 2–3 for deep teardowns, and (2) produce a single lightweight landscape entry (the template applied at half depth) covering the remainder. Record the reduced depth in each file's body.

If the user wants a **self-teardown** (teardown of their own product):
  → Accept — self-teardowns surface positioning drift. Apply `teardown-template.md` as-is (no structural variant), name the real alternative in the So What, and flag in the body that findings are self-reported bias without a blind reviewer.

If **no verifiable source exists** (target is private, pre-launch, or the user has only hearsay):
  → Do not fabricate sources. Proceed with the teardown but mark every unsourced claim `inferred` with basis, and set `Confidence` to `speculative`. In the So What, flag that the teardown is a hypothesis sketch — and recommend a `test-assumption` before using it to anchor a framing decision.

If an **existing teardown exists** for the same target:
  → Read it first. Ask whether to:
  - **Refresh** — update in place when changes are small; bump the date and note what changed in the body.
  - **Supersede** — rename the old to `teardown-<slug>-YYYY-MM-DD.md` and write a new file at `teardown-<slug>.md`. Use when the lens, scope, or underlying facts have materially shifted.
  - **Add a lens variant** — use a lens qualifier in the slug (e.g., `teardown-notion-pricing.md`) and link back to the primary teardown in the body.

## Gotchas

- **A features parade with no So What is the most common failure mode.** If the teardown reads as a list of "they have X, they have Y", the lens was not applied — return to step 3 and pick one. Five facts inside a lens beat fifty features outside one.
- **Competitor ≠ alternative.** The alternative is wherever the user's problem is solved (or tolerated) today. That is often the status quo, a spreadsheet, or email — not another product. A teardown that excludes the real alternative lets an overrated SaaS competitor set the bar.
- **Recency matters as much as depth.** Capture an access date next to every timestampable source. Omitting dates is the easiest way to mislead downstream readers.
