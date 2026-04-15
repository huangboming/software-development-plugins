# Reference Workflow

Adapt a known public design system to the user's project. Use this workflow when the user names a reference product ("make it feel like Linear", "we want Stripe-style elegance") instead of running the full Create consultation.

Most real-world design starts from a reference, not a blank canvas. When the user can name a product whose vibe matches what they want, anchoring on that product's tokens and adapting deltas is more efficient and produces a more coherent result than the full questionnaire.

## When to Use This Workflow vs. Create

| Situation | Workflow |
|---|---|
| User says "make it feel like X" or names a reference product | **Reference** (this) |
| User has a brand color and a reference product in mind | **Reference** |
| User has no clear reference and wants a structured consultation | **Create** |
| User wants the system anchored on existing codebase patterns | **Establish** |

## Steps

1. Pick the reference
2. Identify deltas
3. Adapt token values
4. Draft `DESIGN.md`
5. Generate preview, verify, and present

## Step 1: Pick the Reference

Survey the available examples in [SKILL.md → Examples](../SKILL.md#examples) — each entry lists archetype and best-fit product types. Each example file is a real public system extracted from awesome-design-md, with full prose, recipes, and Agent Prompt Guide intact.

If none of the vendored examples match, ask the user to pick a product from the [awesome-design-md catalog](https://github.com/VoltAgent/awesome-design-md) and fetch its `DESIGN.md` as the starting point. Vendor the file into `references/examples/` if the user wants it persisted.

Confirm the choice before proceeding: "I'll anchor on the [reference] system. We'll keep its [signature characteristic 1] and [characteristic 2], and adapt the rest to your project."

## Step 2: Identify Deltas

Ask focused questions only about what should differ from the reference. Skip the full Q1-Q17 consultation. Default to 3-6 questions covering:

1. **Brand color** — Does the user have a primary brand color, or should we keep the reference's? If they have one, get the hex.
2. **Density** — Keep the reference's density, or adjust? (e.g., "Linear is very dense — do you want the same, or more breathing room?")
3. **Light/dark** — Keep the reference's mode, invert it, or support both?
4. **Type face** — Keep the reference's font, or substitute? If substitute, what?
5. **Accent uses** — Keep the reference's restraint level (single accent vs. multiple)?
6. **Component library constraint** — Does the user need to align with shadcn/MUI/Chakra/etc., which constrains the token names?

Use multiple-choice questions per the [discovery-guide.md](../references/discovery-guide.md) consultation approach. Each delta the user picks becomes a documented adaptation note.

## Step 3: Adapt Token Values

For each section of the reference, decide: keep, adapt, or replace.

1. **Color** — If brand color changes, regenerate the brand palette using the [token-derivation-guide.md](../references/token-derivation-guide.md) HSL approach. Keep the semantic structure (background/card/popover/muted/primary/etc.) and the surface count. Re-verify WCAG AA contrast on every changed pairing.
2. **Typography** — If font changes, keep the same scale ratio and weight system, just swap the family. If density changes, adjust the scale ratio (denser = smaller ratio).
3. **Spacing** — Keep the reference's base unit unless density changes substantially.
4. **Components** — Keep the reference's recipes unchanged where possible. Update only the values that depend on the changed tokens (background, text color, border).
5. **Motion** — Keep as-is unless the user has different needs.

For every change, record what it replaces in the reference. This becomes the "Adaptation Notes" subsection in Visual Theme & Atmosphere.

## Step 4: Draft

Read [design-system-template.md](../references/design-system-template.md). Then read the chosen reference example in full to internalize its prose voice, recipe density, and section thickness.

Create `DESIGN.md` at the project root:

1. **Visual Theme & Atmosphere** — write 2-3 paragraphs in the same evocative voice as the reference, but describing *the user's product*. Open with one sentence acknowledging the lineage: "This system adapts the [reference] approach for [user's product type]." Then describe the canvas, the typographic voice, the color role, and the structural moves — substituting the user's deltas. Add a "Key Characteristics" bullet list of 6-10 items, mostly inherited from the reference but with the user's deltas folded in. Include an "Adaptation Notes" subsection listing what changed from the reference and why.
2. **Design Principles** — keep the reference's principles where they apply. Substitute or add as needed for the user's product.
3. **Color Palette & Roles** — follow the reference's structure (primitive palette → semantic tokens → accessibility table). Use the user's brand color if specified; otherwise keep the reference's.
4. **Typography Rules** — same structure as the reference, swap the family if needed.
5. **Component Recipes** — copy the reference's recipes verbatim, then update token references where colors changed. Keep the variant set.
6. **Layout Principles** — keep the reference's spacing and radius scales unless density changed.
7. **Depth & Elevation** — keep the reference's shadow philosophy and scale.
8. **Motion** — keep the reference's motion tokens.
9. **Responsive Behavior** — keep the reference's breakpoints and collapsing strategy.
10. **Do's and Don'ts** — keep the reference's Don'ts (these are the identity guardrails) and adapt the Do's to the user's specific tokens.
11. **Agent Prompt Guide** — quick color reference with the user's tokens, 5-8 example component prompts adapted from the reference's, numbered Iteration Guide carrying over the reference's rules.
12. Set "Last updated" to today's date.

## Step 5: Generate Preview, Verify, and Present

Generate the visual preview (see [SKILL.md → Output](../SKILL.md#output) for the command).

Verify against this checklist:

- The Adaptation Notes subsection clearly lists every delta from the reference.
- Brand color (if changed) propagates through every relevant token (primary, primary-foreground, accent, ring, etc.).
- WCAG AA contrast holds on every changed pairing.
- The reference's signature moves (shadow philosophy, weight system, border treatment) are preserved unless deliberately changed.
- Component recipes still type-check against the new color tokens.

Present `DESIGN.md` and `DESIGN-preview.html` together. Highlight the key adaptations and ask whether anything should be pushed further toward the reference or further away.
