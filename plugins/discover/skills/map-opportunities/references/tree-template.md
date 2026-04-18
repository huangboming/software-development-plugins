# Opportunity Solution Tree Template

```markdown
# Opportunity Tree: [Short Name]

**Date mapped:** [today's date]
**Source opportunity:** `.product/discover/opportunities/<slug>.md`

## Root Outcome

[Paste the "What Good Looks Like" from the source framed opportunity verbatim. An end state for the user, not a feature.]

## Sub-Outcome 1: [Name]

[One sentence — still outcome-shaped, one layer more specific than the root.]

### Solutions

- **[Solution A]** — [1–2 sentence description of the product mechanic]
  - Key assumption: [The single claim that, if wrong, this solution fails.]
  - Risk: [low | medium | high] — [one-line rationale]
- **[Solution B]** — ...
  - Key assumption: ...
  - Risk: ...
- **[Solution C — reach]** — ...
  - Key assumption: ...
  - Risk: ...

## Sub-Outcome 2: [Name]

...

## Pruning Notes

[Optional. Capture branches discussed and dropped, with a one-line rationale each. Useful downstream for `prioritize` — records what was considered so the same ideas do not resurface without new evidence.]
```

## Field Guidance

### Root outcome — outcome test

Copy the **What Good Looks Like** from the source framed opportunity verbatim. Do not re-author it here — if it reads as weak or feature-shaped, fix it in the source file first.

| Weak (feature / product-shape) | Strong (user-side end state) |
|--------------------------------|-------------------------------|
| "We ship a configuration wizard" | "A new admin reaches a working configuration in under 10 minutes without support" |
| "Launch a partner API" | "Partners integrate in under a day instead of the current two-week average" |

### Sub-outcome — the middle layer

A sub-outcome is itself outcome-shaped — an end state for the user, one layer more specific than the root. Generate sub-outcomes by slicing the root along one of these dimensions:

- **Journey stages** — what happens before, during, after the main action?
- **User segments** — does a sub-segment experience this outcome differently?
- **Contexts** — first-time vs. returning, solo vs. team, high-trust vs. low-trust.
- **Unmet needs** — specific reported or observed needs under the umbrella of the desired outcome.

| Weak (feature-shaped sub-outcome) | Strong (outcome-shaped sub-outcome) |
|-----------------------------------|--------------------------------------|
| "Add a settings wizard" | "A new admin knows which inherited settings still apply to their team" |
| "Build an onboarding tour" | "A first-session user reaches the aha moment without reading documentation" |

If a sub-outcome reads as "we build X" or names a UI, rewrite it as the user-side end state.

### Per-node branch counts (canonical)

This is the single source of truth for productive branch-count ranges. SKILL.md enforces the minimum of 3; this file owns the upper bound and the splitting signal.

| Node | Minimum | Upper bound | What exceeding the upper bound means |
|------|---------|-------------|---------------------------------------|
| Root → sub-outcomes | 3 | 7 | The root outcome is too broad for one tree. Split it, or accept partial mapping and name the scope explicitly. |
| Sub-outcome → solutions | 3 | 7 | The parent sub-outcome is too broad. Split it into two narrower sub-outcomes. |

Fewer than 3 at either node is premature convergence — revisit before writing.

### Solutions — concrete and comparable

A solution describes a product mechanic at enough grain to be compared against a sibling: "a guided wizard that walks through each inherited setting with a recommendation" is comparable; "improve settings" is not.

Branch counts and splitting signals are in the *Per-node branch counts* table above.

### Reach solutions

At least one reach per sub-outcome. A reach breaks a convention, inverts a default, or imports a mechanic from another domain. Its job is to stretch the evaluation space, not to be selected. If every "reach" feels safe, it is not reaching.

### Key assumption per solution

Every solution rests on a load-bearing claim. Name the single riskiest one using one of four categories:

- **Desirability** — the target user actually wants this.
- **Viability** — the business economics support shipping this.
- **Feasibility** — the team can build this with available tools and time.
- **Usability** — the target user can use this successfully once shipped.

Write the specific claim, not the category:

| Weak (category only) | Strong (specific claim) |
|----------------------|--------------------------|
| "Desirability" | "B2B admins will accept a wizard even though they normally prefer full manual control" |
| "Feasibility" | "We can detect inherited-but-no-longer-applicable settings without a schema migration" |

### Risk calibration

| Level | Meaning |
|-------|---------|
| low | Assumption has direct evidence from signals, research, or a prior shipped feature |
| medium | Assumption is plausible from analogous cases but not directly tested in this context |
| high | Assumption is novel, load-bearing, and has no direct evidence |

`test-assumption` prioritizes `high` first, then `medium`. A solution whose key assumption is `low` is usually ready to enter `prioritize` without a separate test.

### Slug naming

The tree slug matches the source framed opportunity's slug, prefixed with `tree-`.

| Source opportunity | Tree |
|--------------------|------|
| `.product/discover/opportunities/new-admin-config-inheritance.md` | `.product/discover/opportunities/tree-new-admin-config-inheritance.md` |
| `.product/discover/opportunities/weekly-report-reauthoring.md` | `.product/discover/opportunities/tree-weekly-report-reauthoring.md` |

When re-mapping an opportunity, preserve the old tree: rename it to `tree-<slug>-YYYY-MM-DD.md` and write the new tree at `tree-<slug>.md`.
