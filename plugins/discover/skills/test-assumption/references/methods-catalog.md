# Assumption Test Methods

Catalog of methods for testing a load-bearing assumption before committing to build. Read when selecting a method — pick by assumption type, sample access, and cost, in that order.

## Method Selection by Type

Primary match first. Secondary methods listed for when the primary is infeasible (no traffic, no build capacity, no participants).

| Assumption type | Primary methods | Secondary methods |
|-----------------|-----------------|-------------------|
| desirability | Fake door, smoke test, landing page | Concierge, customer-letter / concept test, data mining / cohort backcast |
| viability | Pricing probe, cohort backcast, analog teardown | Smoke test on paid tier, sales-call signal review |
| feasibility | Technical spike, expert review, analog teardown | Prototype-in-one-stack |
| usability | Interactive prototype test, concierge | Expert / heuristic review |

If the assumption spans two types (e.g., desirability *and* usability), split it — each sub-claim gets its own test. A method designed for two things at once usually tests neither cleanly.

## Method Details

### Fake door

A visible entry point (button, menu item, upsell) that leads to a "coming soon" capture page instead of the real feature.

- **What it tests:** Desirability — whether the target segment clicks toward the feature when it is offered in context.
- **What to measure:** Click-through rate relative to the surface's baseline traffic, and — if there is a capture form — email / wait-list submissions.
- **Sample sizing:** Need enough baseline traffic that a meaningful rate is distinguishable from noise. For a 5-point rate lift at p < 0.1, typically ≥ 400–800 visitors on the surface.
- **Default timebox:** 1–2 weeks of active traffic.
- **Gotchas:**
  - Users who click a fake door and hit a "coming soon" page can feel tricked — prepare a graceful message and, ideally, offer to follow up. Running the test on a logged-in surface with no follow-up erodes trust quickly.
  - Click ≠ commitment. A fake door measures interest at the moment of offer, not willingness to adopt. For adoption, pair with concierge or prototype.
  - Placement-sensitive: a fake door buried three menus deep measures navigation, not desirability.

### Smoke test / ad test

A paid or organic ad driving cold traffic to a minimal landing page that describes the proposed value and captures intent (email, wait-list, "notify me", signup).

- **What it tests:** Desirability at the top of the funnel — does the value prop stop someone cold.
- **What to measure:** CTR on ad (relative to channel baseline), landing-page conversion to intent capture.
- **Sample sizing:** Tied to channel — plan for ≥ 1000 impressions per ad variant to separate signal from noise, more for lower-variance messaging.
- **Default timebox:** 1–2 weeks.
- **Gotchas:**
  - Ad-driven traffic self-selects — a cold visitor is not the same population as an existing user. Results mislead when transferred to logged-in contexts.
  - A/B between variants, not just a single ad — a weak ad against itself always "wins" in isolation.
  - Single-visit intent is weak signal on its own. Pair with a follow-up touchpoint (confirmation email open, survey click) to strengthen.

### Landing page

A hosted page with the full value proposition, a clear call to action, and intent capture. Often the destination for a smoke test.

- **What it tests:** Desirability at a level of depth that ad tests do not reach — does the story hold up under a minute of reading.
- **What to measure:** Conversion to CTA (signup, wait-list, "request access"), scroll depth, time on page.
- **Sample sizing:** Typically ≥ 200 qualified visitors for a read on a single variant.
- **Default timebox:** 1–2 weeks.
- **Gotchas:**
  - Copy carries the test. A page that sells the feature badly kills a real assumption. Commit the stimulus in writing so a failing result is the idea's, not the page's.
  - Do not show pricing unless pricing is the claim being tested; otherwise the test conflates desirability with viability.

### Concierge / Wizard of Oz

Deliver the outcome to a small set of real users by hand, while they perceive a product-like surface (or know it is manual and do not care).

- **What it tests:** Desirability *and* usability — does the outcome, once delivered, actually produce the behavior change the solution predicts.
- **What to measure:** Repeat requests, willingness to pay, onward adoption, qualitative debrief on what they would have done otherwise.
- **Sample sizing:** 5–10 participants is usually enough — concierge surfaces patterns, not rates.
- **Default timebox:** 2–3 weeks.
- **Gotchas:**
  - Does not test feasibility at scale. If the concierge takes 3 hours per user, the product version has to get to 3 minutes to be viable — that gap is a separate assumption.
  - Attention bias: participants who know they are in a pilot are more patient. Watch for behaviors that would quietly die under normal usage.

### Interactive prototype test

A clickable prototype (Figma, Framer, low-code) in a moderated or unmoderated session where participants attempt a defined task.

- **What it tests:** Usability — can the target user complete the task unaided, and where do they stall.
- **What to measure:** Task completion rate, time to first success, error steps, verbal think-aloud moments.
- **Sample sizing:** 5 users catches ~80% of usability issues at a single variant; 8–10 for higher confidence or two segments.
- **Default timebox:** 1 week recruitment + 1 week sessions.
- **Gotchas:**
  - Does not test desirability. A user who completes a task in a session does not prove they would seek out that task in their day. Pair with a desirability test when that claim matters.
  - Fidelity matters downward: a too-polished prototype invites aesthetic feedback rather than usability feedback. Keep the stimulus rough enough that participants treat it as a work-in-progress.

### Painted door

Variant of fake door. The entry point presents as a real feature with full UI, but under the hood it collects intent or routes to a placeholder.

- **What it tests:** Desirability at a slightly deeper stage — clicking *past* the entry, not just on it.
- **What to measure:** Depth-of-engagement before the placeholder appears.
- **Gotchas:** Identical trust risks to fake door, amplified by the higher-fidelity appearance. Use only with a clear graceful-exit design.

### Customer letter / concept test

Write the launch announcement, faq, and "what this means for you" letter *before* building. Circulate to target users or internal stakeholders for reaction.

- **What it tests:** Desirability at the narrative level — does the value prop land in words.
- **What to measure:** Qualitative reaction — "is this exciting?", "would you switch?", "what is unclear?" — plus willingness to be a design partner.
- **Sample sizing:** 5–10 interviews or reactions is usually sufficient; patterns emerge fast when the message is weak.
- **Default timebox:** 3–5 days of outreach.
- **Gotchas:**
  - Politeness bias is severe — users rarely tell a PM a concept is bad. Ask "what would stop you from using this?" and "what would you buy instead of this?" rather than "would you use this?".
  - Tests the pitch, not the product. A concept that clears the letter test can still miss on usability — sequence it before, not instead of, a usability test.

### Pricing probe

Expose a price point in a smoke test, landing page, or sales conversation and measure intent conversion.

- **What it tests:** Viability — willingness to pay at a target price.
- **What to measure:** Intent-to-pay conversion across two or three price variants. Absolute conversion is less informative than the elasticity between variants.
- **Sample sizing:** Per-variant sizing like smoke tests (≥ 200 qualified visitors or ≥ 10 sales conversations per price point).
- **Gotchas:**
  - Stated willingness ≠ paid willingness. Anchor to behavior (card enters, PO drafted, demo booked) rather than survey response.
  - Single price point tells you almost nothing. Always run ≥ 2 points to read elasticity.

### Technical spike

A short, fixed-scope implementation experiment that answers one feasibility question.

- **What it tests:** Feasibility — can we build X with current tools, current data, current latency budget.
- **What to produce:** A working demo of the load-bearing step (not the full feature), plus a written finding on what did and did not work.
- **Sample sizing:** N/A. Scope-bound, not user-bound.
- **Default timebox:** 1–5 days, fixed upfront. The timebox *is* the test — a spike that overruns is a "not within budget" result even if the work would have eventually succeeded.
- **Gotchas:**
  - Scope creep kills spikes. Write the one question the spike answers before starting, and stop when it is answered — even if the code is half-finished.
  - A passing spike tests only what was built. Generalizing from a spike to the full product is a separate assumption ("the mechanism scales").

### Expert review / heuristic review

Structured critique of the concept or prototype by experts — domain, design, security, infra — before build.

- **What it tests:** Feasibility, usability, or regulatory risk, depending on who is in the room.
- **What to produce:** A short written review with prioritized risks and suggested mitigations.
- **Sample sizing:** 2–3 experts per angle.
- **Default timebox:** 3–5 days.
- **Gotchas:**
  - Experts over-index on their own domain. A security review will find security risks; it will not surface desirability problems. Match reviewer to claim type.
  - Calibrate by asking the expert to name the top *three* risks, not "all the risks" — unbounded critique produces unbounded lists that obscure priority.

### Data mining / cohort backcast

Search existing product data for behavior that the proposed solution would amplify. "If users want X, they already do a workaround for X today" — find the workaround and measure it.

- **What it tests:** Desirability under latent demand — there is behavior evidence in history.
- **What to measure:** Frequency of the workaround, cohort retention of workaround users vs. baseline, trend slope.
- **Sample sizing:** Tied to data availability. Usually a few thousand sessions / users is plenty.
- **Default timebox:** 2–5 days.
- **Gotchas:**
  - Absence of workaround ≠ absence of demand. Users often do not attempt things the product does not hint at. A null result here is inconclusive, not a kill.
  - The instrumentation you have was designed for previous questions. Treat missing columns as "not yet measured", not "not happening."

### Analog teardown

Deep dive on how a different product or industry solves the same shape of problem. Structured enough to extract mechanisms, not just vibes.

- **What it tests:** Feasibility or viability — is there a worked example of the mechanic that shipped and survived.
- **What to produce:** A written teardown (1–2 pages) naming the mechanic, the business model, known failure modes, and what transfers to our context.
- **Sample sizing:** 2–3 analogs for triangulation.
- **Default timebox:** 3–5 days.
- **Gotchas:**
  - Surface-level mimicry fails. Extract the mechanism, not the UI. Copying Linear's keyboard bar without Linear's data model copies the visible 5%.
  - Survivorship bias — studied products shipped and survived. For the full picture, pick one analog that visibly failed in this space.

## Choosing Between Methods

When two methods fit, prefer by cost-of-being-wrong:

- **High cost of false positive** (team will commit real engineering if this passes): prefer concierge or interactive prototype over fake door. Fake-door passes can mislead into building the wrong thing if the clickers do not actually adopt.
- **High cost of false negative** (killing a good idea is expensive): prefer concierge, customer letter, or expert review over smoke test. Smoke tests are cheap but fragile, and a weak stimulus kills strong ideas.
- **Low access to target segment:** prefer analog teardown or data mining over live tests — those do not require participant recruitment.
- **Short timebox (< 1 week):** prefer expert review, data mining, or spike. Live tests with traffic or recruitment need lead time.

When the method depends on a surface that does not yet exist (e.g., a fake door in a UI flow that is not built), route the PM to build the minimum surface first or switch methods — do not design a test the team cannot run.
