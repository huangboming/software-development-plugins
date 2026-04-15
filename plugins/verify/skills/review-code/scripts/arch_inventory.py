#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# ///
"""
Generate a lightweight architecture inventory for a backend repository.

Goal: produce an evidence-oriented starting point for an architecture review, without requiring
any third-party dependencies.

Usage:
    uv run --script arch_inventory.py --repo <path> [--output <path>] [--max-files N] [--max-bytes N] [--no-git]

Output: a Markdown report with sections for:
- Stack & infra signals (languages, frameworks, build tools, docker, k8s, terraform, CI)
- Likely frameworks / libraries (parsed from package.json, pyproject.toml, go.mod)
- Data / messaging hints (databases, queues)
- Observability hints (tracing, metrics, logging)
- Docker Compose services (heuristic YAML parse)
- Key files to read next (docs, config, API schemas, migrations)
- Suggested next steps
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, TypedDict

try:
    import tomllib
except ImportError:
    tomllib = None  # type: ignore[assignment]


MAX_KEY_FILES_PER_GROUP = 200


class InventoryResult(TypedDict):
    repo: str
    generated_at: str
    file_count: int
    hints: dict[str, list[str]]
    key_files: dict[str, list[str]]
    frameworks: list[str]
    data_hints: list[str]
    observability_hints: list[str]
    compose_services: dict[str, list[str]]


DEFAULT_IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "out",
    "coverage",
    "target",
    "vendor",
}


IMPORTANT_FILE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("Docs", re.compile(r"(^|/)(README|CHANGELOG|CONTRIBUTING)\b.*", re.IGNORECASE)),
    ("Docs", re.compile(r"^docs/|(^|/)ADR[s]?/", re.IGNORECASE)),
    ("Docker", re.compile(r"(^|/)Dockerfile(\..+)?$", re.IGNORECASE)),
    ("Docker", re.compile(r"(^|/)(docker-compose\.ya?ml|compose\.ya?ml)$", re.IGNORECASE)),
    ("Kubernetes", re.compile(r"(^|/)(kustomization\.ya?ml|Chart\.ya?ml)$", re.IGNORECASE)),
    ("Terraform", re.compile(r"\.tf$", re.IGNORECASE)),
    ("CI/CD", re.compile(r"^\.github/workflows/|^\.gitlab-ci\.ya?ml$|(^|/)Jenkinsfile$", re.IGNORECASE)),
    ("API", re.compile(r"(^|/)(openapi|swagger)\.(ya?ml|json)$", re.IGNORECASE)),
    ("API", re.compile(r"\.proto$", re.IGNORECASE)),
    ("API", re.compile(r"(^|/)(schema|graphql)\.(graphql|gql)$", re.IGNORECASE)),
    ("DB", re.compile(r"(^|/)(migrations|alembic|prisma|flyway|liquibase)(/|$)", re.IGNORECASE)),
    ("Config", re.compile(r"(^|/)\.env(\.|$)", re.IGNORECASE)),
    ("Config", re.compile(r"(^|/)(config|configs|configuration)(/|$)", re.IGNORECASE)),
]


PACKAGE_JSON_DEP_KEYS = ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies")


NODE_FRAMEWORKS = {
    "express": "Express",
    "@nestjs/core": "NestJS",
    "fastify": "Fastify",
    "koa": "Koa",
    "@hapi/hapi": "hapi",
    "hono": "Hono",
    "next": "Next.js (often fullstack)",
}

PY_FRAMEWORKS = {
    "fastapi": "FastAPI",
    "django": "Django",
    "flask": "Flask",
    "starlette": "Starlette",
    "sanic": "Sanic",
}

GO_FRAMEWORKS = {
    "github.com/gin-gonic/gin": "Gin",
    "github.com/labstack/echo": "Echo",
    "github.com/gofiber/fiber": "Fiber",
    "go.uber.org/fx": "Fx",
}


DATA_TECH_HINTS = {
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "mariadb": "MariaDB",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "dynamodb": "DynamoDB",
    "elasticsearch": "Elasticsearch",
    "opensearch": "OpenSearch",
}

MESSAGING_HINTS = {
    "kafka": "Kafka",
    "rabbitmq": "RabbitMQ",
    "nats": "NATS",
    "sqs": "AWS SQS",
    "sns": "AWS SNS",
    "pubsub": "GCP Pub/Sub",
}

OBSERVABILITY_HINTS = {
    "opentelemetry": "OpenTelemetry",
    "otel": "OpenTelemetry (otel)",
    "prometheus": "Prometheus",
    "grafana": "Grafana",
    "jaeger": "Jaeger",
    "datadog": "Datadog",
    "newrelic": "New Relic",
    "sentry": "Sentry",
}


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, check=False)


def list_repo_files(repo: Path, max_files: int, prefer_git: bool) -> list[str]:
    if prefer_git and (repo / ".git").exists():
        proc = _run(["git", "ls-files", "-z"], cwd=repo)
        if proc.returncode == 0:
            files = [p for p in proc.stdout.split("\0") if p]
            return files[:max_files]

    files: list[str] = []
    for root, dirnames, filenames in os.walk(repo):
        rel_root = os.path.relpath(root, repo)
        if rel_root == ".":
            rel_root = ""

        # Mutate dirnames in-place to prune traversal
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_IGNORED_DIRS]
        for filename in filenames:
            rel_path = str(Path(rel_root) / filename) if rel_root else filename
            files.append(rel_path)
            if len(files) >= max_files:
                return files
    return files


def _read_text(path: Path, max_bytes: int) -> str:
    try:
        with path.open("rb") as f:
            data = f.read(max_bytes + 1)
        data = data[:max_bytes]
        return data.decode("utf-8", errors="replace")
    except OSError:
        return ""


def _detect_from_paths(repo: Path, files: list[str]) -> dict[str, set[str]]:
    hints: dict[str, set[str]] = {}

    def add(cat: str, label: str, evidence: str) -> None:
        hints.setdefault(cat, set()).add(f"{label} (evidence: {evidence})")

    for rel in files:
        lower = rel.lower()
        p = Path(rel)

        if p.name == "package.json":
            add("Build/Deps", "Node package.json", rel)
        if p.name in {"pnpm-lock.yaml", "yarn.lock", "package-lock.json"}:
            add("Build/Deps", f"JS lockfile ({p.name})", rel)
        if p.name == "tsconfig.json":
            add("Build/Deps", "TypeScript", rel)

        if p.name == "pyproject.toml":
            add("Build/Deps", "Python pyproject.toml", rel)
        if p.name in {"requirements.txt", "requirements-dev.txt"}:
            add("Build/Deps", f"Python requirements ({p.name})", rel)
        if p.name in {"poetry.lock", "Pipfile", "Pipfile.lock"}:
            add("Build/Deps", f"Python tooling ({p.name})", rel)

        if p.name == "go.mod":
            add("Build/Deps", "Go module (go.mod)", rel)

        if p.name in {"pom.xml", "build.gradle", "settings.gradle", "gradlew"}:
            add("Build/Deps", f"JVM build ({p.name})", rel)

        if p.name == "Cargo.toml":
            add("Build/Deps", "Rust (Cargo.toml)", rel)

        if p.name in {"docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"}:
            add("Infra/Deploy", "Docker Compose", rel)
        if p.name.lower().startswith("dockerfile"):
            add("Infra/Deploy", "Dockerfile", rel)

        if p.name in {"Chart.yaml", "kustomization.yaml"}:
            add("Infra/Deploy", f"Kubernetes/Helm ({p.name})", rel)
        if "k8s" in lower.split("/"):
            add("Infra/Deploy", "Kubernetes manifests (k8s/)", rel)

        if lower.endswith(".tf"):
            add("Infra/Deploy", "Terraform", rel)
        if p.name in {"serverless.yml", "serverless.yaml"}:
            add("Infra/Deploy", "Serverless Framework", rel)

        if lower.startswith(".github/workflows/") or p.name == ".gitlab-ci.yml":
            add("CI/CD", "CI pipeline config", rel)
        if p.name == "Jenkinsfile":
            add("CI/CD", "Jenkins", rel)

        if p.name.lower() in {"openapi.yaml", "openapi.yml", "openapi.json", "swagger.yaml", "swagger.yml"}:
            add("API/Schema", f"OpenAPI/Swagger ({p.name})", rel)
        if lower.endswith(".proto"):
            add("API/Schema", "Protobuf (.proto)", rel)
        if lower.endswith((".graphql", ".gql")):
            add("API/Schema", "GraphQL schema", rel)

        if p.name == ".env" or p.name.startswith(".env."):
            add("Config", "Env file (.env*)", rel)

        if any(part in {"migrations", "alembic", "prisma", "flyway", "liquibase"} for part in p.parts):
            add("Data", "Migrations/schema tooling", rel)

    return hints


def _parse_package_json(repo: Path, rel_path: str, max_bytes: int) -> tuple[set[str], set[str], set[str]]:
    frameworks: set[str] = set()
    data: set[str] = set()
    obs: set[str] = set()

    text = _read_text(repo / rel_path, max_bytes=max_bytes)
    if not text:
        return frameworks, data, obs

    try:
        obj = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return frameworks, data, obs

    deps: dict[str, str] = {}
    for key in PACKAGE_JSON_DEP_KEYS:
        part = obj.get(key, {})
        if isinstance(part, dict):
            deps.update({str(k): str(v) for k, v in part.items()})

    for dep, label in NODE_FRAMEWORKS.items():
        if dep in deps:
            frameworks.add(f"{label} (evidence: {rel_path} dependency '{dep}')")

    for needle, label in {**DATA_TECH_HINTS, **MESSAGING_HINTS}.items():
        if any(needle in k.lower() for k in deps):
            data.add(f"{label} (evidence: {rel_path} dependencies)")

    for needle, label in OBSERVABILITY_HINTS.items():
        if any(needle in k.lower() for k in deps):
            obs.add(f"{label} (evidence: {rel_path} dependencies)")

    return frameworks, data, obs


def _parse_pyproject(repo: Path, rel_path: str, max_bytes: int) -> tuple[set[str], set[str]]:
    frameworks: set[str] = set()
    obs: set[str] = set()

    if tomllib is None:
        return frameworks, obs

    text = _read_text(repo / rel_path, max_bytes=max_bytes)
    if not text:
        return frameworks, obs
    try:
        parsed = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return frameworks, obs

    deps: list[str] = []
    proj = parsed.get("project", {})
    if isinstance(proj, dict):
        proj_deps = proj.get("dependencies", [])
        if isinstance(proj_deps, list):
            deps.extend([str(x) for x in proj_deps])

    tool = parsed.get("tool", {})
    if isinstance(tool, dict):
        poetry = tool.get("poetry", {})
        if isinstance(poetry, dict):
            poetry_deps = poetry.get("dependencies", {})
            if isinstance(poetry_deps, dict):
                deps.extend(list(poetry_deps.keys()))

    deps_lower = [d.lower() for d in deps]
    for dep, label in PY_FRAMEWORKS.items():
        if any(dep == d.split()[0].split("[")[0] for d in deps_lower):
            frameworks.add(f"{label} (evidence: {rel_path} dependency '{dep}')")

    for needle, label in OBSERVABILITY_HINTS.items():
        if any(needle in d for d in deps_lower):
            obs.add(f"{label} (evidence: {rel_path} dependencies)")

    return frameworks, obs


def _parse_go_mod(repo: Path, rel_path: str, max_bytes: int) -> set[str]:
    frameworks: set[str] = set()
    text = _read_text(repo / rel_path, max_bytes=max_bytes)
    if not text:
        return frameworks
    for dep, label in GO_FRAMEWORKS.items():
        if dep in text:
            frameworks.add(f"{label} (evidence: {rel_path} contains '{dep}')")
    return frameworks


def _parse_compose_services(repo: Path, rel_path: str, max_bytes: int) -> list[str]:
    content = _read_text(repo / rel_path, max_bytes=max_bytes)
    if not content:
        return []

    services: list[str] = []
    in_services = False
    services_indent: int | None = None
    service_key_indent: int | None = None

    for line in content.splitlines():
        if not in_services:
            m = re.match(r"^(\s*)services:\s*(#.*)?$", line)
            if m:
                in_services = True
                services_indent = len(m.group(1))
            continue

        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())
        if services_indent is not None and indent <= services_indent:
            break

        m = re.match(r"^(\s*)([A-Za-z0-9_.-]+):\s*(#.*)?$", line)
        if not m:
            continue

        key_indent = len(m.group(1))
        key = m.group(2)
        if key.startswith("x-"):
            continue

        if service_key_indent is None:
            service_key_indent = key_indent

        if key_indent == service_key_indent:
            services.append(key)

    return list(dict.fromkeys(services))


def analyze_repo(repo: Path, files: list[str], max_read_bytes: int) -> InventoryResult:
    hints = _detect_from_paths(repo, files)

    key_files: dict[str, list[str]] = {}
    for rel in files:
        for group, pattern in IMPORTANT_FILE_PATTERNS:
            if pattern.search(rel):
                key_files.setdefault(group, []).append(rel)
                break

    frameworks: set[str] = set()
    data_hints: set[str] = set()
    obs_hints: set[str] = set()

    for rel in files:
        if Path(rel).name == "package.json":
            fws, data, obs = _parse_package_json(repo, rel, max_bytes=max_read_bytes)
            frameworks |= fws
            data_hints |= data
            obs_hints |= obs
        elif Path(rel).name == "pyproject.toml":
            fws, obs = _parse_pyproject(repo, rel, max_bytes=max_read_bytes)
            frameworks |= fws
            obs_hints |= obs
        elif Path(rel).name == "go.mod":
            frameworks |= _parse_go_mod(repo, rel, max_bytes=max_read_bytes)

    compose_services: dict[str, list[str]] = {}
    for rel in key_files.get("Docker", []):
        if Path(rel).name in {"docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"}:
            services = _parse_compose_services(repo, rel, max_bytes=max_read_bytes)
            if services:
                compose_services[rel] = services

    return {
        "repo": str(repo),
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "file_count": len(files),
        "hints": {k: sorted(v) for k, v in hints.items()},
        "key_files": {k: sorted(set(v))[:MAX_KEY_FILES_PER_GROUP] for k, v in key_files.items()},
        "frameworks": sorted(frameworks),
        "data_hints": sorted(data_hints),
        "observability_hints": sorted(obs_hints),
        "compose_services": compose_services,
    }


def _md_list(items: Iterable[str]) -> str:
    lines = []
    for item in items:
        lines.append(f"- {item}")
    return "\n".join(lines) if lines else "- (none found)"


def render_markdown(result: InventoryResult) -> str:
    lines: list[str] = []
    lines.append("# Architecture Inventory")
    lines.append("")
    lines.append(f"- Repo: `{result['repo']}`")
    lines.append(f"- Generated (UTC): `{result['generated_at']}`")
    lines.append(f"- Files considered: `{result['file_count']}`")
    lines.append("")

    lines.append("## Stack & Infra Signals (Path-Based)")
    lines.append("")
    for category in sorted(result["hints"]):
        lines.append(f"### {category}")
        lines.append("")
        lines.append(_md_list(result["hints"][category]))
        lines.append("")

    lines.append("## Likely Frameworks / Libraries (Dependency-Based)")
    lines.append("")
    lines.append(_md_list(result["frameworks"]))
    lines.append("")

    lines.append("## Data / Messaging Hints (Dependency-Based)")
    lines.append("")
    lines.append(_md_list(result["data_hints"]))
    lines.append("")

    lines.append("## Observability Hints (Dependency-Based)")
    lines.append("")
    lines.append(_md_list(result["observability_hints"]))
    lines.append("")

    lines.append("## Docker Compose Services (Heuristic Parse)")
    lines.append("")
    if result["compose_services"]:
        for rel, services in result["compose_services"].items():
            lines.append(f"### `{rel}`")
            lines.append("")
            lines.append(_md_list(services))
            lines.append("")
    else:
        lines.append("- (none found)")
        lines.append("")

    lines.append("## Key Files To Read Next")
    lines.append("")
    if result["key_files"]:
        for group in sorted(result["key_files"]):
            lines.append(f"### {group}")
            lines.append("")
            lines.append(_md_list([f"`{p}`" for p in result["key_files"][group]]))
            lines.append("")
    else:
        lines.append("- (none found)")
        lines.append("")

    lines.append("## Suggested Next Steps")
    lines.append("")
    lines.append('- Read the files in "Key Files To Read Next" and confirm the inventory is correct.')
    lines.append("- Identify the main request/flow(s) and draw a sequence diagram.")
    lines.append("- Draft C4-style context + container diagrams to validate component boundaries.")
    lines.append("- Analyze findings against anti-patterns, coupling metrics, layering patterns, and resilience patterns.")
    lines.append("")

    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an architecture inventory Markdown report.")
    parser.add_argument("--repo", default=".", help="Path to the repository to analyze (default: .)")
    parser.add_argument(
        "--output",
        default=".hand-offs/architecture-inventory.md",
        help="Where to write the Markdown report (default: .hand-offs/architecture-inventory.md)",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=30000,
        help="Max number of files to consider (default: 30000)",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=200_000,
        help="Max bytes to read per file when parsing (default: 200000)",
    )
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Do not use git ls-files even if .git exists (default: false)",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    repo = Path(args.repo).expanduser().resolve()
    if not repo.exists() or not repo.is_dir():
        print(f"[ERROR] Repo path is not a directory: {repo}", file=sys.stderr)
        return 2

    files = list_repo_files(repo, max_files=args.max_files, prefer_git=not args.no_git)
    result = analyze_repo(repo, files, max_read_bytes=args.max_bytes)

    output_path = Path(args.output).expanduser()
    if not output_path.is_absolute():
        output_path = (Path.cwd() / output_path).resolve()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown(result), encoding="utf-8")
    print(f"[OK] Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
