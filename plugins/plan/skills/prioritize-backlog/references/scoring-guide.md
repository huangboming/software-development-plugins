# Scoring Guide

Best practices for scoring, bias countermeasures, and quality checks for prioritization.

## Scoring Best Practices

### Anchor Before Scoring

Before scoring any item, establish calibration:

1. Pick one item that everyone agrees is "medium" across dimensions. Score it together. This is the **reference item**.
2. Walk through what each score level means concretely for *this* backlog. "Impact = High" means different things for a B2B SaaS tool vs. a consumer mobile app.
3. Score all subsequent items relative to the reference — not in absolute terms.

### Score Honestly, Not Optimistically

| Dimension | Common Inflation | Corrective |
|-----------|-----------------|------------|
| Impact | Everything scored "High" or "Massive" | Enforce distribution: at most 20% of items at the highest level |
| Confidence | Default to 80% for everything | Default to 50% when uncertain. 80%+ requires data, not intuition |
| Reach | Aspirational "all users" | Use actual analytics. If no data, drop Confidence to reflect it |
| Effort | Best-case "just coding time" | Include all roles: design, PM, QA, documentation, coordination overhead |
| Ease (ICE) | Overestimate simplicity | Ask the engineer building it, not the PM requesting it |

### Write Rationale, Not Just Numbers

Every score needs a one-sentence rationale. Numbers without reasoning cannot be challenged constructively.

| Weak | Strong |
|------|--------|
| Reach = 5,000 | Reach = ~5,000/quarter — based on current notification click-through rate from product analytics |
| Impact = High | Impact = High (2) — reduces a 4-step manual process to 1 click for the core daily workflow |
| Confidence = 80% | Confidence = 50% — estimate based on 3 customer interviews, no quantitative validation yet |

## Cognitive Bias Countermeasures

| Bias | What Happens | Countermeasure |
|------|-------------|----------------|
| **HiPPO** | Senior stakeholder's preference anchors everyone | Score independently before discussing. Reveal after all scores are in. |
| **Anchoring** | First score stated becomes the reference for others | Everyone writes scores privately first. No "starter scores." |
| **Recency bias** | Items discussed recently feel more important | Randomize item order. Score all items before any discussion. |
| **Effort underestimation** | Optimism about speed | Require bottom-up estimates from the building team. Apply a 1.5x buffer when history shows optimism. |
| **Impact inflation** | Every feature scored as transformative | Enforce a distribution cap: only X% at the top level. |
| **Scope creep as prioritization** | Adding items to inflate a category's importance | Enforce timeboxed scope. Won't Have must be populated before Must Have. |
| **Confirmation bias** | Scores justify a pre-decided outcome | Score before discussing solutions. Separate "what problem" from "what solution." |

## Handling Scoring Disagreements

When two scorers diverge by more than one level on the same dimension:

1. Do not average — averages hide information. Discuss first.
2. Ask the high-scorer: "What information makes you confident in this score?"
3. Ask the low-scorer: "What makes you skeptical?"
4. If disagreement is about a **factual unknown** (e.g., "how many users hit this?"), flag it as a research question. Score at low Confidence until answered.
5. If disagreement persists after discussion, **the lower score wins** — asymmetric conservatism reduces overconfidence.

## When to Re-Prioritize vs Hold

**Re-prioritize when:**
- New user research changes importance or satisfaction signals materially
- A competitive move makes a previously low-priority item urgent
- Technical constraints discovered during development change the Effort score significantly
- Business objectives shift (new OKR cycle, strategic pivot)
- More than 6 weeks have passed since last prioritization

**Hold current priorities when:**
- A new stakeholder request arrives without new data (this is recency bias)
- An item becomes "urgent" due to internal pressure without customer evidence
- Prioritization was done less than 4 weeks ago and no new signal has arrived

## Documenting Excluded Items

Every prioritization excludes items. Document them — undocumented exclusions get relitigated.

For each excluded item, record:
- **What** — the item name
- **Why excluded** — one sentence (e.g., "Low Reach — affects <100 users/quarter", "Infeasible — requires platform migration first")
- **Revisit trigger** — what would change this (e.g., "Revisit if requests exceed 50/month", "Reconsider after migration in Q3")

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| **Score-and-forget** | Prioritization done once, never revisited as context changes | Schedule re-prioritization on a cadence (e.g., quarterly). |
| **Framework theater** | Going through scoring motions but overriding with gut feel | If the framework's answer is always wrong, the scores are wrong — fix the scores, not the ranking. |
| **Effort amnesia** | Consistently underestimating effort, making high-effort items look attractive | Track actual vs. estimated effort. Apply a correction factor. |
| **Confidence ceiling** | Every item scored at 80%+ Confidence regardless of evidence | Default to 50%. Require specific data to score above 80%. |
| **Missing Won't Have** | No items explicitly excluded — everything is "planned eventually" | Populate Won't Have / Excluded first. Cannot-do discipline enables can-do focus. |
| **Mixing levels** | Epics scored alongside stories; scores become incomparable | Normalize granularity before scoring. One level per session. |

## Quality Checklist

- [ ] Every item has a composite score *and* a per-dimension rationale
- [ ] Scores are calibrated against a reference item — no dimension is uniformly the same across all items
- [ ] Assumptions are stated explicitly, not hidden inside scores
- [ ] Excluded items are documented with rationale and revisit trigger
- [ ] The ranking passes the gut check — if #1 feels wrong, revisit scoring
- [ ] Framework selection is documented with reasoning
- [ ] Time window, target outcome, and capacity constraint are stated
- [ ] The cut line is clear — committed vs. stretch vs. next cycle
- [ ] Participants and date are recorded
- [ ] No item scored without sufficient context — vague items flagged, not scored optimistically
