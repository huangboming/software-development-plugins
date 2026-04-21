# Cagan Canon and Writing Guide

The knowledge spine for the `define-vision` skill. Read this before drafting any vision document and again during review.

## Contents

1. [What a product vision is](#1-what-a-product-vision-is)
2. [The 10 principles](#2-the-10-principles-validation-criteria-not-sections)
3. [Distinctions from adjacent artifacts](#3-distinctions-from-adjacent-artifacts)
4. [Timeframe, format, ownership](#4-timeframe-format-ownership)
5. [The default 6-section scaffold](#5-the-default-6-section-scaffold)
6. [Section-by-section writing guide](#6-section-by-section-writing-guide)
7. [Quality checklist (8 failure modes)](#7-quality-checklist-8-failure-modes)

---

## 1. What a product vision is

A product vision describes **the future you are trying to create** — specifically, how that future improves the lives of your customers. It is a persuasive, emotional artifact whose purpose is to inspire teams to want to help make it real. It is not a spec, not a roadmap, and not a set of features.

Core framing, attributed to Marty Cagan (*Inspired*, 2nd ed.; *Transformed*):

- "The product vision describes the future we are trying to create — typically 2 to 5 years out" (10 years for hardware).
- "Vision is not about the product. It is about the problem you are solving and the world you are creating."
- "Its primary purpose is to communicate this vision and inspire the teams to want to help make this vision a reality."

Cagan explicitly rejects the idea that a product vision is a written spec. The written vision document is one acceptable format among several (visiontype prototype, vision video, storyboard), and it must remain a persuasive artifact — narrative prose, not a bulleted feature list.

## 2. The 10 principles (validation criteria, not sections)

Cagan offers 10 principles that a product vision must satisfy (*Inspired*, 2nd ed., Chapter 25). These are quality criteria to validate the draft against, not a document structure to copy.

1. **Start with why** — articulate purpose first; everything follows from that.
2. **Fall in love with the problem, not the solution.**
3. **Don't be afraid to think big.**
4. **Don't be afraid to disrupt yourself** — if you don't, someone else will.
5. **The vision must inspire.**
6. **Embrace relevant and meaningful trends.**
7. **Skate to where the puck is heading**, not where it was.
8. **Stubborn on vision, flexible on details.**
9. **Any vision is a leap of faith** — "if you could truly validate a vision, then your vision probably isn't ambitious enough."
10. **Evangelize continuously and relentlessly** — there is no such thing as over-communicating the vision.

Use these as the first pass of the quality checklist during review.

## 3. Distinctions from adjacent artifacts

A common failure is confusing vision with something else. Hold these distinctions explicitly.

### Vision vs. Mission

| Mission | Product Vision |
|---|---|
| Organizational purpose — why we exist now | Future state we are creating |
| Enduring slogan about purpose | Concrete picture of future customer experience |
| Short (one sentence) | Narrative (hundreds to a few thousand words) |

Cagan has stated that "most people, when they show their product vision, are really showing their mission statement — confusing a slogan about purpose with a product vision" (attributed; SVPG blog). Guard against this aggressively in Section 4 of the scaffold (What This Is Not).

### Vision vs. Strategy

| Product Vision | Product Strategy |
|---|---|
| Where are we going? | How do we get there? |
| 2–10 years | Quarterly |
| Changes rarely (every ~5 years) | A living thing, revisited quarterly |
| Inspiring narrative | Specific set of problems / beachheads |

"The difference between vision and strategy is analogous to the difference between good leadership and good management. Leadership inspires and sets the direction; management helps us get there." (Cagan, *Inspired* 2nd ed.)

Strategy work is **out of scope** for `define-vision`. If the user describes quarterly bets or beachheads, redirect them — this belongs in a future `write-strategy` skill.

### Vision vs. Product Principles

Principles are a **companion document**, not the vision itself. Cagan often packages them together ("the product vision and principles") but they are logically distinct:

- **Vision** = where we're going and why it matters to customers
- **Principles** = standing rules for resolving trade-offs along the way

In the default scaffold, principles appear as Section 6, clearly labeled as a separate concern. See `principles-guide.md` for how to write them.

### Vision vs. North Star Metric

Cagan does not treat "North Star Metric" as a primary construct — that framing belongs to Amplitude / Sean Ellis / growth PM tradition. Cagan uses "north star" *metaphorically* to describe what the vision provides ("a north star that brings all teams toward the same destination"). NSM is a strategy/measurement tool, not equivalent to vision.

Do not include a North Star Metric section in `vision.md`. If the user asks, explain the distinction and suggest they track NSM separately in their strategy or OKR docs.

### Vision vs. OKRs

OKRs are team objectives — the output of strategy applied to individual teams. They sit three levels below vision:

```
Product Vision
  → Product Strategy (beachheads / focus)
    → Team Objectives (OKRs)
      → Product Discovery (solutions)
```

OKRs are out of scope. Do not generate them as part of `define-vision`.

### Vision vs. Roadmap

A roadmap is a delivery plan. Vision is an aspirational future state. "The product vision is not in any sense a spec" (Cagan, attributed). Listing features, dates, or milestones in `vision.md` is **failure mode FM-3** and must be rejected during review.

## 4. Timeframe, format, ownership

**Timeframe:**
- Software products: 2–5 years
- Hardware / device-centric: 5–10 years
- Revision cadence: approximately every 5 years (not quarterly — that's strategy)

Ask the user which product type applies; default to software (2–5 years) if unclear.

**Format:**
- Narrative prose, not bulleted feature lists
- Persuasive and emotional — written to inspire, not to document
- Length: 800–2,500 words is typical. Slack's memo is ~3,000 words; treat that as the outer bound, not a target.
- Section 6 (Product Principles) is the only structurally distinct section — it uses a ranked list format.

**Ownership:**
- Product vision is a **leadership artifact** — owned by the Chief Product Officer, VP Product, or founder. Not owned by individual product teams.
- If the user is writing a vision "for my team" or "for my feature area," stop and explain the distinction. Suggest they either (a) write a team-scoped OKR doc instead, or (b) escalate vision-writing to product leadership.

## 5. The default 6-section scaffold

Cagan prescribes no fixed document template — this scaffold is synthesized from his 10 principles plus real-world calibration examples (Slack's "We Don't Sell Saddles Here" memo, Linear's README, Amazon Working Backwards press-release format). **Do not describe this scaffold as "Cagan's structure."** Describe it as "a practical scaffold informed by Cagan's principles."

| # | Section | Length | Purpose |
|---|---|---|---|
| 1 | The Future We're Creating | 200–600 words, narrative | The picture of where we're going, from the customer's perspective |
| 2 | Who We're Building For | 100–300 words, narrative | 1–3 persona sketches showing what changes in *their* life |
| 3 | The Insight | 100–300 words, prose | The non-obvious belief this vision rests on |
| 4 | What This Is Not | 50–200 words, prose or list | Anti-vision: what we explicitly reject becoming |
| 5 | Timeframe & Review | 1–3 sentences | 2–5 or 5–10 years; next review date |
| 6 | Product Principles | 5–8 ranked principles | Standing trade-off rules (see `principles-guide.md`) |

Plus a one-line **distribution note** at the top or bottom of the document: "This vision is referenced in every PRD kickoff and reviewed annually in Q1" (or similar). This is the FM-5 countermeasure — acknowledging that a vision nobody reads is a vision that failed.

Plus standard front matter: `Last updated: <date>`, `Next review: <date + 2 years>`, `Owner: <product leader name or TBD>`, `Status: Draft | Approved`.

**When to deviate from this scaffold:** if the user prefers Slack-style (6-act narrative), Linear-style (3-act manifesto), or Amazon Working Backwards (PR + FAQ), read `alternative-scaffolds.md` and use the selected structure instead. Sections 5 and 6 still apply regardless of scaffold choice.

## 6. Section-by-section writing guide

### Section 1: The Future We're Creating

**Purpose:** Paint a concrete picture of the customer's future — their day, their workflow, what is different, what they stopped having to do. Customer-outcome framing, not feature framing.

**Weak → Strong example:**

| Weak | Strong |
|---|---|
| "Our product will be the leading collaboration platform for engineering teams, with AI-powered features, seamless integrations, and best-in-class performance." | "In 2029, a new engineer joins a team on Monday morning. By lunchtime, she has opened a pull request, read three design docs relevant to her task, and asked two questions of the codebase in plain English — all without interrupting a single teammate. The artifacts she needs find her; the people she would have interrupted keep their focus." |

The strong version names a specific customer (new engineer), a specific moment (Monday morning, lunchtime), specific outcomes (opened PR, found docs, asked questions without interrupting), and leaves the *product* entirely offstage. The weak version lists company aspirations and could be said about any competitor in the space.

**Tactics:**
- Start with a customer, not a company
- Pick a specific moment in time (a day, a week, a project milestone)
- Describe what changed by omission — what they *stopped* doing
- Avoid the words "we," "our," "platform," "leading," "best-in-class"

### Section 2: Who We're Building For

**Purpose:** Identify 1–3 distinct customer types, each as a short narrative sketch. Focus on what changes in *their* life when the vision is realized.

**Weak → Strong example:**

| Weak | Strong |
|---|---|
| "Target users: software engineers, designers, product managers." | "We're building for engineers in their second and third year at fast-growing companies — the ones drowning in context they didn't help create, spending half their week piecing together why decisions were made and who owns what. By 2029, this engineer closes her laptop at 6pm because the work she did that day was work only she could do." |

The strong version is opinionated about *which* engineer (second/third year, fast-growing company), names the specific pain (drowning in context, piecing together decisions), and ends with a concrete outcome (closes laptop at 6pm because work was uniquely hers).

**Tactics:**
- Pull from `.product/discover/research/*.md` if it exists — use personas, JTBD, and pain points as raw material
- Limit to 1–3 personas; more dilutes focus
- Use specific role titles, not generic labels ("second-year backend engineer at a Series B," not "developer")
- End each sketch with a concrete before/after moment

### Section 3: The Insight

**Purpose:** Name the non-obvious belief this vision rests on. What do we believe about the world that most of the market does not? This is the "leap of faith" Cagan describes in Principle 9 — if a skeptic could validate the insight today with a survey, the vision is too safe.

**Weak → Strong example:**

| Weak | Strong |
|---|---|
| "Users want AI-powered tools that save them time." | "We believe engineers' biggest bottleneck isn't writing code — it's reconstructing context. Most tools treat context as documentation; we treat it as the primary artifact. Everything else (code, PRs, decisions) is metadata attached to context, not the other way around. If we're right, the productivity ceiling for engineering teams is 10x higher than the industry assumes." |

The strong version makes a specific claim (context, not code, is the bottleneck), an inversion (context is primary, code is metadata), and a falsifiable consequence (10x productivity ceiling). A skeptic could disagree with any of these — that's what makes it a real insight.

**Tactics:**
- One sentence: "We believe X, while most of the industry believes Y."
- Make it falsifiable — what would prove us wrong?
- Ground it in a specific observation (why do we believe this? what did we see?)
- If the insight is obvious, it's not an insight. Rework it until it would upset a competitor to read.

### Section 4: What This Is Not

**Purpose:** Product-level non-goals. What we explicitly reject becoming. This is the FM-1 (mission confusion) and FM-2 (aspirational vagueness) countermeasure — if you can't name what you're *not*, your vision is probably a platitude.

**Weak → Strong example:**

| Weak | Strong |
|---|---|
| "We are not trying to be everything to everyone." | "We are not building a general-purpose project management tool. We do not serve teams of 500+. We will not ship a mobile-first experience in this horizon. We reject the 'no-code' framing — our users *are* engineers and want tools that respect that. If you're a PM looking for a Jira replacement, we are not for you." |

The strong version names specific rejected markets (general PM, 500+ teams, mobile-first), specific rejected positioning (no-code), and specific rejected personas (PMs looking for Jira replacement). A reader can immediately tell whether the product is for them.

**Tactics:**
- Name at least 3 specific rejections
- Include at least one counterintuitive rejection (something a reasonable person would assume is in scope)
- Include one rejected *framing* (not just a rejected feature) — the language/positioning we refuse to adopt
- Each rejection should create visible opportunity cost — "we're saying no to X because saying yes would compromise Y"

### Section 5: Timeframe & Review

One sentence for timeframe, one for review cadence, one for ownership.

> **Timeframe:** 3 years (2026–2029).
> **Next review:** 2028-04-08.
> **Owner:** [Name], Head of Product.

### Section 6: Product Principles

See `principles-guide.md` for full treatment. Structural summary:

- 5–8 principles, ranked
- Each principle = one sentence of position + one sentence of rationale
- Each must resolve a non-obvious trade-off (the conflict-resolution test)
- Rank order is load-bearing — it tells teams which principle wins when two conflict

## 7. Quality checklist (8 failure modes)

Review every draft against every item before presenting to the user. If any item fails, revise and re-check. Do not present a draft that fails the checklist.

### Vision failure modes

- [ ] **FM-1: Not a mission statement.** The document answers "where are we going" (future), not "why we exist" (present purpose). A reader cannot collapse it to a one-sentence slogan.
- [ ] **FM-2: Not aspirational vagueness.** A reader from a rival company would specifically disagree with at least one claim in the document. The vision could not be copy-pasted to a competitor.
- [ ] **FM-3: No roadmap in disguise.** Zero features, zero dates, zero milestones, zero revenue targets. If the document lists capabilities, rewrite them as customer outcomes.
- [ ] **FM-4: Customer-outcome framing.** Zero mentions of "market leader," "market share," "the leading X," or company-position claims. Every claim describes what changes in the customer's life.
- [ ] **FM-5: Distribution acknowledged.** The document has a one-line distribution note stating how it will be evangelized. "Poster on the wall" is an explicit failure mode — acknowledge it.
- [ ] **FM-6: Product-level, not team-level.** Front matter explicitly states ownership at the product-leadership level. The document covers the full product, not a single feature area.
- [ ] **FM-7: Ambitious enough to require a leap of faith.** If a skeptic could validate the insight today with a survey or existing data, rework it. "Stubborn on vision" implies the vision is worth being stubborn about.
- [ ] **FM-8: Not a strategy in disguise.** No quarterly bets, no beachheads, no sequencing of initiatives. Strategy is downstream and belongs in a future `write-strategy` skill.

### Principle failure modes

See `principles-guide.md` for the full principle checklist. Core items:

- [ ] Each principle resolves a real conflict between competing values (conflict-resolution test)
- [ ] Principles are ranked, not unordered
- [ ] Each principle is one sentence of position + one sentence of rationale
- [ ] Principle count is 5–8

### Structural checks

- [ ] Front matter includes `Last updated`, `Next review`, `Owner`, `Status`
- [ ] Distribution note is present
- [ ] Narrative sections are prose, not bullet lists
- [ ] Document length is between 800 and 2,500 words (excluding front matter)

If every item passes, present the draft and ask for feedback.
