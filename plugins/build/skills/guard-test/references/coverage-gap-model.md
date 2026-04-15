# Coverage Gap Model

How to classify production code by testability, detect coverage gaps, and prioritize which gaps to fill.

## Contents

- [Code Classification Quadrant](#code-classification-quadrant) — Two-axis model (complexity x collaborators) with quadrant actions
- [Unit Test Gaps](#unit-test-gaps) — Gap types for Domain Model code (error paths, boundaries, state transitions)
- [Integration Test Gaps](#integration-test-gaps) — Gap types for Controllers (failure handling, side-effect verification)
- [Prioritization](#prioritization) — Unified ordering for filling gaps across both test types

## Scope

This model covers **unit tests** and **integration tests**. E2E tests are out of scope — if encountered, note "E2E coverage not assessed by this skill" and move on.

## Code Classification Quadrant

Classify every in-scope function along two axes before deciding what kind of test it needs.

```
                    HIGH COMPLEXITY
                         |
    DOMAIN MODEL /       |       OVERCOMPLICATED
    BUSINESS LOGIC       |       CODE
    → Unit test          |       → Refactor first
                         |
  FEW ───────────────────┼─────────────────── MANY
  COLLABORATORS          |              COLLABORATORS
                         |
    TRIVIAL CODE         |       CONTROLLERS /
    → Skip               |       ORCHESTRATION
                         |       → Integration test
                    LOW COMPLEXITY
```

### Axis Definitions

**Complexity axis** — count decision points (`if`, `else if`, `match` arms, guard clauses, early returns, ternaries):
- 0-2 = low, 3+ = high
- Business rules (validation, eligibility, pricing, permissions) count as high regardless of branch count

**Collaborator axis** — count out-of-process dependencies (DB, HTTP, queues, filesystem, external services, system clock):
- 0-1 = few, 2+ = many
- In-process collaborators (your own classes/functions) do NOT count

### Quadrant Actions

| Quadrant | Test Type | guard-test Action |
|----------|-----------|---------------------|
| **Domain Model** | Unit test | **Write unit tests** for untested functions |
| **Trivial** | None | **Skip** — acknowledge and move on |
| **Controllers** | Integration test | **Write integration tests** for untested orchestration |
| **Overcomplicated** | Refactor first | **Flag as design issue** — recommend Humble Object extraction, then test the extracted parts |

### Worked Example

```
process_refund(order, reason):          # 5 branches, 0 collaborators → Domain Model → unit test
  if order.status != "completed": ...   #   guard clause
  if order.age_days > 30: ...           #   business rule (30-day window)
  if reason == "defective": ...         #   full refund path
  elif reason == "changed_mind": ...    #   partial refund path
  else: ...                             #   standard refund path
  return RefundResult(...)

handle_refund_request(request):         # 1 branch, 3 collaborators (DB + payment API + event bus) → Controllers → integration test
  order = db.get_order(request.order_id)
  result = process_refund(order, request.reason)
  payment_api.refund(result.amount)
  db.save_refund(result)
  events.publish("refund.created", result)
  return Response(200, result)

get_refund_amount(refund):              # 0 branches, 0 collaborators → Trivial → skip
  return refund.amount
```

## Unit Test Gaps

| Gap Type | Priority | Signal |
|----------|----------|--------|
| **Untested Domain Model** | Critical | Domain logic function with zero tests |
| **Missing error paths** | High | Guard clauses or error returns exist, only happy path tested |
| **Missing boundary values** | High | Thresholds or ranges exist, only mid-range values tested |
| **Untested state transitions** | High | State machine with transitions, not all paths covered |
| **Missing equivalence classes** | Medium | Different input categories produce different behavior, not all tested |
| **Weak assertions** | Medium | Test exists but only asserts non-null or type |

## Integration Test Gaps

| Gap Type | Priority | Signal |
|----------|----------|--------|
| **Untested Controller** | High | Orchestration function with zero integration tests |
| **Missing failure handling** | High | Controller calls external services but no test verifies behavior when a service fails or returns an error |
| **Missing side-effect verification** | High | Controller writes to DB and/or publishes events, but tests only assert on the return value |
| **Missing concurrent/ordering scenarios** | Medium | Controller processes items in sequence or handles concurrent requests, but tests only cover single happy-path calls |

## Prioritization

Fill gaps in this order across both test types:

1. **Domain Model with zero coverage** — highest-value unit test targets
2. **Controllers with zero coverage** — highest-value integration test targets
3. **Error/failure paths** — guard clauses in unit tests, service failures in integration tests
4. **Boundary conditions** — off-by-one, threshold crossings, empty collections
5. **Side-effect verification** — DB writes, events, external calls asserted in integration tests
6. **Equivalence class coverage** — one test per distinct input category
7. **State transitions** — every valid transition + key invalid transitions

### High-Value Target Signals

**For unit tests** — prioritize functions containing: conditional business logic, pricing/fee calculations, permission checks, data validation, date/time arithmetic, state machine transitions, retry/fallback logic.

**For integration tests** — prioritize controllers that: write to persistent storage, call external APIs with financial impact, publish events consumed by other services, handle authentication/authorization flows, have complex error recovery (retries, compensating transactions).

### Borderline Classifications

- **Domain Model vs. Trivial**: Any business rules or data transformation beyond field access → Domain Model
- **Domain Model vs. Overcomplicated**: Mixed business logic + I/O → recommend extracting logic into a pure function, then unit test the extraction
- **Controllers vs. Overcomplicated**: Orchestration with conditional branching on business rules → Overcomplicated, extract the branching logic into Domain Model (unit testable) + thin Controller (integration testable)
