#!/usr/bin/env python3
"""
SessionStart hook — surfaces a pending template upgrade at the top of the session.

`init.py --upgrade --apply-safe` applies auto+new files but STAGES files the user
has modified and writes `docs/upgrade-plan.md` (version is NOT bumped until the merge
is finished). This hook detects that pending state and injects an instruction so that
— regardless of what the user typed first — the model offers `/apply-template-upgrade`
before starting other work. The merge skill deletes `docs/upgrade-plan.md` on
completion, so the notice self-terminates (silent once resolved).

Registered without a matcher: fires on every SessionStart, exits silently when there
is no pending upgrade. Shared across templates (single source at 999.claude/shared/hooks/).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Run relative to project root regardless of shell cwd
os.chdir(Path(__file__).resolve().parents[2])

PLAN = Path("docs/upgrade-plan.md")


def main() -> None:
    sys.stdin.read()
    if not PLAN.is_file():
        sys.exit(0)
    try:
        plan = PLAN.read_text(encoding="utf-8")
    except OSError:
        sys.exit(0)
    # First heading line for a one-glance summary (e.g. version transition).
    head = next((ln for ln in plan.splitlines() if ln.strip()), "").lstrip("# ").strip()
    ctx = (
        "У проекта есть НЕЗАВЕРШЁННЫЙ template-upgrade: существует `docs/upgrade-plan.md` "
        f"({head}). `--apply-safe` уже применил безопасные файлы, но файлы с твоими "
        "правками застейджены в `.claude/.template-staging/`, версия НЕ бампнута.\n"
        "ПЕРЕД тем как браться за то, что написал пользователь — предложи одной строкой "
        "запустить `/apply-template-upgrade` (домержит застейдженное + бампнет версию). "
        "Не запускать молча и не мерджить самому вне скилла — только предложить; "
        "пользователь решает делать сейчас или отложить."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": ctx,
        }
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
