#!/usr/bin/env python3
"""
SessionStart hook — injects docs/.compact-snapshot.md into the fresh context.

PreCompact hook (pre_compact_snapshot.py) writes the snapshot; this hook delivers it
deterministically on the next session start (compact / clear / resume / startup) and
consumes the file. Replaces the old always-on rule "if snapshot exists — read it
first", which relied on the model remembering to check.

Registered without a matcher: fires on every SessionStart, exits silently when no
snapshot exists. Shared across templates (single source at 999.claude/shared/hooks/).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Run relative to project root regardless of shell cwd
os.chdir(Path(__file__).resolve().parents[2])

SNAPSHOT = Path("docs/.compact-snapshot.md")


def main() -> None:
    sys.stdin.read()
    if not SNAPSHOT.is_file():
        sys.exit(0)
    try:
        content = SNAPSHOT.read_text(encoding="utf-8")
    except OSError:
        sys.exit(0)
    try:
        SNAPSHOT.unlink()
    except OSError:
        pass  # stale copy will be re-consumed on the next session start
    ctx = (
        "Post-compact snapshot (авто-инъекция SessionStart-хуком; файл уже удалён). "
        "Заполни <!-- ... --> плейсхолдеры из git log / недавних правок и продолжай "
        "текущую задачу с этим состоянием:\n\n" + content
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
