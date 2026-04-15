# Backend Security Review Checklist

Detection catalog for implementation review. Each entry: pattern name, detection heuristic, severity, risk.

## Table of Contents

- [Injection](#injection)
- [Authentication](#authentication)
- [Authorization](#authorization)
- [Input Validation](#input-validation)
- [Secrets Management](#secrets-management)
- [Data Exposure](#data-exposure)
- [Rate Limiting & DoS](#rate-limiting--dos)
- [CORS & Headers](#cors--headers)
- [Cryptography](#cryptography)
- [Logging & Monitoring](#logging--monitoring)

---

## Injection

### SQL Injection

- **Detect**: String concatenation/interpolation in SQL queries; `f"SELECT ... WHERE id = {id}"`, `"... WHERE name = '" + name + "'"`, `fmt.Sprintf("... WHERE id = %s", id)` passed to query functions
- **Severity**: Critical
- **Risk**: Full database compromise; data exfiltration; data destruction; privilege escalation

### Command Injection

- **Detect**: User input passed to `os.system()`, `subprocess.call(shell=True)`, `exec.Command()` with string interpolation; unsanitized input in shell commands
- **Severity**: Critical
- **Risk**: Remote code execution; server takeover

### Template Injection (SSTI)

- **Detect**: User input rendered directly in server-side templates; `render_template_string(user_input)`, `Template(user_input).render()`
- **Severity**: Critical
- **Risk**: Remote code execution via template engine

### NoSQL Injection

- **Detect**: User input passed directly as MongoDB query operators; `{"$gt": ""}` accepted from request; unsanitized objects in query filters
- **Severity**: High
- **Risk**: Authentication bypass; data exfiltration

### Path Traversal

- **Detect**: User input used in file paths without sanitization; `open(f"/uploads/{filename}")` where filename comes from request; no check for `../`
- **Severity**: High
- **Risk**: Reading arbitrary files; accessing sensitive configuration; potential RCE via file upload

---

## Authentication

### Broken Authentication Flow

- **Detect**: Custom password hashing (not bcrypt/argon2/scrypt); plaintext password storage or comparison; no password complexity requirements; no account lockout after failed attempts
- **Severity**: Critical
- **Risk**: Credential compromise; brute force attacks succeed

### Insecure Token Management

- **Detect**: JWT with `none` algorithm accepted; tokens that never expire; refresh tokens without rotation; tokens stored in localStorage (XSS-accessible); no token revocation mechanism
- **Severity**: High
- **Risk**: Token theft enables persistent unauthorized access

### Missing Authentication on Endpoints

- **Detect**: API endpoints without auth middleware/decorators; admin operations accessible without login; internal endpoints exposed without auth
- **Severity**: Critical
- **Risk**: Unauthorized access to data and operations

### Session Fixation

- **Detect**: Session ID not regenerated after login; same session token before and after authentication
- **Severity**: High
- **Risk**: Attacker can fix a session ID and hijack after user authenticates

---

## Authorization

### Broken Access Control (IDOR)

- **Detect**: Object access by user-supplied ID without ownership check; `GET /api/orders/{id}` returns any order regardless of authenticated user; `User.objects.get(id=request.params['id'])` without filtering by current user
- **Severity**: Critical
- **Risk**: Users access other users' data; horizontal privilege escalation

### Missing Role/Permission Checks

- **Detect**: Admin operations without role verification; destructive actions (delete, modify) without permission check; relying solely on UI to hide admin features
- **Severity**: Critical
- **Risk**: Vertical privilege escalation; unauthorized operations

### Client-Side Authorization

- **Detect**: Authorization logic only in frontend; API trusts `role` field from request body; no server-side permission verification
- **Severity**: Critical
- **Risk**: Trivially bypassed; any authenticated user gains admin access

---

## Input Validation

### Missing Input Validation

- **Detect**: Request body fields used without type or presence checks; no schema validation library (Pydantic, Zod, Joi); raw `request.body` or `request.json()` used directly
- **Severity**: High
- **Risk**: Type confusion errors; unexpected behavior; potential injection vectors

### Insufficient Validation

- **Detect**: Length limits missing on string fields; numeric ranges not enforced; email/URL format not validated; file upload size/type unchecked
- **Severity**: Medium
- **Risk**: Buffer abuse; storage exhaustion; malicious file upload; invalid data in database

### Mass Assignment / Over-Posting

- **Detect**: Request body spread directly into model: `User.create(**request.json)`, `Object.assign(user, req.body)`, `user.update(request.data)` without allowlisted fields
- **Severity**: High
- **Risk**: Attacker sets `is_admin=true`, `role=admin`, `balance=999999`

### Missing Content-Type Validation

- **Detect**: Endpoint accepts any content type; no check for `Content-Type: application/json`; XML parsing enabled by default
- **Severity**: Medium
- **Risk**: XXE attacks via XML; unexpected parsing behavior

---

## Secrets Management

### Hardcoded Credentials

- **Detect**: Passwords, API keys, tokens as string literals in source code; `password = "mysecret"`; database URLs with embedded credentials
- **Severity**: Critical
- **Risk**: Credential exposure in version control; cannot rotate without deploy

### Secrets in Logs

- **Detect**: Request/response logging that includes auth headers, tokens, passwords, or API keys; `logger.info(f"Request: {request.headers}")`
- **Severity**: High
- **Risk**: Credentials exposed in log aggregation systems; persistent exposure

### Secrets in Error Responses

- **Detect**: Error handlers that include environment variables, config values, or connection strings in responses
- **Severity**: High
- **Risk**: Credential disclosure to clients; aids reconnaissance

### Missing Environment Variable Usage

- **Detect**: Configuration values hardcoded instead of read from environment; no `.env` support; no config management
- **Severity**: Medium
- **Risk**: Different environments share credentials; difficult rotation

---

## Data Exposure

### Over-Fetching / Verbose Responses

- **Detect**: API returns full database model including internal fields (password hash, internal IDs, metadata); no response serializer/DTO filtering
- **Severity**: High
- **Risk**: Sensitive data leakage; internal implementation exposed to clients

### PII in URLs

- **Detect**: Email, SSN, phone number, or other PII in URL path or query parameters; `GET /users?email=user@example.com`
- **Severity**: Medium
- **Risk**: PII logged in access logs, browser history, referrer headers

### Missing Data Encryption

- **Detect**: Sensitive fields (SSN, credit card, health data) stored in plaintext; no encryption-at-rest for PII columns
- **Severity**: High (for regulated data)
- **Risk**: Data breach exposure; compliance violations (GDPR, HIPAA, PCI-DSS)

---

## Rate Limiting & DoS

### No Rate Limiting

- **Detect**: No rate limiter middleware; no `429 Too Many Requests` responses; authentication endpoints without brute-force protection
- **Severity**: High
- **Risk**: Brute force attacks; credential stuffing; API abuse; resource exhaustion

### Unbounded Operations

- **Detect**: Endpoints that accept user-controlled batch sizes without limits; file upload without size limit; query without result cap
- **Severity**: Medium
- **Risk**: Memory exhaustion; CPU abuse; storage filling; denial of service

### Missing Timeout on External Calls

- **Detect**: HTTP client calls without timeout; database queries without statement timeout; no circuit breaker for downstream services
- **Severity**: High
- **Risk**: Thread/connection exhaustion from slow external services; cascading failures

---

## CORS & Headers

### Overly Permissive CORS

- **Detect**: `Access-Control-Allow-Origin: *` with credentials; origin reflected without allowlist; wildcard CORS on authenticated endpoints
- **Severity**: High
- **Risk**: Cross-origin attacks; credential theft; unauthorized API access from malicious sites

### Missing Security Headers

- **Detect**: No `Strict-Transport-Security`; no `X-Content-Type-Options: nosniff`; no `X-Frame-Options`; no `Content-Security-Policy`
- **Severity**: Medium
- **Risk**: Clickjacking; MIME-type sniffing attacks; protocol downgrade attacks

### HTTP Without TLS Enforcement

- **Detect**: Application serves over HTTP without redirect to HTTPS; no HSTS header; mixed content
- **Severity**: High
- **Risk**: Man-in-the-middle attacks; credential interception; session hijacking

---

## Cryptography

### Weak Hashing Algorithms

- **Detect**: MD5 or SHA1 for password hashing; `hashlib.md5(password)`; custom crypto implementations
- **Severity**: Critical
- **Risk**: Passwords crackable with rainbow tables; collision attacks

### Insecure Random Number Generation

- **Detect**: `random.random()` (Python), `Math.random()` (JS), `rand()` (Go) for security-sensitive values (tokens, IDs, nonces)
- **Severity**: High
- **Risk**: Predictable tokens; session hijacking; CSRF bypass

### Hardcoded Encryption Keys / IVs

- **Detect**: Encryption key as string literal; fixed IV/nonce for AES; same key for all environments
- **Severity**: Critical
- **Risk**: Trivial decryption by anyone with source access

---

## Logging & Monitoring

### Missing Audit Logging

- **Detect**: No logging for authentication events (login, logout, failed attempts); no logging for authorization failures; no logging for data modifications; admin actions unlogged
- **Severity**: Medium
- **Risk**: Cannot detect or investigate security incidents; compliance violations

### Insufficient Error Logging

- **Detect**: Errors swallowed silently; catch blocks with no logging; `except: pass`; `catch (e) {}`
- **Severity**: Medium
- **Risk**: Silent failures; bugs go undetected; data corruption without alert

### Log Injection

- **Detect**: User input written directly to logs without sanitization; `logger.info(f"User: {username}")` where username contains newlines
- **Severity**: Medium
- **Risk**: Log forging; hiding attack evidence; exploiting log analysis tools
