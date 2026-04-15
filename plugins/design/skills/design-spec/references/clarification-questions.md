# Clarification Questions

Multiple-choice question patterns for Step 4. Pick 3-5 relevant questions based on the feature and its scope (backend, frontend, or full-stack). Prioritize questions that resolve the most ambiguity — skip questions whose answers are obvious from the codebase or initial request.

Sections are grouped by track. Full-stack features should draw from both **Backend** and **Frontend** groups.

## Contents

- [Shared](#shared) — Scope & Priority, Users & Access
- [Backend](#backend) — Data & Storage, Integration & Events, Performance & Reliability, API Design
- [Frontend](#frontend) — Surface & Devices, Rendering & Delivery, State & Data, UX States, Accessibility, Design System
- [Domain-Specific Question Sets](#domain-specific-question-sets) — auth, payments, notifications, search, multi-tenant, file/media, dashboards, forms, real-time

---

# Shared

## Scope & Priority

**Scope**: What's the MVP scope?
- A) Minimal — Core functionality only, ship fast
- B) Standard — Core + essential edge cases
- C) Comprehensive — Full feature set with all edge cases

**Timeline**: What's the urgency?
- A) ASAP — Ship within days
- B) Normal — Standard development cycle
- C) Flexible — Quality over speed

## Users & Access

**User Type**: Who uses this feature?
- A) Internal only (employees, admins)
- B) External users (customers)
- C) Both internal and external
- D) Machine-to-machine (API clients)

**Scale**: Expected user volume?
- A) Low (< 100 DAU)
- B) Medium (100 - 10,000 DAU)
- C) High (10,000+ DAU)

---

# Backend

## Data & Storage

**Data Sensitivity**: What type of data is involved?
- A) Public data (non-sensitive)
- B) Internal data (business sensitive)
- C) PII (personally identifiable information)
- D) Financial/Payment data

**Consistency**: What consistency level is needed?
- A) Strong consistency (always up-to-date reads)
- B) Eventual consistency (slight delay acceptable)
- C) Depends on operation (specify)

## Integration & Events

**External Services**: Are external APIs involved?
- A) No external dependencies
- B) Yes, existing integrations (which ones?)
- C) Yes, new integrations needed (which ones?)

**Events**: Should this trigger notifications or downstream processing?
- A) No events needed
- B) Internal events (for other services)
- C) External notifications (email, push, webhook)
- D) Both internal and external

## Performance & Reliability

**Latency**: What's the acceptable response time?
- A) Real-time (< 100ms)
- B) Fast (< 500ms)
- C) Standard (< 2s)
- D) Background processing OK (async)

**Failure Mode**: How should failures be handled?
- A) Fail fast — Return error immediately
- B) Retry — Automatic retry with backoff
- C) Graceful degradation — Partial functionality
- D) Queue for later — Store and retry

## API Design

**API Style**: What API pattern to use?
- A) REST (standard CRUD operations)
- B) GraphQL (flexible queries)
- C) gRPC (high performance, internal)
- D) WebSocket (real-time bidirectional)

---

# Frontend

## Surface & Devices

**Target devices**: Where does this feature need to work well?
- A) Desktop only
- B) Mobile-first (responsive)
- C) Desktop + mobile web (responsive)
- D) Mobile web + native app parity

**Browser support**: What's the baseline?
- A) Latest evergreen browsers only
- B) Latest + one previous major version
- C) Broad legacy support (specify)

## Rendering & Delivery

**Rendering**: How should this page/feature render?
- A) Client-side only (SPA) — behind auth, no SEO
- B) Server-rendered (SSR) — needs fast first paint or SEO
- C) Static / pre-rendered (SSG / ISR) — content changes infrequently
- D) Mixed — static shell, client-rendered interactive parts

**SEO**: Does this need to be indexed?
- A) No — auth-gated or internal
- B) Yes — public, SEO matters
- C) Partial — some pages public, some gated

## State & Data

**Data freshness**: How fresh does data need to be?
- A) Real-time (subscriptions / websockets)
- B) Near real-time (poll / refetch on focus)
- C) Fetched on navigation, cached otherwise
- D) Static (fetched once)

**Offline**: Should this work without a network?
- A) No — requires network
- B) Read-only offline (cached view)
- C) Offline reads + queued writes (sync later)

**Shared state**: Does state need to cross routes?
- A) No — contained in a single page
- B) Yes — shared across a few related routes (context)
- C) Yes — truly global (global store)

## UX States

**Empty / loading / error states**: Which are in scope for MVP?
- A) Happy path only (cut others for later)
- B) Loading + error, skip empty-state polish
- C) All three designed explicitly

**Undo / destructive actions**: How are destructive actions handled?
- A) Immediate, no confirmation
- B) Confirmation modal
- C) Soft delete with undo (toast)
- D) Two-step (archive then delete)

## Accessibility

**A11y target**: What level are we meeting?
- A) Basic — semantic HTML, keyboard reachable
- B) WCAG AA (recommended default)
- C) WCAG AAA or strict procurement requirements

**Input methods**: Which do we need to support explicitly?
- A) Mouse + keyboard
- B) + Touch
- C) + Screen readers (full a11y pass)
- D) + Voice / switch control

## Design System & Look

**Design system reuse**: How much is new vs reused?
- A) Reuse existing primitives only — no new components
- B) Reuse primitives, one or two new composite components
- C) Mostly new — feature needs bespoke UI

**Visual design source**: Where do the visuals come from?
- A) Existing design-system patterns (no new designs needed)
- B) Figma / designer handoff available
- C) Claude designs it (confirm style guide)

---

## Domain-Specific Question Sets

### For Authentication Features
1. **Auth method**: OAuth 2.0, magic link, JWT with email/password, SSO?
2. **MFA**: Required, optional, or not needed?
3. **Session duration**: Short (1hr), medium (1 day), long (30 days)?
4. **Account recovery**: Email reset, admin reset, self-service?

### For Payment Features
1. **Payment types**: One-time, subscription, or both?
2. **Provider**: Stripe, PayPal, or other?
3. **Currencies**: Single or multi-currency?
4. **Refunds**: Automatic, manual approval, or not supported?
5. **Compliance**: PCI-DSS scope — are you handling card data directly or using tokenized hosted fields?

### For Notification Features
1. **Channels**: Email, push, SMS, in-app, or combination?
2. **Delivery**: Real-time or batched/digest?
3. **Preferences**: User-configurable or system-defined?
4. **Retry**: On failure, retry or log and move on?

### For Search Features
1. **Scope**: Single entity or cross-entity search?
2. **Matching**: Exact match, fuzzy, or full-text?
3. **Filters**: Basic filters or advanced faceted search?
4. **Freshness**: Real-time index updates or periodic rebuild acceptable?
5. **UI**: Instant search (type-to-search) or submit-to-search?

### For Multi-Tenant Features
1. **Isolation**: Shared DB with tenant column, schema-per-tenant, or DB-per-tenant?
2. **Data access**: Strict tenant isolation or cross-tenant analytics needed?
3. **Customization**: Per-tenant configuration, branding, or feature flags?

### For File/Media Features
1. **Storage**: Cloud object storage (S3/GCS) or self-hosted?
2. **Size limits**: What's the max upload size?
3. **Processing**: On-upload (thumbnails, transcoding) or on-demand?
4. **Access control**: Public URLs, signed URLs, or auth-gated?
5. **Upload UX**: Single file, multi-file, drag-and-drop, resumable?

### For Dashboard / Data-Visualization Features
1. **Data volume**: How many rows / series per view?
2. **Interactivity**: Static charts, hover details, drill-down, or cross-filter?
3. **Export**: View-only, CSV export, image export, scheduled reports?
4. **Refresh**: Real-time, on demand, or scheduled?
5. **Charting library**: Reuse existing (specify), introduce new (justify)?

### For Form-Heavy Features
1. **Form length**: Single-page, multi-step wizard, or long-scroll?
2. **Validation**: On submit, on blur, or live (as-you-type)?
3. **Autosave**: Manual save, autosave draft, or both?
4. **Conditional fields**: Static schema or fields that appear/disappear based on answers?
5. **File uploads**: Part of the form or separate flow?

### For Real-Time / Collaborative Features
1. **Transport**: WebSocket, SSE, or polling?
2. **Concurrency**: Last-write-wins, operational transform, or CRDT?
3. **Presence**: Show other users' cursors / online status?
4. **Offline / reconnect**: Queue changes and sync, or require online?
