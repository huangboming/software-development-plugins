# Teardown Template

````markdown
# Teardown: [Target Name]

**Date drafted:** [today's date]
**Lens:** [job-to-be-done | pricing-and-packaging | positioning | gaps-and-frictions | technical]
**Status:** drafted
**Confidence:** [strong | moderate | emerging | speculative]

## Target

[One paragraph: what the target is, who it serves, what form factor it takes (SaaS, self-hosted, spreadsheet workaround, DIY script, status quo). Include the freshness date of the snapshot this teardown is based on.]

## Sources

- [URL or reference] — [what this source contributes | accessed YYYY-MM-DD]
- [URL or reference] — [what this source contributes | accessed YYYY-MM-DD]
- ...

## Findings

[Structured by the selected lens — see references/lenses.md for what goes under each lens and what to skip. Every factual claim is either linked to a source above or marked `inferred` in-line with the basis.]

## So What

[One paragraph. The implication for our framing or solution search. Completes the sentence: "Because of what this teardown found, we should...". Names the downstream artifact this feeds — a framed opportunity, an assumption to test, an analog branch in a solution tree, a positioning call, or an explicit pass.]

## Non-Goals

[What this teardown explicitly does NOT cover: adjacent products, deferred segments, unexamined lenses. Optional — fill when readers are likely to over-extend the scope.]

## Related

[Links to other teardowns, framed opportunities, or signals on adjacent targets. Otherwise "None yet."]
````

## Field Guidance

### Sourcing discipline — observed vs. inferred

Every factual claim in Findings must be traceable. Two acceptable shapes:

- **Observed** — links to an entry in Sources. Default shape. Example: "Pricing starts at $8/user/month (source: pricing page, accessed 2026-04-10)."
- **Inferred** — marked in-line with `(inferred: [basis])`. Use when the claim is reasoned from general knowledge, pattern-matching, or indirect signals. Example: "Team plans cap at 50 seats (inferred: absent from landing page, referenced by two G2 reviewers cited above)."

Unmarked unsourced claims are fabricated-evidence liabilities. A downstream reviewer must be able to distinguish what the teardown saw from what it guessed.

### The So What test

The So What passes if a reader can finish this sentence:

> "Because of what this teardown found, we should..."

...with one of:

- Frame (or reframe) an opportunity in `.product/discover/opportunities/`.
- Test an assumption in `.product/discover/assumptions/`.
- Add an analog branch to an opportunity solution tree.
- Change our positioning, category, or scoping.
- Pass — this target does not inform the decision at hand (explicit pass is valid; silent no-implication is not).

If the sentence cannot be finished, the teardown has no reader. Deepen the lens or narrow the scope before writing.

### Confidence calibration

| Level | Criteria |
|-------|----------|
| strong | Multiple primary sources (product docs, pricing page, public financials, direct interviews with users of the target), all within 3 months |
| moderate | One primary source plus secondary (G2, Reddit, public blog posts), within 6 months |
| emerging | Secondary sources only, or material older than 6 months |
| speculative | Inferred-heavy teardown, no verifiable primary source, or target is private / pre-launch |

Default to the lower adjacent level when in doubt. Underrating confidence protects against over-reach in the So What.

### Status field lifecycle

Written by this skill as `drafted`. Downstream updates:

| Status | Set by |
|--------|--------|
| drafted | `teardown-competitor` (this skill) |
| synthesized | `synthesize-research` when folded into a cross-cut |
| superseded | manual or this skill on re-teardown |
| archived | manual, when the target is no longer relevant — record reason in the file |

Do not invent new statuses — downstream skills filter on these values.

### Slug naming

Derive `<slug>` from the target name, not the lens: lowercase, kebab-case, 1–3 words. Examples:

- "Notion" → `notion`
- "Google Sheets" → `google-sheets`
- "Status quo (email + meetings)" → `status-quo-email-meetings`

If a file with the same slug exists, first decide Refresh / Supersede / Lens variant (see SKILL.md Edge Cases). For lens variants, append the lens qualifier: `teardown-notion-pricing.md`. For same-slug collisions that are neither refresh nor variant, append the drafting date: `teardown-<slug>-YYYY-MM-DD.md`.

## Quality check

Before writing, confirm:

- [ ] Every claim in Findings is either linked to an entry in Sources or marked `inferred` with basis.
- [ ] Findings is structured by the selected lens, not a generic feature dump.
- [ ] The So What passes the "Because of what this teardown found, we should..." test.
- [ ] The target and at least one indirect alternative were considered in scope, or the scoping choice is noted in the body.
- [ ] Access dates are present on every source that can be timestamped.
- [ ] Confidence matches the sourcing posture per the calibration table above.

Correct violations in place. If a violation requires input the user has not supplied (e.g., the So What cannot be named without a target framed opportunity), pause and ask. If all six items pass, proceed to write.
