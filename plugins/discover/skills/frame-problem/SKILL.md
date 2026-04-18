---
name: frame-problem
description: "Frame a research theme or signal cluster into a structured opportunity (Who / Pain / Why Now / Cost of Inaction / What Good Looks Like) and write it to .product/discover/opportunities/. Produces the handoff artifact from discover to define. Triggers: 'frame this problem', 'frame a problem', 'turn this theme into an opportunity', 'turn this into a problem statement', 'write a problem statement', 'write an opportunity', 'create an opportunity brief', 'formalize this problem', 'what's the opportunity here', 'frame the opportunity', 'opportunity brief', 'ready to frame from synthesis', '/frame-problem'."
---

# Frame Problem

Turn upstream research or signals into a framed opportunity and write it to `.product/discover/opportunities/<slug>.md`. A framed opportunity is the handoff artifact from `discover` to `define` — it names a problem narrowly enough to prioritize against, while leaving the solution space open.

## References

- [references/opportunity-template.md](references/opportunity-template.md) — Template for opportunity records and field guidance (Who specificity test, Pain observability test, outcome-vs-solution criterion for What Good Looks Like, confidence calibration, status lifecycle, slug naming, classification examples). Read before writing a framed opportunity.

## Process

Four steps: gather upstream input, classify what was given, structure the framed problem, write and confirm.

### 1. Gather Upstream Input

Identify what to frame. Three input shapes:

- **User points to a synthesis** (a file in `.product/discover/research/` or an explicit theme name) → read the synthesis, focus on the named theme and its grounding signals.
- **User describes a theme or problem inline** → use it as the seed, then scan `.product/discover/research/` and `.product/discover/signals/` for related evidence to link.
- **User says "frame a problem" without specifying** → list framed-eligible themes in `.product/discover/research/` (any theme at `strong` or `moderate` strength that is not already represented in `.product/discover/opportunities/`) and ask which to frame.

Before structuring, confirm at least one grounding signal or research theme exists. If none exists, proceed but default Confidence to `speculative` and name the evidence gap in the opportunity body.

### 2. Classify Input

Route by shape:

- **Problem-shaped** (describes a user, a pain, a situation — no solution embedded) → proceed to step 3.
- **Solution-shaped** ("we should build X", "add feature Y", "ship a dashboard for Z") → reframe before structuring (see reframing example below). If the user insists on solution framing: (1) accept once, (2) write their original input verbatim in the Hypothesis field, (3) frame the best-inferred underlying problem in Who / Pain / What Good Looks Like, (4) set Confidence to `speculative`, and (5) add a body note: "Framing is user-directed from a stated solution; underlying problem is inferred." If no underlying problem can be inferred, write "Not determined" in Pain and proceed — the file still gets written, with Hypothesis populated.
- **Too-broad theme** (covers multiple distinct users or multiple distinct pains) → ask the user to split. Each opportunity should have one Who and one Pain; mixing them blocks prioritization. If the user declines to split, proceed with the broadest scoping they provide, drop Confidence one level below what evidence would otherwise support, and note in the body which sub-segments were combined. See `references/opportunity-template.md` for a splitting example.

**Reframing example — solution to problem:**

```
User: "Frame an opportunity for a config wizard for new admins."

Agent: "That names a solution. What's the underlying problem —
       what do new admins experience today that a wizard would address?"

User: "They inherit a config from the last admin, can't tell which settings
      matter, and we see a spike in support tickets in their first week."

→ Who: B2B admins inheriting a configuration from a predecessor
  Pain: First-week support tickets spike; admins ask which inherited
        settings still apply
  What good looks like: A new admin reaches a working configuration in
        under 10 minutes without support
  (The wizard is one possible solution — captured for map-opportunities,
   not locked in here.)
```

### 3. Structure the Problem

Read [opportunity-template.md](references/opportunity-template.md) for the template and field guidance, then fill each field applying the tests described there (Who specificity, Pain observability, Why Now trigger anchoring, outcome-vs-solution for What Good Looks Like, Confidence calibration). Populate Hypothesis only when framing was user-directed from a stated solution (see step 2); omit the section otherwise.

### 4. Write and Confirm

1. Create `.product/discover/opportunities/` if it does not exist.
2. Write the opportunity at `.product/discover/opportunities/<slug>.md` with Status `framed`.
3. Present a summary and ask the user to confirm or correct. If the user requests corrections, apply them in place, re-test the corrected fields against the reference criteria, update the file, and re-present only the changed fields — do not restart the full process.

**Summary example:**

```
Framed: **New admins inherit a broken configuration**
- Who: B2B admins inheriting config from a predecessor
- Pain: First-week support tickets spike (+42% in Q1)
- Confidence: moderate (synthesis theme "admin handoff" + 3 signals)
- File: .product/discover/opportunities/new-admin-config-inheritance.md

Next: map-opportunities (explore solution shapes) or prioritize (in define).
```

For batch framing (multiple themes handed over at once): scan all inputs first and collect classification flags (solution-shaped, too-broad) together, surface them in one pass before processing any, then process each opportunity through steps 2–4 and present a summary table at the end with one row per opportunity.

## Edge Cases

If the input is **a raw signal with no synthesis** (a single observation, untested):
  → Framing off one signal produces anecdote-shaped opportunities. Offer to run `synthesize-research` first if other related signals exist. If the user wants to proceed, frame with Confidence `speculative` or `emerging` and name the thin evidence in the body.

If an **existing opportunity overlaps** the one being framed:
  → Read the existing file. Ask whether to merge (update the existing file, add evidence), supersede (archive the old, write a new one, link them in Related Opportunities), or keep separate (if the Who or Pain is genuinely different).

If **Why Now cannot be answered**:
  → Proceed with the framing but write "No recent trigger identified" in the Why Now field and drop Confidence one level. A problem without a recent trigger is often a `someday` problem — surface that to the user. If Confidence is already `speculative` (no grounding signal exists), the one-level drop is a no-op — do not invent a lower level. Instead, flag to the user that the opportunity has both thin evidence and no timing anchor, and note it as a strong candidate for `test-assumption` before prioritization.

If the user provides **a finished opportunity statement inline** (already structured):
  → Do not re-author. Validate each field against the tests in the reference (Who specificity, Pain observability, outcome-vs-solution). Fix failing fields; write the file; surface what was changed.

## Gotchas

- **"Users" is the most common Who failure.** If the Who is "users" or "customers", the opportunity cannot be prioritized — every initiative claims it helps users. Narrow to a segment a reader can picture.
- **`test-assumption` is the right way to raise Confidence.** Overrating here to make an opportunity feel shippable skips validation and contaminates prioritization downstream.
- **Evidence links that go stale are worse than no links.** Before linking a signal or synthesis file, confirm it exists on disk. A broken path reads as fabricated evidence when it is really just a typo.
