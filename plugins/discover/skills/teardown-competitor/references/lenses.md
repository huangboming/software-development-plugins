# Teardown Lenses

Pick one lens per teardown. The lens determines what goes under Findings and what to skip — a lens-less teardown becomes a feature parade.

## Job-to-Be-Done (default for discover work)

**Use when** the decision is about what user need this serves, and how the target shapes user expectations.

**Capture:**

- Primary job the target is hired for — the progress a user is trying to make. Phrase as: "When [situation], I want to [motivation] so I can [outcome]".
- Triggering situations — what pushes a user to reach for the target now.
- Prior workflow — what the user was doing before (often the real alternative).
- Jobs left unserved — tasks users still complete outside the target.
- Switching barriers — what locks a user in, what would make them leave.

**Skip:** Feature lists unless a feature is load-bearing for the job. Detailed pricing unless pricing blocks job fit.

**Questions this lens answers:**

- What progress is the user making?
- Which related jobs is the target not serving?
- Where is the user forced to work around the target?

## Pricing-and-Packaging

**Use when** the decision is about monetization, price ceiling, or packaging strategy in this space.

**Capture:**

- Price points and tiers — with access dates.
- Packaging axes — seats, usage, features, data volume, workspaces, per-environment.
- Free tier shape — what is given away, what gates monetization.
- Enterprise or custom pricing signals — "contact sales" thresholds, case studies of deal sizes.
- Price-sensitive segments inferred from packaging breaks.

**Skip:** Job framing, positioning narrative, technical architecture unless they explain a price break.

**Questions this lens answers:**

- What price does the market tolerate?
- What is the packaging unit of value?
- Where does the target leave monetization on the table?

## Positioning

**Use when** the decision is about category definition, narrative, or where the white space is.

**Capture:**

- Category claim — often on the hero page, homepage headline, or tagline.
- Primary differentiation claim — what they say they do better.
- ICP signals — which segment the marketing copy, case studies, and testimonials address.
- Narrative arc — the story the target tells about user pain and its resolution.
- Comparison pages — who they name as competitors (a direct signal of self-positioning).

**Skip:** Deep job capture, technical architecture.

**Questions this lens answers:**

- What category is this in, per the target?
- What narrative is the target betting on?
- Where is the white space — an unclaimed position, category, or segment?

## Gaps-and-Frictions

**Use when** the decision is about what unmet need the target leaves on the table, or where adoption breaks.

**Capture:**

- Frequent complaints across reviews (G2, Trustpilot, Capterra) — cite the review source.
- Feature requests that repeat across communities (Reddit, Slack, forums).
- Onboarding drop-off signals — community questions, docs pages with heavy Q&A.
- Integration or extension gaps named by users.
- Support-ticket patterns where publicly visible.

**Skip:** Positive marketing claims — they are self-reported and uncheckable.

**Questions this lens answers:**

- What repeatedly fails for users of the target?
- What gaps suggest an adjacent opportunity?
- Which frictions are "accepted" vs. still actively painful?

## Technical

**Use when** the decision is about architecture, integrations, or technical constraints shared across incumbents.

**Capture:**

- API shape — REST, GraphQL, webhooks, SDKs, rate limits.
- Integration surface — which other systems the target natively connects to.
- Data model shape inferred from public docs (entities, relationships, cardinality).
- Deployment model — cloud, self-hosted, hybrid, on-device.
- Stack signals — frontend, backend, infra choices when publicly disclosed (job postings, engineering blog).

**Skip:** Job framing, pricing, positioning unless they constrain architecture.

**Questions this lens answers:**

- What technical path has the category converged on?
- Where is the integration surface sparse?
- What architectural constraints will new entrants face?

## When one lens is not enough

If the decision genuinely spans two lenses (e.g., "can we monetize this job well *and* position differently"), produce two teardown files with lens qualifiers in the slug (`teardown-notion-pricing.md`, `teardown-notion-positioning.md`) rather than combining lenses in one file. A dual-lens file dilutes both — the goal is signal per lens, not coverage.
