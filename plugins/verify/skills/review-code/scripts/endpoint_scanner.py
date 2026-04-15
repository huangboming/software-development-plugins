#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# ///
"""
Scan a backend repository for implementation review hot spots.

Identifies API endpoints, database query patterns, error handling,
and security-related patterns to guide an implementation review
toward the highest-value targets.

Usage:
    uv run --script endpoint_scanner.py --repo <path> [--output <path>] [--max-files N]

Output: Markdown report (default: .hand-offs/endpoint-scan.md)
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".go", ".rs", ".java", ".kt", ".rb",
    ".cs", ".scala",
}

IGNORED_DIRS = {
    ".git", ".hg", ".svn", ".idea", ".vscode",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".venv", "venv", "env", "node_modules",
    "dist", "build", "out", "coverage", "target", "vendor",
    ".next", ".nuxt", ".output",
}

EXT_TO_LANG: dict[str, str] = {
    ".py": "python",
    ".js": "javascript", ".ts": "javascript", ".jsx": "javascript", ".tsx": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java", ".kt": "java", ".scala": "java",
    ".rb": "ruby",
    ".cs": "csharp",
}

TEST_INDICATORS = re.compile(
    r"(^test_|_test\.|\.test\.|\.spec\.|_spec\.|/tests?/|/specs?/|/__tests__/)",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Detection patterns
# ---------------------------------------------------------------------------

# API route/endpoint patterns
ROUTE_PATTERNS: dict[str, list[re.Pattern[str]]] = {
    "python": [
        re.compile(r"""@\w+\.(get|post|put|patch|delete|head|options)\s*\(["']([^"']+)["']""", re.IGNORECASE),
        re.compile(r"""@(?:api_view|action)\s*\(\s*\[["'](\w+)["']""", re.IGNORECASE),
        re.compile(r"""\.(?:add_url_rule|route)\s*\(\s*["']([^"']+)["']"""),
        re.compile(r"""path\s*\(\s*["']([^"']+)["']"""),
    ],
    "javascript": [
        re.compile(r"""(?:app|router|server)\.(get|post|put|patch|delete|all|use)\s*\(\s*["'`]([^"'`]+)["'`]""", re.IGNORECASE),
        re.compile(r"""\.(?:onRequest|handle)\s*\("""),
    ],
    "go": [
        re.compile(r'''\.(?:GET|POST|PUT|PATCH|DELETE|Handle|HandleFunc|Group)\s*\(\s*"([^"]+)"'''),
        re.compile(r'''(?:http\.)?(?:HandleFunc|Handle)\s*\(\s*"([^"]+)"'''),
        re.compile(r'''r\.(?:Get|Post|Put|Patch|Delete|Route)\s*\(\s*"([^"]+)"'''),
    ],
    "rust": [
        re.compile(r'''\.route\s*\(\s*"([^"]+)"'''),
        re.compile(r'''#\[(?:get|post|put|patch|delete)\s*\(\s*"([^"]+)"'''),
        re.compile(r'''web::\s*(?:get|post|put|patch|delete|resource)\s*\(\s*"([^"]+)"'''),
    ],
    "java": [
        re.compile(r"""@(?:Get|Post|Put|Patch|Delete|Request)Mapping\s*\(\s*(?:value\s*=\s*)?["']([^"']+)["']"""),
        re.compile(r'''@(?:GET|POST|PUT|PATCH|DELETE)\s*\n\s*@Path\s*\(\s*"([^"]+)"'''),
    ],
    "ruby": [
        re.compile(r"""(?:get|post|put|patch|delete|resources?|match)\s+["']([^"']+)["']"""),
    ],
}

# Database query patterns
DB_PATTERNS: dict[str, list[tuple[str, re.Pattern[str]]]] = {
    "python": [
        ("raw_sql", re.compile(r"""(?:execute|executemany|raw|cursor)\s*\(.*(?:SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)""", re.IGNORECASE)),
        ("orm_query", re.compile(r"""\.(?:filter|exclude|annotate|aggregate|select_related|prefetch_related|values|values_list|all|get|create|update|delete|bulk_create|bulk_update)\s*\(""")),
        ("raw_sql", re.compile(r"""(?:text|RawSQL)\s*\(\s*["'](?:SELECT|INSERT|UPDATE|DELETE)""", re.IGNORECASE)),
        ("transaction", re.compile(r"""(?:atomic|begin|commit|rollback|transaction|savepoint)""")),
        ("n_plus_one_risk", re.compile(r"""for\s+\w+\s+in\s+.*\.(?:all|filter|objects)\b""")),
    ],
    "javascript": [
        ("raw_sql", re.compile(r"""\.(?:query|raw|execute)\s*\(\s*[`"'](?:SELECT|INSERT|UPDATE|DELETE)""", re.IGNORECASE)),
        ("orm_query", re.compile(r"""\.(?:findMany|findUnique|findFirst|find|findOne|create|update|delete|aggregate|groupBy|where|select)\s*\(""")),
        ("raw_sql", re.compile(r"""(?:knex|db|pool|client)\s*\.\s*(?:query|raw)\s*\(""")),
        ("transaction", re.compile(r"""(?:\$transaction|\.transaction|BEGIN|COMMIT|ROLLBACK)""")),
    ],
    "go": [
        ("raw_sql", re.compile(r"""(?:Query|QueryRow|Exec|Prepare)\s*\(\s*(?:ctx\s*,\s*)?["`](?:SELECT|INSERT|UPDATE|DELETE)""", re.IGNORECASE)),
        ("orm_query", re.compile(r"""\.(?:Find|First|Create|Save|Delete|Where|Joins|Preload|Association)\s*\(""")),
        ("transaction", re.compile(r"""(?:Begin|Commit|Rollback|\.Tx)\b""")),
    ],
    "rust": [
        ("raw_sql", re.compile(r"""(?:query|query_as|execute)\s*!\s*\(\s*["r].*(?:SELECT|INSERT|UPDATE|DELETE)""", re.IGNORECASE)),
        ("orm_query", re.compile(r"""\.(?:filter|find|insert_into|update|delete|select|load|get_result)\s*\(""")),
        ("transaction", re.compile(r"""(?:begin|commit|rollback|transaction)\b""")),
    ],
    "java": [
        ("raw_sql", re.compile(r"""(?:createQuery|createNativeQuery|prepareStatement|executeQuery|executeUpdate)\s*\(\s*"(?:SELECT|INSERT|UPDATE|DELETE)""", re.IGNORECASE)),
        ("orm_query", re.compile(r"""(?:CriteriaBuilder|JpaRepository|findBy|save|delete|findAll|getOne)\b""")),
        ("transaction", re.compile(r"""@Transactional|\.beginTransaction|\.commit|\.rollback""")),
    ],
}

# Error handling patterns
ERROR_PATTERNS: dict[str, list[tuple[str, re.Pattern[str]]]] = {
    "python": [
        ("bare_except", re.compile(r"""except\s*:""")),
        ("broad_except", re.compile(r"""except\s+(?:Exception|BaseException)\b""")),
        ("pass_except", re.compile(r"""except.*:\s*\n\s+pass\b""")),
        ("error_response", re.compile(r"""(?:HTTPException|abort|JsonResponse|Response)\s*\(.*(?:4\d{2}|5\d{2}|status)""")),
        ("raise_generic", re.compile(r"""raise\s+Exception\s*\(""")),
    ],
    "javascript": [
        ("empty_catch", re.compile(r"""catch\s*\([^)]*\)\s*\{\s*\}""")),
        ("console_error", re.compile(r"""catch\s*\([^)]*\)\s*\{\s*console\.\w+""")),
        ("error_response", re.compile(r"""(?:res\.status|response\.status|throw\s+new\s+\w*(?:Error|Exception))""")),
        ("unhandled_promise", re.compile(r"""\.then\s*\([^)]*\)\s*(?!\.catch)""")),
    ],
    "go": [
        ("ignored_error", re.compile(r"""(?:_\s*=|,\s*_\s*:?=)\s*\w+\.\w+\s*\(""")),
        ("error_check", re.compile(r"""if\s+err\s*!=\s*nil""")),
        ("wrap_error", re.compile(r"""fmt\.Errorf\s*\(\s*".*%w""")),
        ("bare_error", re.compile(r"""return\s+.*errors\.New\s*\(""")),
    ],
    "rust": [
        ("unwrap", re.compile(r"""\.unwrap\s*\(\s*\)""")),
        ("expect", re.compile(r"""\.expect\s*\(\s*"[^"]*"\s*\)""")),
        ("error_type", re.compile(r"""impl\s+(?:std::)?(?:error::)?Error\s+for""")),
        ("question_mark", re.compile(r"""\?\s*;""")),
    ],
}

# Security-related patterns
SECURITY_PATTERNS: dict[str, list[tuple[str, re.Pattern[str]]]] = {
    "python": [
        ("hardcoded_secret", re.compile(r"""(?:password|secret|api_key|token|private_key)\s*=\s*["'][^"']{8,}["']""", re.IGNORECASE)),
        ("sql_injection_risk", re.compile(r"""(?:execute|raw)\s*\(\s*(?:f["']|["'].*%s|.*\.format\()""")),
        ("command_injection", re.compile(r"""(?:os\.system|subprocess\.call|subprocess\.Popen|os\.popen)\s*\(.*(?:f["']|\+|\.format)""")),
        ("no_auth", re.compile(r"""@\w+\.(get|post|put|patch|delete)\s*\(""")),
        ("cors", re.compile(r"""(?:CORS|cors|Access-Control-Allow-Origin)""")),
        ("debug_mode", re.compile(r"""(?:DEBUG\s*=\s*True|\.run\s*\(.*debug\s*=\s*True)""")),
    ],
    "javascript": [
        ("hardcoded_secret", re.compile(r"""(?:password|secret|apiKey|token|privateKey)\s*[:=]\s*["'][^"']{8,}["']""", re.IGNORECASE)),
        ("sql_injection_risk", re.compile(r"""(?:query|execute)\s*\(\s*(?:`.*\$\{|["'].*\+)""")),
        ("xss_risk", re.compile(r"""(?:innerHTML|dangerouslySetInnerHTML|document\.write)\s*[=({]""")),
        ("eval_usage", re.compile(r"""(?:eval|Function)\s*\(""")),
        ("cors", re.compile(r"""(?:cors|Access-Control-Allow-Origin)""")),
    ],
    "go": [
        ("hardcoded_secret", re.compile(r'''(?:password|secret|apiKey|token)\s*[:=]\s*"[^"]{8,}"''', re.IGNORECASE)),
        ("sql_injection_risk", re.compile(r"""(?:Query|Exec)\s*\(\s*(?:ctx\s*,\s*)?(?:fmt\.Sprintf|.*\+)""")),
        ("command_injection", re.compile(r"""exec\.Command\s*\(.*(?:\+|fmt\.Sprintf)""")),
    ],
    "rust": [
        ("hardcoded_secret", re.compile(r'''(?:password|secret|api_key|token)\s*[:=]\s*"[^"]{8,}"''', re.IGNORECASE)),
        ("sql_injection_risk", re.compile(r"""(?:query|execute)\s*\(\s*&?format!\s*\(""")),
        ("unsafe_block", re.compile(r"""unsafe\s*\{""")),
    ],
}

# Auth/middleware patterns (positive signals)
AUTH_PATTERNS: dict[str, list[re.Pattern[str]]] = {
    "python": [
        re.compile(r"""(?:@login_required|@permission_required|@auth|@jwt_required|@requires_auth|IsAuthenticated|Depends\(.*auth|Depends\(.*current_user)"""),
    ],
    "javascript": [
        re.compile(r"""(?:authenticate|authorize|isAuth|requireAuth|verifyToken|passport\.|jwt\.verify|auth\s*middleware)""", re.IGNORECASE),
    ],
    "go": [
        re.compile(r"""(?:AuthMiddleware|RequireAuth|JWTMiddleware|WithAuth|authRequired)"""),
    ],
    "rust": [
        re.compile(r"""(?:auth|jwt|bearer|require_auth|validate_token)""", re.IGNORECASE),
    ],
}

# Input validation patterns (positive signals)
VALIDATION_PATTERNS: dict[str, list[re.Pattern[str]]] = {
    "python": [
        re.compile(r"""(?:pydantic|Schema|Serializer|validate|validator|Field\(|@validates)"""),
    ],
    "javascript": [
        re.compile(r"""(?:zod|yup|joi|ajv|celebrate|express-validator|\.validate|\.parse)"""),
    ],
    "go": [
        re.compile(r"""(?:validate|binding:"required|validator\.New)"""),
    ],
    "rust": [
        re.compile(r"""(?:Validate|#\[validate|serde|Deserialize)"""),
    ],
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class EndpointInfo:
    method: str
    path: str
    file: str
    line: int
    has_auth: bool = False
    has_validation: bool = False


@dataclass
class DBQueryInfo:
    kind: str  # raw_sql, orm_query, transaction, n_plus_one_risk
    file: str
    line: int
    snippet: str = ""


@dataclass
class ErrorInfo:
    kind: str
    file: str
    line: int
    snippet: str = ""


@dataclass
class SecurityFinding:
    kind: str
    file: str
    line: int
    snippet: str = ""


@dataclass
class ScanResult:
    endpoints: list[EndpointInfo] = field(default_factory=list)
    db_queries: list[DBQueryInfo] = field(default_factory=list)
    error_patterns: list[ErrorInfo] = field(default_factory=list)
    security_findings: list[SecurityFinding] = field(default_factory=list)
    files_scanned: int = 0
    files_with_endpoints: set[str] = field(default_factory=set)
    files_with_db: set[str] = field(default_factory=set)
    auth_present: set[str] = field(default_factory=set)
    validation_present: set[str] = field(default_factory=set)


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

def iter_source_files(repo: Path, max_files: int) -> Iterator[Path]:
    count = 0
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in sorted(files):
            p = Path(root) / f
            if p.suffix in EXTENSIONS:
                yield p
                count += 1
                if count >= max_files:
                    return


def scan_file(path: Path, repo: Path, result: ScanResult) -> None:
    try:
        content = path.read_text(errors="replace")
    except (OSError, PermissionError):
        return

    rel = str(path.relative_to(repo))
    if TEST_INDICATORS.search(rel):
        return

    lang = EXT_TO_LANG.get(path.suffix, "")
    if not lang:
        return

    lines = content.splitlines()

    # Check for auth and validation presence in the file
    file_has_auth = False
    file_has_validation = False
    for pat in AUTH_PATTERNS.get(lang, []):
        if pat.search(content):
            file_has_auth = True
            result.auth_present.add(rel)
            break
    for pat in VALIDATION_PATTERNS.get(lang, []):
        if pat.search(content):
            file_has_validation = True
            result.validation_present.add(rel)
            break

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("//"):
            continue

        # Endpoints
        for pat in ROUTE_PATTERNS.get(lang, []):
            m = pat.search(line)
            if m:
                groups = [g for g in m.groups() if g]
                method = groups[0].upper() if len(groups) >= 2 else "?"
                path_str = groups[-1] if groups else "?"
                result.endpoints.append(EndpointInfo(
                    method=method,
                    path=path_str,
                    file=rel,
                    line=i,
                    has_auth=file_has_auth,
                    has_validation=file_has_validation,
                ))
                result.files_with_endpoints.add(rel)

        # DB patterns
        for kind, pat in DB_PATTERNS.get(lang, []):
            if pat.search(line):
                snippet = stripped[:120]
                result.db_queries.append(DBQueryInfo(kind=kind, file=rel, line=i, snippet=snippet))
                result.files_with_db.add(rel)

        # Error patterns
        for kind, pat in ERROR_PATTERNS.get(lang, []):
            if pat.search(line):
                snippet = stripped[:120]
                result.error_patterns.append(ErrorInfo(kind=kind, file=rel, line=i, snippet=snippet))

        # Security patterns
        for kind, pat in SECURITY_PATTERNS.get(lang, []):
            if pat.search(line):
                snippet = stripped[:120]
                result.security_findings.append(SecurityFinding(kind=kind, file=rel, line=i, snippet=snippet))


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(result: ScanResult, repo: Path) -> str:
    lines: list[str] = []
    w = lines.append

    w("# Endpoint & Implementation Scan")
    w("")
    w(f"> Repository: `{repo}` | Generated: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    w("")

    # Summary
    w("## Summary")
    w("")
    w("| Metric | Value |")
    w("|--------|-------|")
    w(f"| Files scanned | {result.files_scanned} |")
    w(f"| API endpoints found | {len(result.endpoints)} |")
    w(f"| Files with endpoints | {len(result.files_with_endpoints)} |")
    w(f"| DB query patterns | {len(result.db_queries)} |")
    w(f"| Files with DB access | {len(result.files_with_db)} |")
    w(f"| Error handling patterns | {len(result.error_patterns)} |")
    w(f"| Security findings | {len(result.security_findings)} |")
    w(f"| Files with auth patterns | {len(result.auth_present)} |")
    w(f"| Files with validation | {len(result.validation_present)} |")
    w("")

    # Endpoints
    if result.endpoints:
        w("## API Endpoints")
        w("")
        w("| Method | Path | File | Auth | Validation |")
        w("|--------|------|------|------|------------|")
        for ep in result.endpoints[:50]:
            auth = "Yes" if ep.has_auth else "**No**"
            val = "Yes" if ep.has_validation else "**No**"
            w(f"| {ep.method} | `{ep.path}` | `{ep.file}:{ep.line}` | {auth} | {val} |")
        if len(result.endpoints) > 50:
            w(f"| ... | *{len(result.endpoints) - 50} more endpoints* | | | |")
        w("")

        # Unprotected endpoints
        unprotected = [ep for ep in result.endpoints if not ep.has_auth]
        if unprotected:
            w("### Endpoints Without Auth Patterns")
            w("")
            w(f"**{len(unprotected)} of {len(result.endpoints)} endpoints** lack visible auth decorators/middleware.")
            w("These may be intentionally public or may be missing auth — verify each one.")
            w("")

    # DB patterns
    if result.db_queries:
        w("## Database Patterns")
        w("")

        # Group by kind
        by_kind: dict[str, list[DBQueryInfo]] = {}
        for q in result.db_queries:
            by_kind.setdefault(q.kind, []).append(q)

        kind_labels = {
            "raw_sql": "Raw SQL Queries",
            "orm_query": "ORM Queries",
            "transaction": "Transaction Handling",
            "n_plus_one_risk": "N+1 Query Risk",
        }

        for kind, label in kind_labels.items():
            items = by_kind.get(kind, [])
            if items:
                w(f"### {label} ({len(items)})")
                w("")
                w("| File | Snippet |")
                w("|------|---------|")
                for q in items[:20]:
                    w(f"| `{q.file}:{q.line}` | `{q.snippet}` |")
                if len(items) > 20:
                    w(f"| ... | *{len(items) - 20} more* |")
                w("")

    # Error handling
    if result.error_patterns:
        w("## Error Handling Patterns")
        w("")

        by_kind: dict[str, list[ErrorInfo]] = {}
        for e in result.error_patterns:
            by_kind.setdefault(e.kind, []).append(e)

        kind_labels = {
            "bare_except": "Bare Except (catches everything)",
            "broad_except": "Broad Exception Catch",
            "pass_except": "Swallowed Exceptions (except + pass)",
            "empty_catch": "Empty Catch Blocks",
            "console_error": "Console-only Error Handling",
            "ignored_error": "Ignored Errors (Go _ = err)",
            "unwrap": "Unwrap Without Context (Rust)",
            "raise_generic": "Generic Exception Raised",
            "unhandled_promise": "Unhandled Promise (no .catch)",
        }

        for kind, label in kind_labels.items():
            items = by_kind.get(kind, [])
            if items:
                w(f"### {label} ({len(items)})")
                w("")
                w("| File | Snippet |")
                w("|------|---------|")
                for e in items[:15]:
                    w(f"| `{e.file}:{e.line}` | `{e.snippet}` |")
                if len(items) > 15:
                    w(f"| ... | *{len(items) - 15} more* |")
                w("")

        # Also show positive patterns
        positive_kinds = {"error_check", "wrap_error", "error_response", "error_type", "question_mark", "expect"}
        positive = {k: v for k, v in by_kind.items() if k in positive_kinds}
        if positive:
            w("### Positive Error Handling Patterns")
            w("")
            for kind, items in positive.items():
                w(f"- **{kind}**: {len(items)} occurrences")
            w("")

    # Security findings
    if result.security_findings:
        w("## Security Findings")
        w("")

        by_kind: dict[str, list[SecurityFinding]] = {}
        for s in result.security_findings:
            by_kind.setdefault(s.kind, []).append(s)

        kind_labels = {
            "hardcoded_secret": "Potential Hardcoded Secrets",
            "sql_injection_risk": "SQL Injection Risk",
            "command_injection": "Command Injection Risk",
            "xss_risk": "XSS Risk",
            "eval_usage": "Eval / Dynamic Code Execution",
            "unsafe_block": "Unsafe Blocks (Rust)",
            "debug_mode": "Debug Mode Enabled",
            "cors": "CORS Configuration",
        }

        for kind, label in kind_labels.items():
            items = by_kind.get(kind, [])
            if items:
                w(f"### {label} ({len(items)})")
                w("")
                w("| File | Snippet |")
                w("|------|---------|")
                for s in items[:15]:
                    w(f"| `{s.file}:{s.line}` | `{s.snippet}` |")
                if len(items) > 15:
                    w(f"| ... | *{len(items) - 15} more* |")
                w("")

    # Files to review
    w("## Priority Files for Review")
    w("")
    w("Files with the most signals (endpoints + DB + error + security patterns):")
    w("")

    file_scores: dict[str, int] = {}
    for ep in result.endpoints:
        file_scores[ep.file] = file_scores.get(ep.file, 0) + 2
        if not ep.has_auth:
            file_scores[ep.file] += 1
    for q in result.db_queries:
        file_scores[q.file] = file_scores.get(q.file, 0) + 1
        if q.kind in ("raw_sql", "n_plus_one_risk"):
            file_scores[q.file] += 2
    for e in result.error_patterns:
        file_scores[e.file] = file_scores.get(e.file, 0) + 1
        if e.kind in ("bare_except", "pass_except", "empty_catch", "ignored_error"):
            file_scores[e.file] += 2
    for s in result.security_findings:
        file_scores[s.file] = file_scores.get(s.file, 0) + 3

    ranked = sorted(file_scores.items(), key=lambda x: x[1], reverse=True)
    if ranked:
        w("| File | Score | Signals |")
        w("|------|-------|---------|")
        for fpath, score in ranked[:20]:
            signals = []
            ep_count = sum(1 for e in result.endpoints if e.file == fpath)
            db_count = sum(1 for q in result.db_queries if q.file == fpath)
            err_count = sum(1 for e in result.error_patterns if e.file == fpath)
            sec_count = sum(1 for s in result.security_findings if s.file == fpath)
            if ep_count:
                signals.append(f"{ep_count} endpoints")
            if db_count:
                signals.append(f"{db_count} DB")
            if err_count:
                signals.append(f"{err_count} errors")
            if sec_count:
                signals.append(f"{sec_count} security")
            w(f"| `{fpath}` | {score} | {', '.join(signals)} |")
        w("")
    else:
        w("No significant signals detected.")
        w("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Scan repo for implementation review hot spots")
    parser.add_argument("--repo", required=True, help="Path to repository root")
    parser.add_argument("--output", default=None, help="Output path (default: <repo>/.hand-offs/endpoint-scan.md)")
    parser.add_argument("--max-files", type=int, default=5000, help="Max files to scan")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"Error: {repo} is not a directory", file=sys.stderr)
        sys.exit(1)

    output = Path(args.output) if args.output else repo / ".hand-offs" / "endpoint-scan.md"
    output.parent.mkdir(parents=True, exist_ok=True)

    # Scan
    result = ScanResult()
    files = list(iter_source_files(repo, args.max_files))
    if not files:
        print(f"No source files found in {repo}", file=sys.stderr)
        sys.exit(1)

    result.files_scanned = len(files)
    print(f"Scanning {len(files)} source files...", file=sys.stderr)

    for f in files:
        scan_file(f, repo, result)

    # Generate report
    report = generate_report(result, repo)
    output.write_text(report)
    print(f"Report written to {output}", file=sys.stderr)
    print(report)


if __name__ == "__main__":
    main()
