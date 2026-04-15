---
name: prioritize-backlog
description: "Score and rank backlog items to decide what to build next. Triggers: 'prioritize', 'what should we build next', 'rank features', 'RICE score', 'ICE score', 'MoSCoW', 'WSJF', 'help me prioritize', '/prioritize-backlog'."
---

# Prioritize Backlog

Score and rank backlog items using a structured framework to decide what to build next. Produces a prioritization document at `docs/product/backlog/prioritization/<name>.md`.

## References

- [references/framework-guide.md](references/framework-guide.md) — Scoring definitions, formulas, scales, and worked examples for RICE, ICE, MoSCoW, Value vs Effort, and WSJF. Read when scoring items.
- [references/prioritization-template.md](references/prioritization-template.md) — Template for prioritization documents. Read when drafting the output.
- [references/scoring-guide.md](references/scoring-guide.md) — Scoring best practices, bias countermeasures, disagreement handling, and quality checklist. Read before and after scoring.

## Process

1. Load backlog and select framework
2. Triage (if needed)
3. Calibrate and score items
4. Draft the prioritization document
5. Update backlog and present

### Step 1: Load Backlog and Select Framework

#### Load Items

1. Read `docs/product/backlog/backlog.md`. Filter to items with status `Ready`.
2. If the user wants to include `New` items, warn: "New items may lack context for accurate scoring — consider clarifying them first."
3. If no backlog doc exists, ask: "Want me to create a backlog first, or do you have a list to score directly?"

#### Select Framework

| User Situation | Recommended Framework |
|---|---|
| Data-rich product team, feature-level decisions | **RICE** |
| Growth team, rapid experiment triage, early-stage product | **ICE** |
| Sprint or release scoping with stakeholders | **MoSCoW** |
| High-level strategic bet sizing, visual comparison | **Value vs Effort** |
| SAFe organization, PI planning, sequencing work | **WSJF** |
| No preference stated | Default to **RICE**; offer alternatives after |
| User names a specific framework | Use that framework |

If the user's situation suggests a different framework than the one they named, mention the alternative and why, but defer to their choice.

#### Establish Scope Anchors

Before scoring, align on three anchors that make scores comparable. Ask the user:

**Example:** "Before we score, I need to align on three things: (1) What time window for Reach estimates — per quarter? (2) What goal are we prioritizing toward? (3) How much capacity does the team have this cycle?"

### Step 2: Triage (If Needed)

Triage when there are more than 15 scorable items. Purpose is elimination, not precision.

1. For each item, quick High/Medium/Low judgment on **value** and **feasibility**.
2. Present a 3-bucket sort:

   | Bucket | Criteria | Next Step |
   |--------|----------|-----------|
   | **Score now** | High value, feasible | Proceed to Step 3 |
   | **Defer** | Low value or infeasible now | Park with one-line rationale |
   | **Needs clarity** | Cannot assess — missing context | Ask user to clarify |

3. Confirm the triage with the user before proceeding.

### Step 3: Calibrate and Score Items

Read [framework-guide.md](references/framework-guide.md) for scoring definitions and [scoring-guide.md](references/scoring-guide.md) for bias countermeasures.

#### Calibrate

1. **Pick a reference item.** Choose one item the user considers "medium" across dimensions. Score it together to establish the baseline.
2. **Align on scales.** Walk through what each score level means for *this* backlog. Concrete examples matter more than abstract labels.

#### Score Each Item

For each item:

1. Present the item name and description.
2. Walk through each scoring dimension in order:
   - State the question being answered
   - Propose a score with a one-sentence rationale
   - Ask the user to confirm, adjust, or provide context
3. Calculate the composite score.
4. Record the rationale — one sentence per dimension.

Scoring dimension order for each framework is defined in [framework-guide.md](references/framework-guide.md).

**Example scoring interaction (RICE):**

"**Item: CSV export for reports**
'Export reports and dashboards as CSV files — top customer request'

- **Reach:** ~3,200 users/quarter based on report page traffic. Does that sound right?
- **Impact:** High (2) — eliminates a manual copy-paste workflow for the core reporting use case. Agree?
- **Confidence:** 100% — we have 12 direct customer requests and analytics on report usage. Fair?
- **Effort:** 1.5 person-months (1 eng + 0.5 QA). Reasonable?

RICE = (3200 x 2 x 1.0) / 1.5 = **4,267**"

#### Validate the Ranking

After scoring all items, present the ranked list and ask: "Does this ranking feel right? Any items that seem too high or too low?"

If the user disagrees, explore which specific scores feel off rather than re-ranking arbitrarily. Adjust dimension scores with rationale, then recalculate.

### Step 4: Draft the Prioritization Document

Read [prioritization-template.md](references/prioritization-template.md) and [scoring-guide.md](references/scoring-guide.md).

1. Create `docs/product/backlog/prioritization/<name>.md` using the template. Name after the scope (e.g., `q2-features.md`, `sprint-14.md`).
2. Fill the scoring table with all items, ranked by composite score (descending).
3. Write a one-sentence rationale for each item.
4. Document excluded items with rationale and revisit trigger.
5. List key assumptions and what would change if wrong.
6. If capacity is constrained, draw a clear cut line: committed vs. stretch vs. next cycle.
7. Set "Last updated" to today's date and record participants.

#### Self-Review

Before presenting, check:

- Every item has a score *and* a rationale — numbers without reasoning are not useful
- Scores are calibrated — no dimension uniformly the same across all items
- Assumptions are stated, not hidden inside scores
- Excluded items have reasons documented
- The ranking passes the gut check — if #1 feels wrong, revisit the scoring

### Step 5: Update Backlog and Present

1. Update `docs/product/backlog/backlog.md` to reflect results:
   - Committed items → status `In Progress`
   - Deferred items → keep status, note in description when to revisit
   - Dropped items → status `Dropped` with rationale
2. Present the final prioritization to the user and ask for feedback.

## Edge Cases

If all items score similarly (within 10% of each other):
  → The framework isn't differentiating. Try: (1) decompose the most uncertain dimension with more granularity, (2) add a tiebreaker dimension (e.g., strategic alignment), or (3) switch to forced ranking for tied items.

If the user wants to override the framework's ranking:
  → Ask which specific scores they disagree with and why. Update scores to reflect new information, not the desired outcome. If the override is political, document it: "Manually prioritized above framework ranking per [stakeholder] — rationale: [reason]."

If a single stakeholder dominates scoring (HiPPO effect):
  → Suggest independent scoring: each participant scores privately, then compare. Discuss divergences before finalizing.

If the user cannot estimate Reach or Effort:
  → For Reach: check analytics, support ticket volume, or feature request counts. If no data, use Confidence=50% to penalize uncertainty. For Effort: propose t-shirt sizes (S/M/L/XL) mapped to the framework's scale. Flag as an assumption.

If the user wants to re-prioritize an existing document:
  → Read the existing prioritization at `docs/product/backlog/prioritization/`. Ask: "What changed?" — new data, competitive move, shifted objectives, revised effort estimates. Rescore only the affected items; carry forward unchanged scores.

If no backlog doc exists and the user asks to prioritize:
  → Offer to create the backlog first from their list, or proceed with a one-off prioritization without a persistent backlog doc.

If the user wants to combine frameworks (e.g., RICE + MoSCoW):
  → Two-pass approach: MoSCoW first to scope a release, then RICE within Must Have to sequence. Document both passes.
