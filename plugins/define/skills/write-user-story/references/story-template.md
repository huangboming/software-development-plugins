# Story Template

Template for a single user story and field guidance. Read during SKILL.md Step 4. The quality check runs in two passes: a first pass on the draft (before writing to disk) to catch violations early, and a second pass on the written file as the final self-review.

## Template

```markdown
---
Status: ready
Source PRD: .product/define/specs/<feature>/v<N>.md
Source slice: .product/define/slices/<slug>.md   # omit if not applicable
Size: <S | M | L | team convention | TBD>
Last updated: <YYYY-MM-DD>
---

# Story: <verb-led, user-visible title>

## Story statement

**As a** <named role — the specific user type, not "user">,
**I want** <user-observable capability, present tense>,
**So that** <concrete benefit — the job that gets done better>.

## Acceptance criteria

Happy path first, then edge cases. Each criterion is an observable behavior, independently testable.

- [ ] **Given** <context / pre-condition>, **When** <user action>, **Then** <observable outcome>.
- [ ] **Given** ... **When** ... **Then** ...
- [ ] <empty state>
- [ ] <boundary>
- [ ] <error / permission denied / service unavailable>

## Dependencies

- <Other stories that must ship first, with a link>, or `none`.

## Assumptions

- <What must be true for this story to be implementable; link to assumptions in `.product/discover/assumptions/` if any>.

## Open questions

- [ ] <Unresolved item the dev team will need answered before or during implementation>.
```

## Slug naming

Each story gets its own file under `.product/define/stories/<feature>/`. The feature directory reuses the PRD's feature name.

Story slug rules:

- Verb-led, kebab-case, no role prefix. `filter-orders-by-date` passes; `user-filters-orders` does not.
- Short — 3–6 words.
- No dates in the filename (dates go in the Last updated field).
- One capability per file. If a slug needs "and", split into two stories.

Examples:

- `.product/define/stories/weekly-report/export-current-report-to-csv.md`
- `.product/define/stories/weekly-report/filter-by-campaign.md`
- `.product/define/stories/weekly-report/share-report-by-link.md`

## Status lifecycle

| Status | Meaning |
|---|---|
| `ready` | Written and grain-checked. Ready for a developer to pick up. |
| `blocked` | A dependency or open question blocks pickup. Name the blocker in the body. |
| `in-progress` | A developer has started implementation. |
| `done` | Implementation shipped and the acceptance criteria have been verified. |
| `superseded` | Replaced by a newer story (e.g., after a PRD revision). Keep the file; mark the status. |

Do not delete superseded stories — they record what was decomposed and why the shape changed.

## Quality check

Run this check twice: once on the draft (before writing to disk) to catch violations early, and once on the written file as the final self-review. Correct violations in place before presenting to the user.

- **Role is specific.** "Paying subscriber on the team plan" passes; "user" does not. Generic roles produce generic criteria.
- **Capability is user-observable.** The user can see, hear, or feel the result. "Filter orders by date" passes; "call the orders endpoint with a date range" does not.
- **Benefit is a job, not a feature.** "So that I can build a shortlist quickly" passes; "so that I can use the filter feature" does not.
- **Acceptance criteria are in Given/When/Then.** Plain bullets drift into implementation talk; the Given/When/Then frame keeps them user-facing.
- **Each criterion is independently testable.** A tester can pass or fail the criterion without reading another criterion. If two criteria are always verified together, combine them.
- **Edge cases are named.** Happy path alone is not story-complete. Cover at least one of: empty state, boundary value, error, permission denied.
- **Dependencies are named or declared none.** Silence means "I did not consider this" — not "there are none". Write `none` explicitly when there are none.
- **Size is present.** `S/M/L`, story points, or a day-bound (`≤ 3 days`). `TBD` is acceptable only when the team has not set a convention yet — state so in the story.
- **No implementation details.** No technologies, endpoints, table names, or architectural decisions. If a detail crept in, move it to a separate implementation note or delete it.
- **Grain test passes** (see `splitting-patterns.md`): not too big (≤ ~5 days, ≤ ~7 criteria), not too small (not a technical task), vertically sliced, valuable on its own.

### The observability rewording test for acceptance criteria

Rephrase each criterion as: "A tester opens the product, performs `<action>`, and sees `<outcome>`." If the outcome is an internal system state ("the row is written to the database", "the cache is invalidated", "the event fires"), rewrite until the outcome is user-observable ("the updated value appears", "the next page load shows the new state", "a confirmation message is shown"). Internal-state criteria are tasks masquerading as acceptance criteria.

## Summary format

After writing the files, present a summary in this format:

```
Stories drafted for <feature>: <N>
- Source PRD: .product/define/specs/<feature>/v<N>.md (link block added)
- Stories:
  1. <story-slug> — <one-line capability> — size <S/M/L>
  2. <story-slug> — <one-line capability> — size <S/M/L>
  ...
- Dependencies: <count of cross-story deps, or "none">
- Blocked: <count in `blocked` status, with blockers named>, or "none"
- Folder: .product/define/stories/<feature>/

Next: engineering picks up stories in dependency order. When a story ships, update its Status to `done` and record the release link in the story file.
```

The summary is a decision record of what was decomposed, not a restatement of each story's criteria. Keep each line to one piece of information.

## Edge case playbook

Handle these conditions as described. Each entry names the trigger and the response.

If the **PRD already contains inline user stories that conflict with the derived split** (e.g., the PRD lists 3 inline stories but the split suggests 5):
  → Present both shapes. Ask which to proceed with. If the user wants the inline set, formalize those and run the grain test on each — do not silently invent new stories. If the user wants the derived set, note in the summary that the PRD's inline stories have been superseded; offer to update the PRD in a follow-up `write-prd` pass rather than editing the PRD silently here.

If a **candidate story names a non-user stakeholder role** (e.g., "As an admin", "As a support agent", "As the billing system"):
  → Admin and support-agent stories are fine — they are still human users with a job. Use their specific role name. System roles ("as the billing system") are not stories — they describe integrations. Convert to a user-facing story ("as a customer, I want my subscription to renew automatically…") or move to an implementation note.

If a **candidate is a spike** (investigation work with no shippable outcome, e.g., "spike: evaluate payment providers"):
  → Do not write it as a user story. Spikes have no user-observable outcome and fail the grain test. Record them in the PRD's Open Questions or in a separate implementation plan; they do not live in `.product/define/stories/`.

If a **cross-cutting concern** (logging, auth, analytics, i18n) appears as a candidate:
  → Ask whether it delivers a user-visible capability. If yes (e.g., "user can sign in with SSO"), keep it as a story. If no (e.g., "add structured logging to the orders endpoint"), it is a task — move it out of the backlog. Cross-cutting tasks are tracked as engineering work, not product stories.

If **stories already exist** for the same feature:
  → Read the existing folder first. Ask whether to:
  - **Add** — new stories alongside existing ones (e.g., a v2 PRD added scope). Reuse the existing folder; new stories get `ready`.
  - **Supersede** — rewrite stories after a PRD revision changed the shape. For each replaced story, set its Status to `superseded` and write the new story at a new slug if the capability changed, or append `-v2` to the slug if the story still represents the same capability. Never edit a `done` or `in-progress` story in place — the history of what was built matters.

If the **slice is the only input** (no PRD has been drafted):
  → Write stories but set `Source PRD: none — slice-only`. State in each story's Assumptions that the PRD has not been drafted and the stories may churn once `write-prd` runs. Offer to route the user to `write-prd` first if they want stable stories rather than preliminary ones.

If the **PRD has no acceptance criteria yet**:
  → The PRD is incomplete. Ask whether to route back to `write-prd` to fill acceptance criteria first, or proceed by deriving criteria from the PRD's user-flow descriptions. If the user proceeds, note in each story's Open Questions that the acceptance criteria were derived, not authored by the PRD — and surface the derived criteria to the user for confirmation before writing.

If the **size estimate is contested** (eng thinks L, PM thinks M):
  → Write both. Record `Size: M (PM) / L (eng)` with a one-sentence note on the disagreement. A single averaged size hides the disagreement without resolving it; sizing conversations often reveal hidden requirements.

If **every candidate story requires another to ship first** (a fully serial chain):
  → The feature is not splittable by the patterns chosen. Re-read `splitting-patterns.md` and try a different split axis (e.g., switch from CRUD split to happy-path-vs-edge-case split). If no split produces independently shippable stories, the feature may genuinely be one story — write it as one with a clear single capability, rather than forcing an artificial split.
