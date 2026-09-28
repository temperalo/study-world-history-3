#!/usr/bin/env python3
"""
Stop hook — verifies discipline before session ends.

Rules:
  1. If today's session log references a large/extra-high/max (high+) task AND
     docs/.rules-audit.md has no entry today → block.
  2. If changes committed today AND no session log exists today → block.
  3. Soft hint: 5+ high+ tasks in last 14 days + audit stale 30+ days → suggest /rules-retro.

Otherwise allow.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# Run relative to project root regardless of shell cwd
os.chdir(Path(__file__).resolve().parents[2])


SCALE_RE = re.compile(r"\((high|extra high|max|large)\)", re.IGNORECASE)


def session_log_path() -> Path:
    return Path("docs/sessions") / f"session_{date.today():%y%m%d}.md"


def has_large_scale(log: Path) -> bool:
    if not log.is_file():
        return False
    try:
        return bool(SCALE_RE.search(log.read_text(encoding="utf-8", errors="ignore")))
    except OSError:
        return False


def audit_has_today_entry(audit: Path) -> bool:
    if not audit.is_file():
        return False
    try:
        text = audit.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    return f"{date.today():%Y-%m-%d}" in text


def code_committed_today() -> bool:
    try:
        out = subprocess.run(
            ["git", "log", f"--since={date.today():%Y-%m-%d}", "--oneline"],
            capture_output=True, text=True, timeout=5,
        )
        return bool(out.stdout.strip())
    except (OSError, subprocess.TimeoutExpired):
        return False


def count_recent_large_tasks(days: int = 14) -> int:
    sessions = Path("docs/sessions")
    if not sessions.is_dir():
        return 0
    cutoff = datetime.now() - timedelta(days=days)
    count = 0
    for s in sessions.glob("session_*.md"):
        if datetime.fromtimestamp(s.stat().st_mtime) < cutoff:
            continue
        try:
            text = s.read_text(encoding="utf-8", errors="ignore")
            count += len(SCALE_RE.findall(text))
        except OSError:
            pass
    return count


def audit_file_age_days() -> int:
    audit = Path("docs/.rules-audit.md")
    if not audit.is_file():
        return 999
    age = datetime.now() - datetime.fromtimestamp(audit.stat().st_mtime)
    return age.days


def main() -> None:
    sys.stdin.read()  # drain

    log = session_log_path()
    audit = Path("docs/.rules-audit.md")

    # Rule 1: high+ task → require audit entry
    if has_large_scale(log) and not audit_has_today_entry(audit):
        print(json.dumps({
            "decision": "block",
            "reason": (
                "Task was high/extra-high/max scale. "
                "Write audit entry to docs/.rules-audit.md per workflow.md §Rules audit."
            ),
        }))
        return

    # Rule 2: commits without session log
    if not log.is_file() and code_committed_today():
        print(json.dumps({
            "decision": "block",
            "reason": f"Changes committed today but no session log at {log}. Write it.",
        }))
        return

    # Rule 3: soft hint for /rules-retro
    recent_large = count_recent_large_tasks(14)
    if recent_large >= 5 and audit_file_age_days() >= 30:
        print(json.dumps({
            "decision": "allow",
            "reason": (
                f"Hint: {recent_large} high+ tasks accumulated in last 14 days and "
                f"audit is stale ({audit_file_age_days()}d). Consider running `/rules-retro`."
            ),
        }))
        return

    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
