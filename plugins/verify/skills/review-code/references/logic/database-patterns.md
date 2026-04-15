# Database Usage Patterns & Anti-Patterns

Detection catalog for implementation review. Each entry: pattern name, detection heuristic, severity, risk.

## Table of Contents

- [Query Patterns](#query-patterns)
- [Transaction Handling](#transaction-handling)
- [Schema & Migrations](#schema--migrations)
- [Connection Management](#connection-management)
- [Data Integrity](#data-integrity)

---

## Query Patterns

### N+1 Queries

- **Detect**: Loop that executes a query per iteration; ORM access to related objects inside a loop without eager loading; `SELECT` inside `for row in results`; missing `select_related` / `prefetch_related` (Django), `includes` (Rails/Prisma), `Preload` / `Joins` (GORM), `joinRelated` (Objection)
- **Severity**: Critical
- **Risk**: Linear query growth with data size; latency spikes; database connection exhaustion under load
- **Fix**: Eager load relations; batch queries; use JOINs or subqueries

### SELECT * in Production Code

- **Detect**: `SELECT *` in queries; ORM calls without explicit column selection on large tables
- **Severity**: Medium
- **Risk**: Fetches unnecessary data; breaks when columns added; prevents covering index optimization; wastes memory and bandwidth

### Missing WHERE Clauses

- **Detect**: `UPDATE` or `DELETE` without `WHERE`; ORM `.update()` or `.delete()` without filter
- **Severity**: Critical
- **Risk**: Accidental data modification or deletion of entire table

### Unparameterized Queries

- **Detect**: String concatenation or interpolation in SQL: `f"SELECT * FROM users WHERE id = {user_id}"`; `"... WHERE name = '" + name + "'"`
- **Severity**: Critical
- **Risk**: SQL injection vulnerability; data breach; data destruction
- **Fix**: Use parameterized queries / prepared statements in all cases

### Expensive Queries Without LIMIT

- **Detect**: Aggregations (`COUNT`, `SUM`, `GROUP BY`) on unbounded result sets; full table scans for analytics in request path
- **Severity**: High
- **Risk**: Query duration grows with data; blocks other queries; timeout under load
- **Fix**: Add `LIMIT`; move analytics to background jobs or materialized views

### Missing Indexes

- **Detect**: `WHERE` clause on column without index; `JOIN` on non-indexed foreign key; `ORDER BY` on unindexed column; slow query patterns in code without corresponding index migration
- **Severity**: High
- **Risk**: Full table scans; degrading performance as data grows; query timeouts

### Over-Indexing

- **Detect**: Index on every column; indexes on low-cardinality columns (booleans, status enums with 3 values); redundant composite indexes
- **Severity**: Low–Medium
- **Risk**: Write performance degradation; increased storage; index maintenance overhead

---

## Transaction Handling

### Missing Transaction Boundaries

- **Detect**: Multiple related writes without transaction wrapping; create parent + children in separate queries without atomicity; money transfer with separate debit/credit queries
- **Severity**: Critical
- **Risk**: Partial writes on failure; data inconsistency; lost updates

### Overly Broad Transactions

- **Detect**: Transaction wrapping entire request lifecycle; HTTP calls or external API calls inside transaction; file I/O inside transaction; long-running computations inside transaction
- **Severity**: High
- **Risk**: Lock contention; connection pool exhaustion; deadlocks; external call failures holding locks

### Missing Rollback on Error

- **Detect**: `BEGIN` without corresponding `ROLLBACK` in error path; manual transaction management without try/finally; ORM transaction context not using context manager
- **Severity**: High
- **Risk**: Abandoned transactions hold locks; connection leaks; data corruption

### Nested Transaction Confusion

- **Detect**: `@transaction.atomic` inside another `@transaction.atomic` without understanding savepoint behavior; nested `BEGIN` statements
- **Severity**: Medium
- **Risk**: Unexpected rollback scope; partial commits when inner transaction fails

### Read Operations Inside Write Transactions

- **Detect**: Read-only queries (reports, searches) wrapped in write transactions
- **Severity**: Low–Medium
- **Risk**: Unnecessary lock acquisition; reduced concurrency; potential deadlocks

---

## Schema & Migrations

### Unsafe Migration Patterns

- **Detect**: `ALTER TABLE ... ADD COLUMN ... NOT NULL` without default on large table; `CREATE INDEX` without `CONCURRENTLY` (Postgres); renaming columns in use; dropping columns without deprecation period
- **Severity**: High
- **Risk**: Table locks during migration; downtime; failed deployments; broken running code

### Missing Foreign Key Constraints

- **Detect**: `_id` columns without `REFERENCES`; ORM relationships defined only in code, not in schema; orphan records possible
- **Severity**: Medium
- **Risk**: Data integrity violations; orphaned records; inconsistent state

### No Soft Delete Strategy

- **Detect**: `DELETE FROM` for user-facing data without audit trail; no `deleted_at` column or equivalent; no archival pattern
- **Severity**: Medium (context-dependent)
- **Risk**: Irrecoverable data loss; compliance violations; broken references from other tables

### Missing Timestamps

- **Detect**: Tables without `created_at` / `updated_at` columns; no audit trail for when records change
- **Severity**: Low
- **Risk**: Debugging difficulty; no way to order by recency; compliance gaps

---

## Connection Management

### No Connection Pooling

- **Detect**: New database connection created per request; `connect()` / `createConnection()` called directly in request handlers
- **Severity**: High
- **Risk**: Connection exhaustion under load; high latency from connection setup; database max_connections hit

### Connection Leak

- **Detect**: Connection acquired but not released in error paths; missing `finally` / `defer` / context manager for connection cleanup; pooled connection not returned
- **Severity**: Critical
- **Risk**: Pool exhaustion; application hangs; requires restart to recover

### No Connection Timeout

- **Detect**: Database connection or query without timeout configuration; no `statement_timeout` or equivalent
- **Severity**: Medium
- **Risk**: Runaway queries consume connections indefinitely; cascading failures

### Hardcoded Connection Strings

- **Detect**: Database URL with credentials in source code; `host=localhost password=secret` in config files
- **Severity**: Critical
- **Risk**: Credential exposure; cannot rotate without code change; environment mismatch

---

## Data Integrity

### Race Conditions in Read-Modify-Write

- **Detect**: Read value, compute new value, write back without optimistic locking or `SELECT ... FOR UPDATE`; counter increment without atomic operation; `UPDATE SET balance = balance - amount` pattern missing in favor of read-then-write
- **Severity**: High
- **Risk**: Lost updates under concurrency; incorrect balances; data corruption

### Missing Unique Constraints

- **Detect**: Business-unique fields (email, slug, code) without `UNIQUE` constraint; uniqueness enforced only in application code
- **Severity**: High
- **Risk**: Duplicate records under concurrent requests; data quality degradation

### Storing Derived Data Without Sync

- **Detect**: Computed/cached values stored in DB without refresh mechanism; denormalized counts or totals without triggers or background sync
- **Severity**: Medium
- **Risk**: Stale derived data; silent inconsistency between source and cached values
