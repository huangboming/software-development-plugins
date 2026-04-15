# Boundary Violation Catalog

Patterns for identifying boundary violations across four levels. Each pattern has concrete detection signals, a confidence level, and either an auto-fix or architectural recommendation.

## Contents

- [Guiding Principle](#guiding-principle) — What makes a boundary good or bad
- [Confidence Rules](#confidence-rules) — When to auto-fix (clear) vs. present for approval (judgment)
- [Transform Ordering](#transform-ordering) — Apply auto-fixes in correct order
- [Level 1: Module / File](#level-1-module--file) — Mixed concerns, over-exposure, barrel re-exports, temporal decomposition
- [Level 2: Class / Type](#level-2-class--type) — God classes, low cohesion, data bags, anemic models
- [Level 3: Function / Interface](#level-3-function--interface) — Parameter bloat, flag params, leaky signatures, fat interfaces, pass-through methods
- [Level 4: Cross-Boundary](#level-4-cross-boundary) — Internal imports, circular deps, feature envy, transitive leakage, Law of Demeter

## Guiding Principle

A good boundary hides a design decision (Parnas, 1972) and provides significant functionality behind a simple interface (Ousterhout, 2018). These two criteria — **what** is hidden and **how well** it's hidden — are the foundation for every violation in this catalog.

- **Parnas test:** "What design decision does this module hide?" If the answer is "nothing" or "the same thing as another module," the boundary is in the wrong place.
- **Ousterhout depth test:** "Is this module's interface simpler than its implementation?" If the interface is nearly as complex as the implementation (many parameters, many methods, caller must understand internals), the module is *shallow* — it adds organizational overhead without hiding complexity.

Every violation below is a specific way that a boundary fails one or both of these tests.

## Confidence Rules

Every finding is classified as **clear** (auto-fix without asking) or **judgment** (present for approval).

**Default to clear when:**
- The violation is mechanically detectable and objectively measurable (e.g., parameter count, unused export)
- The fix is local — no callers are affected, or all callers can be updated trivially
- The change cannot alter observable behavior (tightening visibility on genuinely unused items)

**Default to judgment when:**
- The violation requires understanding intent (is this class deliberately broad, or accidentally?)
- The fix has architectural impact (splitting a class, redesigning an interface)
- The pattern could be an intentional design choice (a large parameter list on a builder, a god class that is actually a facade)
- The module is in a critical path (payments, auth, data integrity)

**Override to judgment** any normally-clear finding if:
- The item appears widely used across the codebase (tightening visibility could break consumers)
- The codebase has an established convention that contradicts the finding

## Transform Ordering

Apply auto-fixes in this order:

| Order | Level | Rationale |
|-------|-------|-----------|
| 1 | Cross-boundary (clear only) | Fix import path violations before modifying module structure |
| 2 | Module/File (clear only) | Prune barrel re-exports before analyzing type/function exposure |
| 3 | Function/Interface (clear only) | Localized signature fixes |
| 4 | Present all judgment findings | Grouped by impact, highest first |

Within each level, process bottom-up (last line first) to preserve line numbers.

## Level 1: Module / File

Violations at the module or file boundary — what a module exposes and whether it has a single, coherent purpose.

### 1.1 Mixed Concerns

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | File contains code from 2+ of: request/response handling, business/domain logic, data access/persistence, serialization/deserialization, infrastructure/config |
| **Detection** | Mixed import domains (HTTP framework + ORM + business types in one file). Functions span layers — e.g., a function that parses a request, applies business rules, and writes to DB. |
| **Recommendation** | Extract into separate modules by concern. Name each module by what it owns, not what it does to data. |

**Worked example:** `orders.py` contains `handle_order_request()` (HTTP), `calculate_total()` (domain), `save_order()` (persistence), `serialize_order()` (serialization) — 4 layers in one file → split into `orders_api.py`, `orders_domain.py`, `orders_repo.py`.

### 1.2 Over-Exposed Module

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Module exports >60% of its definitions, but external usage analysis shows a fraction are consumed by other modules |
| **Detection** | Count public/exported items vs total. Grep for external usage of each exported item. High export count with low external consumption = over-exposure. |
| **Recommendation** | Make non-consumed items internal/private. If the language uses conventions (Python `_prefix`, JS not in `export`), apply them. If it uses access modifiers, tighten them. |

**Litmus test:** For each public item, ask: "If I made this private, would anything outside this module break?" If no — it should be private.

**Worked example:**
```
Module: src/utils/string_helpers.py
  Total definitions: 20 functions
  Exported (public): 18 functions
  Used externally: 4 functions (slugify, truncate, normalize_whitespace, strip_html)

  Finding: 90% of definitions exported, but only 22% consumed externally.
           14 functions are public but have zero external callers.
  Recommendation: Prefix the 14 unused exports with `_` (Python) or remove
                  from `__all__`. External surface drops from 18 → 4.
```

### 1.3 Barrel Re-Export

| | |
|---|---|
| **Confidence** | Clear |
| **Signal** | Index/barrel file (`index.ts`, `__init__.py`, `mod.rs`) re-exports all internals with no filtering |
| **Detection** | `export * from` patterns, `from .module import *`, `pub use submodule::*` |
| **Auto-fix** | Replace wildcard re-exports with explicit named exports of only externally consumed items |

### 1.4 Missing Public API Surface

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Directory/package with multiple files but no clear entry point — consumers import from arbitrary internal files |
| **Detection** | External imports target different internal files rather than a single entry point. No `index`, `__init__`, `mod`, or `public` API file exists, or it exists but is incomplete. |
| **Recommendation** | Define an explicit public API entry point that re-exports only the intended public surface. |

### 1.5 Temporal Decomposition

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Module boundaries drawn by *when* things happen in a process (e.g., `Initializer`, `Processor`, `Finalizer`) rather than *what* design decision each module hides |
| **Detection** | Multiple modules share the same data structure or state, each operating on it at a different stage. Module names describe process steps rather than owned concepts. The same type appears in the signatures of 3+ modules in sequence. |
| **Recommendation** | Redecompose by information hiding: each module should own one design decision (data representation, algorithm, I/O mechanism). The process ordering becomes an implementation detail of an orchestrator, not a module boundary. |

**Distinction from Mixed Concerns (1.1):** Mixed concerns is multiple layers *within* one file. Temporal decomposition is the opposite problem — code is split *across* files, but along the wrong axis (sequential steps instead of hidden decisions), so the modules look single-purpose but share state.

**Worked example:**
```
# Modules split by process step — all share the same OrderData structure
order_parser.py:     parse_raw_input(data) -> OrderData
order_validator.py:  validate(order: OrderData) -> OrderData
order_enricher.py:   enrich(order: OrderData) -> OrderData
order_persister.py:  save(order: OrderData)

Finding: 4 modules share OrderData and form a linear pipeline. None hides
         a design decision — changing OrderData's structure forces changes in all 4.
Recommendation: Decompose by what's hidden: OrderInput (owns parsing + validation),
                Order (owns domain logic + enrichment), OrderRepository (owns persistence).
                The pipeline sequence becomes internal to a coordinator.
```

## Level 2: Class / Type

Violations at the class or type boundary — cohesion, responsibility, and what data structures cross boundaries.

### 2.1 God Class

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Class with >7 public methods that cluster into 2+ groups accessing disjoint instance state |
| **Detection** | Build a method-to-field matrix: list which instance fields each method reads/writes. If methods form 2+ clusters with <30% field overlap between clusters, the class has multiple responsibilities. Entry thresholds: class >300 LOC, >7 public methods, or class name contains "Manager"/"Handler"/"Processor"/"Service" with 2+ unrelated verb groups (e.g., `create_*` + `send_*` + `calculate_*`). |
| **Recommendation** | Split along responsibility clusters. Each resulting class should have methods that share instance state. |

**Worked example:**
```
class OrderService:
  # Group A: order lifecycle (uses self.db, self.validator)
  create_order()
  update_order()
  cancel_order()
  validate_order()

  # Group B: pricing (uses self.tax_calculator, self.discount_engine)
  calculate_total()
  apply_discount()
  compute_tax()

  # Group C: notifications (uses self.email_client, self.sms_client)
  send_confirmation()
  send_cancellation()
  notify_status_change()

  Finding: 3 responsibility clusters with disjoint state.
  Recommendation: Split into OrderLifecycle, OrderPricing, OrderNotifier.
```

**When this is OK:** Facade classes that intentionally present a unified interface over multiple subsystems (e.g., `OrderFacade` delegating to `OrderLifecycle`, `OrderPricing`, `OrderNotifier`). Verify that the class *owns* no logic itself — if it does more than delegate, it's a god class wearing a facade label. Also acceptable for DI-wired orchestrators where method count is high but each method is a thin delegation with error handling or transaction management.

### 2.2 Low Cohesion

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Class methods divide into groups where each group accesses a disjoint set of instance variables |
| **Detection** | For each method, list which instance fields it reads or writes. If the field sets form distinct clusters with <30% overlap, cohesion is low. |
| **Recommendation** | Extract classes along cluster boundaries. Each new class owns its fields and the methods that operate on them. |

**Distinction from God Class:** A god class is obviously too large. Low cohesion can appear in a normal-sized class — 6 methods, 4 fields, but two groups of 3 methods that never touch the same fields.

### 2.3 Data Bag Crossing Boundary

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Plain data structure (no behavior) passed across module boundaries as parameter or return type |
| **Detection** | Type has only fields/properties and no meaningful methods (getters/setters don't count). It appears in function signatures of modules other than where it's defined. |
| **Recommendation** | Either: (a) add behavior to the type so it becomes a proper domain object, (b) define an interface that the consumer owns and the producer implements, or (c) if it genuinely is just data transfer, make it an explicit DTO at the boundary and keep the internal representation separate. |

**When this is OK:** DTOs at system boundaries (API request/response types, serialization models) are expected to be behavior-free. Only flag data bags that cross *internal* module boundaries.

### 2.4 Anemic Domain Model

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Data class paired with a service class where the service operates exclusively on the data class's fields |
| **Detection** | Service methods take the data class as parameter and access 3+ of its fields. The data class has no methods beyond accessors. Business rules live entirely in the service. |
| **Recommendation** | Move behavior into the domain class. The service should delegate to the domain object, not reach into its fields. |

**Worked example:**
```
class Order:                          # Data bag: fields only
  id, customer_id, items, status,
  discount_code, shipping_address

class OrderService:
  def calculate_total(self, order):   # Accesses order.items, order.discount_code
  def can_cancel(self, order):        # Accesses order.status, order.created_at
  def apply_discount(self, order):    # Accesses order.items, order.discount_code

  Finding: OrderService accesses 4+ Order fields across 3 methods. Business
           rules (total calculation, cancellation policy, discount logic) live
           in the service, not the domain object.
  Recommendation: Move calculate_total, can_cancel, apply_discount into Order.
```

## Level 3: Function / Interface

Violations at the function or method boundary — parameter design, return types, and whether interfaces express intent.

### 3.1 Large Parameter List

| | |
|---|---|
| **Confidence** | Clear (>6 params), Judgment (5-6 params) |
| **Signal** | Function takes many parameters |
| **Detection** | Count parameters. Exclude `self`/`this`/`cls`. |
| **Auto-fix (>6)** | Suggest introducing a parameter object or options type |
| **Recommendation (5-6)** | Evaluate whether parameters naturally group into a type |

**Exception:** Builder patterns, factory methods, and DI constructors may legitimately have many parameters. Flag as judgment regardless of count if the function name suggests these patterns.

### 3.2 Boolean / Flag Parameter

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Boolean parameter that switches between two substantially different code paths (each branch >10 LOC or calling different dependencies) |
| **Detection** | Boolean/flag parameter with `if flag:` or `switch` early in the body. Flag when: each branch is >10 LOC, or branches call different external dependencies, or branches have <30% shared logic. |
| **Recommendation** | Split into two functions named by intent. The boolean flag is the caller encoding a decision that should be made at a higher level. |

**Worked example:** `process_payment(amount, use_new_gateway=False)` where `use_new_gateway` switches between 20-line new gateway path and 25-line legacy path → split into `process_payment_v2()` and `process_payment_legacy()`.

**Not a violation:** `include_deleted=False` that adds one `WHERE` clause — minor variation, not a separate code path.

### 3.3 Internal Type in Public Signature

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Public function's parameter or return type uses a type that is internal to another module |
| **Detection** | Parameter/return type is defined in another module's internal/private namespace, or is a framework-specific type (ORM model, HTTP request object) appearing in a domain/business function's signature. |
| **Recommendation** | Accept a domain type or interface instead. The caller should not need to know the implementation's type system. |

### 3.4 Implementation-Shaped Interface

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Public method names describe implementation steps rather than user intent |
| **Detection** | Method names contain implementation verbs: `queryDatabaseFor...`, `serializeToJson...`, `callApiFor...`, `parseXmlFrom...`. The name tells you *how* it works, not *what* it does. |
| **Recommendation** | Rename to express intent: `findUser` not `queryDatabaseForUser`, `export` not `serializeToJson`. The interface should survive an implementation change. |

**Litmus test:** "If I replaced the implementation (swapped DB for cache, JSON for protobuf), would this method name still make sense?" If no, it's implementation-shaped.

### 3.5 Leaky Return Type

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Function returns an implementation-specific type (ORM model, framework response, raw DB row) across a module boundary |
| **Detection** | Return type is framework-specific (e.g., SQLAlchemy model, Mongoose document, ActiveRecord object) and the function is consumed by modules that shouldn't depend on that framework. |
| **Recommendation** | Return a domain type or DTO. Map from the internal type at the boundary. |

### 3.6 Fat Interface (ISP Violation)

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Interface/abstract class/protocol with many methods, where concrete clients use only a subset |
| **Detection** | An interface has N methods, but implementations throw `NotImplementedError` / `UnsupportedOperationException` for some. Or: consumers of the interface only call a subset of its methods (grep call sites). Or: interface name contains "And" or mixes unrelated verb groups (e.g., `UserAuthAndPreferences`). |
| **Recommendation** | Split into smaller, client-specific interfaces. Each interface should represent one role the implementer plays for a specific consumer. |

**Worked example:**
```
interface OrderOperations:
  create_order()
  update_order()
  delete_order()
  calculate_total()
  apply_discount()
  generate_invoice()
  send_notification()

Consumer A (checkout flow): calls create_order, calculate_total, apply_discount
Consumer B (admin panel):   calls update_order, delete_order
Consumer C (billing):       calls generate_invoice, send_notification

Finding: 3 consumers each use 2-3 of 7 methods. Each consumer is coupled to
         methods it never calls — a change to send_notification forces Consumer A
         to recompile/redeploy despite never using it.
Recommendation: Split into OrderLifecycle (create/update/delete),
                OrderPricing (calculate/discount), OrderFulfillment (invoice/notify).
```

**When this is OK:** Standard CRUD interfaces (`Repository<T>` with find/save/delete) are acceptable if all methods are used by most clients. Only flag when usage analysis shows clear subset patterns.

### 3.7 Pass-Through Method

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Method that does nothing except delegate to another method with the same or nearly the same arguments — adds no logic, no transformation, no error handling |
| **Detection** | Method body is a single call to another method. Parameters are forwarded unchanged (or with trivial renaming). The method adds no branching, no validation, no mapping, and no error handling. |
| **Recommendation** | Remove the pass-through and let callers use the underlying method directly. If the pass-through exists for abstraction, it should add depth — error handling, caching, default arguments, or translation between domains. |

**Worked example:** `UserService.get_user()` → `self.user_repository.get_user()`, `save_user()` → `self.user_repository.save_user()` — 3 methods, all pure delegation. The class adds interface complexity without hiding anything → either remove or add depth (validation, caching, access control).

**Not a violation:** Facade/adapter patterns that intentionally wrap another interface. Flag only when the wrapper adds zero depth across *all* its methods. If some methods add logic and others don't, flag only the pass-throughs.

## Level 4: Cross-Boundary

Violations in how modules interact — dependency direction, coupling, and what knowledge crosses boundaries.

### 4.1 Reaching Into Internals

| | |
|---|---|
| **Confidence** | Clear (language-enforced paths), Judgment (convention-based) |
| **Signal** | Module A imports from Module B's internal/private submodules, bypassing B's public API |
| **Detection** | Import paths contain `internal`, `_private`, `impl`, or target files that aren't part of B's entry point. Also detect: importing a submodule's helper that isn't re-exported by the parent. |
| **Auto-fix** | If the needed functionality exists in B's public API, switch the import |
| **Recommendation** | If it doesn't exist in B's public API, either add it to B's public surface or question whether A should depend on B at all |

**Worked example:**
```
# src/billing/calculator.py imports from orders' internals:
from src.orders._internal.tax_utils import calculate_tax_rate
from src.orders._internal.discount import apply_volume_discount

# src/orders/__init__.py (public API) exports:
from .service import OrderService, Order, OrderStatus

Finding: billing imports 2 items from orders._internal that aren't in orders' public API.
Auto-fix: If OrderService exposes equivalent methods → switch imports.
Recommendation: If not → add calculate_tax_rate to orders' public surface,
                or question whether billing should compute tax independently.
```

### 4.2 Circular Dependency

| | |
|---|---|
| **Confidence** | Clear (detection), Judgment (fix) |
| **Signal** | Module A imports Module B, and Module B imports Module A (directly or transitively) |
| **Detection** | Trace import chains. Direct cycles are obvious. Transitive cycles (A→B→C→A) require following the chain. |
| **Recommendation** | Three resolution strategies: (1) Extract shared concern into a third module that both depend on. (2) Apply dependency inversion — define an interface in the depended-upon module, implement it in the other. (3) Merge the modules if they are genuinely one concern that was artificially split. |

**Worked example:**
```
src/billing/service.py → imports → src/orders/service.py (OrderService.get_total)
src/orders/service.py  → imports → src/billing/service.py (BillingService.has_credit)

Finding: Direct circular dependency between billing and orders.
Resolution options:
  (1) Extract: Create src/credit/service.py owning has_credit() — both import from credit.
  (2) Invert: Define CreditChecker interface in orders, implement in billing.
  (3) Merge: If billing and orders are truly one concern, combine into one module.
```

### 4.3 Feature Envy

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Method in class/module A primarily accesses data from class/module B |
| **Detection** | Method references 3+ fields/methods of another class/module and at most 1 of its own. The method "envies" the other class's data. |
| **Recommendation** | Move the method to the class it envies. If it needs data from both, consider whether the method reveals a missing abstraction that should own the combined data. |

**Worked example:**
```
class InvoiceGenerator:
  def format_customer_address(self, customer):
    return f"{customer.name}\n{customer.street}\n{customer.city}, {customer.state} {customer.zip}"

Finding: format_customer_address accesses 5 Customer fields and 0 InvoiceGenerator fields.
Recommendation: Move to Customer as formatted_address() or address_block().
```

### 4.4 Transitive Dependency Exposure

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Module A's public API returns or requires types from Module C, which A only knows about through Module B |
| **Detection** | Public function signature uses a type that isn't defined in A or in A's direct dependency's public API — it leaks from a transitive dependency. |
| **Recommendation** | Wrap in A's own types at the boundary. Consumers of A should not need to know about C. |

**Worked example:**
```
# src/api/handlers.py
from src.billing import BillingService

def get_invoice(request):
    invoice = BillingService.get_invoice(request.id)
    return invoice  # Returns src.billing.db.models.InvoiceRow (ORM model)

# api → billing → billing.db.models (transitive dependency)
# If billing swaps its ORM, api breaks despite having no direct relationship with billing.db.

Finding: api's get_invoice leaks a type from billing's transitive dependency (billing.db.models).
Recommendation: BillingService.get_invoice should return an Invoice domain type or DTO.
                Map from InvoiceRow → Invoice at billing's boundary.
```

### 4.5 Law of Demeter Violation

| | |
|---|---|
| **Confidence** | Judgment |
| **Signal** | Method navigates through an object graph to reach a distant collaborator (depth 2+) |
| **Detection** | A method `M` on object `O` calls methods on objects that are NOT: (1) `O` itself, (2) arguments to `M`, (3) instance fields of `O`, (4) objects created within `M`. Concrete pattern: `a.getB().getC().doSomething()` — intermediate calls return domain objects, not `this`. Also detect the disguised form spread across variables: `b = a.getB(); c = b.getC(); c.doSomething()`. |
| **Recommendation** | Apply "tell, don't ask": ask the nearest object to do the work instead of reaching through it. Move the operation to the object that owns the data. |

**Worked example:**
```
def calculate_shipping(order):
  city = order.get_customer().get_address().get_city()    # depth 3: order → customer → address → city
  if city in FREE_SHIPPING_CITIES:
    return 0
  return order.get_items().get_total_weight() * RATE_PER_KG  # depth 2: order → items → weight

Finding: calculate_shipping navigates 3 levels deep into order's internal structure.
         It knows that Order has a Customer, Customer has an Address, Address has a city.
         A change to any of these structures breaks this function.
Recommendation: Ask order directly: order.get_shipping_city() or order.calculate_shipping().
                The internal object graph is Order's secret, not the caller's business.
```

**Common false positives — do NOT flag these:**

| Pattern | Why it's OK |
|---|---|
| Fluent APIs / builders | `query.select("x").where("y").limit(10)` returns `this`, not a new object — no graph traversal |
| Stream/collection pipelines | `list.stream().filter(...).map(...)` operates on a single collection, not nested domain objects |
| Value object / primitive chains | `string.trim().toLowerCase()` — value objects have no encapsulation boundary to violate |
| Optional/Result chaining | `result.map(...).orElse(...)` — monadic composition, not object graph traversal |

## Summary Table

Quick reference for all violations:

| ID | Violation | Level | Confidence | Auto-fixable? |
|----|-----------|-------|------------|---------------|
| 1.1 | Mixed concerns | Module | Judgment | No |
| 1.2 | Over-exposed module | Module | Judgment | No |
| 1.3 | Barrel re-export | Module | Clear | Yes |
| 1.4 | Missing public API surface | Module | Judgment | No |
| 1.5 | Temporal decomposition | Module | Judgment | No |
| 2.1 | God class | Class | Judgment | No |
| 2.2 | Low cohesion | Class | Judgment | No |
| 2.3 | Data bag crossing boundary | Class | Judgment | No |
| 2.4 | Anemic domain model | Class | Judgment | No |
| 3.1 | Large parameter list | Function | Clear/Judgment | Partial |
| 3.2 | Boolean/flag parameter | Function | Judgment | No |
| 3.3 | Internal type in public signature | Function | Judgment | No |
| 3.4 | Implementation-shaped interface | Function | Judgment | No |
| 3.5 | Leaky return type | Function | Judgment | No |
| 3.6 | Fat interface (ISP) | Function | Judgment | No |
| 3.7 | Pass-through method | Function | Judgment | No |
| 4.1 | Reaching into internals | Cross-boundary | Clear/Judgment | Partial |
| 4.2 | Circular dependency | Cross-boundary | Clear/Judgment | No |
| 4.3 | Feature envy | Cross-boundary | Judgment | No |
| 4.4 | Transitive dependency exposure | Cross-boundary | Judgment | No |
| 4.5 | Law of Demeter violation | Cross-boundary | Judgment | No |
