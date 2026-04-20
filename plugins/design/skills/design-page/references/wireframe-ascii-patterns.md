# ASCII Wireframe Patterns

Low-fidelity ASCII wireframe templates per archetype, plus conventions for drafting new ones. Use these at the wireframe step of the workflow — paste the archetype pattern and adapt to the page's specific above-the-fold ranking and component composition.

Page-design artifacts live in Markdown and cannot embed images. ASCII wireframes are the practical substitute: low-fi enough to iterate fast, structured enough for a reviewer to spot problems, and legible to both humans and future agents that render the artifact.

## Contents

1. [Conventions](#conventions)
2. [Landing](#landing)
3. [Dashboard](#dashboard)
4. [Form](#form)
5. [List + detail](#list--detail)
6. [Article](#article)
7. [Wizard](#wizard)
8. [Settings](#settings)
9. [Empty / error](#empty--error)
10. [Mobile wireframe pattern](#mobile-wireframe-pattern)

## Conventions

A consistent notation makes wireframes reviewable at a glance.

| Element | Notation | Example |
|---|---|---|
| Frame | `+----+` with `|` edges | (encloses the viewport) |
| Section | Dotted or dashed inner divider | `+------+` / `:      :` |
| Text block | `~~~~~` or real words | `~~~~~~~~~~~~~~` for lorem |
| Heading | `==== Heading ====` | `=== Product Name ===` |
| Image or media | `[ IMG ]` | `[ hero video ]` |
| Button (primary) | `[ Label ]` | `[ Sign up ]` |
| Button (secondary) | `( Label )` | `( Learn more )` |
| Input field | `[............]` | `[email@...........]` |
| Dropdown | `[ Label ▾ ]` | `[ All regions ▾ ]` |
| Icon | `(i)` or `<+>` | `<+>` for add, `(x)` for close |
| State marker | `{state}` | `{loading}`, `{empty}` |
| Annotation | `// note` at end of line | `[ Submit ]  // disabled when empty` |

State markers should appear wherever the state matters. Instead of one wireframe per state, annotate the region with possible states inline — the artifact has separate state catalogs for detail.

Use monospaced fenced blocks (` ```ascii ` or plain) so indentation and alignment are preserved.

**Do not aim for pixel perfection.** The goal is hierarchy and component inventory. If you find yourself pixel-tweaking, you are doing visual design — that belongs in the design system.

## Landing

Desktop default (top of page, above-the-fold). Adapt text and visual ranking to the specific page.

```
+--------------------------------------------------------------+
|  === Logo ===     Nav 1   Nav 2   Nav 3           ( Sign in ) |
+--------------------------------------------------------------+
|                                                                |
|   ==== One-sentence value proposition ====                     |
|                                                                |
|   Supporting one-liner that answers "for whom" / "so what"     |
|                                                                |
|   [ Primary CTA ]   ( Secondary CTA )                          |
|                                                                |
|   +---------------------------+                                |
|   |                           |                                |
|   |      [ Product visual ]   |                                |
|   |                           |                                |
|   +---------------------------+                                |
|                                                                |
|   -- Trusted by -- [logo] [logo] [logo] [logo] [logo]          |
+--------------------------------------------------------------+
|  (scroll: features, social proof, FAQ, footer)                 |
+--------------------------------------------------------------+
```

Key ranking decisions to annotate: which element is the h1, where the primary CTA lives on mobile (often sticky bottom), whether supporting visual is a video or static image.

## Dashboard

Desktop default. Left side nav + top utility nav + central content grid.

```
+--------------------------------------------------------------+
| === App ===            [ Search / ]      (i) (bell) [avatar]   |
+--------+-----------------------------------------------------+
|        |   === Welcome back, <name> ===                        |
| Home   |                                                       |
| Proj.  |   +----------------+  +----------------+  +---------+|
| Inbox  |   | Metric A       |  | Metric B       |  | MetricC ||
| Team   |   |   42           |  |   87%          |  |   3.2k  ||
| Set.   |   |   {loading}    |  |   {loading}    |  |         ||
|        |   +----------------+  +----------------+  +---------+|
|        |                                                       |
|        |   === Recent activity ===                             |
|        |                                                       |
|        |   • Item 1  ................................ 2h ago  |
|        |   • Item 2  ................................ 5h ago  |
|        |   • Item 3  ................................ 1d ago  |
|        |                          ( See all activity )         |
|        |   {empty: "No activity yet — create your first X"}    |
+--------+-----------------------------------------------------+
```

States to annotate: first-run empty, partial-data degraded, permission-subset (some widgets locked).

## Form

Vertical stack; single-column is the default for readability.

```
+--------------------------------------------------------------+
| === Request a demo ===                                         |
| Takes about 2 minutes. We'll follow up within one business day.|
+--------------------------------------------------------------+
|                                                                |
|  Full name *                                                   |
|  [............................................]               |
|                                                                |
|  Work email *                                                  |
|  [............................................]               |
|  {validation: inline on blur}                                  |
|                                                                |
|  Company size                                                  |
|  [ 1-10 ▾ ]                                                    |
|                                                                |
|  What brings you to us?                                        |
|  [                                                      ]     |
|  [                                                      ]     |
|                                                                |
|  [ Submit ]    // disabled when required fields empty          |
|                // sticky on mobile                             |
|                                                                |
|  Your info stays private. See our privacy policy.              |
+--------------------------------------------------------------+
```

States to annotate: submitting (spinner, disabled), server error (preserve input), success (redirect or inline replacement).

## List + detail

Two-pane: list on left, detail on right (desktop). Split-view is the default; modal or navigation are alternatives.

```
+--------------------------------------------------------------+
| [ Search / ]   Sort [ Recent ▾ ]   Filter [ All ▾ ]   [ + New ]|
+---------------------------+----------------------------------+
|  • Item 1 — summary       |  === Item 1 ===                   |
|  • Item 2 — summary        |                                   |
|  • Item 3 — summary        |  Field A: ~~~~~~~~~~~~            |
|  • Item 4 — summary        |  Field B: ~~~~~~~~~~~~            |
|  • Item 5 — summary        |                                   |
|  • Item 6 — summary        |  ~~~~~~~~~~~~~~~~~~~~~~~~~~       |
|   ...                      |  ~~~~~~~~~~~~~~~~~~~~~~~~~~       |
|   {empty-filtered}         |                                   |
|   ( Clear filters )        |  [ Edit ]  ( Archive )            |
|                            |   {loading | not-found | denied}  |
|   [ Load more ]            |                                   |
+---------------------------+----------------------------------+
```

States to annotate: first-run empty (create first), filtered-to-empty (clear filters), detail loading/not-found/permission-denied.

## Article

Single-column reading layout with optional right-rail TOC on wide screens.

```
+--------------------------------------------------------------+
|  === Article headline ===                                      |
|  By <author> · <date> · <N> min read                           |
|                                                                |
|  +-------------------------------+                             |
|  |                               |                             |
|  |       [ Hero image ]          |                             |
|  |                               |                             |
|  +-------------------------------+                             |
|                                                                |
|  Lede paragraph that pulls the reader in and sets up the       |
|  rest of the piece. One to three sentences, dense with        |
|  specifics.                                                    |
|                                                                |
|  == Section A ==                                               |
|  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                  |
|  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                  |
|                                                                |
|  ```code block```                                              |
|    // copy button on hover AND on focus                        |
|                                                                |
|  == Section B ==                                               |
|  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                  |
|                                                                |
|  +-- Related reading -----------+                              |
|  | • Related article 1          |                              |
|  | • Related article 2          |                              |
|  +------------------------------+                              |
+--------------------------------------------------------------+
```

On xl / 2xl: promote TOC to a right-rail sticky sidebar. On sm/md: TOC collapses to an "In this article" accordion at the top.

## Wizard

Step indicator at top; one step fully visible at a time; summary sidebar on desktop.

```
+--------------------------------------------------------------+
|  [1] Account    [2] Plan    >[3] Payment<    [4] Confirm       |
+--------------------------------------------------------------+
|                                                                |
|  === Step 3 of 4: Payment ===                                  |
|  We accept Visa, Mastercard, Amex.                             |
|                                                                |
|  Card number                                                   |
|  [............................................]               |
|                                                                |
|  Expiry           CVC                                          |
|  [ MM / YY ]     [ .... ]                                     |
|                                                                |
|  [x] Save payment method for next time                         |
|                                                                |
|  ( Back )                            [ Continue ]              |
|                                                                |
|  ---- Summary ----                                             |
|  Plan:     Pro (annual)                                        |
|  Trial:    14 days free                                        |
|  Total:    $X on <date>                                        |
+--------------------------------------------------------------+
```

States to annotate: URL reflects step (e.g., `/signup?step=3`), back preserves data, abandon mid-flow recovery.

## Settings

Left side nav + content area with grouped fields. Destructive actions at bottom only.

```
+--------------------------------------------------------------+
| === Settings ===            [ Search settings / ]              |
+---------+----------------------------------------------------+
| Account |   === Notifications ===                              |
| Notif.> |                                                      |
| Billing |   Email notifications                                |
| Team    |   [x] New messages                                   |
| Sec.    |   [x] Weekly summary                                 |
| Integr. |   [ ] Product updates                                |
|         |                                                      |
|         |   Push notifications                                 |
|         |   [x] Mentions                                       |
|         |   [ ] Assignments                                    |
|         |                                                      |
|         |   {inline save feedback | "Saved" via aria-live}    |
|         |                                                      |
|         |   ---------------------------                        |
|         |   Danger zone                                        |
|         |   ---------------------------                        |
|         |   ( Delete account )   // modal with type-to-confirm |
+---------+----------------------------------------------------+
```

States to annotate: dirty-form warn-on-navigate, permission-gated (disabled with reason), plan-gated (locked with upgrade path).

## Empty / error

Short by design. Message → context → action.

```
+--------------------------------------------------------------+
|                                                                |
|                                                                |
|                         (icon)                                 |
|                                                                |
|               === We couldn't find that page ===               |
|                                                                |
|          The link may be outdated or the page moved.           |
|                                                                |
|                  [ Go home ]   ( Search docs )                 |
|                                                                |
|                                                                |
|                  Still stuck? contact@example.com              |
+--------------------------------------------------------------+
```

States to annotate: the status code (404/403/500/503) as secondary text, not the primary message. For offline, show cached content instead of a wall where possible.

## Mobile wireframe pattern

For any archetype, also include a mobile version showing the reflow. Default width roughly 40 chars to represent a phone viewport.

```
+--------------------------------------+
| === App ===                 (≡)      |
+--------------------------------------+
|                                      |
|   ==== Value proposition ====        |
|                                      |
|   Supporting line about for-whom.    |
|                                      |
|   [ Primary CTA ]                    |
|   ( Secondary CTA )                  |
|                                      |
|   +-------------------------------+  |
|   |     [ Product visual ]        |  |
|   +-------------------------------+  |
|                                      |
|   -- Trusted by --                   |
|   [logo] [logo] [logo]               |
+--------------------------------------+
|    [ Sticky primary CTA ]            |  // sticky bottom
+--------------------------------------+
```

Annotate the reflow decisions the mobile wireframe embodies: primary CTA sticky at bottom (always reachable), nav collapsed to hamburger, logos drop from 5 to 3 with horizontal scroll, product visual moves below CTA (mobile priority is action-first, not visual-first).
