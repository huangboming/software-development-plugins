# Card Sort Prep

Produces a prep document for a card sort study — a method for understanding how users categorize and label information. Used for information architecture, navigation design, and feature organization decisions.

## Prep Document Template

```markdown
# Card Sort Prep: [Domain / Feature Area]

**Date:** [today]
**Method:** Card sort ([open | closed | hybrid])
**Estimated participants:** [15–30 for statistical patterns]
**Format:** [remote tool (Optimal Workshop, Maze, etc.) | in-person with physical cards]

## Research Goals

1. [What IA or categorization questions we need to answer]
2. [...]

**Grounding signals:** [List any signals from .product/discover/signals/ that motivated this study]

## Sort Type Rationale

**Open sort:** Participants create their own groups and labels. Use when exploring how users naturally think about the domain — no existing IA to validate.

**Closed sort:** Participants sort cards into predefined categories. Use when testing whether a proposed IA structure makes sense to users.

**Hybrid sort:** Predefined categories, but participants can create new ones. Use when you have a starting structure but want to discover gaps.

**Chosen type:** [open | closed | hybrid] — because [rationale].

[If closed or hybrid, list the predefined categories:]
### Predefined Categories
1. [Category name] — [brief description if the label might be ambiguous]
2. [...]

## Card List

[30–60 cards. Each card represents one item users need to find or interact with.]

| # | Card Label | Notes |
|---|---|---|
| 1 | [Short, clear label — use the user's language, not internal jargon] | [Optional: why this card is included, edge case it tests] |
| 2 | [...] | |
| ... | | |

## Pre-Sort Questions

[2–3 questions to understand the participant's context before sorting]
- "How familiar are you with [domain]?"
- "When you need to [relevant task], where do you typically look first?"

## Post-Sort Questions

[Ask after sorting is complete]
- "Were any cards difficult to place? Which ones and why?"
- "Were there any groups where you weren't sure what to call them?" (open sort)
- "Did any of the categories feel wrong or confusing?" (closed sort)
- "Is there anything missing — something you'd expect to find that wasn't a card?"

## Analysis Plan

**For open sorts:**
- Similarity matrix — which cards are grouped together most often
- Dendrogram — hierarchical clustering to reveal natural groupings
- Category labels — what names participants give to groups (and how they vary)

**For closed sorts:**
- Completion rate per category — what % of participants placed each card correctly
- Misplacement patterns — where do cards consistently end up in the wrong category?

**Success criteria:**
- Cards placed in the "expected" category by ≥70% of participants → strong agreement
- Cards below 50% agreement → label or category needs rethinking
```

## Gotchas

- **Keep cards at consistent granularity.** Mixing "Account Settings" with "Change Password" creates a parent-child relationship that distorts grouping. All cards should be at roughly the same level of specificity.
- **30–60 cards maximum.** Fewer than 20 doesn't produce meaningful patterns. More than 60 causes fatigue and noisy data. If the domain has more items, split into separate sorts by area.
- **Use the user's language on cards, not internal product terminology.** "SSO Configuration" means nothing to a user who thinks in terms of "Sign in with Google." If you're unsure of the user's vocabulary, run 3–5 exploratory interviews first.
- **Cards that everyone agrees on are wasted cards.** If you already know where "My Profile" goes, don't include it. Focus cards on items where the team has genuine uncertainty about placement.
- **Open sort category labels are data — don't ignore them.** The groups participants create matter, but the names they give those groups are equally valuable. Those labels are candidates for your actual navigation labels.
- **Randomize card order per participant.** Presentation order biases grouping — participants sort early cards more carefully. Most remote tools handle this automatically; verify the setting.
