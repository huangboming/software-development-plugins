# Tech Spec Template

Use this template when generating `.product/development/specs/<feature-name>.md` in Step 7. After writing, review it in Step 8 and reconcile findings in Step 9.

**Guiding principle:** this is a **design** document, not an implementation document. Explain structure, behavior, and decisions. Visualize with mermaid. Do not paste function bodies, full DDL, or large payload examples — describe shapes in tables.

The template below lists every section with guidance in `[brackets]`. Include sections relevant to the feature's scope (backend, frontend, or both); omit sections that do not apply and note why in a one-line "N/A — reason" stub so reviewers know the omission was intentional.

## Contents

1. **Introduction & Context** — Problem, background, goals, non-goals
2. **Proposed Solution**
   - 2.1 Architecture Overview
   - 2.2 Module Structure & Boundaries (code architecture, dependency direction)
   - 2.3 Data Flow
   - 2.4 Data Model
   - 2.5 State Machine
   - 2.6 API Design (backend / full-stack)
   - 2.7 UI Design (frontend / full-stack)
   - 2.8 Client State Management (frontend / full-stack)
   - 2.9 Third-Party Tools / Libraries
3. **Implementation Details** — Phased plan, edge cases, testing strategy
4. **Risks & Alternatives** — Trade-offs, alternatives, security, scalability, migration
- **Appendix** — Glossary, references

---

## Spec Skeleton

### Header

```
# [Feature Name] - Technical Specification

**Author:** [Name]
**Date:** [Date]
**Status:** Draft | In Review | Approved
**Scope:** Backend | Frontend | Full-stack
```

---

### 1. Introduction & Context

- **Problem Statement** — What user/business problem are we solving?
- **Background** — Why now? What led to this?
- **Goals** — Measurable outcomes (e.g., "reduce p95 latency by 200ms", "lift task completion from 60% → 85%")
- **Non-Goals** — What we are explicitly not solving; prevents scope creep

---

### 2. Proposed Solution

#### 2.1 Architecture Overview

One-paragraph summary of the approach, then a mermaid architecture diagram. Pick the flavor that fits:

**Backend system architecture** (flowchart):

~~~mermaid
flowchart LR
  Client[Client] -->|HTTPS| Gateway[API Gateway]
  Gateway --> Service[Feature Service]
  Service --> DB[(Primary DB)]
  Service --> Cache[(Cache)]
  Service -->|publish| Queue[[Event Queue]]
  Queue --> Worker[Async Worker]
~~~

**Frontend component architecture** (flowchart):

~~~mermaid
flowchart TD
  Page[FeaturePage]
  Page --> Header[Header]
  Page --> List[ItemList]
  List --> Item[ItemCard]
  Page --> Drawer[DetailDrawer]
  Drawer --> Form[EditForm]
~~~

#### 2.2 Module Structure & Boundaries

Name the modules (or packages), their single responsibility, and the public API each one exposes. Show dependency direction explicitly with a mermaid diagram — arrows must point inward per clean architecture (adapters → application → domain; infrastructure implements ports defined by application/domain).

~~~mermaid
flowchart LR
  subgraph Adapters
    HTTP[HTTP Handlers]
    UI[UI Components]
  end
  subgraph Application
    UC[Use Cases]
    PORTS[Ports / Interfaces]
  end
  subgraph Domain
    DM[Domain Model]
  end
  subgraph Infrastructure
    DB[Repository Impl]
    EXT[External API Client]
  end
  HTTP --> UC
  UI --> UC
  UC --> DM
  UC --> PORTS
  DB -.implements.-> PORTS
  EXT -.implements.-> PORTS
~~~

| Module | Responsibility (one sentence) | Public API | Depends on |
|--------|------------------------------|-----------|------------|
| `domain/<aggregate>` | Aggregate, invariants, state transitions | named types + domain ops | — |
| `app/<feature>/<use-case>` | Orchestrate one user-visible operation | `doThing(input): Result` | `domain/*`, ports |
| `infra/<feature>/<adapter>` | Concrete implementation of a port | `implements <Port>` | external lib |
| `web/<feature>` or `features/<feature>` | Adapter layer (HTTP route or UI screen) | routes / exported components | `app/*` |

**Encapsulation rule:** anything not listed in "Public API" is internal. Deep imports into a module's internals are a refactor signal, not a feature — call them out.

**Cross-cutting concerns** (auth, logging, tracing, metrics, error translation) live in middleware / decorators / higher-order hooks — name where, so reviewers can check they aren't interleaved with business logic.

**Boundary enforcement** (optional but recommended when layering is load-bearing): name the tool that keeps the direction honest — e.g. `eslint-plugin-boundaries`, `dependency-cruiser`, `tach`, `archunit`. Without enforcement, the layering rots.

---

#### 2.3 Data Flow

Show how data moves through the system. Use `sequenceDiagram` for request/response or user interactions:

~~~mermaid
sequenceDiagram
  participant U as User
  participant UI as UI
  participant API as API
  participant DB as Database
  U->>UI: Submits form
  UI->>API: POST /resource
  API->>DB: Insert
  DB-->>API: OK
  API-->>UI: 201 Created
  UI-->>U: Success state
~~~

#### 2.4 Data Model (backend or shared state)

Use `erDiagram` to show entities and relationships. List fields and constraints in a table — do **not** paste `CREATE TABLE` DDL.

~~~mermaid
erDiagram
  USER ||--o{ ORDER : places
  ORDER ||--|{ ORDER_ITEM : contains
  PRODUCT ||--o{ ORDER_ITEM : "listed in"
~~~

| Entity | Field | Type | Constraints | Notes |
|--------|-------|------|-------------|-------|
| Order | id | UUID | PK | |
| Order | user_id | UUID | FK → User, NOT NULL | Indexed |
| Order | status | enum | NOT NULL, default `pending` | See State Machine |
| Order | total_amount | decimal(10,2) | NOT NULL | |

**Indexes:** `(user_id)`, `(status, created_at)` for dashboard queries.

#### 2.5 State Machine (if the entity or view has a lifecycle)

~~~mermaid
stateDiagram-v2
  [*] --> Pending
  Pending --> Confirmed: payment_ok
  Pending --> Cancelled: user_cancel / timeout
  Confirmed --> Shipped: fulfilled
  Shipped --> Delivered: carrier_confirm
  Delivered --> [*]
  Cancelled --> [*]
~~~

#### 2.6 API Design (backend / full-stack)

List endpoints in a table. Describe request/response **shapes** in sub-tables, not full JSON examples.

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| POST | `/api/v1/orders` | Create order | User |
| GET | `/api/v1/orders/{id}` | Fetch order | Owner |
| PATCH | `/api/v1/orders/{id}` | Update status | Owner / Admin |

**`POST /api/v1/orders` — request**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| items | array | yes | Non-empty |
| items[].product_id | UUID | yes | |
| items[].quantity | int | yes | > 0 |

**Responses**

| Status | Meaning | Shape |
|--------|---------|-------|
| 201 | Created | `{ id, status, total_amount, created_at }` |
| 400 | Validation error | `{ error.code: VALIDATION_ERROR, error.message }` |
| 401 | Unauthorized | `{ error.code: UNAUTHORIZED }` |
| 409 | Conflict (e.g., stale state) | `{ error.code: CONFLICT }` |

Underspecified error handling is the #1 spec mistake — list every non-happy-path response explicitly.

#### 2.7 UI Design (frontend / full-stack)

- **Screens / routes** — list routes and what they render
- **Key interactions** — loading, empty, error, and success states for each screen
- **Responsive behavior** — breakpoints and what changes
- **Accessibility** — keyboard navigation, focus management, aria roles, color contrast

**Route table**

| Route | Component | Data | Auth |
|-------|-----------|------|------|
| `/orders` | OrderListPage | list orders | User |
| `/orders/:id` | OrderDetailPage | fetch order | Owner |

**View-state diagram** for a key screen:

~~~mermaid
stateDiagram-v2
  [*] --> Loading
  Loading --> Empty: no data
  Loading --> Ready: data
  Loading --> Error: fetch failed
  Ready --> Editing: user edits
  Editing --> Saving: submit
  Saving --> Ready: ok
  Saving --> Error: fail
  Error --> Loading: retry
~~~

#### 2.8 Client State Management (frontend / full-stack)

Describe where state lives and why. Split by concern:

| Concern | Location | Example |
|---------|----------|---------|
| Server data | Query cache (e.g., React Query) | order list, order detail |
| URL state | Router params / search params | selected tab, filters |
| Ephemeral UI state | Component local | modal open, form draft |
| Cross-page shared state | Global store (only if needed) | current user, theme |

#### 2.9 Third-Party Tools / Libraries

State all external services and libraries explicitly — do not assume Redis, Kafka, a charting library, etc. exist.

| Tool | Purpose | Why Chosen |
|------|---------|------------|
| [Library] | [Purpose] | [Justification] |

---

### 3. Implementation Details

#### 3.1 Step-by-Step Plan

Rough sequence; order matters.

1. **Phase 1: [Name]** — minimal shippable slice
   - [ ] Task
2. **Phase 2: [Name]** — extend
   - [ ] Task
3. **Phase 3: [Name]** — polish / scale
   - [ ] Task

#### 3.2 Edge Cases

| Scenario | Handling |
|----------|----------|
| User has no network | [Behavior] |
| Input exceeds limit | [Behavior] |
| External service unavailable | [Behavior] |
| Concurrent modifications | [Behavior] |
| Slow list (1000+ items, frontend) | [Behavior — virtualize? paginate?] |

#### 3.3 Testing Strategy

- **Unit** — what logic needs isolated tests
- **Integration** — what boundaries need real dependencies exercised
- **End-to-End** — critical user flows to automate in a browser
- **Load / Perf** — thresholds and how they're verified (backend RPS, frontend bundle/interaction budgets)
- **Accessibility** (frontend) — axe / manual keyboard checks for critical flows

---

### 4. Risks & Alternatives

#### 4.1 Trade-offs

| Decision | Trade-off | Rationale |
|----------|-----------|-----------|
| [Choice A over B] | [What we give up] | [Why it's acceptable] |

#### 4.2 Alternatives Considered

- **Alternative 1:** [name] — approach / why rejected
- **Alternative 2:** [name] — approach / why rejected

#### 4.3 Security Considerations

- Authentication — how users are authenticated
- Authorization — how access is controlled
- Data protection — how sensitive data is handled (PII, tokens, secrets)
- Input validation — where and how inputs are validated
- Frontend-specific — XSS exposure (user content rendering), CSRF on mutating requests, secrets never embedded in the bundle

#### 4.4 Scalability / Performance

Backend capacity table:

| Load | Expected Behavior | Mitigation |
|------|-------------------|------------|
| 1K users | Normal | — |
| 10K users | [Behavior] | [Strategy] |
| 100K users | [Behavior] | [Strategy] |

Frontend performance budgets (when relevant):

| Metric | Budget |
|--------|--------|
| Initial JS (gzipped) | < 200KB |
| LCP | < 2.5s on 4G |
| INP | < 200ms |
| List render (1000 items) | virtualized, < 100ms scroll |

#### 4.5 Migration & Backward Compatibility

How do existing clients, URLs, data, or stored user preferences survive the change? Required for any schema / API / route change.

---

### Appendix

- **Glossary** — domain-specific terms
- **References** — related specs, PRDs, tickets, external docs
