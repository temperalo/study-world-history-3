#!/usr/bin/env python3
"""
PreCompact hook — dumps a fixed-schema snapshot before context compaction.

The agent reads docs/.compact-snapshot.md on resume, fills the <!-- ... -->
placeholders, and deletes the file.

The fixed schema is what matters — it gives the agent a known structure to
recover from. Content of placeholders is filled post-compact by the agent
itself (hook doesn't know plan/decisions from stdin).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Run relative to project root regardless of shell cwd
os.chdir(Path(__file__).resolve().parents[2])

SNAPSHOT = Path("docs/.compact-snapshot.md")


def git(*args: str) -> str:
    try:
        out = subprocess.run(
            ["git", *args],
            capture_output=True, text=True, timeout=5,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return ""


def git_tail() -> str:
    return git("log", "--oneline", "-5") or "(no git)"


def git_status() -> str:
    return git("status", "--short") or "(clean)"


def git_diff_stat() -> str:
    return git("diff", "--stat") or "(no diff)"


def main() -> None:
    sys.stdin.read()  # drain
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# Compact snapshot — {ts}

## Active plan
<!-- one-paragraph summary if ExitPlanMode was used this session, else: "no active plan" -->

## Recent decisions (unlogged)
<!-- last 3 decisions NOT yet in decisions-log.md / style-decisions.md -->

## Current task
- Label: <!-- label from §1.1 -->
- Scale: <!-- small / medium / large -->
- Effort: <!-- low / medium / high / extra high / max -->

## Open questions
<!-- unresolved, or "none" -->

## Git log (auto-filled)
```
{git_tail()}
```

## Git status (auto-filled)
```
{git_status()}
```

## Git diff stat (auto-filled)
```
{git_diff_stat()}
```
"""
    SNAPSHOT.write_text(content, encoding="utf-8")
    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
