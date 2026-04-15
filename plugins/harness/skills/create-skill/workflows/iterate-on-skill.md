# Workflow: Iterate on an Existing Skill

Run this workflow after the skill has been used on real tasks and at least one failure (or near-miss) has been observed. Use it standalone — there's no need to re-run `create-new-skill`.

## What to Capture on Each Failure

- The specific symptom (what Claude got wrong, not the general category).
- The default behavior that caused it (why Claude's baseline was incorrect here).
- The minimum correction — usually a single Gotchas bullet, workflow step, or rule.

## Step 1: Apply the Recording Threshold

Not every observation is worth saving — capturing trivia bloats the skill and dilutes high-cost lessons. Apply this 2-of-3 filter before adding anything:

- **Repeatable** — Will future tasks hit this again? One-off workarounds don't qualify.
- **Costly** — How much time does the baseline mistake waste? A few minutes of retry don't qualify; 30+ minutes of debugging does.
- **Code-invisible** — Could Claude infer this from reading the code? If the convention is already obvious from existing code, no capture is needed.

At least 2 of 3 must be true.

## Step 2: Generalize Before Recording

Captured lessons must read as portable patterns, not project narrative. Strip specific file, class, and feature names; reframe as a rule that survives a refactor.

| Weak (project narrative) | Strong (generalized) |
|--------------------------|----------------------|
| "In `OrderController`, always validate the product ID first" | "API handlers validate entity IDs before dispatching to the service layer" |
| "Our pagination resets when switching tabs in the Products view" | "When switching UI contexts (tab, view, filter), reset pagination to page 1" |
| "Don't forget `rebuildCache()` in `UserService.createUser`" | "Cached entities require explicit invalidation on create — the cache does not auto-rebuild" |

**The test:** if the specific file were renamed or deleted tomorrow, would the lesson still make sense? If not, generalize further.

## Step 3: Place the Lesson in the Right Location

Classify by content shape (see `references/skill-anatomy.md` for the full taxonomy):

- "You must do X" (imperative) → `rules/`
- "Do step 1, then step 2" (ordered) → `workflows/`
- "Be careful of X" / "X happens because Y" (descriptive) → `references/`
- Specific symptom + fix (quiet footgun) → `## Gotchas` in SKILL.md, or `references/gotchas.md` if the list grows large

## Step 4: Activate, Don't Just Store

A gotcha buried in a reference file is invisible unless Claude is routed to read it on the task that would trigger the failure. Storage alone is not activation — every capture needs a route.

Ask: "Will Claude actually encounter this on the task path that would hit the failure?" If no, the lesson is filed, not captured. Surface mechanisms, in order of preference:

1. Add to the `## Gotchas` section of SKILL.md (highest visibility — always loaded once the skill triggers).
2. Add to the specific workflow step's checklist or preconditions, so it fires during execution.
3. Add as an index entry in a referenced file that the task path already loads.

If the failing task path doesn't currently load any file that would surface the lesson, either promote the lesson to SKILL.md directly or update routing so the right reference gets loaded.

## Step 5: Prefer Gotchas Over Rewrites

Gotchas entries are cheap, composable, and accumulate into institutional knowledge. Rewrites lose signal and often undo valid prior decisions. Escalate beyond a Gotchas entry only when:

- The same failure recurs despite the entry — move it higher in SKILL.md or make it more imperative.
- A new use case emerges that the current structure cannot express — then restructure.
- A Gotchas list grows past ~10 entries in one skill — cluster by theme, or lift recurring patterns into scripts or references.

Iterate right after using the skill, while the failure mode is still fresh. A week later the specifics are gone and only a vague "it didn't work well" remains — not enough to write a useful entry.
