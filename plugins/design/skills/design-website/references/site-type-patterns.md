# Site-Type Patterns

Page inventory, navigation paradigm, common flows, and gotchas — by site type. Site type is the single biggest variable in website-level design; choose it before drafting the sitemap. Default-shaped patterns are listed; every design must adapt them to the specific user JTBDs and business outcomes captured in the strategy preamble.

## Contents

1. [Choosing a site type](#choosing-a-site-type)
2. [Marketing / landing site](#1-marketing--landing-site)
3. [SaaS application](#2-saas-application)
4. [E-commerce store](#3-e-commerce-store)
5. [Content / editorial site](#4-content--editorial-site)
6. [Documentation site](#5-documentation-site)
7. [Portfolio / personal site](#6-portfolio--personal-site)
8. [Community / forum](#7-community--forum)
9. [Internal tool](#8-internal-tool)
10. [Hybrid sites](#hybrid-sites)

## Choosing a site type

Pick exactly one **primary** type. Hybrid sites pick a primary and treat the secondary as a sub-surface (see [Hybrid sites](#hybrid-sites)). Use this matrix when the choice isn't obvious:

| If the dominant user goal is... | Type |
|---|---|
| Convince a stranger to convert (sign up, book a demo, buy) | Marketing |
| Use a feature inside a logged-in product | SaaS |
| Browse a catalog and check out | E-commerce |
| Read articles for entertainment, learning, or news | Content |
| Look up how to do a specific task with a product | Documentation |
| Showcase work to a hiring manager / client | Portfolio |
| Ask, answer, and discuss with peers | Community |
| Get a job done at work, no public visitors | Internal tool |

Adjacent: when the answer is "two of the above are equally important," design two surfaces (e.g., marketing site + SaaS app under separate subdomains or path prefixes), do not blend.

---

## 1. Marketing / landing site

**Audience.** Cold visitors arriving from search, ads, social, referrals. Most have never heard of the product. A subset are warm leads doing comparison.

**Primary JTBDs.**
- Understand what the product is and whether it solves my problem (in <10 seconds).
- See proof it works (testimonials, logos, case studies, metrics).
- Convert to the next step (sign up, request demo, contact sales, start trial).
- Comparison-shop against alternatives.

**Canonical page inventory.**

| Page | Purpose |
|---|---|
| Home | Above-the-fold value prop + primary CTA + social proof. The ONE page every other page links back to. |
| Product / Features | What the product does, broken into the 3-7 core capabilities. May be one page or one per capability. |
| Pricing | Plan tiers, feature comparison, FAQ on billing. Conversion-critical. |
| About / Company | Trust-building: team, mission, funding, customers. |
| Customers / Case studies | Proof. One page per logo or a feed page + detail pages. |
| Blog / Resources | SEO surface + nurture content. Often the largest section by page count. |
| Contact / Demo | Conversion endpoint for high-touch sales. |
| Login / Sign up | Hand-off to the app surface. |

**Dominant nav paradigm.** Top nav with 4-7 items + footer with full sitemap. Mega menu only if Product or Resources has >5 children. Sticky CTA in nav (Sign up / Get demo) is conventional.

**Common flows.**
- Home → Pricing → Sign up
- Home → Features → Case study → Demo request
- Search/social → Blog post → newsletter signup → Sign up later
- Comparison: Home → Pricing → competitor compare page → Sign up

**Type-specific gotchas.**
- Every page is a landing page (deep links from search). Each must answer: what is this product, who is it for, what's the next step?
- Pricing page is the most-visited deep page after the home page; it is not optional and rarely belongs in the footer.
- Blog posts must include product-context sidebars or in-content CTAs; an SEO-optimized post that doesn't bridge to the product is wasted traffic.
- Don't bury the primary CTA below the fold or behind a menu. Conversion sites have one CTA repeated relentlessly.

---

## 2. SaaS application

**Audience.** Authenticated users with a job to do inside the product. Power users return daily; new users churn within hours if onboarding is poor.

**Primary JTBDs.**
- Sign in / sign up → land in the right place.
- Complete the core task this product exists for (one or two top jobs).
- Find and edit a piece of data they created previously.
- Configure account, team, billing, integrations.
- Recover from errors and find help.

**Canonical page inventory (separate from any marketing surface).**

| Page / view | Purpose |
|---|---|
| Sign in / Sign up | Auth entry. Often shares URL with marketing site. |
| Onboarding flow | First-run setup; usually 2-5 steps. |
| Dashboard / Home | Default authenticated landing. Surfaces recent activity + entry to top tasks. |
| Core feature views | One per primary capability (e.g., "Projects," "Reports," "Inbox"). The reason the product exists. |
| Detail / record views | One per resource type (e.g., individual project, individual report). |
| Search / Command palette | Cross-cutting findability for power users. |
| Notifications / Activity | Async signal surface. |
| Account settings | Profile, password, notifications. |
| Workspace / Team settings | Members, roles, permissions. |
| Billing / Plan | Plan, invoices, payment methods, usage. |
| Integrations / API | Third-party connections, API keys, webhooks. |
| Help / Support | In-product link to docs + contact path. |
| Legal | TOS, privacy, sub-processors. |

**Dominant nav paradigm.** Persistent left side nav for primary feature areas + top utility nav (search, notifications, account). Command palette (Cmd-K) for power users in any product with >20 destinations. Mobile collapses side nav into a hamburger or bottom tab bar.

**Common flows.**
- Sign up → onboarding → first core task completed
- Sign in → dashboard → resume in-progress work
- Invite teammate → role assignment → teammate accepts → first collaborative action
- Upgrade plan: settings → billing → plan select → checkout → confirmation
- Recover account: forgot password → email → reset → sign in

**Type-specific gotchas.**
- Dashboard ≠ home page. A dashboard is a workspace, not a marketing surface; resist filling it with feature tours after week one.
- Empty states are first-class views — design "you have no projects yet" as carefully as the populated state.
- Auth gates create implicit page pairs (signed-out / signed-in); enumerate both.
- Settings sprawl is the silent killer; group by *who owns it* (me / workspace / billing) not *what it controls*.
- Power users live in keyboard shortcuts and search; if you don't design for them, they leave.

---

## 3. E-commerce store

**Audience.** Browsing shoppers (high intent or low intent), returning customers, gift-buyers, comparison-shoppers.

**Primary JTBDs.**
- Find a product I have in mind (search) or didn't know I wanted (browse).
- Evaluate a specific product (PDP) — see it, read reviews, check fit/size/specs.
- Buy with minimum friction.
- Manage post-purchase: track order, return, repurchase.

**Canonical page inventory.**

| Page | Purpose |
|---|---|
| Home | Curated feature: hero collection, new arrivals, bestsellers. Less critical than in marketing sites — many users land on category or PDP. |
| Category / PLP | Product list page per category, with filters/sort/pagination. |
| Product / PDP | Single product: images, price, variants, add to cart, reviews, related. The conversion engine. |
| Search results | Full-text search with the same filter system as PLP. |
| Cart | Line items, quantities, promo code, totals, checkout CTA. |
| Checkout | Multi-step or single-page: shipping → payment → review → confirm. |
| Order confirmation | Receipt, what happens next, related upsell. |
| Account / Orders | Order history, addresses, payment methods, returns. |
| About / Brand | Trust-building. |
| Contact / Help | Returns policy, shipping policy, FAQ, contact. |
| Legal | TOS, privacy. |

**Dominant nav paradigm.** Top nav with category mega menu + persistent search bar + cart icon. Faceted filters as left sidebar on category pages. Mobile: hamburger nav, sticky bottom add-to-cart on PDP.

**Common flows.**
- Search/social → PDP → cart → checkout → confirmation
- Browse: home → category → PLP (filtered) → PDP → cart → checkout
- Returning customer: account → order history → reorder
- Gift: PDP → gift options → checkout with separate billing/shipping

**Type-specific gotchas.**
- The home page is not the entry point most users see; design every PDP and category page as a stand-alone landing.
- Search and filters are the primary navigation, not the top menu — invest there.
- Checkout abandonment compounds with every step; default to guest checkout, single page, address autofill.
- Empty cart, out-of-stock, sold-out variant, and back-in-stock states are first-class — design them.
- Reviews and shipping/return policy are conversion-critical; treat them as primary content, not boilerplate.

---

## 4. Content / editorial site

**Audience.** Readers (subscribers + drive-by from social and search), occasional contributors, editors.

**Primary JTBDs.**
- Discover new content matching my interests.
- Read an article without friction (deep-link from search/social).
- Subscribe / save / share content.
- Find related content after finishing.

**Canonical page inventory.**

| Page | Purpose |
|---|---|
| Home / Feed | Editorial curation: featured + recent + by section. |
| Section / Category | Filtered feed per topic (politics, tech, etc.). |
| Tag / Author pages | Filtered feed per tag or contributor. |
| Article | The atomic content unit. Reading-optimized layout. |
| Search results | Full-text + faceted (date, section, author). |
| Subscribe / Newsletter | Conversion endpoint for retention. |
| About / Masthead | Editorial team, contact, ethics, ads. |
| Account (if subscribers) | Subscription management. |
| Legal | TOS, privacy, comments policy. |

**Dominant nav paradigm.** Top nav with sections + persistent search + subscribe CTA. Long content needs in-article TOC for >2000-word pieces. Footer often duplicates the section list as a sitemap.

**Common flows.**
- Search/social → article → related article → subscribe
- Home → section → article → next article
- Subscriber: sign in → saved articles → resume

**Type-specific gotchas.**
- Article pages dominate traffic; the rest of the site is decoration. Optimize the article template ruthlessly.
- Related-content modules drive depth-of-visit; design the algorithm and the UI together.
- Paywall states (free → metered → blocked) are first-class views.
- Comment sections, if present, are a separate IA problem with their own moderation surface.
- Tag pages metastasize; cap the visible tag taxonomy or you get "10,000 tag pages with one article each."

---

## 5. Documentation site

**Audience.** Developers and power users with a *specific* task they're trying to accomplish. They arrived from Google or the in-product help link. They will leave the moment they find the answer.

**Primary JTBDs.**
- Find the answer to "how do I do X?" in under 30 seconds.
- Copy/paste code that works.
- Understand a concept well enough to make a decision.
- Browse the API reference.

**Canonical page inventory.**

| Page | Purpose |
|---|---|
| Home / Landing | Funnel into the right doc set: getting started, guides, reference. Often shorter than a homepage. |
| Getting started / Quickstart | Hand-holding from zero to first success. Single linear path. |
| Guides / Tutorials | Topical, task-oriented. One per major concept. |
| Concepts / Explainers | "Why" content. Architecture, mental models. |
| API reference | Auto-generated or hand-written, one page per endpoint/class/method. |
| CLI reference | If applicable. |
| SDK reference | If applicable, per language. |
| Examples / Cookbook | Copy-pasteable recipes. |
| Changelog / Release notes | Version-by-version changes. |
| Migration guides | Version-N to version-N+1 upgrade paths. |
| FAQ / Troubleshooting | Common errors, gotchas. |
| Search | Site-wide search. The primary nav. |

**Dominant nav paradigm.** Persistent left sidebar with hierarchical TOC + persistent search bar (search-first; users prefer keyword search over browse). Right sidebar in-article TOC for long pages. Top nav segments by audience or product (e.g., "Docs / API / SDK / Changelog"). Versioned docs need a version switcher.

**Common flows.**
- Google → guide → success (most common — design every guide as a deep-link landing).
- Quickstart → first API call works → guide for next concept.
- Reference: search → API method page → example → back to building.
- Version migration: changelog → migration guide → updated reference.

**Type-specific gotchas.**
- Search is the primary nav, not the top menu. Invest in search quality before nav structure.
- Code blocks are the highest-value element; design copy-button, language tabs, and runnable examples first.
- Version drift kills doc sites — every page should declare its version and have a clear path to current.
- Auto-generated reference looks comprehensive but is unreadable; hand-write the top 20% of pages users actually visit.
- Every "page not found" is a search query in disguise; route 404s to search results scoped to the URL.

---

## 6. Portfolio / personal site

**Audience.** Hiring managers, recruiters, prospective clients, occasional networkers. Spend ≤2 minutes on the site.

**Primary JTBDs.**
- Decide quickly whether this person is worth contacting.
- See proof of work (projects, case studies, writing).
- Find a contact path.
- Confirm credibility (résumé, links to canonical profiles).

**Canonical page inventory.**

| Page | Purpose |
|---|---|
| Home / About | Who I am, what I do, what I'm looking for, primary CTA. Often the only page a visitor reads. |
| Work / Projects | List of projects with thumbnails. May be inline on home. |
| Project detail | One per project: problem, role, process, outcome, visuals. |
| Writing / Blog | If applicable. |
| Contact | Email, scheduling link, social. May be inline on home. |
| Résumé / CV | Linkable, downloadable. |

**Dominant nav paradigm.** Top nav with 3-5 items (Work, Writing, About, Contact) or single-page scrolling site for minimalist portfolios. Footer with secondary contact + social.

**Common flows.**
- Home → project detail → contact
- Search/LinkedIn → home → résumé → contact

**Type-specific gotchas.**
- Resist over-design; visitors want signal density, not animation.
- Project detail pages need explicit *role* and *outcome* — "I worked on this" is a weak signal vs "I led X resulting in Y."
- The "About" page often goes unread; integrate self-introduction into the home page.

---

## 7. Community / forum

**Audience.** Lurkers (read-only majority), occasional askers, frequent answerers, moderators.

**Primary JTBDs.**
- Search for an answer to a question already asked.
- Post a new question or topic.
- Reply to a thread I'm subscribed to.
- Browse what's active or trending.
- Build reputation / status (badges, karma, contributor metrics).

**Canonical page inventory.**

| Page | Purpose |
|---|---|
| Home / Feed | Active threads, trending, "for you." |
| Category / Subforum | Filtered feed by topic. |
| Tag / topic | Filtered feed by tag. |
| Thread / Question | The atomic unit. Original post + replies + voting. |
| New post composer | Standalone or modal. |
| Search | Critical — most users are here to find an answer. |
| Profile | User's posts, replies, badges, reputation. |
| Notifications | Replies, mentions, subscriptions. |
| Settings | Account, notification preferences. |
| Moderation queue | If user is a mod. |
| Rules / Guidelines | Posting rules, code of conduct. |
| Legal | TOS, privacy. |

**Dominant nav paradigm.** Top nav with categories + persistent search + post-CTA + notification icon. Some communities use left side nav for categories instead. Mobile-first: bottom tab bar with feed/search/post/notifications/profile.

**Common flows.**
- Google → existing thread → answer found (lurker majority path)
- Sign in → notifications → reply → back to feed
- New question: post composer → category select → submit → wait for replies
- Reputation: profile → recent activity → badge progression

**Type-specific gotchas.**
- Search results are often higher-traffic than the home page; treat them as a first-class page.
- Empty-feed / no-replies-yet states are first-class.
- Anti-spam, throttling, and onboarding gates create extra states (new user must verify email, post-rate-limited, shadow-banned, etc.) — enumerate them.
- Moderation queues are a parallel IA usually invisible to most users; design them explicitly if mods exist.
- Tag taxonomy and category structure drift; plan for a periodic merge/cleanup process.

---

## 8. Internal tool

**Audience.** Employees with a specific job to do. No public traffic. Login is enforced. Aesthetic matters less than throughput; cognitive load matters most.

**Primary JTBDs.**
- Complete the workflow this tool exists for, fast.
- Look up a record.
- Bulk-edit or batch-process.
- Audit history / who-did-what.

**Canonical page inventory.**

| Page | Purpose |
|---|---|
| Sign in (often SSO) | Auth via corporate identity. |
| Dashboard / Home | Default landing — surface in-progress work and queue. |
| Workflow views | One per task type the tool supports. |
| Record list / table | Tabular, filterable, sortable. The dominant UI shape. |
| Record detail | One per resource type. Edit-in-place common. |
| Search | Often global. |
| Reports / Analytics | If part of the tool's purpose. |
| Audit log | Who did what when. |
| Admin / Settings | Permissions, team, integrations. |
| Help (rare) | Often replaced by Slack channel link. |

**Dominant nav paradigm.** Persistent left side nav. Dense data tables (think Retool, Airtable, Linear-internal). Keyboard shortcuts mandatory for power users. Bulk-action affordances. No marketing surface, no public footer.

**Common flows.**
- Sign in (SSO) → queue → process record → next record
- Search → record → edit → save → audit log entry
- Bulk: list view → filter → select all → action

**Type-specific gotchas.**
- Visual polish is low priority; data density and keyboard speed are high priority.
- Permission granularity creates many sub-states (read-only, can-edit, can-approve, admin); enumerate them.
- Auditability often forces a separate read-only "history" view per record.
- Empty states matter less; populated, dense states matter more.
- Onboarding usually happens out-of-band (training session, runbook); design accordingly — no in-product feature tour.

---

## Hybrid sites

Many real sites combine types. Common combinations and how to handle them:

| Combination | Approach |
|---|---|
| Marketing + SaaS app | Two surfaces under different paths (`/` marketing, `/app` product) or subdomains. Separate nav, separate IA, single auth handoff at sign-in. |
| E-commerce + Content (brand storytelling + shop) | One nav, but cleanly partition: shop in primary nav, journal/blog in secondary. Don't blend feeds. |
| SaaS app + Documentation | Docs as a separate subdomain (`docs.example.com`) with its own IA; in-app help links into it. |
| Marketing + Community | Marketing primary, community as a section (`/community`) with its own internal IA matching the community pattern. |
| Portfolio + Blog | Single site; blog is a section. Use the portfolio pattern as the spine. |

**Rule:** name a primary type and design its IA first. Secondary surfaces inherit the primary's nav shell when they share an audience; otherwise they get their own surface.
