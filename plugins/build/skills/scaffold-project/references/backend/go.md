# Go Backend Scaffold

## Project Structure

```
<project-name>/
├── cmd/<project-name>/
│   └── main.go
├── internal/
│   └── handler/
│       └── health.go
├── go.mod
├── go.sum
├── Makefile
├── .gitignore
├── .golangci.yml
├── .pre-commit-config.yaml
├── .github/workflows/ci.yml
└── CLAUDE.md
```

## go.mod

Initialize with `go mod init <module-path>`. Ask user for the module path (e.g., `github.com/user/project`).

## Makefile

```makefile
.PHONY: install dev format lint test check

install:
	go mod download

dev:
	go run ./cmd/<project-name>

format:
	gofmt -w .
	goimports -w .

lint:
	golangci-lint run ./...

test:
	go test -v -race ./...

check: lint test
```

## .golangci.yml

```yaml
linters:
  enable:
    - errcheck
    - govet
    - staticcheck
    - unused
    - gosimple
    - ineffassign
    - goimports

linters-settings:
  goimports:
    local-prefixes: <module-path>

run:
  timeout: 5m
```

## .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: check-added-large-files
      - id: detect-private-key
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
      - id: go-vet
      - id: golangci-lint
```

## .gitignore

```
# Binaries
*.exe
*.exe~
*.dll
*.so
*.dylib
/bin/

# Test
*.test
*.out
coverage.txt

# Dependency
/vendor/

# IDE
.idea/
.vscode/
*.swp
```

## .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: "1.23"
      - uses: golangci/golangci-lint-action@v6
      - run: go test -v -race ./...
```

## cmd/<project-name>/main.go

```go
package main

import (
	"log"
	"net/http"

	"<module-path>/internal/handler"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", handler.Health)

	log.Println("listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", mux))
}
```

## internal/handler/health.go

```go
package handler

import (
	"encoding/json"
	"net/http"
)

func Health(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}
```

## internal/handler/health_test.go

```go
package handler_test

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"<module-path>/internal/handler"
)

func TestHealth(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	w := httptest.NewRecorder()

	handler.Health(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected 200, got %d", w.Code)
	}
}
```

## CLAUDE.md

```markdown
# CLAUDE.md

## Commands

\```bash
make install    # Download dependencies
make dev        # Run development server
make format     # Format with gofmt + goimports
make lint       # Lint with golangci-lint
make test       # Run tests with race detection
make check      # Run lint + test
\```

## Architecture

Go backend using stdlib net/http, golangci-lint for linting, go test for testing.

\```
cmd/<project-name>/
  main.go           # Entry point, routing
internal/
  handler/          # HTTP handlers
\```
```
