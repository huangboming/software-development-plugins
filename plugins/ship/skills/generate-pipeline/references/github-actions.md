# GitHub Actions Reference

## File Location

Place workflow files at `.github/workflows/<name>.yml`. Use descriptive names:
- `ci.yml` — primary lint/test/build pipeline
- `deploy.yml` — deployment pipeline
- `release.yml` — release automation

## Workflow Structure

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# Cancel in-progress runs for the same branch/PR
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    # ...
  test:
    # ...
  build:
    needs: [lint, test]
    # ...
```

## Trigger Patterns

| Scenario | Trigger |
|---|---|
| Every push and PR to main | `on: { push: { branches: [main] }, pull_request: { branches: [main] } }` |
| Only PRs | `on: { pull_request: { branches: [main] } }` |
| Tags for releases | `on: { push: { tags: ['v*'] } }` |
| Monorepo path filtering | `on: { push: { paths: ['services/api/**'] } }` |
| Scheduled (nightly) | `on: { schedule: [{ cron: '0 2 * * *' }] }` |
| Manual trigger | `on: { workflow_dispatch: { inputs: { environment: { type: choice, options: [staging, production] } } } }` |

## Job Patterns by Stage

### Lint

```yaml
lint:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - # Language-specific setup (see below)
    - name: Lint
      run: <lint-command>
    - name: Format check
      run: <format-check-command>
```

### Test

```yaml
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - # Language-specific setup
    - name: Install dependencies
      run: <install-command>
    - name: Run tests
      run: <test-command>
```

### Build

```yaml
build:
  runs-on: ubuntu-latest
  needs: [lint, test]
  steps:
    - uses: actions/checkout@v4
    - # Language-specific setup
    - name: Build
      run: <build-command>
    - name: Upload artifact
      uses: actions/upload-artifact@v4
      with:
        name: build-output
        path: <build-dir>
```

### E2E Tests

```yaml
e2e:
  runs-on: ubuntu-latest
  needs: [build]
  steps:
    - uses: actions/checkout@v4
    - # Language-specific setup
    - name: Install dependencies
      run: <install-command>
    - name: Install Playwright browsers
      run: npx playwright install --with-deps chromium
    - name: Run E2E tests
      run: npx playwright test
    - name: Upload test report
      if: ${{ !cancelled() }}
      uses: actions/upload-artifact@v4
      with:
        name: playwright-report
        path: playwright-report/
```

### Deploy

```yaml
deploy:
  runs-on: ubuntu-latest
  needs: [build]
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  environment: production
  steps:
    - uses: actions/checkout@v4
    - # Deploy steps vary by target (see Deploy Targets below)
```

## Language-Specific Setup

### Node.js (pnpm)

```yaml
- uses: pnpm/action-setup@v4
  with:
    version: 10
- uses: actions/setup-node@v4
  with:
    node-version: 22
    cache: pnpm
- run: pnpm install --frozen-lockfile
```

Commands: `pnpm lint`, `pnpm format --check`, `pnpm test`, `pnpm build`

### Python (uv)

```yaml
- uses: astral-sh/setup-uv@v5
- run: uv sync
```

Commands: `uv run ruff check src tests`, `uv run ruff format --check src tests`, `uv run pytest -v`

### Go

```yaml
- uses: actions/setup-go@v5
  with:
    go-version-file: go.mod
- uses: golangci/golangci-lint-action@v6
```

Commands: `go test -v -race ./...`, `go build ./...`

### Rust

```yaml
- uses: dtolnay/rust-toolchain@stable
  with:
    components: clippy, rustfmt
- uses: Swatinem/rust-cache@v2
```

Commands: `cargo clippy -- -D warnings`, `cargo fmt -- --check`, `cargo test`, `cargo build --release`

## Caching Strategies

| Language | Approach |
|---|---|
| Node (pnpm) | `actions/setup-node` with `cache: pnpm` — automatic |
| Python (uv) | `astral-sh/setup-uv` handles caching automatically |
| Go | `actions/setup-go` with `go-version-file` — caches `~/go/pkg/mod` automatically |
| Rust | `Swatinem/rust-cache@v2` — caches `target/` and registry |

## Matrix Builds

Use for testing across multiple versions:

```yaml
test:
  strategy:
    matrix:
      node-version: [20, 22]
    fail-fast: false
  runs-on: ubuntu-latest
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
```

Only add matrix builds when the user explicitly requests multi-version testing. Default to a single latest version.

## Service Containers

For tests requiring databases or other services:

```yaml
test:
  runs-on: ubuntu-latest
  services:
    postgres:
      image: postgres:16
      env:
        POSTGRES_PASSWORD: postgres
        POSTGRES_DB: test
      ports:
        - 5432:5432
      options: >-
        --health-cmd pg_isready
        --health-interval 10s
        --health-timeout 5s
        --health-retries 5
    redis:
      image: redis:7
      ports:
        - 6379:6379
```

## Deploy Targets

### Docker Build and Push

```yaml
- uses: docker/setup-buildx-action@v3
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
- uses: docker/build-push-action@v6
  with:
    push: true
    tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### Vercel

```yaml
- uses: amondnet/vercel-action@v25
  with:
    vercel-token: ${{ secrets.VERCEL_TOKEN }}
    vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
    vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
    vercel-args: --prod
```

### AWS (ECS / S3)

```yaml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1
```

### Fly.io

```yaml
- uses: superfly/flyctl-actions/setup-flyctl@master
- run: flyctl deploy --remote-only
  env:
    FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

## Secrets

Reference secrets via `${{ secrets.SECRET_NAME }}`. Remind the user to add secrets in the repository's Settings → Secrets and variables → Actions. List all required secrets in a comment at the top of the workflow file:

```yaml
# Required secrets:
#   DEPLOY_TOKEN - Token for deployment service
#   DATABASE_URL - Production database connection string
```

## Best Practices

1. **Pin action versions** to major tags (`@v4`) not `@main` or `@latest`
2. **Use `concurrency`** to cancel stale runs on the same branch
3. **Separate lint from test** — fast feedback on style issues before slower test runs
4. **Use `needs`** to create a dependency graph: build only after lint+test pass
5. **Gate deploys** with `if: github.ref == 'refs/heads/main'` and `environment:` for approval controls
6. **Use `--frozen-lockfile`** (pnpm) or equivalent to ensure reproducible installs
7. **Upload artifacts** for build outputs and test reports
8. **Use `fail-fast: false`** in matrix builds so all combinations run even if one fails
