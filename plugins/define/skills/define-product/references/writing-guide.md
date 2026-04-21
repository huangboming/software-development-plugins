# Product Definition Writing Guide

Section-by-section guidance for drafting `.product/define/product.md`. Read during drafting and during review.

## Working Backwards: Start with the Customer

`product.md` defines a product that exists (or is about to exist) for a real user. Before writing, answer:

1. **Who** uses this product today (or will, at launch)?
2. **What** did their workflow look like before the product existed?
3. **What** do they do now with the product that they couldn't do before?

Every section flows from those three answers. If any section drifts into solution-first framing ("we have a dashboard that..."), rewrite it in customer terms.

## Purpose

### Weak vs. strong

| Weak | Strong |
|---|---|
| "A collaborative platform for modern teams." | "For 2–10 person product teams, a single place to go from user research signals to shippable feature specs — replacing the handoff chain of Notion pages, Loom videos, and ad-hoc Slack threads." |

**Why the strong version works:** names the segment (2–10 person product teams), states the user workflow being collapsed (research → spec), and calls out what it replaces (Notion + Loom + Slack chain). The weak version could describe hundreds of products.

### The competitor-substitution test

Write a one-sentence Purpose. Now try to paste the same sentence into a competitor's homepage. If it fits, the Purpose is too generic — sharpen until only this product could claim it.

## Target Users

Keep segments to **2–4**. More than that usually means one of:
- The product is too broad — trim scope, or accept this in product.md and note it as a positioning risk.
- Segments are sliced too finely — merge by primary pain.

### Persona fields

| Field | Include | Skip |
|---|---|---|
| Role / context | Job title, team size, when/where they encounter the problem | Demographics, career history, personal interests |
| Key characteristics | What distinguishes this segment — sophistication, tooling, scale, buying authority | Generic traits that could apply to anyone |
| Primary pain today | The specific friction this product removes | Aspirational "needs" like "wants to move faster" |
| What using the product means | The concrete hook or habit — "they log in Monday morning to see weekend signals" | Feature list, vision-y framing |

### Weak vs. strong — segment characteristics

| Weak | Strong |
|---|---|
| "Modern software teams that value quality." | "Product teams at Series A–B SaaS companies, 3–8 PMs, already running weekly user research, comfortable with markdown-based tooling, Linear or Jira users." |

## Value Proposition & Positioning

The value proposition answers: **why does this user pick this product over what they're doing today?** The comparison is the whole point — state it explicitly.

### Weak vs. strong

| Weak | Strong |
|---|---|
| "Saves time and improves collaboration." | "Instead of a 3-tool chain (Notion for PRDs, Loom for walkthroughs, Slack for debate), one tool that ties research signals directly to shippable specs — typically cutting PRD cycle time from 2 weeks to 3 days." |

**Why the strong version works:** names the alternative (3-tool chain), names the specific alternatives (Notion, Loom, Slack), quantifies the delta (2 weeks → 3 days).

### Positioning statement (optional)

The "For <segment> who <need>, <product> is a <category> that <benefit>, unlike <alternative>, which <shortcoming>" template is a useful forcing function even if it doesn't ship in the final document. If the blanks are hard to fill, the product doesn't have a sharp identity yet — surface that as an Open Question rather than papering over it.

## Scope & Non-Goals

### What product-level non-goals look like

Product-level non-goals shape the product's identity. Feature-level cuts ("no dark mode in v1") belong in feature PRDs, not here.

| Weak (feature-level, wrong altitude) | Strong (product-level) |
|---|---|
| "Not building mobile app in v1." | "**Team-wide analytics and reporting** — this is a tool for the PM doing the work, not an executive dashboard. Teams needing rollups integrate with existing BI." |
| "No dark mode yet." | "**Offline-first operation** — we expect always-on connectivity; users without reliable internet are not a target segment." |

### The "reasonable assumption" test

A good non-goal is something a stakeholder could reasonably assume is in scope but isn't. If no one would assume it, it's not worth listing.

## Product Stage

One line is enough. The value is in making the stage-specific pressures explicit so feature decisions reflect them.

| Stage | Typical pressure |
|---|---|
| Pre-launch | Optimize for shipping something — learning beats polish. |
| MVP | Optimize for learning — measurement and iteration speed matter more than completeness. |
| Scaling | Guardrails, reliability, and onboarding take priority over new surface area. |
| Mature | New surface area requires strategic justification; default is refinement. |
| Sunsetting | No new investment; focus shifts to migration and wind-down. |

## Boundary with `define-vision`

`vision.md` and `product.md` partition the "what are we?" question by **time** and **certainty**:

| | `vision.md` | `product.md` |
|---|---|---|
| Tense | Future (3–10yr) | Present |
| Audience | Leadership, hiring, long-horizon decisions | Anyone joining or buying today |
| Level of certainty | Aspirational, leap of faith | Grounded, what we can defend today |
| Users | Directional archetype | Concrete segments with characteristics |
| "Not" section | Rejection (philosophical — "we don't believe in X") | Scope boundaries (pragmatic — "we don't serve X") |
| Features | None | None |

If a draft sentence is making a 3+ year claim or taking an ambitious position the product doesn't yet earn, move it to `vision.md`. If a draft sentence in `vision.md` is just describing today, move it here.

## Quality Checklist

Before presenting:

- [ ] Purpose passes the competitor-substitution test — this sentence couldn't describe a different product.
- [ ] Purpose is present tense and concrete, not aspirational 3+yr framing.
- [ ] 2–4 target segments, each with role/context, distinguishing characteristics, primary pain, and what using the product means for them.
- [ ] Value proposition names a specific alternative (status quo, competitor, spreadsheet, DIY script) — not "saves time" or "improves collaboration".
- [ ] Non-goals are product-level (identity-shaping), not feature-level (version cuts).
- [ ] Non-goals would genuinely surprise a stakeholder who hadn't read the document.
- [ ] Product stage is named, with a one-line note on what pressure that stage puts on decisions.
- [ ] No feature list. No success metrics. No implementation details.
- [ ] No content that belongs in `vision.md` — no aspirational future, no philosophical rejection, no principles.
- [ ] Open Questions capture genuine unknowns about the product's definition, not rhetorical questions.
