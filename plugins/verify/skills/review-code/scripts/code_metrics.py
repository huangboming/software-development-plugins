#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# ///
"""
Scan a backend repository for clean-code hot spots.

Produces a Markdown report with file sizes, function counts, and flagged
hot spots (large files, long functions, high import counts) to guide a
clean-code review toward the highest-value targets.

Usage:
    uv run --script code_metrics.py --repo <path> [--output <path>] [--max-files N]

Output: Markdown report (default: .hand-offs/code-metrics.md)
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
    ".cs", ".scala", ".swift",
}

IGNORED_DIRS = {
    ".git", ".hg", ".svn", ".idea", ".vscode",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".venv", "venv", "env", "node_modules",
    "dist", "build", "out", "coverage", "target", "vendor",
    ".next", ".nuxt", ".output",
}

# Thresholds
LARGE_FILE_LOC = 300
LONG_FUNCTION_LOC = 40
HIGH_IMPORT_COUNT = 15
MANY_FUNCTIONS = 20
HIGH_PARAM_COUNT = 5

# Regex patterns for function/method detection (language-grouped)
FUNC_PATTERNS: dict[str, re.Pattern[str]] = {
    "python":     re.compile(r"^\s*(async\s+)?def\s+(\w+)\s*\("),
    "javascript": re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(|^\s*(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)|[^=])\s*=>"),
    "go":         re.compile(r"^func\s+(?:\([^)]+\)\s+)?(\w+)\s*\("),
    "rust":       re.compile(r"^\s*(?:pub\s+)?(?:async\s+)?fn\s+(\w+)"),
    "java":       re.compile(r"^\s*(?:public|private|protected|static|final|abstract|synchronized|native|\s)*\s+\w+(?:<[^>]*>)?\s+(\w+)\s*\("),
    "ruby":       re.compile(r"^\s*def\s+(\w+)"),
}

CLASS_PATTERNS: dict[str, re.Pattern[str]] = {
    "python":     re.compile(r"^\s*class\s+(\w+)"),
    "javascript": re.compile(r"^\s*(?:export\s+)?class\s+(\w+)"),
    "go":         re.compile(r"^type\s+(\w+)\s+struct\b"),
    "rust":       re.compile(r"^\s*(?:pub\s+)?struct\s+(\w+)"),
    "java":       re.compile(r"^\s*(?:public|private|protected|abstract|final|\s)*class\s+(\w+)"),
    "ruby":       re.compile(r"^\s*class\s+(\w+)"),
}

IMPORT_PATTERNS: dict[str, re.Pattern[str]] = {
    "python":     re.compile(r"^\s*(?:import|from)\s+"),
    "javascript": re.compile(r"^\s*import\s+|^\s*(?:const|let|var)\s+.*=\s*require\s*\("),
    "go":         re.compile(r"^\s*\"[^\"]+\""),  # inside import block
    "rust":       re.compile(r"^\s*use\s+"),
    "java":       re.compile(r"^\s*import\s+"),
    "ruby":       re.compile(r"^\s*require\s+"),
}

PARAM_PATTERN = re.compile(r"\(([^)]*)\)")

EXT_TO_LANG: dict[str, str] = {
    ".py": "python",
    ".js": "javascript", ".ts": "javascript", ".jsx": "javascript", ".tsx": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java", ".kt": "java", ".scala": "java",
    ".rb": "ruby",
    ".cs": "java", ".swift": "java",
}

TEST_INDICATORS = re.compile(
    r"(^test_|_test\.|\.test\.|\.spec\.|_spec\.|/tests?/|/specs?/|/__tests__/)",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class FunctionInfo:
    name: str
    line: int
    loc: int = 0
    param_count: int = 0


@dataclass
class FileMetrics:
    path: str
    loc: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    import_count: int = 0
    function_count: int = 0
    class_count: int = 0
    functions: list[FunctionInfo] = field(default_factory=list)
    is_test: bool = False
    max_nesting: int = 0


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

def iter_source_files(repo: Path, max_files: int) -> Iterator[Path]:
    """Walk repo yielding source files, respecting ignore list and max count."""
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


def count_params(line: str) -> int:
    """Estimate parameter count from a function signature line."""
    m = PARAM_PATTERN.search(line)
    if not m:
        return 0
    params = m.group(1).strip()
    if not params or params == "self" or params == "cls":
        return 0
    # Filter out self/cls for Python
    parts = [p.strip() for p in params.split(",") if p.strip() not in ("self", "cls", "")]
    return len(parts)


def estimate_nesting(line: str, lang: str) -> int:
    """Estimate nesting depth from indentation."""
    stripped = line.expandtabs(4)
    indent = len(stripped) - len(stripped.lstrip())
    if lang == "python":
        return indent // 4
    else:
        return indent // 4  # rough heuristic for brace languages


def analyze_file(path: Path, repo: Path) -> FileMetrics | None:
    """Analyze a single source file for metrics."""
    try:
        content = path.read_text(errors="replace")
    except (OSError, PermissionError):
        return None

    rel = str(path.relative_to(repo))
    lang = EXT_TO_LANG.get(path.suffix, "")
    lines = content.splitlines()

    m = FileMetrics(
        path=rel,
        loc=len(lines),
        is_test=bool(TEST_INDICATORS.search(rel)),
    )

    func_pat = FUNC_PATTERNS.get(lang)
    class_pat = CLASS_PATTERNS.get(lang)
    import_pat = IMPORT_PATTERNS.get(lang)

    current_func: FunctionInfo | None = None
    func_start_line = 0
    max_nesting = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Blank lines
        if not stripped:
            m.blank_lines += 1
            continue

        # Comment lines (rough)
        if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("/*"):
            m.comment_lines += 1

        # Imports
        if import_pat and import_pat.match(line):
            m.import_count += 1

        # Nesting
        nest = estimate_nesting(line, lang)
        if nest > max_nesting:
            max_nesting = nest

        # Classes
        if class_pat and class_pat.match(line):
            m.class_count += 1

        # Functions
        if func_pat and func_pat.match(line):
            # Close previous function
            if current_func:
                current_func.loc = i - func_start_line
                m.functions.append(current_func)

            groups = func_pat.match(line).groups()  # type: ignore[union-attr]
            name = next((g for g in groups if g), "anonymous")
            current_func = FunctionInfo(
                name=name,
                line=i,
                param_count=count_params(line),
            )
            func_start_line = i
            m.function_count += 1

    # Close last function
    if current_func:
        current_func.loc = len(lines) - func_start_line + 1
        m.functions.append(current_func)

    m.max_nesting = max_nesting
    return m


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(metrics: list[FileMetrics], repo: Path) -> str:
    """Generate a Markdown report from file metrics."""
    lines: list[str] = []
    w = lines.append

    total_files = len(metrics)
    source_files = [m for m in metrics if not m.is_test]
    test_files = [m for m in metrics if m.is_test]
    total_loc = sum(m.loc for m in metrics)

    w(f"# Code Metrics Report")
    w(f"")
    w(f"> Repository: `{repo}` | Generated: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    w(f"")

    # Summary
    w(f"## Summary")
    w(f"")
    w(f"| Metric | Value |")
    w(f"|--------|-------|")
    w(f"| Source files | {len(source_files)} |")
    w(f"| Test files | {len(test_files)} |")
    w(f"| Total LOC | {total_loc:,} |")
    w(f"| Source LOC | {sum(m.loc for m in source_files):,} |")
    w(f"| Test LOC | {sum(m.loc for m in test_files):,} |")
    if source_files:
        avg_loc = sum(m.loc for m in source_files) // len(source_files)
        w(f"| Avg file size (source) | {avg_loc} LOC |")
        test_ratio = len(test_files) / len(source_files) if source_files else 0
        w(f"| Test-to-source ratio | {test_ratio:.2f} |")
    w(f"")

    # Hot spots: Large files
    large_files = sorted(
        [m for m in source_files if m.loc >= LARGE_FILE_LOC],
        key=lambda m: m.loc,
        reverse=True,
    )
    if large_files:
        w(f"## Large Files (>={LARGE_FILE_LOC} LOC)")
        w(f"")
        w(f"| File | LOC | Functions | Classes | Imports |")
        w(f"|------|-----|-----------|---------|---------|")
        for m in large_files[:30]:
            w(f"| `{m.path}` | {m.loc} | {m.function_count} | {m.class_count} | {m.import_count} |")
        w(f"")

    # Hot spots: Long functions
    long_funcs: list[tuple[str, FunctionInfo]] = []
    for m in source_files:
        for f in m.functions:
            if f.loc >= LONG_FUNCTION_LOC:
                long_funcs.append((m.path, f))
    long_funcs.sort(key=lambda x: x[1].loc, reverse=True)

    if long_funcs:
        w(f"## Long Functions (>={LONG_FUNCTION_LOC} LOC)")
        w(f"")
        w(f"| File | Function | LOC | Params |")
        w(f"|------|----------|-----|--------|")
        for path, f in long_funcs[:30]:
            w(f"| `{path}:{f.line}` | `{f.name}` | {f.loc} | {f.param_count} |")
        w(f"")

    # Hot spots: High import count
    high_imports = sorted(
        [m for m in source_files if m.import_count >= HIGH_IMPORT_COUNT],
        key=lambda m: m.import_count,
        reverse=True,
    )
    if high_imports:
        w(f"## High Import Count (>={HIGH_IMPORT_COUNT})")
        w(f"")
        w(f"| File | Imports | LOC |")
        w(f"|------|---------|-----|")
        for m in high_imports[:20]:
            w(f"| `{m.path}` | {m.import_count} | {m.loc} |")
        w(f"")

    # Hot spots: Many functions per file
    many_funcs = sorted(
        [m for m in source_files if m.function_count >= MANY_FUNCTIONS],
        key=lambda m: m.function_count,
        reverse=True,
    )
    if many_funcs:
        w(f"## Files With Many Functions (>={MANY_FUNCTIONS})")
        w(f"")
        w(f"| File | Functions | LOC | Classes |")
        w(f"|------|-----------|-----|---------|")
        for m in many_funcs[:20]:
            w(f"| `{m.path}` | {m.function_count} | {m.loc} | {m.class_count} |")
        w(f"")

    # Hot spots: Functions with many parameters
    high_params: list[tuple[str, FunctionInfo]] = []
    for m in source_files:
        for f in m.functions:
            if f.param_count >= HIGH_PARAM_COUNT:
                high_params.append((m.path, f))
    high_params.sort(key=lambda x: x[1].param_count, reverse=True)

    if high_params:
        w(f"## Functions With Many Parameters (>={HIGH_PARAM_COUNT})")
        w(f"")
        w(f"| File | Function | Params | LOC |")
        w(f"|------|----------|--------|-----|")
        for path, f in high_params[:20]:
            w(f"| `{path}:{f.line}` | `{f.name}` | {f.param_count} | {f.loc} |")
        w(f"")

    # No hot spots found
    if not any([large_files, long_funcs, high_imports, many_funcs, high_params]):
        w(f"## Hot Spots")
        w(f"")
        w(f"No significant hot spots detected. File sizes, function lengths, and import counts are within normal ranges.")
        w(f"")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Scan repo for clean-code hot spots")
    parser.add_argument("--repo", required=True, help="Path to repository root")
    parser.add_argument("--output", default=None, help="Output path (default: <repo>/.hand-offs/code-metrics.md)")
    parser.add_argument("--max-files", type=int, default=5000, help="Max files to scan")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"Error: {repo} is not a directory", file=sys.stderr)
        sys.exit(1)

    output = Path(args.output) if args.output else repo / ".hand-offs" / "code-metrics.md"
    output.parent.mkdir(parents=True, exist_ok=True)

    # Scan
    files = list(iter_source_files(repo, args.max_files))
    if not files:
        print(f"No source files found in {repo}", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {len(files)} source files...", file=sys.stderr)
    metrics = []
    for f in files:
        m = analyze_file(f, repo)
        if m:
            metrics.append(m)

    # Generate report
    report = generate_report(metrics, repo)
    output.write_text(report)
    print(f"Report written to {output}", file=sys.stderr)
    print(report)


if __name__ == "__main__":
    main()
