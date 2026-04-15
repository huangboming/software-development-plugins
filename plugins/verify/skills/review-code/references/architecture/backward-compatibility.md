# Backward Compatibility

Detection catalog for architecture review. Each entry: pattern name, detection heuristic, severity, risk.

## Table of Contents

- [API Contract Evolution](#api-contract-evolution)
- [Database Schema Migration Safety](#database-schema-migration-safety)
- [Event & Message Schema Evolution](#event--message-schema-evolution)
- [Configuration & Dependency Changes](#configuration--dependency-changes)

---

## API Contract Evolution

### Breaking Response Shape Changes

- **Detect**: Fields renamed or removed from API responses; response type changed (object → array, string → number); nullable field made non-nullable; enum values removed
- **Severity**: Critical
- **Risk**: Existing clients break silently or crash; mobile apps in the wild cannot be force-updated
- **Safe alternative**: Add new fields, deprecate old ones; keep both until all consumers migrate

### Breaking Request Contract Changes

- **Detect**: New required fields added to request body; optional field made required; accepted value range narrowed; content type changed
- **Severity**: Critical
- **Risk**: Existing client requests rejected; integrations fail without code changes on the client side

### Endpoint Removal or Rename

- **Detect**: Route handler deleted or path changed without redirect/alias; HTTP method changed (POST → PUT)
- **Severity**: Critical
- **Risk**: Existing clients get 404/405; no migration path for consumers

### Missing Deprecation Strategy

- **Detect**: No versioning scheme (URL prefix, header, or content negotiation); no `Sunset` or `Deprecated` headers; breaking changes shipped in the same version; no documentation of deprecation timeline
- **Severity**: High
- **Risk**: Consumers have no warning before breakage; no way to migrate incrementally

### Status Code Semantic Changes

- **Detect**: Success response code changed (200 → 201, 200 → 204); error code changed for the same condition (400 → 422); clients rely on specific codes for control flow
- **Severity**: Medium
- **Risk**: Client-side branching logic breaks; retry behavior changes unexpectedly

---

## Database Schema Migration Safety

### Non-Additive Schema Changes Under Rolling Deployment

- **Detect**: Column rename (old code reads old name, new code reads new name — both run simultaneously during deploy); column removal while old code still references it; type change that invalidates existing data
- **Severity**: Critical
- **Risk**: Rolling deployment means old and new code coexist — non-additive changes cause errors for whichever version doesn't match the schema

### Locking Migrations on Large Tables

- **Detect**: `ALTER TABLE ... ADD COLUMN ... NOT NULL` without default; `CREATE INDEX` without `CONCURRENTLY` (Postgres); `ALTER TABLE ... MODIFY COLUMN` on high-traffic tables; any DDL that acquires `ACCESS EXCLUSIVE` lock
- **Severity**: High
- **Risk**: Table locked during migration; reads and writes blocked; downtime proportional to table size

### Safe Migration Patterns (what to look for)

The expand-contract pattern enables zero-downtime schema evolution:

1. **Expand**: Add new column/table (nullable or with default); deploy code that writes to both old and new
2. **Migrate**: Backfill existing data from old to new
3. **Contract**: Remove old column/table once all code reads from new only

**Red flags** that expand-contract is not being followed:
- Single migration that both adds and removes columns
- No backfill step between schema change and code change
- Migration and code change deployed in the same release with no intermediate state

### Foreign Key Changes Breaking Referential Integrity

- **Detect**: Foreign key constraint added to existing column without data cleanup; constraint dropped without understanding downstream impact; cascade delete added to a high-traffic parent table
- **Severity**: High
- **Risk**: Migration fails on existing invalid data; cascade deletes remove unexpected rows

### Irreversible Migrations

- **Detect**: `DROP TABLE`, `DROP COLUMN` with no backup or reversibility plan; data-destructive `UPDATE` without `WHERE` clause in migration; `TRUNCATE` in migration
- **Severity**: Critical
- **Risk**: Cannot roll back if the deploy fails; data loss is permanent

---

## Event & Message Schema Evolution

### Breaking Event Schema Changes

- **Detect**: Fields removed from published events; field types changed; required fields added without default; event name/topic renamed
- **Severity**: Critical
- **Risk**: Existing consumers fail to deserialize; events silently dropped or land in dead-letter queues

### Missing Schema Registry or Contract Testing

- **Detect**: Event schemas defined only in code (no schema registry, no Avro/Protobuf/JSON Schema); no consumer-driven contract tests; producers and consumers in different repos with no shared schema artifact
- **Severity**: High
- **Risk**: Schema drift between producer and consumer goes undetected until runtime failure

### Consumer Compatibility Not Verified

- **Detect**: Producer schema change deployed without verifying all consumers can handle the new shape; no forward-compatibility check; consumers use strict deserialization (fail on unknown fields)
- **Severity**: High
- **Risk**: Downstream consumers crash on unknown fields or missing fields; cascading failures across services

### Safe Event Evolution Patterns

- Add optional fields with defaults (forward-compatible)
- Never remove or rename fields in active schemas — deprecate and add new
- Use schema versioning: `event.v1`, `event.v2` with parallel publishing during migration
- Consumers should tolerate unknown fields (open-world assumption)

---

## Configuration & Dependency Changes

### Environment Variable Removal or Rename

- **Detect**: `os.environ["OLD_VAR"]` replaced with `os.environ["NEW_VAR"]`; config key renamed without fallback; required env var added without documentation or default
- **Severity**: High
- **Risk**: Existing deployments fail on startup; ops team unaware of new requirements; rolling deployments break when old instances read old config

### Feature Flag Rollout Without Backward Compatibility

- **Detect**: Feature flag guards removed before 100% rollout confirmed; behavior change deployed without flag; flag defaults changed from off to on without gradual rollout
- **Severity**: Medium
- **Risk**: Abrupt behavior change for all users; cannot roll back without redeploy

### Dependency Version Bumps With Breaking Changes

- **Detect**: Major version bump in dependencies (semver breaking change); library API used in ways that changed between versions; transitive dependency conflicts introduced
- **Severity**: Medium–High
- **Risk**: Build failures; runtime behavior changes; subtle bugs from API semantic changes
