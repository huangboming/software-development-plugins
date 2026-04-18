---
name: prioritize
description: "Score and rank framed opportunities in .product/discover/opportunities/ to decide what to spec next. Writes a prioritization document to .product/define/prioritization/. Triggers: 'prioritize', 'prioritize opportunities', 'what should we build next', 'which opportunity first', 'rank opportunities', 'rank features', 'RICE score', 'ICE score', 'MoSCoW', 'WSJF', 'help me prioritize', '/prioritize'."
---

# Prioritize

Score and rank framed opportunities using a structured framework to decide which to spec next. Reads framed opportunities from `.product/discover/opportunities/*.md`, writes a prioritization document to `.product/define/prioritization/<name>.md`, and updates the Status field on each opportunity that was decided in this round.

## References

- [references/framework-guide.md](references/framework-guide.md) — Scoring definitions, formulas, scales, and worked examples for RICE, ICE, MoSCoW, Value vs Effort, and WSJF. Read when scoring items.
- [references/prioritization-template.md](references/prioritization-template.md) — Template for prioritization documents. Read when drafting the output.
- [references/scoring-guide.md](references/scoring-guide.md) — Scoring best practices, bias countermeasures, disagreement handling, and quality checklist. Read before and after scoring.

## Process

1. Load opportunities and select framework
2. Triage (if needed)
3. Calibrate and score opportunities
4. Draft the prioritization document
5. Update opportunity status and present

### Step 1: Load Opportunities and Select Framework

#### Load Opportunities

1. List `.product/discover/opportunities/*.md`. Read each and filter to those with Status `framed` (ready to prioritize against).
2. Exclude opportunities already marked `committed`, `deferred`, or `dropped` — those have been decided. If the user wants to re-prioritize a previously decided opportunity, include it explicitly.
3. If no framed opportunities exist, ask: "No framed opportunities found. Want to `frame-problem` first, or do you have a list to score directly?"

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

Triage when there are more than 15 scorable opportunities. Purpose is elimination, not precision.

1. For each opportunity, quick High/Medium/Low judgment on **value** and **feasibility**.
2. Present a 3-bucket sort:

   | Bucket | Criteria | Next Step |
   |--------|----------|-----------|
   | **Score now** | High value, feasible | Proceed to Step 3 |
   | **Defer** | Low value or infeasible now | Park with one-line rationale |
   | **Needs clarity** | Cannot assess — missing context | Route back to `frame-problem` or `test-assumption` |

3. Confirm the triage with the user before proceeding.

### Step 3: Calibrate and Score Opportunities

Read [framework-guide.md](references/framework-guide.md) for scoring definitions and [scoring-guide.md](references/scoring-guide.md) for bias countermeasures.

#### Calibrate

1. **Pick a reference opportunity.** Choose one the user considers "medium" across dimensions. Score it together to establish the baseline.
2. **Align on scales.** Walk through what each score level means for *this* set of opportunities. Concrete examples matter more than abstract labels.

#### Score Each Opportunity

For each opportunity:

1. Present its name and one-sentence problem statement (from the opportunity file's Who / Pain fields).
2. Walk through each scoring dimension in order:
   - State the question being answered
   - Propose a score with a one-sentence rationale
   - Ask the user to confirm, adjust, or provide context
3. Calculate the composite score.
4. Record the rationale — one sentence per dimension.

Scoring dimension order for each framework is defined in [framework-guide.md](references/framework-guide.md).

**Example scoring interaction (RICE):**

"**Opportunity: weekly-report-reauthoring**
'Marketing managers spend 2+ hours each Monday compiling performance data from three tools.'

- **Reach:** ~3,200 users/quarter based on report page traffic. Does that sound right?
- **Impact:** High (2) — eliminates a manual copy-paste workflow for the core reporting use case. Agree?
- **Confidence:** 100% — we have 12 direct customer requests and analytics on report usage. Fair?
- **Effort:** 1.5 person-months (1 eng + 0.5 QA). Reasonable?

RICE = (3200 x 2 x 1.0) / 1.5 = **4,267**"

#### Validate the Ranking

After scoring all opportunities, present the ranked list and ask: "Does this ranking feel right? Any opportunities that seem too high or too low?"

If the user disagrees, explore which specific scores feel off rather than re-ranking arbitrarily. Adjust dimension scores with rationale, then recalculate.

### Step 4: Draft the Prioritization Document

Read [prioritization-template.md](references/prioritization-template.md) and [scoring-guide.md](references/scoring-guide.md).

1. Create `.product/define/prioritization/<name>.md` using the template. Name after the scope (e.g., `q2-opportunities.md`, `sprint-14.md`).
2. Fill the scoring table with all opportunities, ranked by composite score (descending). Link each row to its source opportunity file.
3. Write a one-sentence rationale for each opportunity.
4. Document excluded opportunities with rationale and revisit trigger.
5. List key assumptions and what would change if wrong.
6. If capacity is constrained, draw a clear cut line: committed vs. stretch vs. next cycle.
7. Set "Last updated" to today's date and record participants.

#### Self-Review

Before presenting, check:

- Every opportunity has a score *and* a rationale — numbers without reasoning are not useful
- Scores are calibrated — no dimension uniformly the same across all opportunities
- Assumptions are stated, not hidden inside scores
- Excluded opportunities have reasons documented
- The ranking passes the gut check — if #1 feels wrong, revisit the scoring

### Step 5: Update Opportunity Status and Present

1. Update the Status field on each source opportunity file in `.product/discover/opportunities/`:
   - Committed → Status `committed` (next step: `write-prd`)
   - Deferred → Status `deferred`, note revisit trigger in the opportunity file
   - Dropped → Status `dropped` with one-line rationale
   - Unscored (triaged out, needs clarity) → leave Status as `framed` and note the routing in the prioritization doc
2. Present the final prioritization to the user and ask for feedback.

## Edge Cases

If all opportunities score similarly (within 10% of each other):
  → The framework isn't differentiating. Try: (1) decompose the most uncertain dimension with more granularity, (2) add a tiebreaker dimension (e.g., strategic alignment), or (3) switch to forced ranking for tied opportunities.

If the user wants to override the framework's ranking:
  → Ask which specific scores they disagree with and why. Update scores to reflect new information, not the desired outcome. If the override is political, document it: "Manually prioritized above framework ranking per [stakeholder] — rationale: [reason]."

If a single stakeholder dominates scoring (HiPPO effect):
  → Suggest independent scoring: each participant scores privately, then compare. Discuss divergences before finalizing.

If the user cannot estimate Reach or Effort:
  → For Reach: check analytics, support ticket volume, or feature request counts. If no data, use Confidence=50% to penalize uncertainty. For Effort: propose t-shirt sizes (S/M/L/XL) mapped to the framework's scale. Flag as an assumption.

If the user wants to re-prioritize an existing document:
  → Read the existing prioritization at `.product/define/prioritization/`. Ask: "What changed?" — new data, competitive move, shifted objectives, revised effort estimates. Rescore only the affected opportunities; carry forward unchanged scores.

If no opportunities exist and the user asks to prioritize a raw list:
  → Offer to run `frame-problem` first on each item so they become comparable opportunities, or proceed with a one-off prioritization against the raw list without persisting opportunity files.

If the user wants to combine frameworks (e.g., RICE + MoSCoW):
  → Two-pass approach: MoSCoW first to scope a release, then RICE within Must Have to sequence. Document both passes.
