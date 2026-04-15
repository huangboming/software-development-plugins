# Discovery Guide

Framework for the design consultation process. Covers five discovery tracks, brand personality mapping, product type differentiation, and consultation anti-patterns.

## Table of Contents

1. [Consultation Approach](#consultation-approach)
2. [Five Discovery Tracks](#five-discovery-tracks)
3. [Brand Personality Framework](#brand-personality-framework)
4. [Vibe-to-Tokens Heuristics](#vibe-to-tokens-heuristics)
5. [Product Type Matrix](#product-type-matrix)
6. [Consultation Anti-Patterns](#consultation-anti-patterns)

## Consultation Approach

Present multiple-choice options for every question possible. Users react to curated options far more easily than they generate answers from a blank canvas. This reduces cognitive load and produces more precise design signals.

- Generate 3-6 labeled options per question, tailored to the conversation context.
- Include an "Other" escape hatch for questions where the options might not cover the user's situation.
- Allow multi-select where appropriate (mark with "pick all that apply").
- Only use open-ended questions when the answer is truly unique to the user's situation.
- Pace at 2-4 questions per round, 3-4 rounds total. Later rounds should feel informed by earlier answers.

## Five Discovery Tracks

### Track 1: Product Context

Establish who uses this product, why, and under what conditions. This determines the entire design register.

Ask about (multiple-choice for each):

1. **What the product does** — open-ended, one sentence is enough
2. **Primary user archetype** — role and technical proficiency
3. **User mindset during use** — focused execution, exploration, under pressure, routine check-in, creative flow, etc.
4. **Voluntary vs required** — user chose it, org chose it, or mixed
5. **Session pattern** — all-day tool, regular sessions, quick check-ins, occasional visits

### Track 2: Brand Personality and Aesthetic Direction

Translate abstract brand attributes into visual parameters.

Ask about (multiple-choice for each):

1. **Product-as-person** — present personality archetypes that map to Aaker dimensions (see [Brand Personality Framework](#brand-personality-framework))
2. **Admired products** — curated list of well-known products with distinct visual identities, pick 2-3. Include a range spanning B2B, consumer, developer, and creative tools.
3. **Word-pair spectrum** — pick the side that fits:
   - Minimal ←→ Rich
   - Serious ←→ Playful
   - Traditional ←→ Modern
   - Quiet ←→ Bold
   - Technical ←→ Approachable

### Track 3: Content and Interaction Model

Determines spacing philosophy, type scale, and component priorities.

Ask about (multiple-choice for each):

1. **Primary content types** — multi-select: data tables, forms, dashboards, long-form text, media, code, cards, conversational UI, etc.
2. **Information density** — scale from very dense (multi-panel dashboards) to spacious (single-focus screens)
3. **Primary interaction mode** — task completion, data analysis, content consumption, discovery, creation, monitoring

### Track 4: Technical Constraints

Directly constrains token architecture.

Ask about (multiple-choice for each):

1. **Frontend framework** — common options plus "not decided yet"
2. **Styling approach** — Tailwind, CSS modules, CSS-in-JS, plain CSS, etc.
3. **Component library** — common options plus "building custom" and "not decided yet"
4. **Dark mode** — yes from day one, planned for later, no
5. **Accessibility target** — WCAG AA (standard) or AAA (stricter)
6. **Platforms** — multi-select: desktop web, responsive mobile, native, desktop app

### Track 5: Existing Visual Patterns (Establish mode only)

Run after the codebase audit. Use audit findings to populate the options.

1. **Keep or replace** — present each audit finding as a keep/replace choice
2. **Intentional brand colors** — list the most frequently appearing colors, ask which are deliberate vs. drift
3. **Gold standard** — open-ended: which components or pages should new work match?

## Brand Personality Framework

Based on Aaker's five brand personality dimensions. When presenting product-as-person options in Track 2, map each archetype to a dimension.

| Archetype direction | Primary Dimension |
|---------------------|-------------------|
| Calm, competent advisor | Competence |
| Energetic creative partner | Excitement |
| Precise, no-nonsense expert | Competence + Ruggedness |
| Approachable, helpful friend | Sincerity |
| Polished, confident leader | Sophistication |

### Dimension Profiles

| Dimension | Traits | Colors | Typography | Shapes | Spacing |
|-----------|--------|--------|------------|--------|---------|
| **Sincerity** | Honest, wholesome, cheerful | Warm neutrals, muted pastels, natural greens | Humanist sans (Inter, DM Sans), moderate weight | Subtle rounding, organic | Generous |
| **Excitement** | Daring, spirited, imaginative | Saturated, high-contrast, gradients | Bold weights, larger scale ratio, display type | Dynamic, asymmetric | Tight hero, generous content |
| **Competence** | Reliable, intelligent, successful | Blues, cool grays, minimal accents | Geometric/transitional sans (IBM Plex, Söhne) | Precise geometry, small radius | Consistent, systematic |
| **Sophistication** | Elegant, charming, premium | Muted, low saturation, jewel tones | Serif display, thin weights, ample tracking | Minimal radius, fine borders | Very generous |
| **Ruggedness** | Tough, outdoorsy, robust | Dark tones, high contrast, earthy | Heavy weights, condensed display | Sharp corners, bold borders | Tight, purposeful |

Most products blend 2-3 dimensions. Identify the primary and secondary to resolve conflicts.

**Applying the framework:**

1. Map personality archetype to primary dimension, reference products to refine, word-pairs to confirm
2. Use dimension profiles to set initial ranges for each visual property
3. Refine based on product type matrix

### The "Opposite Word" Test

For each brand attribute, identify its opposite. The visual decision should sit clearly on the intended side without hitting the extreme.

Example: "professional" (4px radius) vs "playful" (16px radius) — 0px is aggressively cold, 24px is aggressively casual. The right answer is rarely the extreme.

## Vibe-to-Tokens Heuristics

Direct mappings from visual property values to perceived character.

### Border Radius → Approachability

```
0px      = sharp, technical, precise, cold
2-4px    = structured, B2B neutral
6-8px    = approachable, modern
12-16px  = friendly, consumer, playful
24px+    = casual, bubble-like
```

### Color Temperature → Emotional Register

```
Cool (blue, teal, purple)    = trust, calm, intelligence
Warm (red, orange, yellow)   = energy, urgency, warmth
Neutral (gray, stone, slate) = sophisticated, professional
Natural (sage, terracotta)   = organic, grounded
```

### Saturation → Brand Intensity

```
High    = bold, youthful, attention-seeking
Medium  = balanced, mainstream
Low     = restrained, premium, mature
```

### Typography Weight → Authority

```
Light/thin    = elegant, delicate, minimal
Regular       = approachable, neutral
Medium/semi   = confident, clear
Bold/black    = authoritative, impactful
```

### Type Style → Personality

```
Geometric sans (Circular, Futura)      = modern, clean, tech
Humanist sans (Inter, DM Sans)         = friendly, readable
Transitional sans (IBM Plex, Söhne)    = intelligent, editorial
Serif (Playfair, Freight)              = traditional, authoritative
Monospace                              = technical, developer-facing
```

### Spacing Density → Use Context

```
Tight (4px base)      = data-dense, professional tools
Standard (8px base)   = general purpose
Generous (12px+ base) = consumer, marketing, editorial
```

### Color Count → Personality

```
1-2 accents  = focused, disciplined, premium
3-4 accents  = expressive, functional variety
5+ accents   = data visualization or chaotic
```

## Product Type Matrix

Four discriminating questions determine product type:

1. **Buyer vs user** — same person (consumer) or different (enterprise)?
2. **Voluntary vs required** — optimize for first impression or thousandth use?
3. **Primary interaction** — task completion, exploration, data analysis, or content?
4. **Session pattern** — daily heavy use (avoid fatigue) or occasional (be expressive)?

| Dimension | B2B SaaS | Consumer App | Developer Tool | Marketing Site | E-commerce |
|-----------|----------|--------------|----------------|----------------|------------|
| **Density** | High | Low-medium | High | Low | Medium |
| **Spacing base** | 4-8px | 8px | 4px | 8-12px | 8px |
| **Border radius** | 2-6px | 8-16px | 0-4px | 6-12px | 6-10px |
| **Type scale ratio** | 1.125-1.200 | 1.250-1.333 | 1.067-1.250 | 1.333-1.500 | 1.250 |
| **Palette** | Muted, 1-2 accents | Expressive, 2-4 accents | Monochrome + 1 accent | Brand-bold | Neutral + strong CTA |
| **Dark mode** | Optional | Expected | Essential | Rare | Rare |
| **Motion** | Minimal | Expressive | Minimal | Purposeful | Subtle |
| **Typography** | Geometric/transitional sans | Humanist sans, display variety | Monospace present | Display-heavy, brand type | Clear hierarchy, price/CTA focus |

## Consultation Anti-Patterns

Avoid these:

- **Open-ended questions where choices work** — curated options produce more precise design signals than blank-canvas questions.
- **Front-loading all questions** — feels like a form. Ask 2-4 per round, build context progressively.
- **Designing for stakeholders, not users** — ground decisions in user demographics, use context, and task patterns.
- **Skipping the audit (Establish mode)** — builds the wrong system. Always inventory what exists before proposing replacements.
- **Accepting vibe words at face value** — "premium" means different things to different people. Anchor with reference product examples.
- **Proposing without rationale** — every recommendation needs a "because" tied to discovery findings.
