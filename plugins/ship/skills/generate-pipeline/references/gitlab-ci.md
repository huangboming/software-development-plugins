# GitLab CI Reference

## File Location

Pipeline config goes in `.gitlab-ci.yml` at the repository root.

## Pipeline Structure

```yaml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  # Global variables available to all jobs

lint:
  stage: lint
  # ...

test:
  stage: test
  # ...

build:
  stage: build
  needs: [lint, test]
  # ...

deploy:
  stage: deploy
  needs: [build]
  # ...
```

## Stage Patterns

### Lint

```yaml
lint:
  stage: lint
  image: <language-image>
  script:
    - <install-command>
    - <lint-command>
    - <format-check-command>
```

### Test

```yaml
test:
  stage: test
  image: <language-image>
  script:
    - <install-command>
    - <test-command>
  coverage: '/<regex-for-coverage-line>/'
  artifacts:
    reports:
      junit: <test-report-path>
    when: always
```

### Build

```yaml
build:
  stage: build
  image: <language-image>
  needs: [lint, test]
  script:
    - <build-command>
  artifacts:
    paths:
      - <build-output-dir>/
    expire_in: 1 week
```

### Deploy

```yaml
deploy:
  stage: deploy
  needs: [build]
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: on_success
    - when: never
  script:
    - <deploy-command>
```

## Language-Specific Patterns

### Node.js (pnpm)

```yaml
variables:
  PNPM_VERSION: "10"

.node-setup: &node-setup
  image: node:22-slim
  before_script:
    - corepack enable
    - corepack prepare pnpm@$PNPM_VERSION --activate
    - pnpm install --frozen-lockfile
  cache:
    key:
      files:
        - pnpm-lock.yaml
    paths:
      - .pnpm-store/
    policy: pull-push

lint:
  stage: lint
  <<: *node-setup
  script:
    - pnpm lint
    - pnpm format --check

test:
  stage: test
  <<: *node-setup
  script:
    - pnpm test
```

### Python (uv)

```yaml
.python-setup: &python-setup
  image: python:3.13-slim
  before_script:
    - pip install uv
    - uv sync
  cache:
    key:
      files:
        - uv.lock
    paths:
      - .venv/
    policy: pull-push

lint:
  stage: lint
  <<: *python-setup
  script:
    - uv run ruff check src tests
    - uv run ruff format --check src tests

test:
  stage: test
  <<: *python-setup
  script:
    - uv run pytest -v --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml
```

### Go

```yaml
.go-setup: &go-setup
  image: golang:1.23
  cache:
    key:
      files:
        - go.sum
    paths:
      - /go/pkg/mod/
    policy: pull-push

lint:
  stage: lint
  <<: *go-setup
  image: golangci/golangci-lint:latest
  script:
    - golangci-lint run

test:
  stage: test
  <<: *go-setup
  script:
    - go test -v -race -coverprofile=coverage.out ./...
  coverage: '/total:\s+\(statements\)\s+(\d+\.\d+)%/'
```

### Rust

```yaml
.rust-setup: &rust-setup
  image: rust:latest
  cache:
    key:
      files:
        - Cargo.lock
    paths:
      - target/
      - /usr/local/cargo/registry/
    policy: pull-push

lint:
  stage: lint
  <<: *rust-setup
  script:
    - rustup component add clippy rustfmt
    - cargo clippy -- -D warnings
    - cargo fmt -- --check

test:
  stage: test
  <<: *rust-setup
  script:
    - cargo test
```

## Caching

GitLab CI caching uses `cache:` with key-based invalidation:

```yaml
cache:
  key:
    files:
      - <lockfile>          # Invalidate when dependencies change
  paths:
    - <dependency-dir>/     # What to cache
  policy: pull-push          # pull-push (default), pull (read-only), push (write-only)
```

Use `pull` policy for jobs that only read cached data (lint, test). Use `pull-push` for the install job.

## Service Containers

```yaml
test:
  stage: test
  services:
    - name: postgres:16
      alias: db
      variables:
        POSTGRES_PASSWORD: postgres
        POSTGRES_DB: test
    - name: redis:7
      alias: cache
  variables:
    DATABASE_URL: "postgresql://postgres:postgres@db:5432/test"
    REDIS_URL: "redis://cache:6379"
```

## Rules and Conditions

Use `rules:` (preferred over `only:/except:`):

```yaml
# Run only on main branch pushes
rules:
  - if: $CI_COMMIT_BRANCH == "main"

# Run on merge requests
rules:
  - if: $CI_PIPELINE_SOURCE == "merge_request_event"

# Run on tags
rules:
  - if: $CI_COMMIT_TAG

# Run on main OR merge requests (typical CI pattern)
rules:
  - if: $CI_COMMIT_BRANCH == "main"
  - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

## Deploy Targets

### Docker Build and Push (GitLab Registry)

```yaml
build-image:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

### Environment-Based Deploys

```yaml
deploy-staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  script:
    - <deploy-to-staging>

deploy-production:
  stage: deploy
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_TAG
      when: manual
  script:
    - <deploy-to-production>
```

## Variables and Secrets

- Define non-sensitive variables in `.gitlab-ci.yml` under `variables:`
- Store secrets in GitLab → Settings → CI/CD → Variables (mark as "Masked" and "Protected")
- Reference with `$VARIABLE_NAME`
- Comment required variables at the top of the file:

```yaml
# Required CI/CD variables (Settings → CI/CD → Variables):
#   DEPLOY_TOKEN - Deployment service token (masked, protected)
#   DATABASE_URL - Production database URL (masked, protected)
```

## Best Practices

1. **Use YAML anchors** (`&name` / `*name` / `<<: *name`) to DRY up repeated setup
2. **Use `needs:`** for DAG-based pipelines instead of relying on stage ordering alone
3. **Set `artifacts: expire_in`** to avoid unbounded storage growth
4. **Use `rules:` over `only:/except:`** — more expressive and less surprising
5. **Use `interruptible: true`** on long-running jobs so new commits cancel stale pipelines
6. **Gate production deploys** with `when: manual` for approval control
7. **Use `coverage:` regex** to surface test coverage in merge request widgets
8. **Cache with lockfile keys** so caches invalidate when dependencies change
