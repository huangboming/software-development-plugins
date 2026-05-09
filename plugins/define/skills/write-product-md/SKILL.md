---
name: write-product-md
description: "Write or update .product/define/product.md, the present-tense definition of what the product is today. For alignment first, use grill-me. Triggers: '/write-product-md', 'write product.md', 'write the product definition', 'create product.md', 'update product.md'."
---

Write or update `.product/define/product.md` — the present-tense, concrete definition of what the product is today. No feature list — features live in PRDs.

If alignment is shaky, run `grill-me` first using the template below as the decision tree.

## Process

1. **Locate the file.** Target is `.product/define/product.md`. Read it if it exists; flag any inconsistency between it and the inputs you were given.
2. **Draft against the template** using the aligned context (typically from a prior `grill-me` session, plus existing artifacts under `.product/`). If inputs are insufficient, stop and run `grill-me`. Do not invent.
3. **Review against the quality bar; revise; present.**

## Template

````markdown
# <Product Name>

> Last updated: <YYYY-MM-DD>

## Purpose

<2–3 sentences, present tense. What the product does for its users and the user problem it solves today. Start with the customer, not the solution. If product stage shapes current decisions ("early MVP — optimizing for learning"), say so here.>

## Target Users

<1–4 primary segments. For each: who they are, the friction this product removes, and what "using our product" looks like for them — 2–3 sentences each, prose not bullets.>

## Why this over alternatives

<One paragraph. State the comparison explicitly — "instead of doing X in a spreadsheet" or "unlike <competitor>".>

## Non-goals

- <Adjacent problem someone might assume is in scope but isn't, with a one-line reason.>
````

## Quality bar

- Purpose stays present-tense. "Eventually…" or "One day…" belongs in a separate aspirational doc.
- Target Users name decision-shaping characteristics ("2–10 person dev teams shipping weekly"), not archetypes ("developers who value craft").
- No feature list. Purpose + "Why this over alternatives" answer "what does our product do?" at the right altitude.
- Non-goals would genuinely surprise a first-time reader.
- Named alternative is stated. If the inputs don't surface one, stop and run `grill-me` — nearly every product competes with the status quo, a spreadsheet, or a manual process.
