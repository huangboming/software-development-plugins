# Rust Backend Scaffold

## Project Structure

Initialize with `cargo init <project-name>`, then customize.

```
<project-name>/
├── src/
│   └── main.rs
├── tests/
│   └── health_test.rs
├── Cargo.toml
├── Makefile
├── .gitignore
├── rustfmt.toml
├── clippy.toml
├── .pre-commit-config.yaml
├── .github/workflows/ci.yml
└── CLAUDE.md
```

## Cargo.toml

```toml
[package]
name = "<project-name>"
version = "0.1.0"
edition = "2024"

[dependencies]
axum = "0.8"
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"

[dev-dependencies]
reqwest = { version = "0.12", features = ["json"] }
tokio-test = "0.4"
```

## Makefile

```makefile
.PHONY: install dev format lint test check

install:
	cargo build

dev:
	cargo run

format:
	cargo fmt

lint:
	cargo clippy -- -D warnings

test:
	cargo test

check: lint test
```

## rustfmt.toml

```toml
edition = "2024"
max_width = 100
```

## clippy.toml

```toml
too-many-arguments-threshold = 4
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
        exclude: "^\\.vscode/"
      - id: check-merge-conflict
      - id: check-added-large-files
      - id: detect-private-key
  - repo: local
    hooks:
      - id: cargo-fmt
        name: cargo fmt
        entry: cargo fmt --
        language: system
        types: [rust]
      - id: cargo-clippy
        name: cargo clippy
        entry: cargo clippy -- -D warnings
        language: system
        types: [rust]
        pass_filenames: false
```

## .gitignore

Cargo generates a .gitignore. Ensure it includes:

```
/target
Cargo.lock
```

Note: include `Cargo.lock` in .gitignore for libraries, but commit it for binaries/applications. Since this is a backend service, **commit Cargo.lock** (remove it from .gitignore).

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
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt
      - run: cargo fmt --check
      - run: cargo clippy -- -D warnings
      - run: cargo test
```

## src/main.rs

```rust
use axum::{routing::get, Json, Router};
use serde_json::{json, Value};

#[tokio::main]
async fn main() {
    let app = Router::new().route("/health", get(health));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await.unwrap();
    println!("listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, app).await.unwrap();
}

async fn health() -> Json<Value> {
    Json(json!({"status": "ok"}))
}
```

## tests/health_test.rs

```rust
use axum::{routing::get, Json, Router};
use axum::body::Body;
use axum::http::Request;
use serde_json::{json, Value};
use tower::ServiceExt;

async fn health() -> Json<Value> {
    Json(json!({"status": "ok"}))
}

#[tokio::test]
async fn test_health() {
    let app = Router::new().route("/health", get(health));

    let response = app
        .oneshot(Request::builder().uri("/health").body(Body::empty()).unwrap())
        .await
        .unwrap();

    assert_eq!(response.status(), 200);
}
```

## CLAUDE.md

```markdown
# CLAUDE.md

## Commands

\```bash
make install    # Build the project
make dev        # Run development server
make format     # Format with rustfmt
make lint       # Lint with clippy
make test       # Run tests
make check      # Run lint + test
\```

## Architecture

Rust backend using axum, clippy for linting, rustfmt for formatting, cargo test for testing.

\```
src/
  main.rs       # Entry point, routing, handlers
tests/
  health_test.rs
\```
```
