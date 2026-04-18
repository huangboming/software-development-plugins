# Issue Record Template

```markdown
# Issue: [Short Name]

**Date captured:** [today's date]
**Category:** [bug | refactor | tech-debt | perf-internal]
**Source:** [where this came from — specific enough to trace back: "QA session 2026-04-15", "prod logs incident INC-482", "code review on PR #312", "oncall rotation 2026-04". If the issue was reported conversationally with no external reference, use: "Reported in Claude Code session, YYYY-MM-DD"]
**Status:** New

## Summary

[One to two sentences. What is broken, messy, or slow — facts only, no proposed fix.]

## Details

[Category-dependent — see field guidance below. For bugs: expected vs. actual + repro steps. For refactor/tech-debt: what the current shape is and why it hurts. For perf-internal: baseline numbers + where it's felt.]

## Impact

[Who or what is affected, and how badly. For bugs: blast radius (users, environments, frequency). For refactor/tech-debt: what future work it slows. For perf-internal: which systems or SLOs degrade.]

## Assessment

**Severity:** [blocker | high | medium | low — required for bugs, optional otherwise]
**Rough size:** [small — hours to a day | medium — days | large — week+]
**Clarity:** [clear — can act on it | partial — needs investigation | vague — needs reproduction or design]

## Pointers

[Optional. Links to related code paths, PRs, incidents, logs, traces, prior issues. One per line.]

## Raw Notes

[Optional. Verbatim quotes, error messages, stack traces, screenshots, or supporting material. Preserve original wording and formatting.]
```

## Field Guidance

### Category definitions

| Category | When to use |
|----------|-------------|
| bug | Something behaves incorrectly — wrong output, crash, data corruption, regression |
| refactor | Code works, but the structure makes future work harder — duplication, coupling, unclear boundaries |
| tech-debt | A known shortcut or deprecation that has to be paid down — outdated dependency, missing tests, deferred migration |
| perf-internal | Internal performance problem that is not yet felt by users — slow CI, slow local build, slow background job, memory growth in a worker |

User-facing performance problems (slow page loads, laggy UI, timeouts users see) are product signals — route to `capture-signal` in the `discover` plugin.

### Severity (bugs only)

| Level | Meaning |
|-------|---------|
| blocker | Production down, data loss, security breach, or a critical flow broken for all users |
| high | Major feature broken, affects many users, or no acceptable workaround |
| medium | Noticeable defect, affects some users, workaround exists |
| low | Cosmetic, rare edge case, or minor inconvenience |

For non-bugs, severity is usually irrelevant — leave blank or mark `n/a`.

### Repro quality for bugs

A bug record without reproduction detail rots fast. Capture at least:

- **Expected behavior** — one sentence.
- **Actual behavior** — one sentence.
- **Repro steps** — numbered, specific enough that a teammate can follow them. Include environment, input values, and the command or UI path.
- **Frequency** — always, sometimes (with a rate if known), or once.

If the bug is not currently reproducible, say so explicitly and set clarity to `partial` or `vague`. Do not fabricate steps.

### Rough size calibration

Size reflects end-to-end effort including test and rollout, not just coding.

- **Small (hours to a day):** Localized fix, clear scope, low blast radius.
- **Medium (days):** Touches multiple files or modules, needs design input or broader testing.
- **Large (week+):** Crosses subsystems, requires migration, or needs coordination.

When uncertain, round up. Optimistic sizing is a more common failure mode than pessimistic.

### Clarity levels

| Level | Meaning | Signal |
|-------|---------|--------|
| clear | Problem, cause direction, and fix path are well-defined | Ready to work |
| partial | Problem is understood but cause or fix is unclear | Needs investigation before pickup |
| vague | Problem is fuzzy — can't reproduce, no clear owner, or speculative | Needs reproduction, evidence, or scoping |

### Slug naming

Derive `<slug>` from the short name: lowercase, kebab-case, 2-5 words. Prefix with category only when it aids scanning.

Examples:
- "CSV export truncates rows beyond 10k" → `csv-export-row-truncation`
- "Split UserService into smaller services" → `split-user-service`
- "Slow CI on main branch" → `slow-ci-main`

If a file with the same slug already exists, append the capture date: `<slug>-YYYY-MM-DD.md`. If still taken, add a numeric tiebreak: `<slug>-YYYY-MM-DD-2.md`.
