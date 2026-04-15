# OWASP API Security Top 10 (2023) — Code Review Reference

Framework-specific detection patterns for the OWASP API Security Top 10.
Use this reference when reviewing API endpoints for security vulnerabilities.

## Table of Contents

- [Overview](#overview)
- [API1 — Broken Object Level Authorization (BOLA)](#api1--broken-object-level-authorization-bola)
- [API2 — Broken Authentication](#api2--broken-authentication)
- [API3 — Broken Object Property Level Authorization](#api3--broken-object-property-level-authorization)
- [API4 — Unrestricted Resource Consumption](#api4--unrestricted-resource-consumption)
- [API5 — Broken Function Level Authorization](#api5--broken-function-level-authorization)
- [API6 — Unrestricted Access to Sensitive Business Flows](#api6--unrestricted-access-to-sensitive-business-flows)
- [API7 — Server-Side Request Forgery (SSRF)](#api7--server-side-request-forgery-ssrf)
- [API8 — Security Misconfiguration](#api8--security-misconfiguration)
- [API9 — Improper Inventory Management](#api9--improper-inventory-management)
- [API10 — Unsafe Consumption of APIs](#api10--unsafe-consumption-of-apis)
- [Commonly Missed in Reviews](#commonly-missed-in-reviews)
- [Framework Quick-Reference](#framework-quick-reference)

---

## Overview

| ID | Name | Severity |
|----|------|----------|
| API1:2023 | Broken Object Level Authorization (BOLA/IDOR) | Critical |
| API2:2023 | Broken Authentication | Critical |
| API3:2023 | Broken Object Property Level Authorization | High |
| API4:2023 | Unrestricted Resource Consumption | High |
| API5:2023 | Broken Function Level Authorization | Critical |
| API6:2023 | Unrestricted Access to Sensitive Business Flows | High |
| API7:2023 | Server-Side Request Forgery (SSRF) | High |
| API8:2023 | Security Misconfiguration | Medium–High |
| API9:2023 | Improper Inventory Management | Medium |
| API10:2023 | Unsafe Consumption of APIs | High |

---

## API1 — Broken Object Level Authorization (BOLA)

Endpoint accepts an object ID from the client and queries it without verifying the caller owns or is authorized to access that object.

### Red Flags

- Route parameter (`{id}`) passed directly to DB query with no ownership check alongside `current_user`
- No cross-reference between DB object's owner field and authenticated user's identity
- Sequential integer IDs (enables enumeration) — UUIDs are safer
- Auth check at function entry but not per-object within a batch loop
- List endpoints accepting `user_id` filter from client instead of defaulting to authenticated user

### Detection by Framework

**Python — FastAPI**: Handler accepts path param but does NOT reference `current_user` in `.filter()`:
```python
# VULNERABLE
order = db.query(Order).filter(Order.id == order_id).first()
# SAFE
order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
```

**Python — Django DRF**: `get_queryset()` returns `.objects.all()` without `user=self.request.user`:
```python
# VULNERABLE
def get_queryset(self):
    return Order.objects.all()
# SAFE
def get_queryset(self):
    return Order.objects.filter(user=self.request.user)
```

**Node.js — Express**: DB lookup by `req.params.id` without `req.user.id`:
```javascript
// VULNERABLE
const invoice = await Invoice.findById(req.params.id);
// SAFE
const invoice = await Invoice.findOne({ _id: req.params.id, userId: req.user.id });
```

**Go — Gin**: GORM query without user filter:
```go
// VULNERABLE
db.First(&project, c.Param("id"))
// SAFE
db.Where("id = ? AND user_id = ?", c.Param("id"), userID).First(&project)
```

**Rust — Axum**: No `AuthUser` extractor or user filter in DB call:
```rust
// VULNERABLE — no user parameter
async fn get_order(Path(order_id): Path<Uuid>, State(db): State<DbPool>) -> impl IntoResponse { ... }
// SAFE — AuthUser extractor carries identity into query
async fn get_order(Path(order_id): Path<Uuid>, AuthUser(user): AuthUser, State(db): State<DbPool>) -> ... {
    db.get_order_for_user(order_id, user.id).await
}
```

---

## API2 — Broken Authentication

### Red Flags

- JWT `alg` field accepted from token header (algorithm confusion / `alg: none`)
- JWT secret is short or default (`"secret"`, `"jwt_secret"`)
- No token expiry (`exp`) check
- Passwords hashed with MD5, SHA-1, or unsalted SHA-256
- No account lockout or rate limiting on `/login`
- Tokens invalidated only client-side

### Detection by Framework

**Python — PyJWT/jose**: Algorithm not pinned:
```python
# VULNERABLE
payload = jwt.decode(token, SECRET, algorithms=jwt.get_unverified_header(token)["alg"])
# SAFE
payload = jwt.decode(token, SECRET, algorithms=["HS256"])
```

**Node.js — jsonwebtoken**: Missing `algorithms` option:
```javascript
// VULNERABLE
jwt.verify(token, secret);
// SAFE
jwt.verify(token, secret, { algorithms: ['HS256'] });
```

**Go — golang-jwt**: Signing method not checked:
```go
// VULNERABLE
jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) { return []byte(secret), nil })
// SAFE
jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
    if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
        return nil, fmt.Errorf("unexpected alg: %v", token.Header["alg"])
    }
    return []byte(secret), nil
})
```

**Rust — jsonwebtoken**: `Validation::default()` accepts any algorithm:
```rust
// VULNERABLE
let validation = Validation::default();
// SAFE
let mut validation = Validation::new(Algorithm::HS256);
validation.validate_exp = true;
```

---

## API3 — Broken Object Property Level Authorization

Two sub-patterns: **Mass Assignment** (client sets privileged fields) and **Excessive Data Exposure** (API returns internal fields).

### Red Flags (Mass Assignment)

- ORM model created directly from raw request body
- No explicit field allowlist for writes
- Fields like `role`, `is_admin`, `balance` writable from request

### Red Flags (Excessive Exposure)

- `fields = '__all__'` in serializers
- Full model returned as response without DTO filtering
- `password_hash`, `ssn`, `stripe_customer_id` in responses

### Detection by Framework

**Python — FastAPI**: Input schema includes privileged fields, `body.dict()` spread via `setattr`:
```python
# VULNERABLE
for field, value in body.dict().items():
    setattr(user, field, value)  # role="admin" accepted
```

**Python — Django DRF**: Serializer with `fields = '__all__'`

**Node.js**: `Model.create(req.body)` or `Object.assign(user, req.body)` without allowlist:
```javascript
// VULNERABLE
await User.findByIdAndUpdate(req.params.id, { ...req.body });
// SAFE
const allowed = ['name', 'email', 'bio'];
const updates = Object.fromEntries(Object.entries(req.body).filter(([k]) => allowed.includes(k)));
```

**Go**: Request struct includes `Role` field bound from JSON

**Rust**: Serde deserializes privileged fields — use `#[serde(skip_deserializing)]` on `role`

---

## API4 — Unrestricted Resource Consumption

### Red Flags

- No rate limiting on any endpoint (especially `/login`, `/register`, `/search`, file upload)
- No maximum on paginated `limit` parameter
- No payload size limit
- No timeout on expensive operations
- Bulk endpoints without item count caps

### Detection by Framework

- **FastAPI**: No `slowapi` decorator
- **Django**: No `django-ratelimit`
- **Express**: No `express-rate-limit`; check `express.json({ limit: ... })`
- **Gin**: No `golang.org/x/time/rate` middleware; check `http.MaxBytesReader`
- **Axum**: No `tower-governor` layer; check `RequestBodyLimitLayer`

---

## API5 — Broken Function Level Authorization

### Red Flags

- Admin endpoints reachable without role check
- HTTP method auth gaps: GET protected, DELETE/PUT on same resource is not
- Route group middleware not applied to all routes within the group
- Admin functionality accessible by changing HTTP verb

### Detection by Framework

**Express**: Middleware on individual routes but not on router group:
```javascript
// VULNERABLE: isAdmin only on GET
router.get('/admin/users', isAdmin, listUsers);
router.post('/admin/users', createUser);  // Missing isAdmin!
// SAFE: Apply to entire router
adminRouter.use(isAdmin);
```

**Gin**: Routes added outside the protected group:
```go
// SAFE
admin := r.Group("/admin")
admin.Use(AdminMiddleware())
{ admin.GET("/users", listUsers); admin.DELETE("/users/:id", deleteUser) }
// NEVER add r.DELETE("/admin/...") outside the group
```

**Axum**: Auth layer missing from nested router:
```rust
let admin_routes = Router::new()
    .route("/users", get(list_users).post(create_user))
    .layer(require_admin_layer());
let app = Router::new().nest("/admin", admin_routes);
```

---

## API6 — Unrestricted Access to Sensitive Business Flows

### Red Flags

- Purchase endpoints with no per-user limit
- Voting/rating callable unlimited times
- Referral/bonus without one-per-account enforcement
- Password reset generation with no rate limit
- No CAPTCHA on high-value flows

---

## API7 — Server-Side Request Forgery (SSRF)

### Red Flags

- Any endpoint accepting a URL parameter that the server fetches
- Webhook registration without URL validation
- Image/file import by URL without allowlist
- HTTP client follows redirects without post-redirect validation (SSRF via redirect chain)
- No check of resolved IP against private ranges: `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.169.254` (cloud metadata)

### Detection Pattern

Any of these without URL validation: `requests.get(user_url)`, `fetch(req.body.url)`, `http.Get(userURL)`, `reqwest::get(body.url)`

Safe pattern: validate scheme is `https`, resolve hostname, check IP is not in private ranges, maintain domain allowlist.

---

## API8 — Security Misconfiguration

### Red Flags

- `CORS: *` with credentials
- `DEBUG = True` in production
- Default credentials unchanged
- Swagger/OpenAPI UI exposed in production without auth
- Stack traces or DB errors in API responses
- `/admin`, `/.env`, `/actuator`, `/debug/pprof`, `/metrics` accessible without auth
- Missing security headers: `Content-Security-Policy`, `X-Content-Type-Options`, `Strict-Transport-Security`

---

## API9 — Improper Inventory Management

### Red Flags

- Multiple active API versions where old versions lack security controls added to new ones
- Endpoints in code not in OpenAPI docs (shadow APIs)
- `/beta/`, `/internal/`, `/debug/`, `/test/` paths reachable in production
- Auth added to v2 but not backported to v1

---

## API10 — Unsafe Consumption of APIs

### Red Flags

- Third-party API response passed directly to DB without schema validation
- SQL/NoSQL query built using fields from external API response
- HTML rendered from third-party content without sanitization
- No timeout on outbound API calls
- Webhook payloads processed without HMAC signature verification

```python
# VULNERABLE
external_data = requests.get("https://partner.com/api/data").json()
user = User(**external_data)
# SAFE
data = PartnerData(**requests.get("https://partner.com/api/data").json())  # Pydantic validation
```

---

## Commonly Missed in Reviews

1. **BOLA on list/filter endpoints** — Reviewers check `GET /orders/{id}` but miss `GET /orders?user_id=123`. Filter params that should default to the authenticated user must not be client-supplied.

2. **Mass assignment via ORM factories** — `User.objects.create(**request.data)` looks normal but accepts `is_admin=true`.

3. **JWT `alg` not pinned** — `jwt.decode(token, secret)` without `algorithms=[...]` may trust the token's own header.

4. **CORS `allow_credentials: true` with regex origins** — `*.example.com` matching is exploitable via `evilexample.com`. Use explicit string allowlist.

5. **Function-level auth gaps after refactoring** — Middleware stacks not carried over when routes are moved. Requires tracing full router hierarchy.

6. **Rate limiting only on `/login`** — `/password-reset`, `/register`, `/resend-verification`, and expensive search endpoints left open.

7. **Old API versions without security backports** — v1 endpoints remain live without auth added in v2.

8. **Webhook payloads without signature verification** — HMAC check (Stripe, GitHub pattern) skipped.

9. **Debug/internal endpoints in production** — Swagger UI, `/metrics`, `/debug/pprof` (Go), `/actuator` (Spring) accessible without auth.

10. **SSRF via redirect chains** — Even with URL allowlisting, HTTP clients following redirects allow `169.254.169.254` access via redirect.

---

## Framework Quick-Reference

| Vulnerability | FastAPI | Django DRF | Express | Gin | Axum |
|---|---|---|---|---|---|
| BOLA | No `current_user` in `.filter()` | `get_queryset()` returns `.all()` | No `userId` in DB query | No `user_id` in `.Where()` | No `AuthUser` extractor |
| Mass Assignment | `setattr` loop from `body.dict()` | `fields = '__all__'` | `Model.create(req.body)` | Full struct bound from JSON | Serde deserializes all fields |
| JWT Auth | `algorithms=` from header | Missing `IsAuthenticated` | Missing `algorithms` in verify | Algorithm not checked | `Validation::default()` |
| Rate Limiting | No `slowapi` | No `django-ratelimit` | No `express-rate-limit` | No rate middleware | No `tower-governor` |
| SSRF | `requests.get(user_url)` | `urllib` on user input | `fetch(req.body.url)` | `http.Get(userURL)` | `reqwest::get(url)` |
| CORS | `allow_origins=["*"]` | `CORS_ALLOW_ALL_ORIGINS` | `cors({ origin: '*' })` | `AllowAllOrigins: true` | `CorsLayer::permissive()` |
| Verbose Errors | Stack in HTTPException | `DEBUG = True` | `err.stack` in response | `gin.Default()` in prod | Panic message exposed |
