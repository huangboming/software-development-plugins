# Framework Guide

## Contents

- [RICE](#rice) — Reach, Impact, Confidence, Effort. Data-rich feature prioritization.
- [ICE](#ice) — Impact, Confidence, Ease. Rapid experiment triage.
- [MoSCoW](#moscow) — Must/Should/Could/Won't. Sprint or release scoping.
- [Value vs Effort Matrix](#value-vs-effort-matrix) — 2x2 quadrants. Strategic bet sizing.
- [WSJF](#wsjf-weighted-shortest-job-first) — Cost of Delay / Job Size. SAFe sequencing.

## Quick Reference

| Framework | Formula | Best For | Scoring Speed |
|-----------|---------|----------|---------------|
| RICE | (Reach × Impact × Confidence) / Effort | Data-rich product teams | ~5 min/item |
| ICE | Impact × Confidence × Ease | Growth experiments, early-stage | ~2 min/item |
| MoSCoW | Category assignment | Stakeholder alignment, release scoping | ~1 min/item |
| Value vs Effort | Quadrant placement | Visual strategic discussion | ~2 min/item |
| WSJF | Cost of Delay / Job Size | SAFe, sequencing by economic value | ~5 min/item |

---

## RICE

**Origin:** Sean McBride at Intercom. Best for data-rich product teams making feature-level decisions.

### Formula

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

The result is "total impact per unit of work" — higher scores go first.

### Dimensions

| Dimension | Question | Unit | Scale |
|-----------|----------|------|-------|
| **Reach** | How many people will this impact in the time window? | Actual number (customers/quarter, transactions/month) | Use real analytics data. Not a 1-10 scale — use the actual count. |
| **Impact** | How much will this impact each person reached? | Fixed multiplier | Massive=3, High=2, Medium=1, Low=0.5, Minimal=0.25 |
| **Confidence** | How confident are you in the Reach and Impact estimates? | Percentage | High=100%, Medium=80%, Low=50%, Moonshot=20% |
| **Effort** | Total team time to ship (all roles, not just engineering) | Person-months | Whole numbers or 0.5 minimum. Include design, PM, QA. |

### Scoring Guidance

**Reach:** Use a consistent time window across all items (e.g., all "per quarter"). Pull from analytics when possible. If estimating, use Confidence to reflect the uncertainty.

**Impact:** This is the hardest to score honestly. The five-point scale prevents false precision. Resist inflating to Massive (3) without strong evidence — the gap between Massive and Medium is a 3x swing in the final score.

**Confidence:** The honesty dial. It penalizes guesswork. If your Impact estimate is based on qualitative feedback from three customers rather than quantitative data, that's 50%. Teams systematically inflate this — default to 50% when uncertain rather than 80%.

**Effort:** Include all roles: engineering, design, PM coordination, QA, documentation. A feature needing 1 engineer-month + 0.5 designer-months + 0.5 PM-months = 2 person-months.

### Example

| Item | Reach | Impact | Confidence | Effort | RICE Score |
|------|-------|--------|------------|--------|------------|
| CSV export for reports | 3,200/quarter | High (2) | 100% | 1.5 | 4,267 |
| AI-powered search | 8,000/quarter | Massive (3) | 50% | 4 | 3,000 |
| Dark mode | 12,000/quarter | Low (0.5) | 80% | 2 | 2,400 |

Despite AI search having higher Reach and Impact, CSV export wins because of high Confidence and low Effort.

---

## ICE

**Origin:** Sean Ellis (GrowthHackers). Best for growth teams running rapid experiments, or early-stage products with sparse data.

### Formula

```
ICE Score = Impact × Confidence × Ease
```

All dimensions use a 1-10 scale. The result is a relative ranking — absolute values are meaningless across different backlogs.

### Dimensions

| Dimension | Question | Scale |
|-----------|----------|-------|
| **Impact** | How much will this move the target metric? | 1-10 (10 = transformative improvement) |
| **Confidence** | How confident are you in the Impact and Ease estimates? | 1-10 (10 = certainty based on data) |
| **Ease** | How easy is it to implement? (inverse of Effort) | 1-10 (10 = trivial, 1 = massive project) |

### ICE vs RICE: When to Choose

| Choose ICE When | Choose RICE When |
|---|---|
| Analytics data is sparse | Reach data is available from analytics |
| Speed matters — many items to score quickly | Precision matters — fewer items, higher stakes |
| Growth experiments with clear success metrics | Feature prioritization with diverse user populations |
| Team is comfortable with subjective 1-10 scales | Team wants anchored, data-driven estimates |

### Example

| Item | Impact | Confidence | Ease | ICE Score |
|------|--------|------------|------|-----------|
| Onboarding tooltip tour | 7 | 8 | 9 | 504 |
| Referral program | 9 | 4 | 3 | 108 |
| Simplify signup form | 6 | 9 | 8 | 432 |

---

## MoSCoW

**Origin:** Dai Clegg, 1994 (DSDM). Best for sprint or release scoping with stakeholders. Simple enough for non-technical participants.

### Categories

| Category | Definition | Test Question |
|----------|-----------|---------------|
| **Must Have** | Non-negotiable; the release fails without it | "Would the release be unusable, illegal, or unsafe without this?" |
| **Should Have** | Important and expected but survivable if absent | "Is this painful to omit but not a showstopper?" |
| **Could Have** | Nice-to-have; marginal value | "Could we ship a complete, valuable product without this?" → Yes = Could Have |
| **Won't Have** | Explicitly out of scope for this time box | "Is this a future cycle candidate, not now?" |

### Process

1. **Define the time box first.** MoSCoW without a time box is meaningless. "For sprint 14" produces different results than "for Q2 release."
2. **Start with Won't Have.** This creates the constraint boundary and prevents scope creep by explicitly parking items.
3. **Apply Must Have with skepticism.** The test is "fails without it," not "important to someone."
4. **Enforce the 60% rule.** Must Haves should consume no more than 60% of available capacity. If they exceed this, the time box is wrong or Must Haves are inflated.
5. **Use dot voting for disputes.** Each participant gets 3 dots to place on items they believe are Must Have. Items without multiple dots get demoted.

### Must-Have Inflation

The dominant failure mode — everything becomes Must Have. Correctives:

- Hard ratio: at most 40% of items can be Must Have
- Historical test: "Has the product shipped without this before?" → If yes, it's Should Have
- Reframe: Won't Have means "not in this time box," not "never"
- Stakeholder test: if one person insists but others disagree, it's Should Have at best

### Example

| Item | Category | Rationale |
|------|----------|-----------|
| User login and authentication | Must Have | Product is unusable without accounts |
| Password reset flow | Must Have | Blocks user recovery; support cost is unacceptable without it |
| Social login (Google, GitHub) | Should Have | Reduces friction significantly but email/password works |
| Custom avatar upload | Could Have | Nice touch for personalization; no impact on core value |
| Admin analytics dashboard | Won't Have | Valuable but not needed for user-facing launch; Q3 candidate |

---

## Value vs Effort Matrix

**Origin:** Common PM practice. Best for visual strategic discussion and high-level bet sizing.

### Axes

| Axis | Definition | How to Estimate |
|------|-----------|----------------|
| **Value** (Y-axis) | User/business value delivered if shipped | Encompasses user satisfaction, revenue impact, risk reduction, strategic importance. Score 1-10 or bin as Low/High. |
| **Effort** (X-axis) | Total resources required to ship | Encompasses engineering, design, PM, QA, and post-launch support. Score 1-10 or bin as Low/High. |

### Quadrants

| Quadrant | Value | Effort | Action |
|----------|-------|--------|--------|
| **Quick Wins** (top-left) | High | Low | Do first — high ROI, fast feedback |
| **Big Bets** (top-right) | High | High | Plan carefully; prototype or validate before committing |
| **Fill-Ins** (bottom-left) | Low | Low | Do if capacity exists; never block Quick Wins for these |
| **Money Pits** (bottom-right) | Low | High | Avoid — highest opportunity cost |

### Handling Center Clustering

Items inevitably cluster near the middle. This reveals undifferentiated estimates, not genuine similarity. Responses:

1. **Force rank within clusters** — items in the same zone must be ordered relative to each other.
2. **Decompose vague estimates** — "Medium effort" usually means "we haven't broken this down." Spend 10 minutes decomposing and the item usually moves decisively.
3. **Run multiple matrices** — plot the same backlog on different axes (Value vs Risk, Value vs Confidence). Items that land in Quick Wins across all views are unambiguous priorities.

### Example

```
       High Value
           │
  Quick    │    Big
  Wins     │    Bets
           │
───────────┼───────────
           │
  Fill-    │    Money
  Ins      │    Pits
           │
       Low Value

     Low Effort → High Effort
```

| Item | Value | Effort | Quadrant |
|------|-------|--------|----------|
| Fix broken search pagination | High | Low | Quick Win |
| Rebuild notification system | High | High | Big Bet |
| Update footer links | Low | Low | Fill-In |
| Custom reporting engine | Low | High | Money Pit |

---

## WSJF (Weighted Shortest Job First)

**Origin:** Don Reinertsen's *Principles of Product Development Flow*. Operationalized in SAFe. Best for sequencing work in SAFe organizations or teams that think in terms of Cost of Delay.

### Core Principle

> "If you only quantify one thing, quantify the Cost of Delay." — Don Reinertsen

WSJF sequences work to maximize economic throughput: items with high cost-of-delay and short duration get done first.

### Formula

```
WSJF = Cost of Delay / Job Size

Cost of Delay = User-Business Value + Time Criticality + Risk Reduction / Opportunity Enablement
```

### Dimensions

All dimensions use a **relative Fibonacci-like scale: 1, 2, 3, 5, 8, 13, 20.** Scores are relative to each other within this backlog, not absolute.

| Dimension | Question | Scoring Guidance |
|-----------|----------|-----------------|
| **User-Business Value** | What is the relative value to users and the business? | Revenue-generating and customer-facing features score high. Internal tooling scores lower unless it unblocks external value. |
| **Time Criticality** | How does value decay if delayed? | Hard deadlines (regulatory, seasonal, competitive parity) score high. "Nice to have before next quarter" scores low. Legal deadline = 13-20. No deadline = 1-2. |
| **Risk Reduction / Opportunity Enablement** | Does this reduce risk or enable future opportunities? | Technical debt causing outages, legal exposure, or platform work that unlocks a product line. Captures indirect value. |
| **Job Size** | How long will this take relative to other items? | Estimated by the team building it, not stakeholders. Smaller = higher WSJF (which is the point). |

### Workshop Process

1. List all items in a table.
2. Pick a **reference item** for each Cost of Delay component — score it 3 (medium). All other items scored relative to it.
3. Score User-Business Value first, then Time Criticality, then RR/OE — all relative.
4. Score Job Size separately (the building team, not stakeholders).
5. Sum CoD = UBV + TC + RR/OE, then divide by Job Size.
6. Sort descending. Top items are sequenced first.

### Example

| Item | UBV | TC | RR/OE | CoD | Job Size | WSJF |
|------|-----|----|-------|-----|----------|------|
| GDPR audit trail | 3 | 13 | 8 | 24 | 3 | 8.0 |
| Search autocomplete | 8 | 2 | 1 | 11 | 5 | 2.2 |
| Platform API for partners | 5 | 3 | 13 | 21 | 13 | 1.6 |

GDPR audit trail wins despite lower business value because of extreme time criticality (regulatory deadline) and risk reduction.
