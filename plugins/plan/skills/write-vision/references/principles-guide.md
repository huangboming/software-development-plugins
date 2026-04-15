# Product Principles Guide

Companion guide for Section 6 of `vision.md`. Read this when drafting or reviewing product principles. Do not load this file when working on any other section.

## Contents

1. [What a product principle is](#1-what-a-product-principle-is)
2. [The canonical example (eBay)](#2-the-canonical-example-ebay)
3. [The conflict-resolution test](#3-the-conflict-resolution-test)
4. [The position + rationale writing pattern](#4-the-position--rationale-writing-pattern)
5. [Ranking and count](#5-ranking-and-count)
6. [Elicitation: how to get principles out of the user](#6-elicitation-how-to-get-principles-out-of-the-user)
7. [Principle quality checklist](#7-principle-quality-checklist)

---

## 1. What a product principle is

A product principle is an explicit statement of which value wins when values conflict. It is a **standing rule for trade-off resolution** — the decision the team has already made so that future arguments do not need to be re-litigated.

Cagan's framing (*Inspired*, 2nd ed., Chapter 27):

> Product principles speak to the nature of the products you want to create. They are intended to inform the very many product decisions that teams will need to make.

Principles are a **companion** to vision, not part of it. Vision says *where* we're going; principles say *how we decide* along the way. They are often packaged together ("the product vision and principles") but serve different purposes.

**What a principle is not:**
- Not a value statement ("we value quality")
- Not an aspiration ("we strive for excellence")
- Not a feature commitment ("we will always support dark mode")
- Not a process rule ("we ship every two weeks")

A principle resolves a conflict. If there is no conflict to resolve, it is not a principle.

## 2. The canonical example (eBay)

The clearest example Cagan cites is eBay's buyer/seller principle (attributed, *Inspired* Chapter 27):

> In cases where the needs of the buyers and the sellers conflict, we will prioritize the needs of the buyer, because that's actually the most important thing we can do for sellers.

Why this is a great principle:

1. **It resolves a real conflict.** Buyers want low prices, quick refunds, and buyer protection. Sellers want high prices, limited returns, and seller protection. These needs actively oppose each other on every product decision.
2. **It's counterintuitive.** eBay's revenue comes from sellers — fees, listings, promoted listings. The obvious bet is to favor the revenue side. The principle goes the other way.
3. **It's grounded in insight.** The rationale ("that's the most important thing we can do for sellers") is not an apology — it's a substantive claim about how the marketplace works. Sellers need buyers, so buyer-friendly moves grow the pool of buyers, which is the biggest lever for seller success.
4. **It's load-bearing.** A product manager facing any buyer-seller decision can apply this principle and get an unambiguous answer. The principle does real work.

Use this example as the calibration standard when reviewing every principle. Ask: "Does this principle resolve a conflict as cleanly as the eBay example?"

## 3. The conflict-resolution test

The single best test for whether a principle is real or a platitude:

> **Could two reasonable people, each advocating for a different legitimate value, use this principle to settle the argument?**

If the answer is "yes, and the principle tells one of them they lose," it is a real principle. If the answer is "both people would agree with this principle," it is a platitude.

### Examples

| Statement | Platitude or principle? | Why |
|---|---|---|
| "We value quality." | Platitude | No reasonable person advocates for low quality. There is no conflict to resolve. |
| "We will ship fewer features at higher polish, even when customers ask for more features." | Principle | Resolves the "ship more vs. polish more" conflict. Tells the "ship more" side they lose. |
| "We prioritize the customer." | Platitude | Every company says this. It does no work. |
| "We prioritize the reader over the writer on every page." | Principle (Medium, circa 2015) | Resolves the "writer wants reach and discovery vs. reader wants clean experience" conflict. Tells the writer-advocacy side they lose. |
| "Our users are engineers; we will never dumb down the interface to attract non-engineers." | Principle | Resolves the "expand the market vs. preserve the user base" conflict. Tells the expand-the-market side they lose. |
| "Community is important to us." | Platitude | No actual trade-off stated. |
| "Community is the most important part of our product — we will reject any feature that creates lurkers instead of participants, even if it boosts top-of-funnel metrics." | Principle | Resolves the "growth metrics vs. community health" conflict. Tells the growth-metrics side they lose. |
| "We ship quickly." | Platitude (or a process rule masquerading as a principle) | Doesn't resolve any conflict about what to build. |

If a candidate principle fails the conflict-resolution test, one of the following is true:

- It is a value, not a principle — move it to the vision narrative or delete it.
- It is a platitude — delete it.
- The real conflict is being avoided — ask the user "what would this principle reject?" and rewrite.

## 4. The position + rationale writing pattern

Every principle should follow this two-sentence structure:

> **[Position]** — a one-sentence statement of what wins when values conflict.
> **Why:** a one-sentence explanation grounded in a specific insight or experience.

The position sentence is the principle itself. The rationale sentence is what elevates it from a bare rule to a decision-support tool — it tells future teams *why* this trade-off was made, so they can extend the principle to new situations.

### Worked examples

**Principle 1: Reader over writer.**
> **Position:** We prioritize the reader's experience over the writer's reach on every page.
> **Why:** Readers generate the attention that writers want; a reader-hostile page collapses the whole attention loop.

**Principle 2: Depth over breadth.**
> **Position:** When choosing between supporting a new file format and polishing an existing one, we polish.
> **Why:** Our power-user segment generates 80% of expansion revenue and 100% of our word-of-mouth; breadth attracts trial users who churn, depth retains power users who pay and refer.

**Principle 3: Refusal over workaround.**
> **Position:** When a feature request would compromise our core abstraction, we refuse rather than add a workaround.
> **Why:** Every workaround we shipped in 2024 became 2x the maintenance cost of the original feature by 2026, and each one made the next refusal harder to justify.

The rationale sentence is what makes a principle **extendable** to novel situations. A team facing a new decision can ask "does this new situation have the same dynamics as the ones cited in the rationale?" and get a real answer.

## 5. Ranking and count

**Count: 5–8 principles.** Fewer than 5 means the vision is probably under-constrained. More than 8 means the principles are doing too many small jobs — most likely some of them are platitudes padding the list.

Cagan's guidance is "fewer than 10" (*Inspired* Chapter 27). Eight is a practical ceiling; five is a practical floor. If you are tempted to include more than eight, ruthlessly apply the conflict-resolution test and cut any that fail.

**Ranking is load-bearing.** When two principles conflict with each other — which happens in the hardest cases — the ranked order tells the team which principle wins. Unordered principles leave future conflicts unresolved.

### Ranking example

Suppose a product has these two principles:

1. **Depth over breadth.** Polish existing features before adding new ones.
2. **Ship weekly.** Maintain a weekly shipping cadence regardless of feature size.

A team facing a polish-vs-ship-on-time conflict needs to know which wins. If depth-over-breadth is ranked higher, they delay the release to polish. If ship-weekly is ranked higher, they ship with rough edges and iterate next week. The ranking makes the decision tractable.

When drafting, ask the user: "If principles A and B conflicted, which one would you want to win?" Use the answer to order them. Do not present principles as an unordered bulleted list.

### Display format in vision.md

```markdown
## Product Principles

These are the standing rules we use to resolve trade-offs. Principles earlier in
the list outrank principles later in the list when they conflict.

### 1. Reader over writer

**Position:** We prioritize the reader's experience over the writer's reach on every page.

**Why:** Readers generate the attention that writers want; a reader-hostile page collapses the whole attention loop.

### 2. Depth over breadth

**Position:** When choosing between supporting a new file format and polishing an existing one, we polish.

**Why:** Our power-user segment generates 80% of expansion revenue and 100% of our word-of-mouth.

### 3. [next principle...]
```

## 6. Elicitation: how to get principles out of the user

Principles are the hardest section to write because they require the user to articulate trade-offs they may never have named out loud. Do not ask "what are your product principles?" — that question produces platitudes.

Instead, ask conflict-shaped questions:

1. **"When your team has an argument about what to build, what is the argument usually about?"** The recurring arguments reveal the conflicts that need principles.
2. **"Name a feature request you rejected recently. Why?"** The rejection rationale is often a latent principle.
3. **"Describe a decision where a reasonable person could have chosen differently, and explain why you chose the way you did."** This surfaces the implicit ranking the team is already using.
4. **"What do your competitors do that you refuse to do, even though it might work for you?"** Refusals reveal positioning principles.
5. **"If you had to give your 100th engineer one rule to settle disputes without escalating, what would it be?"** Forces the user to compress their trade-off judgment into a transferable rule.

After collecting raw material from 2–4 of these questions, draft candidate principles and present them for refinement. Iterate until each principle passes the conflict-resolution test.

**If the user cannot produce any real conflicts:** this is a signal that the product is either too new to have principles (everything is exciting, nothing is constrained yet) or the user is not close enough to product decisions to articulate them. Suggest deferring Section 6 with a placeholder ("TBD — will draft after the first quarter of shipping") rather than filling it with platitudes.

## 7. Principle quality checklist

Review every principle against every item before including it in `vision.md`:

- [ ] **Passes the conflict-resolution test.** Two reasonable people could use this principle to settle a specific argument, and the principle tells one of them they lose.
- [ ] **Names a real trade-off.** The principle identifies what loses, not just what wins.
- [ ] **Uses the position + rationale format.** One sentence of position, one sentence of rationale grounded in a specific insight or experience.
- [ ] **Rationale is extendable.** The "why" tells future teams enough to apply the principle to novel situations they weren't imagined for.
- [ ] **Not a process rule.** Does not describe *how* work is done (ship weekly, review before merge). Describes *what* gets built and for whom.
- [ ] **Not a value statement.** Does not use words like "value," "strive," "believe in" without a specific rejected alternative.
- [ ] **Not a feature commitment.** Does not lock in specific features or capabilities (FM-3 territory).

At the set level:

- [ ] **Count is 5–8.** Fewer than 5 → under-constrained. More than 8 → platitudes padding the list.
- [ ] **Ranked, not unordered.** The user has explicitly stated which principle wins when two conflict.
- [ ] **At least one counterintuitive principle.** The set contains at least one principle that would surprise a newcomer — a principle nobody would have guessed without being told.
- [ ] **No internal contradictions.** No two principles directly oppose each other without the ranking resolving the conflict.

If any principle fails an individual item, rewrite or remove it. If the set fails any set-level item, rebalance.
