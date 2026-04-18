---
name: map-opportunities
description: "Build an opportunity solution tree (OST) from a framed problem and write it to .product/discover/opportunities/tree-<slug>.md. Operates on an already-framed opportunity — run frame-problem first if no file exists in .product/discover/opportunities/. Triggers: 'map opportunities', 'opportunity solution tree', 'explore solution shapes', 'solution options', 'map the solution space', 'diverge on solutions for this opportunity', 'surface assumptions for this opportunity', 'what do we need to learn before building', 'what are our options here', '/map-opportunities'."
---

# Map Opportunities

Build an opportunity solution tree (OST) from a framed opportunity. Output is a markdown tree written to `.product/discover/opportunities/tree-<slug>.md`. The tree branches the desired outcome into sub-outcomes, then into candidate solutions — forcing divergent thinking before any one solution is committed to.

## References

- [references/tree-template.md](references/tree-template.md) — Template for the OST document and field guidance (root outcome test, sub-outcome criteria, solution framing, key-assumption guidance, risk calibration table with downstream routing rule for `test-assumption`, per-node branch-count ranges, slug naming). Read before writing a tree.
- [references/divergence-techniques.md](references/divergence-techniques.md) — Prompts and tactics for generating multiple branches at each level: HMW reframing, journey and context slicing, analogous-domain prompts, constraint removal, reach-branch prompts, stopping signals. Read when a branch feels thin or the user is converging too early.

## Process

Four steps: gather the framed opportunity, verify the root outcome, diverge through two levels, review and write.

### 1. Gather Input

Identify the framed opportunity to map. Three input shapes:

- **User points to an opportunity file** (path or slug) → read it.
- **User names the problem inline** → scan `.product/discover/opportunities/` for files whose name, Who, or Pain field overlaps the user's stated problem. If exactly one file matches, use it and state the match explicitly. If multiple match, list them and ask the user to confirm. If none match, offer to frame one first via `frame-problem` — a tree without a framed root is exploratory brainstorming, not structured divergence.
- **User says "map opportunities" without specifying** → list framed-eligible opportunities (any file in `.product/discover/opportunities/` with Status `framed` and no existing `tree-<slug>.md`) and ask which to map. If zero eligible files exist, surface that and offer to run `frame-problem` first.

### 2. Verify Root Outcome

Read the framed opportunity's **What Good Looks Like** field. That is the root of the tree. Before diverging, check the root passes the outcome test:

- Describes an end state for the affected user, not a feature we ship.
- Does not name a specific UI, screen, or product mechanic.

If the root is solution-shaped (e.g., "we add a config wizard"), stop. Surface the issue and offer to route back to `frame-problem` — a tree rooted in a solution cannot produce honest divergence because one branch has already been chosen.

If the framed opportunity is too broad (multiple Whos or Pains bundled), apply the same splitting check as `frame-problem`: ask the user to split it into distinct files first, then map each. A tree built on a conflated opportunity silently mixes users across branches.

### 3. Diverge

Two levels of divergence. At each level, generate all branches first; evaluation happens in step 4 before the file is written.

**Level 1 — Sub-outcomes (the opportunities).** Break the root into at least 3 specific unmet needs, journey-stage frictions, or contextual sub-problems that, if addressed, would move the user toward the desired outcome. Each sub-outcome is itself outcome-shaped — no solutions yet. Use prompts from [divergence-techniques.md](references/divergence-techniques.md) when stuck.

**Level 2 — Solutions per sub-outcome.** For each sub-outcome, generate at least 3 candidate solutions. Include at least one **reach** solution per sub-outcome — a deliberately unconventional or uncomfortable idea whose job is to widen the space, not to be selected. Use prompts from [divergence-techniques.md](references/divergence-techniques.md) when stuck — especially HMW reframing, analogous-domain prompts, and reach-branch prompts. For each solution, name its **key assumption** — the single load-bearing claim that, if wrong, the solution cannot produce the sub-outcome's desired state. This is the handoff to `test-assumption`.

If the user has a preferred solution and wants the tree to validate it, reframe the task: include their solution as one branch among ≥3 competitors for its sub-outcome. If they decline alternatives, stop the tree — route to `test-assumption` directly and tell the user they must provide the key assumption themselves, since no tree will be written.

See [tree-template.md](references/tree-template.md) for productive branch-count ranges at each node and the signal that a parent node should split.

### 4. Review and Write

Before writing, run the quality check against each branch:

- Each sub-outcome passes the outcome test (end state for the user, not a feature).
- Each sub-outcome has at least 3 solutions.
- Each sub-outcome includes at least 1 reach solution.
- Each solution names a specific key assumption and a risk level per `tree-template.md`.

Correct any violations in place. Then:

1. Create `.product/discover/opportunities/` if it does not exist.
2. Write the tree at `.product/discover/opportunities/tree-<slug>.md`, matching the slug of the source framed opportunity.
3. Present a summary: sub-outcome count, solution count, reach solutions highlighted, and any high-risk assumptions. Ask the user to review.

**Summary example:**

```
Mapped: **new-admin-config-inheritance**
- Source: .product/discover/opportunities/new-admin-config-inheritance.md
- Root outcome: A new admin reaches a working configuration in under 10 minutes, without support
- 4 sub-outcomes × 14 solutions (3 reach)
- 3 solutions carry high-risk assumptions → strong candidates for test-assumption
- File: .product/discover/opportunities/tree-new-admin-config-inheritance.md

Next: test-assumption on the riskiest branch, or prioritize (in define) once the riskiest assumptions have been tested.
```

## Edge Cases

If the framed opportunity **has no "What Good Looks Like"** (field empty or "Not determined"):
  → Stop. A tree without a root outcome is exercise-without-direction. Route to `frame-problem` to complete the field first.

If an **existing tree exists** for the same opportunity:
  → Read it first. Ask whether to:
  - **Supersede** — rename the old to `tree-<slug>-YYYY-MM-DD.md` and write a new tree at `tree-<slug>.md`.
  - **Extend** — add new branches in place, annotate additions with `[added — YYYY-MM-DD]`, and re-apply the divergence minimums to the *merged* tree: flag any sub-outcome that falls below ≥3 solutions or lacks a reach after merging.
  - **Start fresh with a different scope** — treat as a new mapping against a distinct scope; choose a new slug (e.g., adding a scope qualifier) so the existing file stays at its path. If "different scope" collapses to the same slug, merge with supersede instead.

## Gotchas

- **One or two solutions per sub-outcome is usually silent evaluation during generation, not genuine scarcity.** When a branch stops early, ideas have almost always been pruned privately while generating them — before they reached the page. Generate all branches first; evaluate in step 4.
