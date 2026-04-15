# Codebase Exploration Guide

Use this guide when reverse-engineering requirements from an existing codebase. The goal is to translate implementation details into user-facing behavior.

## Exploration Priority Order

Explore in this order — earlier sources yield higher-confidence requirements:

1. **Entry points and routes** — reveal what actions users can perform
2. **Data models and schemas** — entities and relationships encode the domain model and business rules
3. **Validation and business logic** — constraints imply user-facing rules (e.g., `if age < 18` → "Users must be 18 or older to register")
4. **UI components and views** — screen structure reveals user-facing features and flows
5. **Tests** — test descriptions and assertions are often the closest thing to written requirements
6. **Error handling** — error messages and recovery paths reveal edge cases the product was designed to handle
7. **Configuration and feature flags** — reveal optional behaviors and variants

## Translating Code Patterns to Requirements

When you find these patterns in code, express the inferred requirement from the user's perspective. The right column shows how to frame each pattern as a user-facing requirement:

| Code Pattern | Requirement (user terms) | Example |
|---|---|---|
| Input validation (length, format, range) | Data entry rules the user must follow | "Email addresses must be in valid format" |
| Authentication/authorization checks | Role-based access permissions | "Only team admins can invite new members" |
| Retry logic, circuit breakers | Availability and graceful recovery | "The service remains usable during partial outages" |
| Caching layers | Fast responses for repeated actions | "Previously viewed dashboards load instantly" |
| Audit logging | Accountability and compliance tracking | "All changes to billing are recorded with who and when" |
| Pagination | Incremental browsing of large result sets | "Users can page through search results 20 at a time" |
| Rate limiting | Fair usage limits | "Each account can send up to 100 invites per day" |
| Soft deletes | Recoverability of deleted items | "Deleted projects can be restored within 30 days" |
| Internationalization (i18n) | Multi-language support | "The interface is available in English, Spanish, and French" |
| Webhook/event dispatching | Event notifications | "Users receive a notification when their report is ready" |
