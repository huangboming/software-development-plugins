# Alternative Scaffolds

Load this file only when the user wants to deviate from the default 6-section scaffold in `cagan-canon-and-writing.md`. Each scaffold below is grounded in a real high-quality vision artifact — not invented.

## Contents

1. [How to choose a scaffold](#1-how-to-choose-a-scaffold)
2. [Slack 6-section (persuasive memo)](#2-slack-6-section-persuasive-memo)
3. [Linear 3-act manifesto](#3-linear-3-act-manifesto)
4. [Amazon Working Backwards (PR + FAQ)](#4-amazon-working-backwards-pr--faq)
5. [What applies regardless of scaffold](#5-what-applies-regardless-of-scaffold)

---

## 1. How to choose a scaffold

Ask the user one question: **"What shape do you want the vision to take?"** Offer the four options below.

| Scaffold | Best when | Worst when |
|---|---|---|
| **Default 6-section** | First-time vision; user wants structure without strong stylistic preferences | User wants a narrative memo feel, not a template |
| **Slack memo** | User is writing for an internal team and wants a persuasive narrative; product is pre-launch or repositioning | User wants a short, tight document |
| **Linear manifesto** | User wants a public-facing vision that doubles as a recruitment tool; product has a clear "enemy" or status quo to reject | Product is internal-only or lacks a clear antagonist |
| **Amazon PR + FAQ** | User wants the shortest possible artifact; discipline-forcing format is attractive | Vision needs emotional/narrative depth; product is open-ended |

If the user has no preference, keep the default. Do not push them into an alternative scaffold.

## 2. Slack 6-section (persuasive memo)

**Source:** Stewart Butterfield, "We Don't Sell Saddles Here," internal memo to Tiny Speck, 31 July 2013. Public on Medium.

**Shape:** ~3,000 words, narrative prose, six labeled sections. Written as an internal persuasion document, not a public announcement.

**Section structure:**

1. **Build Something People Want** — The gap between what the product can do and whether the market understands they need it. Acknowledge the fundamental marketing challenge.
2. **Marketing from Both Ends** — How the product and its positioning must be refined in parallel. Neither comes first.
3. **Sell the Innovation, Not the Product** — What we're really selling is not the software — it's a new way of working, a category change, an organizational transformation.
4. **Who Do We Want Our Customers to Become?** — The behavioral outcome for the user. Not a feature list; a transformation.
5. **How Do We Do It?** — The execution philosophy. Relentless polish, obsessive craft, refusal to ship anything half-finished.
6. **Why?** — Scope, excellence, holistic purpose. Why this work is worth doing at all.

**When to pick this:**
- The product is pre-launch or in a major repositioning
- The team needs alignment on what category the product is in, not just what it does
- The author is comfortable writing a ~3,000-word persuasive essay
- There is an "innovation to sell" — a specific new behavior or category the product enables

**Mini-template:**

```markdown
# [Product Name]: The Vision

**Author:** [Name] | **Date:** [date] | **Status:** [Draft / Approved]
**Distribution:** [where this will be shared and referenced]

## 1. Build Something [Customer] Wants

[What can the product already do that the market hasn't recognized yet?
What is the gap between product capability and customer understanding?
Why does this gap exist?]

## 2. Marketing from Both Ends

[How does the product and its positioning refine each other?
What does the product need to become to match the positioning?
What does the positioning need to become to match the product?]

## 3. Sell the [Transformation], Not the Product

[What is the real thing we're selling? (Not software. Not features. A new way of working, a category shift, a behavioral transformation.)
Why is this the right frame?]

## 4. Who Do We Want Our Customers to Become?

[Describe the future customer — not their demographics, but their behavior.
What do they do differently because our product exists?
What stops being a problem for them?]

## 5. How Do We Do It?

[The execution philosophy. What do we refuse to compromise on?
What does "done" mean for us, and why is that bar where it is?]

## 6. Why?

[Why is this work worth doing at all?
What happens if we succeed? What's lost if we don't?]

## Timeframe & Review

[2-5 years / 5-10 years. Next review date. Owner.]

## Product Principles

[5-8 ranked principles — see principles-guide.md]
```

**Note:** The Slack memo does not have a dedicated "principles" section — but when using this scaffold for a product vision artifact, append Section 6 (Principles) from the default scaffold. Cagan's principles are a standard feature of a vision document regardless of the narrative shape above them.

## 3. Linear 3-act manifesto

**Source:** Linear README, currently public at linear.app/readme. ~2,500–3,000 words. Public-facing company manifesto.

**Shape:** Three-act narrative borrowing storytelling conventions (past, present, future). Literary tone. Uses specific antagonists ("dark forces") to sharpen the vision.

**Section structure:**

1. **The Past** — The history of what made the domain magical once. Set up the nostalgic / aspirational frame. ("Software was once full of wonder. Computing promised...")
2. **The Present** — What went wrong. Name the antagonists explicitly — the specific things in the current state of the world that the product rejects. (Linear names three "dark forces": noise/distraction, uniform sameness, the cargo-culted past.)
3. **The Future** — What we're building to restore or create. The specific promise, not as a feature list but as a counter to the antagonists in Act 2.

**When to pick this:**
- The vision has a clear enemy or status quo to reject
- You want the vision to double as a public-facing artifact (recruitment, marketing, positioning)
- The team is comfortable with a literary/emotional tone
- The product has strong opinions about how work in the domain *should* be done

**When NOT to pick this:**
- The product is internal-only — the manifesto tone is wasted without a public audience
- There is no clear antagonist — Linear's power comes from naming specific enemies
- The team is not comfortable with storytelling conventions

**Mini-template:**

```markdown
# [Product Name]

## The Past

[Describe the domain as it once was — what was promised, what felt magical, what worked.
Invoke the sense of possibility that existed.]

## The Present

[Name the antagonists. What specifically has gone wrong?
Use concrete nouns — "three dark forces," "two problems," "the compromise."
Each antagonist should be specific enough to be controversial.]

### [Antagonist 1]

[One specific thing that is broken in the current state.]

### [Antagonist 2]

[Another specific thing.]

### [Antagonist 3]

[A third, if applicable. Three is usually the right number.]

## The Future

[What we're building to counter each antagonist.
This is the vision proper — but framed as restoration or rebellion, not as an improvement.
End with a call to the reader: "Who you play in these chapters is for you to decide."]

## Timeframe & Review

[Years. Next review. Owner.]

## Product Principles

[5-8 ranked principles. Often fits as "Our beliefs" or "How we work" in this scaffold — but keep the principles-guide.md structure regardless.]
```

## 4. Amazon Working Backwards (PR + FAQ)

**Source:** Amazon's internal Working Backwards practice. Described in *Working Backwards* by Colin Bryar and Bill Carr (2021). The original template is internal and not public; the structure below is reconstructed from practitioners who have used it.

**Shape:** Two pages, two documents. A fictional press release written as if the product has already shipped successfully, followed by an FAQ of hard questions. Highly constraining — forces every claim to be specific.

**Section structure:**

### Part 1: The Press Release (~1 page)

- **Headline** — product name + primary benefit, one line
- **Subheadline** — who it's for, why they care
- **Summary paragraph** — what it is, in one paragraph
- **Problem paragraph** — the customer problem being solved
- **Solution paragraph** — how the product solves it (no implementation details)
- **Customer quote** — a fictional customer explaining the value in their own words
- **Internal quote** — a company leader explaining why the company is excited
- **Call to action** — how a customer gets started

### Part 2: The FAQ (~1 page)

Two types of questions:

- **Customer-facing FAQ** — "What will this cost?" "How is it different from X?" "When will it be available?" "What do I need to use it?"
- **Internal / hard questions** — "Why will this succeed where competitors failed?" "What is the biggest risk?" "What assumptions are we making?" "What evidence do we have that customers want this?"

**When to pick this:**
- The user wants the shortest possible vision artifact
- Discipline-forcing format is attractive — the PR structure makes every claim earn its place
- The vision is for a specific, nameable product (not an open-ended platform)
- The team will use this as both a vision AND a discovery tool ("if we can't write the PR, we don't have a clear vision")

**When NOT to pick this:**
- The vision needs emotional / narrative depth
- The product is an open-ended platform with no single "launch moment" to describe
- The 2-page format won't capture the complexity the user wants to articulate

**Mini-template:**

```markdown
# [Product Name] — Vision (Working Backwards)

**Owner:** [Name] | **Date:** [date] | **Timeframe:** [2-5 or 5-10 years]
**Distribution:** [where this will be shared]

---

## Press Release (future-dated)

**[DATE 3 YEARS FROM NOW]** — **[Product Name] [primary benefit in one sentence.]**

[One-line subheadline: who it's for, why they care.]

**[CITY]** — [One-paragraph summary of what the product is, from the perspective of a business press release.]

**The problem**

[One paragraph describing the customer pain this product addresses.
Be specific about who experiences it and what they do today.]

**The solution**

[One paragraph describing how the product solves the problem, from the customer's perspective.
No implementation details. No technology names.]

> "[Fictional customer quote that captures the specific benefit.
> Use a named role, not a generic 'user.']"
> — [First Name Last Name], [Title], [Company]

> "[Fictional internal quote from a company leader explaining why this matters.]"
> — [First Name Last Name], [Title], [Company Name]

**How to get started:** [One sentence on how a customer becomes a customer.]

---

## FAQ

**Customer-facing:**

**Q: [Common customer question]**
A: [Answer.]

**Q: [Another common question]**
A: [Answer.]

**Internal / hard questions:**

**Q: Why will this succeed where [competitor] failed?**
A: [Answer grounded in a specific insight about the market or the customer.]

**Q: What is the biggest risk?**
A: [Answer — do not hedge.]

**Q: What assumptions are we making that could be wrong?**
A: [Answer — list 2-3 specific falsifiable assumptions.]

**Q: What evidence do we have that customers actually want this?**
A: [Answer grounded in research, user feedback, or pre-existing behavior. If you have none, say so.]

---

## Product Principles

[5-8 ranked principles — see principles-guide.md]
```

## 5. What applies regardless of scaffold

No matter which scaffold the user picks, these elements stay:

1. **Front matter:** `Last updated`, `Next review`, `Owner`, `Status`
2. **Distribution note:** one-line statement of how the vision will be evangelized (FM-5 countermeasure)
3. **Section 5 (Timeframe):** a statement of the vision's horizon and review cadence
4. **Section 6 (Product Principles):** 5–8 ranked principles per `principles-guide.md`
5. **The full quality checklist from `cagan-canon-and-writing.md`** — all 8 failure modes apply regardless of scaffold choice

Pick the shape that fits the user's taste and product situation, but do not skip these five elements. A Slack-memo-style vision without a principles section is still incomplete; a Linear-manifesto-style vision without a distribution note is still at risk of becoming a poster on the wall.
