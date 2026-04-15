# /// script
# requires-python = ">=3.10"
# ///
"""Gather git commit stats for a given period across one or more repos.

Usage:
    uv run --script scripts/git_stats.py --period {daily,weekly,monthly} [--date DATE] [path ...]

Period formats:
    daily:   --date YYYY-MM-DD  (defaults to today)
    weekly:  --date YYYY-MM-DD  (uses ISO week containing that date; defaults to current week)
    monthly: --date YYYY-MM     (defaults to current month)

If no paths are given, defaults to the current directory.

Output: JSON to stdout.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date, timedelta


def run(cmd: list[str], cwd: str | None = None, stdin: str | None = None) -> str:
    result = subprocess.run(
        cmd, capture_output=True, text=True, check=True, input=stdin, cwd=cwd,
    )
    return result.stdout.strip()


def get_git_user(cwd: str) -> tuple[str, str]:
    name = run(["git", "config", "user.name"], cwd=cwd)
    email = run(["git", "config", "user.email"], cwd=cwd)
    return name, email


def get_repo_name(cwd: str) -> str:
    toplevel = run(["git", "rev-parse", "--show-toplevel"], cwd=cwd)
    return os.path.basename(toplevel)


def parse_period(period: str, date_arg: str | None) -> tuple[date, date]:
    """Return (start_date, end_date) inclusive range for the given period and date."""
    today = date.today()

    if period == "daily":
        if date_arg:
            match = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", date_arg)
            if not match:
                print(f"Error: Invalid date format '{date_arg}'. Expected YYYY-MM-DD for daily.", file=sys.stderr)
                sys.exit(1)
            d = date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        else:
            d = today
        return d, d

    elif period == "weekly":
        if date_arg:
            match = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", date_arg)
            if not match:
                print(f"Error: Invalid date format '{date_arg}'. Expected YYYY-MM-DD for weekly.", file=sys.stderr)
                sys.exit(1)
            d = date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        else:
            d = today
        start = d - timedelta(days=d.weekday())
        end = start + timedelta(days=6)
        return start, end

    elif period == "monthly":
        if date_arg:
            match = re.match(r"^(\d{4})-(\d{2})$", date_arg)
            if not match:
                print(f"Error: Invalid date format '{date_arg}'. Expected YYYY-MM for monthly.", file=sys.stderr)
                sys.exit(1)
            year, month = int(match.group(1)), int(match.group(2))
            if not 1 <= month <= 12:
                print(f"Error: Invalid month '{month}'. Must be 01-12.", file=sys.stderr)
                sys.exit(1)
        else:
            year, month = today.year, today.month
        start = date(year, month, 1)
        if month == 12:
            end = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end = date(year, month + 1, 1) - timedelta(days=1)
        return start, end

    else:
        print(f"Error: Unknown period '{period}'.", file=sys.stderr)
        sys.exit(1)


def date_in_range(date_str: str, start: date, end: date) -> bool:
    """Check if a YYYY-MM-DD date string falls within [start, end] inclusive."""
    try:
        d = date.fromisoformat(date_str)
    except ValueError:
        return False
    return start <= d <= end


CONVENTIONAL_RE = re.compile(
    r"^(?P<type>feat|fix|refactor|test|docs|chore|style|perf|ci|build|revert)"
    r"(?:\((?P<scope>[^)]+)\))?"
    r"!?:\s"
)


def parse_commit_type(message: str) -> tuple[str, str | None]:
    m = CONVENTIONAL_RE.match(message)
    if m:
        return m.group("type"), m.group("scope")
    return "other", None


def git_regex_escape(s: str) -> str:
    """Escape regex metacharacters for git's POSIX ERE using bracket expressions."""
    return re.sub(r"([.+*?^${}()|\\[\]])", r"[\1]", s)


def log_args(email: str) -> list[str]:
    """Common git log arguments. No date filter — Python enforces the range boundary.

    Anchors with <> and escapes regex metacharacters (., +) to prevent over-matching.
    """
    return [f"--author=<{git_regex_escape(email)}>", "--branches", "--remotes"]


def get_deduplicated_commits(
    email: str, start: date, end: date, cwd: str,
) -> tuple[set[str], list[tuple[str, str, str]]]:
    """Return (keep_set, ordered_entries) deduplicated by hash, patch-id, and subject.

    ordered_entries: list of (hash, date_str, subject) for commits in the target range.
    keep_set: set of hashes that survived dedup.
    """
    log_output = run(
        ["git", "log", *log_args(email), "--format=%H|%ad|%s", "--date=short"],
        cwd=cwd,
    )
    if not log_output:
        return set(), []

    # Collect in-range commits, dedup by hash
    ordered: list[tuple[str, str, str]] = []  # (hash, date, subject)
    seen_hashes: set[str] = set()
    for line in log_output.splitlines():
        parts = line.split("|", 2)
        if len(parts) != 3:
            continue
        h, date_str, subject = parts
        if h in seen_hashes:
            continue
        seen_hashes.add(h)
        if not date_in_range(date_str, start, end):
            continue
        ordered.append((h, date_str, subject))

    if not ordered:
        return set(), []

    # Compute patch-ids per commit
    hash_to_pid: dict[str, str] = {}
    for h, _, _ in ordered:
        try:
            diff = run(["git", "diff-tree", "-p", h], cwd=cwd)
            if diff:
                pid_line = run(["git", "patch-id", "--stable"], stdin=diff)
                if pid_line:
                    parts = pid_line.split()
                    if len(parts) >= 2:
                        hash_to_pid[parts[1]] = parts[0]
        except subprocess.CalledProcessError:
            pass

    # Dedup: patch-id first, then subject only for commits that have a patch-id
    seen_pids: set[str] = set()
    seen_subjects: set[str] = set()
    keep: set[str] = set()
    kept_entries: list[tuple[str, str, str]] = []
    for h, date_str, subject in ordered:
        pid = hash_to_pid.get(h)
        if pid:
            if pid in seen_pids:
                continue
            seen_pids.add(pid)
            if subject in seen_subjects:
                continue
            seen_subjects.add(subject)
        keep.add(h)
        kept_entries.append((h, date_str, subject))

    return keep, kept_entries


def build_commits(kept_entries: list[tuple[str, str, str]]) -> list[dict]:
    """Build commit dicts from the already-filtered entries."""
    commits = []
    for hash_, date_str, message in kept_entries:
        ctype, scope = parse_commit_type(message)
        commits.append({
            "hash": hash_[:7],
            "date": date_str,
            "type": ctype,
            "scope": scope,
            "message": message,
        })
    return commits


def get_loc_stats(
    email: str, start: date, end: date, keep: set[str], cwd: str,
) -> dict:
    numstat_output = run(
        ["git", "log", *log_args(email),
         "--numstat", "--format=COMMIT:%H|%ad", "--date=short"],
        cwd=cwd,
    )

    added = 0
    removed = 0
    seen: set[str] = set()
    skip = False
    for line in numstat_output.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("COMMIT:"):
            payload = line[7:]
            parts = payload.split("|", 1)
            hash_ = parts[0]
            date_str = parts[1] if len(parts) > 1 else ""
            skip = (
                hash_ in seen
                or hash_ not in keep
                or not date_in_range(date_str, start, end)
            )
            seen.add(hash_)
            continue
        if skip:
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        a, r, _ = parts
        if a != "-":
            added += int(a)
        if r != "-":
            removed += int(r)

    return {"added": added, "removed": removed, "total": added - removed}


def collect_repo(
    repo_path: str, email: str, start: date, end: date,
) -> dict:
    """Collect stats for a single repo."""
    repo_name = get_repo_name(repo_path)
    keep, kept_entries = get_deduplicated_commits(email, start, end, repo_path)
    commits = build_commits(kept_entries)
    loc = get_loc_stats(email, start, end, keep, repo_path)
    return {
        "name": repo_name,
        "path": os.path.abspath(repo_path),
        "commits": commits,
        "loc": loc,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Git commit stats for a given period")
    parser.add_argument(
        "--period", required=True, choices=["daily", "weekly", "monthly"],
        help="Period granularity",
    )
    parser.add_argument(
        "--date",
        help="Date for the period: YYYY-MM-DD (daily/weekly) or YYYY-MM (monthly). Defaults to current.",
    )
    parser.add_argument("paths", nargs="*", default=["."], help="Repo paths (default: .)")
    args = parser.parse_args()

    start, end = parse_period(args.period, args.date)

    repos = []
    total_added = 0
    total_removed = 0
    for path in args.paths:
        path = os.path.expanduser(path)
        if not os.path.isdir(path):
            print(f"Warning: skipping '{path}' (not a directory)", file=sys.stderr)
            continue
        try:
            name, email = get_git_user(path)
            repo = collect_repo(path, email, start, end)
        except subprocess.CalledProcessError as e:
            print(f"Warning: skipping '{path}' (git error: {e})", file=sys.stderr)
            continue
        except FileNotFoundError:
            print("Error: 'git' not found on PATH.", file=sys.stderr)
            sys.exit(1)
        repo["author"] = f"{name} <{email}>"
        repos.append(repo)
        total_added += repo["loc"]["added"]
        total_removed += repo["loc"]["removed"]

    output = {
        "period": args.period,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "repos": repos,
        "total_loc": {
            "added": total_added,
            "removed": total_removed,
            "total": total_added - total_removed,
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
