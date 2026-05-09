---
name: summarize-git
description: Generate a daily, weekly, or monthly git activity summary across one or more repos. Produces a markdown file with commit details, narrative synthesis, and lines-of-code stats. Use when the user asks for a "daily summary", "weekly summary", "monthly summary", "monthly report", "what did I do today/this week/this month", "git summary", or any request to summarize their work over a period. Triggers on /summarize-git.
---

Generate a markdown summary of the user's git activity for a given period (daily, weekly, or monthly), across one or more repos.

## Workflow

1. Ask the user which repos to include if not specified. Default to the current repo.
2. Determine the period. If the user says "today" or "daily" → daily. "This week" or "weekly" → weekly. "This month" or "monthly" → monthly. If ambiguous, ask.
3. Run the stats script to gather raw data:
   ```bash
   uv run --script ${CLAUDE_PLUGIN_ROOT}/skills/summarize-git/scripts/git_stats.py --period {daily|weekly|monthly} [--date DATE] [path ...]
   ```
   - `--period`: required — `daily`, `weekly`, or `monthly`.
   - `--date`: optional — `YYYY-MM-DD` for daily/weekly, `YYYY-MM` for monthly. Omit to default to the current period.
   - `path`: one or more repo paths. Omit to default to the current directory.
   - The script auto-detects the git user per repo from `git config`.
   - Output is JSON with `period`, `start_date`, `end_date`, `repos[]`, and `total_loc` fields.

4. Parse the JSON and generate a markdown file following the appropriate output format below.

5. Write the file to `.hand-offs/summaries/{period}-{date}.md` in the current directory (create `.hand-offs/summaries/` if needed):
   - Daily: `.hand-offs/summaries/daily-YYYY-MM-DD.md`
   - Weekly: `.hand-offs/summaries/weekly-YYYY-MM-DD.md` (using the Monday date)
   - Monthly: `.hand-offs/summaries/monthly-YYYY-MM.md`

## Output Format — Daily

```markdown
# Daily Summary: {YYYY-MM-DD}

**Repos:** {repo1}, {repo2}, ...

## Repo: {repo_name}

### Changes

#### Features
- {commit message} (`hash`)

#### Fixes
- ...

(Omit empty sections. No narrative synthesis needed — just list commits grouped by type.)

### Lines of Code

| Metric | Lines |
|--------|------:|
| Added | +{added} |
| Removed | -{removed} |
| Net | {total} |
```

## Output Format — Weekly

```markdown
# Weekly Summary: {start_date} — {end_date}

**Period:** {YYYY-MM-DD} — {YYYY-MM-DD}
**Repos:** {repo1}, {repo2}, ...

## Summary

(2-4 bullet points synthesizing the week's key accomplishments across all repos.)

## Repo: {repo_name}

### Highlights

(1-2 sentences on key accomplishments in this repo.)

### Changes

#### Features
- {one-line description synthesized from related commits} (`hash1`, `hash2`, ...)

#### Fixes
- ...

(Omit empty sections. Map commit types: feat→Features, fix→Fixes, refactor→Refactors,
perf→Performance, docs→Documentation, test→Tests, style/chore/ci/build/revert/other→Other.)

### Lines of Code

| Metric | Lines |
|--------|------:|
| Added | +{added} |
| Removed | -{removed} |
| Net | {total} |
```

## Output Format — Monthly

```markdown
# Monthly Summary: {YYYY-MM}

**Period:** {YYYY-MM-01} — {YYYY-MM-last_day}
**Repos:** {repo1}, {repo2}, ...

## Summary

(Write a concise narrative overview of the month's work. Synthesize the commits into
coherent themes/accomplishments — do NOT just restate commit messages. Group related
changes into bullet points that describe what was achieved at a higher level.)

- Built X feature covering A, B, and C
- Refactored Y module to improve Z
- Fixed issues with ...
- Improved test coverage for ...

## Repo: {repo_name}

### Highlights

(2-4 sentence narrative of key accomplishments in this repo.)

### Changes

#### Features
- {one-line description synthesized from related commits} (`hash1`, `hash2`, ...)

#### Fixes
- ...

#### Refactors
- ...

(Omit empty sections. Map commit types: feat→Features, fix→Fixes, refactor→Refactors,
perf→Performance, docs→Documentation, test→Tests, style/chore/ci/build/revert/other→Other.)

### Lines of Code

| Metric | Lines |
|--------|------:|
| Added | +{added} |
| Removed | -{removed} |
| Net | {total} |

(Repeat "## Repo: ..." section for each repo.)

## Total Lines of Code

| Metric | Lines |
|--------|------:|
| Added | +{total_added} |
| Removed | -{total_removed} |
| Net | {total_net} |
```

## Rules

- **Daily**: List commits directly grouped by type. No narrative synthesis — daily output is a simple log.
- **Weekly**: Light synthesis — group closely related commits into single bullets, write short highlights per repo.
- **Monthly**: Full synthesis — group related commits into higher-level accomplishments. For example, 5 commits about "add BIP-39 mnemonic", "add HD derivation", "add wallet types" become one bullet: "Built full HD wallet stack with BIP-39 mnemonics, key derivation, and wallet abstractions".
- Within each type section, order chronologically (oldest first).
- Omit empty type sections entirely.
- Prefix net LoC with `+` if positive, `-` if negative, no prefix if zero.
- Include the total LoC table only when there are multiple repos.
