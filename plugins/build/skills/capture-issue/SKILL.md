---
name: capture-issue
description: "Capture an engineering issue — bug, refactor, tech-debt item, or internal performance problem — and write it to .product/build/issues/. Not for feature ideas, user observations, or user-facing perf problems. Triggers: 'capture a bug', 'file a bug', 'report a bug', 'I found a bug', 'log tech debt', 'mark this as tech debt', 'track this refactor', 'this needs a refactor', 'log an internal perf problem', 'CI is slow', 'triage this bug', '/capture-issue'."
---

# Capture Issue

Capture an engineering issue and write it to `.product/build/issues/<slug>.md`, then update the rolling list at `.product/build/issues/issues.md` so it is discoverable.

Scope is engineering work: **bugs, refactor items, tech-debt items, and internal performance problems**. User-facing performance problems and feature ideas are out of scope — surface them to the user as such rather than capturing them here.

## References

- [references/triage-guide.md](references/triage-guide.md) — Category routing, elicitation questions per category, repro quality bar for bugs, duplicate detection, batch handling. Read at the start of every capture.
- [references/issue-template.md](references/issue-template.md) — Per-issue record template and field guidance (category definitions, severity calibration, size heuristics, slug naming). Read before writing a record.
- [references/issue-list-template.md](references/issue-list-template.md) — Rolling list template and status lifecycle. Read the first time `issues.md` is created.

## Process

Four steps: categorize, elicit, write, confirm.

### 1. Categorize

Read [triage-guide.md](references/triage-guide.md) and classify the input as `bug`, `refactor`, `tech-debt`, or `perf-internal`.

If the input is a user-facing problem or a feature idea, stop and tell the user it is out of scope for this skill — do not capture it here. Surface the decision explicitly.

For batch inputs (multiple issues at once), categorize each individually and process each through steps 2–4.

### 2. Elicit

Follow the category-specific question sets in `triage-guide.md`.

**Termination rule.** Stop eliciting when (a) the category minimum is covered AND (b) clarity can be assessed as at least `partial`. If the user's input is only enough for `vague`, write the record at `vague` clarity rather than asking another round. Use 1–2 follow-up questions only when a single missing piece would lift clarity from `vague` to `partial` or better.

For bugs, enforce the repro quality bar: deterministic steps, a recorded instance, or an explicit note that it is not currently reproducible. Do not fabricate repro steps.

Check for duplicates against `.product/build/issues/issues.md` and per-issue records. Compare by symptom and code area, not surface wording. If a duplicate is found, surface it before writing.

For batch captures, include records written earlier in this session in the dedup check for subsequent issues — duplicates within one batch are common.

### 3. Write

Read `issue-template.md` for the record template and field guidance.

1. Create `.product/build/issues/` if it does not exist.
2. Write the per-issue record at `.product/build/issues/<slug>.md`.
3. Update `.product/build/issues/issues.md`:
   - If it does not exist, read `issue-list-template.md` and create it.
   - Add the new issue as a row in the Open table. Update `Last updated` per the template's usage notes.

### 4. Confirm

Present a summary and ask for corrections. Files are already written — frame the prompt honestly.

- If the user confirms → done.
- If the user corrects → overwrite the record and update `issues.md` in place, then re-present the updated summary. Do not re-run elicitation unless the category changed.

For non-bug categories (refactor, tech-debt, perf-internal), use `severity: n/a`.

**Example (bug):**

```
Written: **CSV export row truncation** (.product/build/issues/csv-export-row-truncation.md)

- Category: bug
- Summary: CSV exports silently drop rows beyond 10,000.
- Severity: high (affects enterprise exports)
- Size: small
- Clarity: clear — deterministic repro with 15k-row dataset

Added to issues.md. Any corrections? I'll overwrite if so.
```

**Example (tech-debt):**

```
Written: **auth middleware on deprecated jwt lib** (.product/build/issues/auth-deprecated-jwt.md)

- Category: tech-debt
- Summary: Auth middleware uses jsonwebtoken v7, deprecated since 2024.
- Severity: n/a
- Size: medium
- Clarity: clear

Added to issues.md. Any corrections? I'll overwrite if so.
```

For batch captures, present the summary table defined in `triage-guide.md` after all items are written.

## Edge Cases

If the user describes a **solution instead of a problem** ("we need to add a cache here"):
  → Ask what the underlying problem is. Capture the problem in Summary and Details; put the proposed solution in Raw Notes.

If the user provides a **mix of engineering issues and product signals**:
  → Capture engineering items here. Surface the product signals and feature ideas back to the user as out of scope. Make the split explicit so the user sees which items went where.

For other cases (not-reproducible bugs, "just capture it" requests, resolved-issue regressions, slug collisions, semantic dedup), see `triage-guide.md` and `issue-template.md`.

## Gotchas

- **User-facing perf is a signal, not an issue** — if users feel the slowness, surface it as a product signal (out of scope here). `perf-internal` covers only team-felt problems: CI, build, background jobs, worker memory.
- **Solutions disguised as issues** — "refactor to use strategy pattern" is a solution; the problem is whatever pain the current shape causes. Capture the pain; put the proposed fix in Raw Notes.
