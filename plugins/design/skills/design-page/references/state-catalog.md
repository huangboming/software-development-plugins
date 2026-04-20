# State Catalog

The full catalog of states a page region can be in, with a rule for when each applies. Use this at the states step of the workflow — walk every data-driven region of the page and decide, per state, *design it* / *not applicable with reason*.

LLMs default to designing only the happy path. Real pages spend 30-50% of user time in non-happy states (loading, empty, error, partial, offline). A design that omits them is a design in name only.

## Contents

1. [Mandatory baseline states](#mandatory-baseline-states)
2. [Conditional states](#conditional-states)
3. [State transitions to specify](#state-transitions-to-specify)
4. [Quick include/exclude matrix by archetype](#quick-includeexclude-matrix-by-archetype)

## Mandatory baseline states

These apply to nearly every data-driven region. If a state is excluded, justify it in the artifact's Open Questions section.

| State | Applies when | What to design | Common mistake |
|---|---|---|---|
| **Loading** | Any async data fetch. | Skeleton for structural content; spinner for actions; progress bar for known-duration fetches. Announce via `aria-busy`. | Blank region during fetch (layout shift) or indistinguishable spinner-everywhere. |
| **Empty — first-run** | User has no data yet because they're new. | Onboarding CTA: explain what would be here + one-click path to create the first record. | Generic "No data" text with no next action. |
| **Empty — filtered** | User's filter/search returned zero. | "No results match your filters" + "Clear filters" action. Distinct from first-run. | Reusing the first-run empty state (user is confused — "wait, I had data"). |
| **Error — fetch failed** | Network or server returned an error during load. | Inline error with specific message + retry action. Show partial data if any loaded. | Full-page error that wipes out other successful regions. |
| **Success — after action** | User completed an action (save, submit, delete). | Confirmation (toast, inline, or redirect). Announce via `aria-live`. Non-blocking. | No feedback at all, or blocking modal the user has to dismiss. |
| **Disabled** | User cannot interact with the control in the current context (not authed, not selected, not allowed). | Visually demoted state; tooltip or inline message on hover/focus explaining why. | Looks clickable but does nothing on click (breaks trust). |

## Conditional states

These apply in specific contexts. Per region, decide *include* / *exclude with reason*.

| State | Applies when | What to design | Common mistake |
|---|---|---|---|
| **Partial** | Some data loaded, some failed or still loading. | Render what's available; inline indicator for the failed/pending parts. | "All or nothing" approach that waits for slowest fetch. |
| **Permission-denied** | User lacks role/plan/scope access. | Locked affordance, specific explanation, path to request access or upgrade. | Hiding the feature entirely so user discovers only by accident. |
| **Offline** | Client has no connectivity. | Cached last-known data with staleness indicator + retry when online. | Full-page "No internet" wall hiding cached content the user could read. |
| **Rate-limited / throttled** | User or IP hit a limit. | Tell user when they can retry (countdown if short; date if long); do not return a generic 429. | Silent failure or generic "try again later." |
| **Read-only** | User can view but cannot edit (lower role, archived record, locked account). | Inputs appear as static text; edit affordances hidden; banner explains why. | Edit controls present but failing on submit. |
| **Stale / outdated** | Data was loaded a while ago; fresher data exists. | Staleness indicator + refresh action. | No indication, so user acts on outdated info. |
| **Saving / submitting** | An action is in flight. | Disable the submit affordance; show spinner; prevent double-submit. | Button stays active, user clicks twice, duplicate request. |
| **Save failed** | Submit rolled back. | Preserve user input; show specific error near the action; support retry. | Lose user input or show generic "something went wrong." |
| **Conflict** | Another client saved a conflicting version (stale write, two tabs, collaborative editing). | Surface the conflict, show both versions, let user choose or merge. | Silent overwrite or silent drop. |
| **Unsaved changes** | User has a dirty form and tries to navigate away. | Warn before unload; offer save. | Lose data silently. |
| **JS disabled** | Progressive enhancement / accessibility fallback. | Render core content + primary action server-side; hide JS-only affordances. | Blank page without JS. |
| **Slow network** | Fetch takes longer than expected. | After ~2s, show loading more explicitly; after ~5s, allow cancel. | Spinner-forever with no escape. |
| **Onboarding incomplete** | User left onboarding mid-flow and returned. | Resume affordance with state restored, or "start over" option. | Dump user back to dashboard as if nothing happened. |
| **Notification / banner** | System-level message (maintenance, new version, plan warning). | Dismissible banner at top; never covers primary content. | Modal that blocks the page on entry. |

## State transitions to specify

This section is a companion checklist to `workflows/design-page.md` § Step 7 — use it while enumerating states per region, not as standalone reference material. Beyond designing each state, specify how the user moves between them. These transitions are where most bugs live.

| Transition | Specify |
|---|---|
| Loading → populated | Animation or instant swap? Skeleton height matches populated content to prevent layout shift? |
| Loading → error | Retry in place, or redirect to error page? |
| Populated → empty (after delete all) | Show empty state or stay on "just deleted" confirmation? |
| Empty → populated (user creates first item) | Transition instantly or animate? Where is focus? |
| Form valid → submitting | Disable submit button; retain all input values in case of error. |
| Submitting → success | Redirect or inline? If inline, where does focus move? |
| Submitting → error | Preserve all input; focus to error message; announce via `aria-live`. |
| Any state → offline | Preserve cached data; show staleness indicator; reconnect resumes live state. |
| Permission revoked mid-session | What happens if user's access is removed while on the page? (Next action fails — handle gracefully.) |

## Quick include/exclude matrix by archetype

Default mandatory states per archetype. `✅` = design this state; `—` = usually not applicable; `partial` = depends on whether the page has this affordance.

| State | Landing | Dashboard | Form | List+detail | Article | Wizard | Settings | Empty/error |
|---|---|---|---|---|---|---|---|---|
| Loading | partial | ✅ | ✅ | ✅ | partial | ✅ | ✅ | — |
| Empty — first-run | — | ✅ | — | ✅ | — | — | partial | ✅ |
| Empty — filtered | — | partial | — | ✅ | — | — | partial | ✅ |
| Error — fetch failed | — | ✅ | ✅ | ✅ | partial | ✅ | ✅ | ✅ |
| Success — after action | partial | ✅ | ✅ | ✅ | partial | ✅ | ✅ | — |
| Disabled | partial | ✅ | ✅ | ✅ | — | ✅ | ✅ | — |
| Partial | — | ✅ | — | ✅ | — | partial | partial | — |
| Permission-denied | — | ✅ | partial | ✅ | partial | partial | ✅ | ✅ |
| Offline | partial | ✅ | partial | ✅ | partial | partial | partial | ✅ |
| Rate-limited | — | partial | ✅ | partial | — | partial | — | ✅ |
| Read-only | — | partial | partial | ✅ | — | — | ✅ | — |
| Saving / submitting | — | partial | ✅ | partial | — | ✅ | ✅ | — |
| Save failed | — | partial | ✅ | partial | — | ✅ | ✅ | — |
| Conflict | — | partial | ✅ | partial | — | partial | ✅ | — |
| Unsaved changes | — | — | ✅ | partial | — | ✅ | ✅ | — |
| JS disabled | ✅ | — | partial | partial | ✅ | — | — | ✅ |
| Slow network | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — |

Always justify excluded states in Open Questions so a reviewer can challenge the call.

**Precedence when sources conflict.** If the archetype matrix in `page-archetype-patterns.md` does not name a state as mandatory but the Mandatory baseline table above marks it `must`, the Mandatory baseline wins — design the state. The archetype matrix adds conditional states specific to that archetype; it does not override the baseline.
