# Edge Pages Checklist

Edge pages are the pages users hit when something is wrong, missing, gated, or required by law. They are not afterthoughts — they are first-class IA. A site that only designs the happy path leaks credibility (404s land on a generic browser error), traps users (no recovery from auth failure), or breaches compliance (no privacy policy).

Use this catalog at the **enumerate edges** step of the workflow. For each category, decide *include* / *exclude with reason* and add to the page inventory. The "Include if…" column gates each page so you don't bloat the inventory with edges that don't apply.

## Contents

1. [Error pages](#error-pages)
2. [Auth & access pages](#auth--access-pages)
3. [Empty / cold-start states](#empty--cold-start-states)
4. [Confirmation & receipt pages](#confirmation--receipt-pages)
5. [System-state pages](#system-state-pages)
6. [Legal & compliance pages](#legal--compliance-pages)
7. [Localization & accessibility variants](#localization--accessibility-variants)
8. [Quick include/exclude matrix](#quick-includeexclude-matrix)

## Error pages

| Page | Include if… | Notes |
|---|---|---|
| 404 — page not found | Always. Every site needs one. | Add a search box and links to top sections; do not just say "Not Found." For docs, route to a search scoped to the URL. |
| 410 — gone | Site has historical URLs that were intentionally removed. | Distinguish from 404 so SEO de-indexes correctly. |
| 500 — server error | Always. | Generic friendly message + status link. Keep static so it works even when the app server is down. |
| 503 — maintenance | Site has scheduled maintenance windows or kill-switch. | Often combined with the maintenance page (below). |
| Permission denied (403) | Site has any auth or role gating. | Distinct from "not found" so users know the URL exists and what to do. |
| Rate limited / throttled | Site has APIs, login, or any rate-controlled endpoints. | Tell user when they can retry. |
| Browser unsupported | Site requires modern browser features. | Often replaced with progressive enhancement; include only if hard-blocking. |
| JavaScript disabled | App requires JS. | One-line message + link to docs/marketing surface that works without JS. |

## Auth & access pages

| Page | Include if… | Notes |
|---|---|---|
| Sign in | Site has any auth. | |
| Sign up | Site has self-serve registration. | |
| Forgot password | Sign-in exists. | Includes the email-sent confirmation and the reset form. |
| Email verification | Sign-up requires email confirmation. | "Check your email" landing + "verified, click here" landing. |
| Two-factor / MFA challenge | 2FA is offered or enforced. | |
| Account locked / disabled | Auth has lockout or admin-disable. | |
| OAuth consent screen | Site is an OAuth provider. | |
| OAuth callback / loading | Site authenticates via OAuth. | Often a flash page during code exchange. |
| Subscription required (paywall) | Site has paid content/features. | Distinguish soft paywall (preview) vs hard paywall (locked). |
| Plan upgrade required | Feature is gated by tier. | Inline modal often, but a standalone landing helps for deep links. |
| Workspace invite acceptance | Multi-tenant SaaS with team invites. | |
| Workspace switcher / no-workspaces | User can belong to multiple workspaces, or to none yet. | |

## Empty / cold-start states

These often live as **states inside other pages** rather than separate URLs, but enumerate them at the IA layer because they affect nav and onboarding.

| State | Include if… | Notes |
|---|---|---|
| Empty list / no records yet | Any page that lists user-created records. | First-run onboarding lives here; this is the most-seen state for new users. |
| No search results | Search exists. | Include suggestions or scoped help. |
| Empty cart | E-commerce. | Include recommended products or recent views. |
| No notifications / inbox zero | Notifications surface exists. | |
| Onboarding incomplete | Multi-step setup is required. | Landing for users who left mid-flow. |
| No teammates yet | Collaboration features. | Invite CTA is the only meaningful content. |

## Confirmation & receipt pages

| Page | Include if… | Notes |
|---|---|---|
| Form submission thank-you | Site has lead-gen forms (contact, demo, newsletter). | One per form, or one shared with dynamic copy. |
| Order confirmation / receipt | E-commerce or any paid checkout. | Often emailed too. |
| Payment processing / pending | Payment provider has an async confirmation step. | |
| Account created | Sign-up completes. | May redirect into onboarding instead. |
| Password changed | Sensitive auth action. | Notification that confirms the action took effect. |
| Subscription canceled / paused | Subscription product. | |

## System-state pages

| Page | Include if… | Notes |
|---|---|---|
| Maintenance / planned downtime | Scheduled maintenance windows are expected. | |
| Status page | Public uptime tracker. | Often on a separate subdomain (`status.example.com`); link from footer. |
| Coming soon / waitlist | Pre-launch marketing surface. | Replace with the live site at launch. |
| Region unavailable / geo-blocked | Service is restricted by region. | Required for some regulated products. |
| Account migrating | Long-running account-level data migration. | Rare but real for enterprise tools. |

## Legal & compliance pages

These are **always required** for public sites collecting any user data or operating commercially.

| Page | Include if… | Notes |
|---|---|---|
| Privacy policy | Always for public sites. Required by GDPR, CCPA, CPRA, etc. | |
| Terms of service / Terms of use | Always for public sites. | |
| Cookie policy + consent banner | Site uses cookies (almost always). EU/UK/CA traffic forces this. | Banner is a UI overlay; the policy is a page. |
| Acceptable use policy | User-generated content or community. | |
| Refund / return policy | E-commerce or paid subscriptions. | |
| Shipping policy | E-commerce with physical goods. | |
| Sub-processors / data processing addendum (DPA) | B2B SaaS handling enterprise customer data. | |
| Accessibility statement | Public sites in jurisdictions with WCAG enforcement (US ADA, EU EAA, UK PSBAR). | Increasingly expected everywhere. |
| Imprint / Legal notice (Impressum) | Site serves Germany, Austria, or Switzerland. | Strict legal requirement. |
| Do Not Sell / Share My Personal Information | CCPA/CPRA-applicable (California traffic). | |
| Copyright / DMCA | User-generated content. | |
| Security disclosure / responsible disclosure | Site has a security policy. | Often `/security` and a `security.txt` file at `/.well-known/security.txt`. |

## Localization & accessibility variants

These multiply the inventory rather than add new pages — call them out explicitly.

| Variant | Include if… | Notes |
|---|---|---|
| Per-locale variants | Site is multilingual. | Decide URL strategy: subdomain (`fr.example.com`), path (`/fr/`), or query (`?lang=fr`). Path is most common for SEO. |
| RTL variants | Locales include Arabic, Hebrew, Persian, Urdu. | Mirror layout, not just translate strings. |
| Per-region variants | Pricing, legal, or product availability differs by region. | Often pricing page + checkout + legal. |
| Print stylesheet pages | Receipts, invoices, articles intended for printing. | Not a separate URL; a CSS variant. Note in IA so it isn't forgotten. |
| Screen-reader-only landmarks | Always for accessible sites. | Skip-to-content link, page-region landmarks. Not URLs but worth noting in nav model. |

## Quick include/exclude matrix

For a fast pass at the end of the workflow, default include/exclude by site type:

| Edge category | Marketing | SaaS | E-commerce | Content | Docs | Portfolio | Community | Internal |
|---|---|---|---|---|---|---|---|---|
| 404 / 500 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Permission denied | — | ✅ | partial | partial | — | — | partial | ✅ |
| Sign in / sign up | partial | ✅ | ✅ | partial | — | — | ✅ | ✅ (SSO) |
| Empty states | — | ✅ | ✅ | ✅ | — | — | ✅ | ✅ |
| Confirmation pages | ✅ | ✅ | ✅ | partial | — | partial | ✅ | partial |
| Maintenance / status | partial | ✅ | ✅ | partial | partial | — | ✅ | partial |
| Privacy / Terms | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | partial |
| Cookie consent | ✅ | ✅ | ✅ | ✅ | ✅ | partial | ✅ | — |
| Refund policy | — | partial | ✅ | — | — | — | — | — |
| Accessibility statement | ✅ | ✅ | ✅ | ✅ | ✅ | partial | ✅ | partial |
| Localization variants | depends on audience |

`✅` = default include; `—` = default exclude; `partial` = depends on site specifics. Always justify exclusions in the artifact's Open Questions section so a reviewer can challenge the call.
