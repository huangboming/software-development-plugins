# Splitting Patterns

Patterns for splitting a feature into well-grained user stories, grain calibration, and anti-patterns. Read in SKILL.md Step 2 (splitting) and Step 3 (grain check).

## The splitting patterns catalog

Pick the pattern that best matches how the feature varies along user-visible axes. More than one may apply; combine them when the feature is multi-dimensional.

### By workflow step

Split along the stages of a user's end-to-end journey. Each stage ships independently and delivers value on its own, even before later stages land.

- Feature: "Onboarding"
  - Split: `complete-profile-details` → `verify-email` → `choose-initial-workspace` → `invite-first-teammate`.
  - Test: can a user benefit from step 1 even if steps 2–4 never ship? If yes, the split is valid.

### By CRUD operation

Split a data-object feature along create / read / update / delete lines. Most products need read first, then create, then update, then delete last.

- Feature: "Manage saved filters"
  - Split: `view-saved-filters` → `create-a-saved-filter` → `rename-a-saved-filter` → `delete-a-saved-filter`.
  - Test: does each operation deliver on its own? Read alone is valuable (even if the filters were seeded); delete-only would not be.

### By user role

Split along distinct user types whose jobs differ. Each role's slice ships independently.

- Feature: "Team billing"
  - Split: `owner-views-billing-history` → `owner-updates-payment-method` → `member-sees-plan-limits` → `admin-exports-invoices`.

### By happy path vs edge cases

Ship the happy path first; ship edge cases as their own stories.

- Feature: "File upload"
  - Split: `upload-single-supported-file` (happy path) → `show-error-on-unsupported-type` → `resume-interrupted-upload` → `enforce-per-user-quota`.
  - Test: does the happy path deliver a coherent slice on its own? If yes, edges can land later.

### By data type or variation

Split along the kinds of data the feature handles. Start with the most common type; add rarer types as their own stories.

- Feature: "Import from external source"
  - Split: `import-from-csv` → `import-from-google-sheets` → `import-from-api`.

### By platform or surface

Split along the surfaces where the feature runs (web, mobile web, native app, email). Each platform is often its own integration effort with its own acceptance criteria.

- Feature: "Notifications"
  - Split: `receive-notification-in-web-inbox` → `receive-notification-by-email` → `receive-notification-in-mobile-app`.

### By rule variation

Split along the business-rule variations the feature supports — tiers, permission levels, pricing plans. Start with the most common rule; layer in variants as separate stories.

- Feature: "Sharing links"
  - Split: `share-view-only-link` → `share-edit-link-requires-login` → `share-password-protected-link` → `share-expiring-link`.

### When to combine patterns

A feature that varies along two axes (e.g., CRUD × role) can produce a large matrix. Do not write every cell — pick the cells that deliver real user value in isolation, and defer the rest to Not-now or to later stories. The goal is a shippable sequence, not a completeness proof.

## The grain-calibration table

Calibrate candidates against this table before writing. Most splits need at least one pass of correction.

| Grain | Looks like | Rewrite to |
|---|---|---|
| **Task** (too small) | "Add a `user_filters` table migration" | Fold into a user-facing story: `create-a-saved-filter`. The migration is implementation. |
| **Task** (too small) | "Wire up `GET /api/reports` endpoint" | Fold into: `view-weekly-report-list`. The endpoint is implementation. |
| **Task** (too small) | "Add loading spinner to reports page" | Fold into an acceptance criterion of an existing story ("when the report is loading, a spinner is shown"). Not a story on its own. |
| **Story** (right-sized) | "As a marketing manager, I want to filter orders by campaign, so that I can compare campaign performance quickly" | Keep. Ships end-to-end; one user, one job, testable. |
| **Story** (right-sized) | "As an owner, I want to invite a teammate by email, so that I can set up the team without sharing credentials" | Keep. Vertical slice: form + send + link + landing. |
| **Epic** (too big) | "As a user, I want to manage my profile" | Split by CRUD: `view-profile`, `edit-name-and-avatar`, `change-password`, `delete-account`. |
| **Epic** (too big) | "As a user, I want reporting" | Split by workflow step or data type; "reporting" is a surface, not a job. |
| **Epic** (too big) | "As a user, I want full-text search" | Split by data type (posts, then comments, then files) or by rule (exact match first, then fuzzy). |

### Size heuristics

- ≤ ~5 engineering days (excluding review/QA) for an experienced dev — target range per story.
- ≤ ~7 Given/When/Then acceptance criteria per story — more than this and a split is usually hiding.
- ≤ ~8 candidate stories per feature — exceeding this ceiling means either the PRD is too large (split the feature via `write-prd`) or the split is over-decomposed (consolidate).
- If a story reads as two sentences joined by "and", split at the "and".
- If the acceptance criteria include more than one user role, split by role.

## Anti-patterns catalog

Reject these shapes. Each is a common way splits go wrong.

### Horizontal slice (technical-layer split)

The feature is split along backend / API / frontend / infra lines. None of the resulting slices deliver user value on its own.

- Symptom: `build-reports-database`, `build-reports-api`, `build-reports-ui`.
- Why it fails: shipping the database alone changes nothing a user can see. None of these pass the "valuable on its own" check.
- Fix: split vertically instead — pick a single user-facing capability and ship the backend + API + UI for that capability as one story. Other capabilities become their own stories.

### Task dressed as a story

A technical action wrapped in As-a/I-want/So-that language, but the "capability" is not observable to the user.

- Symptom: "As a developer, I want to add structured logging to the orders service, so that we can debug issues."
- Why it fails: the beneficiary is the developer, not the product's user; the outcome is internal.
- Fix: move it out of the backlog — it is implementation work. Or, if the user-visible effect is real, rewrite from the user's perspective ("As a customer, I want accurate order history, so that I can verify past purchases" — with logging as one implementation detail).

### Epic dressed as a story

The story is phrased at story grain but the acceptance criteria reveal an epic underneath.

- Symptom: "As a user, I want notifications, so that I stay informed" — with 18 acceptance criteria covering email, mobile push, in-app, preferences, digests, and unsubscribe.
- Why it fails: 18 criteria cannot be tested independently or shipped in ~5 days. The one-sentence story hides the scope.
- Fix: split by workflow step (receive → configure → unsubscribe), platform (web → email → mobile), or rule variation (single-item → digest).

### Spike in story clothing

An investigation task framed as a story. There is no shippable outcome — only a document or a decision.

- Symptom: "As a team, we want to evaluate payment providers, so that we pick the right one."
- Why it fails: no user-observable outcome; the artifact is a research doc.
- Fix: do not write as a story. Record in the PRD's Open Questions, a design doc, or the team's engineering plan.

### "As a user" story

The role is generic, so the acceptance criteria are generic.

- Symptom: "As a user, I want to see my data, so that I can use the product."
- Why it fails: `user` hides the fact that different user types have different jobs; the criteria drift into vague "the system shows the data".
- Fix: name the specific role — "paying subscriber on the team plan", "admin", "support agent on a shared inbox".

### And-joined story

The story statement contains an "and" joining two capabilities.

- Symptom: "As a manager, I want to filter orders by date and export the filtered list, so that I can …"
- Slug symptom: if you cannot form a slug without the word "and", the story statement also contains two capabilities — return to the story statement and split there first.
- Why it fails: two capabilities means two sets of acceptance criteria and two deployment moments. Each can ship independently.
- Fix: split at the "and". `filter-orders-by-date` and `export-filtered-orders-to-csv` are two stories; the second can depend on the first.

### Implementation-detail acceptance criterion

The story is correctly shaped but an acceptance criterion leaks internal state.

- Symptom: "Then the row is inserted into the `orders` table."
- Why it fails: the user cannot observe a database row. A tester cannot verify this through the product surface.
- Fix: rewrite to the observable effect — "Then the new order appears at the top of the order list within 2 seconds."
