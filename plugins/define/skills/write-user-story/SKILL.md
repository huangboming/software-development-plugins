---
name: write-user-story
description: "Break a feature PRD (or slice) into well-formed user stories with acceptance criteria and write them to .product/define/stories/<feature>/<story-slug>.md — one story per file. Enforces story grain: each story is a vertical, user-observable, independently testable capability with Given/When/Then acceptance criteria, INVEST-checked, and sized to a few days of engineering work. Rejects epic grain (too large — must split) and task grain (too small — technical action, not user-visible). Reads .product/define/specs/<feature>/v<N>.md as primary input; falls back to .product/define/slices/<slug>.md when no PRD has been drafted. If the PRD already contains inline user stories, uses them as the starting point — does not invent a parallel set. Feeds the engineering backlog. Requires an existing PRD or slice as input — not for starting from scratch (use write-prd first). Not for drafting the spec itself (use write-prd), not for defining success metrics (use set-success-metrics), and not for scoping what to ship (use slice-mvp). Triggers: 'write user stories', 'write a user story', 'write stories for this feature', 'break down into stories', 'break this feature into stories', 'decompose the PRD into stories', 'decompose a feature into stories', 'split this feature into stories', 'turn this PRD into stories', 'build the backlog from this PRD', 'backlog stories', 'ready-for-dev stories', 'create tickets from this PRD', 'generate stories from the spec', 'create backlog tickets', 'as a user I want stories', 'story breakdown for this feature', 'user story breakdown', 'story grain', 'INVEST stories', '/write-user-story'."
---

# Write User Story

Decompose a feature PRD into well-formed user stories with Given/When/Then acceptance criteria and write them to `.product/define/stories/<feature>/<story-slug>.md` — one story per file. Each story is a vertical, user-observable, independently testable capability sized to a few days of engineering work, ready for a developer to pick up.

This skill writes the stories. It does not draft the spec (that is `write-prd`), does not define success metrics (that is `set-success-metrics`), and does not scope what ships (that is `slice-mvp`).

## References

- [references/story-template.md](references/story-template.md) — Template, field guidance, slug naming, status lifecycle, quality check, observability rewording test, summary format, and edge case playbook. Read at Step 4; consult the edge case playbook whenever an edge case condition applies.
- [references/splitting-patterns.md](references/splitting-patterns.md) — Splitting patterns catalog, grain-calibration table with size thresholds, and anti-patterns catalog (horizontal slice, task dressed as story, epic dressed as story, and-joined story). Read in Step 2 (splitting) and Step 3 (grain check).

## Process

Four steps: gather input, split into candidate stories, grain-check each candidate, write and confirm.

### 1. Gather input

Identify what to decompose:

- **User names a feature** → read `.product/define/specs/<feature>/v<N>.md` (highest N). If a matching slice or metrics doc exists at the same slug, read those too — they name the scope boundary and success signals the stories must honor.
- **User points to a slice (no PRD yet)** → read `.product/define/slices/<slug>.md`. Stories written against a slice alone are preliminary; note in each story file that a PRD has not been drafted and that the stories may churn once `write-prd` runs.
- **User says "write stories" without specifying** → list feature PRDs in `.product/define/specs/*/v*.md` that have no matching `.product/define/stories/<feature>/` folder. Ask which. If zero candidates exist, offer to run against a slice instead or route to `write-prd` first. If the user declines both, state that `write-user-story` requires either a PRD or a slice as input and stop.

Read the PRD's User Stories, Acceptance Criteria, Scope, and Out-of-scope (non-goals) sections in full. If the PRD already contains inline user stories, treat them as the starting draft — this skill formalizes, splits, and grain-checks them; it does not invent a parallel set.

### 2. Split into candidate stories

Generate a first-pass list of stories from the PRD's scope. Read the splitting patterns catalog in `splitting-patterns.md` and pick the pattern(s) that fit the feature.

- Start from the user flows and capabilities described in the PRD, not from the feature's internal modules or technical layers.
- Split vertically: each candidate must deliver something the user can observe end-to-end (submit a form, see a result, receive a notification), not a horizontal layer (add a table, wire up an endpoint).
- Name each candidate in the canonical form: "As a `<specific role>`, I want `<user-observable capability>`, so that `<concrete benefit>`."

Hold the candidate list for grain-check in Step 3 — do not ask the user to confirm yet. A single confirmation happens at the end of Step 3 with grain diagnosis attached.

If the candidate count exceeds the ceiling in the "Size heuristics" section of `splitting-patterns.md`, stop. Diagnose:

- If the PRD's scope spans more than one user job or more than one workflow, the PRD is too large → propose splitting into sub-features via `write-prd` and stop.
- Otherwise, the split is over-decomposed → apply the consolidation rules from the anti-patterns catalog in `splitting-patterns.md` (especially "and-joined story") and reduce the list before proceeding.

Present the diagnosis with the proposed action and wait for confirmation.

### 3. Grain-check each candidate

Every candidate must pass the grain test. The size thresholds and rewrite examples live in the grain-calibration table and anti-patterns catalog in `splitting-patterns.md`.

For each candidate, check all four gates:

1. **Not epic grain.** Exceeds the size bounds in `splitting-patterns.md` → split using one of the patterns in that file.
2. **Not task grain.** Names a technical action rather than a user-observable capability → merge into a user-facing story or drop. Tasks belong in an implementation plan, not the backlog.
3. **Independently testable.** If the candidate can only be observed after another unshipped story ships:
   - If combining the two still fits the size bounds, combine them into one story.
   - If combining would exceed the bounds, keep both and sequence — record the dependency in each story's Dependencies field with a link. The dependent story's Status is `blocked` until the prerequisite ships.
4. **Valuable on its own.** Shipping alone produces nothing user-visible → it is a task. Drop or fold into a user-facing story.

Drop or merge candidates that fail. Present the revised list with a one-line reason for each drop or merge (e.g., "dropped: technical task"; "merged into <slug>: no independent user value") and ask the user to confirm the final list before writing. If the user reinstates a candidate the grain-check dropped, write it with a `[GRAIN WARNING — reason]` note rather than silently accepting it.

### 4. Write and confirm

Execute the following in order:

1. For each confirmed story, draft every field as specified in the template in `story-template.md` — As-a/I-want/So-that, acceptance criteria in Given/When/Then, dependencies, size, open questions.
2. If a required field is blocked on input the user has not provided (user role not named in the PRD, edge case behavior undefined, dependency direction unclear), pause now. State the specific blocker and ask before proceeding, rather than inventing behavior the PRD did not authorize.
3. Run the **quality check** (first pass) from `story-template.md` against each drafted story. Apply the observability rewording test to every acceptance criterion. Fix violations in place.
4. Create `.product/define/stories/<feature>/` if it does not exist.
5. Write each story at `.product/define/stories/<feature>/<story-slug>.md` with Status `ready`. Slug naming is in `story-template.md` (one story per file, verb-led, kebab-case).
6. Append a `Stories:` link block pointing at the new story folder — to the source PRD if the input was a PRD (`.product/define/specs/<feature>/v<N>.md`), or to the source slice if the input was slice-only (`.product/define/slices/<slug>.md`). Do not change the source file's Status; that transitions later.
7. Run the quality check (second pass) against the written files as a final self-review. Fix any violations found in place.
8. Present the summary using the **Summary format** section of `story-template.md` and ask the user to confirm or correct. Apply corrections in place, re-run the quality check on changed stories, and re-present only what changed. If after one correction round a story still fails the grain test and the user cannot or will not resolve it, write the story with the blocker marked `[INCOMPLETE — reason]` and state what is needed before it is ready for dev pickup.

## Edge Cases

For edge cases (PRD has inline stories that conflict with the derived split, non-user stakeholder roles, spikes vs stories, cross-cutting concerns like logging/auth, existing stories for the same feature, slice-only input with no PRD, PRDs without acceptance criteria yet, contested size estimates), see the **Edge case playbook** section of `story-template.md`.
