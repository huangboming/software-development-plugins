---
name: slice-mvp
description: "Scope the smallest coherent shippable thing from a committed opportunity and write it to .product/define/slices/<slug>.md. Slash command: /slice-mvp. Decides in/out/not-now, picks a slicing shape (walking skeleton, vertical slice, concierge, Wizard of Oz, configuration-only, read-only, batch-before-real-time), and commits pre-written success and kill signals before the PRD is drafted. Operates on opportunities with Status `committed` — run prioritize first. Feeds write-prd. Requires a committed opportunity — not for deciding what to build next (use prioritize) and not for writing the spec (use write-prd). Triggers: 'slice the MVP', 'scope the MVP', 'carve an MVP', 'MVP slice', 'smallest shippable thing', 'simplest version of this', 'thin slice', 'lean MVP', 'what should we ship first', 'walking skeleton', 'minimum viable scope', 'v1 scope', 'what goes in v1', 'cut scope', 'scope down this opportunity', 'what''s in / what''s out', 'scope this after we''ve decided to build'."
---

# Slice MVP

Slice a committed opportunity into the smallest coherent shippable thing and write it to `.product/define/slices/<slug>.md`. The slice commits a user + job, in/out/not-now scope, a slicing shape, and pre-written success and kill signals *before* the PRD is drafted — so scope is disciplined by evidence and hypothesis, not by whoever pushes loudest.

This skill scopes the slice. It does not write the spec (that is `write-prd`) and it does not run experiments (that is `test-assumption`).

## References

- [references/slice-template.md](references/slice-template.md) — Template and field guidance: slicing shape selection, in/out/not-now calibration, success/kill signal specificity, sizing bar, slug naming, status lifecycle, summary format. Read before writing (Step 3). Also contains the quality check (falsifiability, pushback test, rewording test) — run before writing the file (Step 4).
- [references/slicing-patterns.md](references/slicing-patterns.md) — Catalog of slicing shapes (walking skeleton, vertical slice, concierge, Wizard of Oz, configuration-only, read-only, batch-before-real-time). Each with what-it-tests, when-to-pick, gotchas, and a minimal example. Read in Step 2 for the risk-type selection table, and in Step 3 for shape preconditions and gotchas.

## Process

Four steps: gather input, pick the load-bearing risk, scope the slice, write and confirm.

### 1. Gather input

Identify which opportunity to slice:

- **User names a slug** → read `.product/discover/opportunities/<slug>.md` and its tree at `.product/discover/opportunities/tree-<slug>.md` if one exists.
- **User points to a prioritization doc** → read it, list its `committed` opportunities, ask which to slice. One slice per invocation.
- **User says "slice the MVP" without specifying** → list opportunities in `.product/discover/opportunities/*.md` with Status `committed` that have no existing slice in `.product/define/slices/`. Ask which. If zero candidates exist, route to `prioritize` first.

If the selected opportunity is not `committed`:
  → Pause. Slicing a `framed` or `drafted` opportunity commits scope before the decision to build is made. Offer to route to `prioritize` first. If the user confirms they are slicing ahead of a decision, continue with Steps 2–4 unchanged and add a one-sentence note to the slice's Assumptions section: "Scoped before prioritize was run; build decision is not yet committed."

### 2. Pick the load-bearing risk

A slice must earn its ship by answering a specific question. Name it before scoping.

Read the opportunity's Confidence field and the tree's Risk fields (if a tree exists). Classify the risk as desirability, feasibility, or viability — definitions and the shape-selection table are in `slicing-patterns.md`.

If two risks are load-bearing, pick the one whose failure would most change the shape of v2. The other becomes a v2 hypothesis, recorded in Not now. If the two risks are genuinely symmetric (equal v2 impact, no visible differentiator), surface both to the user with a one-sentence consequence for each and ask which anchors the slice — do not arbitrarily pick one.

If no risk is load-bearing (the opportunity is fully de-risked), slicing is still useful for capacity discipline — default to the narrowest single-user-single-job vertical slice. Do not manufacture risk to justify a more elaborate shape.

### 3. Scope the slice

Make these decisions in order — each constrains the next. Field rules, formats, and calibration are in `slice-template.md`.

1. **Hypothesis.** One sentence: what the shipped slice will prove or deliver. Must be falsifiable — a reader can name an observation that would contradict it.
2. **Slicing shape.** Pick from `slicing-patterns.md`, driven by the load-bearing risk. Check preconditions (team skill, infra, user access) before committing; do not default to walking skeleton because it is familiar.
3. **User and job.** One segment, one job-to-be-done. If the opportunity's Who field is broad, ask the user to pick the sharpest cut — the segment with the most acute pain and clearest reach.
4. **In / Out / Not now.** Three lists. Formats are in `slice-template.md`; follow the pushback test for each Out item.
5. **Success and kill signals.** Both quantitative, both written before the slice ships. Leave an inconclusive zone between them. Use the rewording test in `slice-template.md`.
6. **Sizing bar.** Upper bound in eng-weeks or sprints. If the user has not provided one, ask — do not estimate without team context.

### 4. Write and confirm

Run the quality check in `slice-template.md` against the six scope decisions and correct any violation in place. If a violation cannot be corrected without input the user has not yet provided — e.g., the success signal cannot be made quantitative without a baseline, or the segment cannot be narrowed without data — pause. State which field is blocked and what is needed, and ask before writing the file.

Then:

1. Create `.product/define/slices/` if it does not exist.
2. Write the slice at `.product/define/slices/<slug>.md` with Status `drafted`. Slug naming is in `slice-template.md` — usually reuse the source opportunity's slug.
3. Update the source opportunity's `Status` frontmatter field to `sliced` and add a link to the slice file.
4. Present a summary using the format in `slice-template.md` and ask the user to confirm or correct. Apply corrections in place, re-run the quality check on changed fields, and re-present only what changed. If after one correction round a field still fails the quality check and the user cannot or will not resolve it, write the file with the field marked `[INCOMPLETE — reason]` and state what is needed before `write-prd` can consume the slice.

## Edge Cases

If the **opportunity has no tree** (`map-opportunities` was skipped):
  → Slicing is still possible but risk identification in Step 2 becomes coarser. Lean on the opportunity's Confidence and Cost of Inaction to infer risk type. If risk cannot be identified with confidence, offer to run `map-opportunities` first for a sharper slice.

If the user wants to **slice across two opportunities at once**:
  → Decline. A slice that spans two framings has two problem statements, two success signals, and two users — it becomes a product PRD, not a slice. Ask which opportunity to slice first; the other becomes a later slice or a Not now entry.

If the **committed opportunity is already narrow** (a single user, a single job, clearly de-risked):
  → Slicing still produces an In / Out / Not now discipline that the PRD consumes. Write the slice with a narrower scope section — the signals still pass the quality check (quantitative, pre-written, with an inconclusive zone). Do not manufacture risk to justify a more elaborate shape.

If **every scope decision triggers a stakeholder conflict** ("sales insists on bulk import", "eng insists on real-time"):
  → Write the slice anyway, putting disputed items in Out with the named pushback and rationale. A slice that satisfies every stakeholder is a full PRD in disguise. Route unresolved conflicts to the user for a call before writing the file.

If an **existing slice exists** for the same opportunity:
  → Read it first. Ask whether to:
  - **Supersede** — rename the old to `<slug>-YYYY-MM-DD.md`, set its Status to `superseded`, and write a new slice at `<slug>.md`. Use when v1 shipped and v2 needs its own slice, or when the prior slice was abandoned.
  - **Iterate in place** — overwrite if the slice has not yet been handed to `write-prd` (Status still `drafted`).

If the **load-bearing risk is an unresolved assumption** already listed in `.product/discover/assumptions/`:
  → Check whether a test plan exists and whether it has landed. If the test is still open, offer to wait for the result before slicing — a slice built on an untested high-risk assumption is a spec of hope. If the user wants to slice anyway, name the pending test in Assumptions and keep v1 scope contingent on the result.
