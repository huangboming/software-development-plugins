# Shared Quality Standards

Standards used across all review modes for finding format, severity classification, verification, and reporting.

## Finding Format

Format every finding as:

```
**[Severity] <Pattern/Issue Name>**
Location: `path/to/file.py:42`, `path/to/other.py:18`
Issue: <What the issue is, concretely>
Risk: <What can go wrong and under what conditions>
Fix: <Specific, actionable recommendation>
```

**Examples:**

```
**[High] N+1 Query Pattern**
Location: `src/orders/service.py:87`
Issue: `get_order_details()` iterates over orders and calls
  `db.query(OrderItem).filter(order_id=order.id)` per iteration.
Risk: 100 orders → 101 queries. Response time degrades linearly with
  data growth — p99 will exceed SLA within ~3 months at current rate.
Fix: Use `joinedload(Order.items)` to fetch all items in one JOIN query.
```

```
**[Critical] Missing Authorization Check (BOLA)**
Location: `src/api/invoices.py:23`, `src/api/invoices.py:47`
Issue: `get_invoice()` and `delete_invoice()` query by `invoice_id`
  from the URL path without filtering by the authenticated user.
Risk: (Inferred) Any authenticated user can read or delete any invoice
  by guessing sequential IDs — verify auth middleware does not handle this.
Fix: Add `user_id=current_user.id` filter to both queries.
```

## Severity Definitions

| Severity | Definition |
|----------|-----------|
| **Critical** | Systemic issue blocking correctness or scaling |
| **High** | Significant maintainability or reliability risk |
| **Medium** | Developer experience issue or tech debt |
| **Low** | Convention issue, no immediate risk |

## Verification Checklist

Before writing the report, apply to every finding:

1. Cites a specific `file:line` location — remove findings without evidence
2. Not a duplicate — consolidate findings describing the same underlying issue
3. Severity is consistent with the definitions above
4. For Critical or High findings, re-read the cited code to confirm the issue is real
5. Pervasive patterns flagged once with a representative example, not per-instance

Revise or remove any finding that fails a check.

## Report Standards

- Ground every finding in specific files and line numbers
- Label inferred risks explicitly as "Inferred" — distinguish from confirmed issues
- Recommend the smallest change that addresses each risk
- Omit dimensions that do not apply to this codebase
- Report honestly — if the codebase is solid, say so
