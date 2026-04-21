# Product Definition Template

Use this scaffold for `.product/define/product.md`. Keep the document under ~2 pages once filled in — `product.md` is a living definition, not a narrative.

**Status values:**
- `Draft` — initial version, not yet validated with the team or stakeholders.
- `Current` — validated and reflects the product today. Edit in place as the product evolves.

```markdown
# <Product Name>

> Status: Draft | Current
> Last updated: <YYYY-MM-DD>

## Purpose

<2–3 sentences, present tense. What the product does for its users, and the user problem it solves today. Start with the customer, not the solution. This is concrete and grounded — leave aspirational 3–10yr framing for vision.md.>

## Target Users

<One sub-section per primary segment. Keep to 2–4 segments. If there are more, the product is probably too broad or segments are too narrow — revisit.>

### <Segment Name>

- **Role / context:** <who they are, when/where they encounter the problem>
- **Key characteristics:** <what distinguishes this segment — size of team, sophistication, tooling, industry, etc.>
- **Primary pain today:** <the specific friction this product removes>
- **What "using our product" means for them:** <concrete — the hook or habit, not the vision>

## Value Proposition & Positioning

<One paragraph. Why a user in the target segment picks this product over the status quo or competitors. State the comparison explicitly — "instead of doing X in a spreadsheet" or "instead of using <competitor>".>

**Positioning statement (optional, one line):**
> For <target segment> who <need/pain>, <product name> is a <category> that <key benefit>, unlike <alternative>, which <shortcoming>.

## Scope & Non-Goals

**In scope for the product:**

- <Capability area the product does cover — stated broadly, not as a feature list>

**Non-goals (product-level):**

- <Adjacent problem someone might reasonably assume is in scope but isn't, with a one-line reason>

<Feature-level scope lives in individual PRDs under `.product/define/specs/<feature>/`. This section is for boundaries that shape the product's identity, not feature cuts.>

## Product Stage

<One of: Pre-launch / MVP / Scaling / Mature / Sunsetting. One sentence of context — what stage-specific pressures shape decisions right now (e.g., "MVP — optimizing for learning over polish" or "Scaling — guardrails and reliability take priority over new surface area").>

## Open Questions

- [ ] <Unresolved question about the product's definition — not about a specific feature>
```

## Notes on sections

**Purpose vs. Vision (`define-vision`'s Future We're Creating):**
- Purpose is **present tense** and **concrete** — what the product does and for whom, right now.
- Vision is **future tense** and **aspirational** — the world being created 3–10yr out, the leap of faith.
- If a sentence starts with "Eventually…" or "One day…", it belongs in vision.md, not here.

**Target Users vs. Vision's "Who We're Building For":**
- Both name the user, but at different resolutions.
- Vision names the archetype directionally ("independent software developers who value craft").
- Product names segments concretely with characteristics that shape product decisions today ("2–10 person dev teams using GitHub, shipping to production weekly, already paying for at least one developer SaaS").

**No features section:**
- Feature inventories go stale fast and duplicate the opportunity/slice/PRD chain.
- If stakeholders ask "what does our product *do*?", Purpose + Value Proposition should answer at the right altitude. Specific capabilities live in feature PRDs.

**No success metrics:**
- Product-level metrics belong in vision (north star) or in per-feature PRDs and the `set-success-metrics` artifact. Keep `product.md` focused on definition, not measurement.
