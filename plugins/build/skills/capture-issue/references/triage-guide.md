# Triage Guide

Elicitation, repro standards, and duplicate detection for engineering issues.

## Categorize Before Eliciting

The category drives what information to gather. Infer from the user's input first; ask only if genuinely ambiguous.

| Signal in the user's input | Likely category |
|----------------------------|-----------------|
| "broken", "crashes", "wrong output", "regression", error message, stack trace | bug |
| "this code is a mess", "hard to change", "duplicated", "god class", "tangled" | refactor |
| "deprecated", "outdated", "we skipped", "should have migrated", "missing tests" | tech-debt |
| "slow", "takes too long", "timeout", "memory grows" + internal context (CI, build, worker, job) | perf-internal |
| "slow", "laggy" + user-facing context (page load, UI, API response user sees) | **not this skill** — out of scope (this is a product signal, not an engineering issue) |

If the boundary is genuinely unclear (e.g., a slow endpoint that may or may not be user-visible), ask one question: "Is this felt by users, or only by the team?"

If the answer is still ambiguous ("both", "possibly"), default to `perf-internal` and note in Raw Notes that user-facing impact is uncertain. If the user explicitly confirms users experience it, the item is out of scope for this skill — surface that and stop.

## Elicitation Questions

Ask only what is missing. Keep it to **2–4 questions in the first round, 1–2 in follow-ups**. Stop when the category's minimum is covered.

### For bugs

Minimum: expected behavior, actual behavior, how to reproduce, how often.

1. What were you trying to do, and what happened instead?
2. Can you reproduce it? If yes, what are the steps?
3. How often does it happen — always, sometimes, once?
4. Where did it happen — environment, version, which users?

### For refactor / tech-debt

Minimum: what the current shape is, what work it slows.

1. What part of the code is the problem?
2. What makes it hard to change — coupling, duplication, unclear boundaries, missing tests, something else?
3. What upcoming work does this block or slow?

### For perf-internal

Minimum: baseline numbers, where it's felt, trend.

1. What is slow, and how slow is it today (rough numbers)?
2. Who feels it — which pipeline, job, or developer workflow?
3. Is it getting worse, stable, or new?

## Repro Quality Bar for Bugs

A bug without repro detail rots. Before writing the record, confirm at least one of:

- **Deterministic repro steps** — numbered, with environment and inputs.
- **A recorded instance** — log excerpt, stack trace, traceID, or incident link.
- **An explicit acknowledgment that it is not currently reproducible** — mark clarity `partial` or `vague`, and record what is known.

Do not invent repro steps. "I think it happens when..." goes in Raw Notes as a hypothesis, not in the repro section.

## Duplicate Detection

### What to check

| Location | What to look for |
|----------|-----------------|
| `.product/build/issues/issues.md` | Open or resolved issues with the same symptom or code area |
| `.product/build/issues/*.md` | Per-issue records for semantic duplicates |

### How to check

1. Read `issues.md` if it exists. If it does not but `.product/build/issues/` contains per-issue records, read those instead. If neither exists, skip — this is the first issue.
2. Compare by **symptom and code area**, not surface wording. "CSV export cuts off" and "exported CSV is missing rows" are the same bug.
3. For refactor/tech-debt items, compare by **affected module** — two entries against the same module often signal a single larger issue.

### When overlap is found

- **Exact duplicate:** Same symptom, same scope → surface the existing issue and ask whether to merge (add evidence to the existing record) or keep separate.
- **Partial overlap:** Related but different scope → note the relationship in the new record's Pointers section.
- **Resolved duplicate:** Existing record is resolved → surface it and ask whether this is a regression (new record, link to the prior one) or the same bug returning (reopen the prior record).

## Batch Capture

When the user provides multiple issues at once (e.g., "here are 5 things from the bug bash"):

1. Process each through the full flow.
2. Write one record per issue.
3. Append all to `issues.md` in one update.
4. Present a summary table at the end:

```markdown
| # | ID | Category | Summary | Severity | Size | Clarity |
|---|-----|----------|---------|----------|------|---------|
```

5. Ask if any need correction before finalizing.

Run the full duplicate check on each item — duplicates within a single batch are common, especially from retros and bug bashes.
