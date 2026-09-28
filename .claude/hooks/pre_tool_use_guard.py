#!/usr/bin/env python3
"""
PreToolUse hook (matcher: Write) — protects learning history from overwrite.

A full Write to an EXISTING file under:
  - artifacts/**          (real applied results — the proof you learned)
  - docs/journal.md       (append-only learning log)
is blocked. These accumulate irreplaceable history; a Write would clobber it.

Allowed without question:
  - Write to a NEW path (creating an artifact / first journal entry) — nothing to lose.
  - Edit / MultiEdit (append/surgical) — not matched by this hook, so untouched.

If overwrite is genuinely intended, the user removes the file first or edits it —
this hook only catches the accidental clobber.

Input:  JSON via stdin (tool_input.file_path).
Output: JSON {"decision":"allow"|"block","reason":"..."} to stdout.
"""

from __future__ import annotations

import fnmatch
import json
import os
import sys
from pathlib import Path

# Run relative to project root regardless of shell cwd
os.chdir(Path(__file__).resolve().parents[2])

PROTECTED_GLOBS = [
    ("artifacts/*", "artifacts/** — real applied result (learning history)"),
    ("artifacts/**/*", "artifacts/** — real applied result (learning history)"),
    ("docs/journal.md", "docs/journal.md — append-only learning log"),
]


def match_protected(path: str) -> str | None:
    normalized = path.replace("\\", "/")
    root = Path.cwd().as_posix().rstrip("/") + "/"
    if normalized.startswith(root):
        normalized = normalized[len(root):]
    for pattern, reason in PROTECTED_GLOBS:
        if fnmatch.fnmatch(normalized, pattern):
            return reason
    return None


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        print(json.dumps({"decision": "allow"}))
        return

    path = (data.get("tool_input") or {}).get("file_path") or ""
    if not path:
        print(json.dumps({"decision": "allow"}))
        return

    # Only an overwrite of an EXISTING protected file is dangerous.
    target = Path(path)
    if not target.is_file():
        print(json.dumps({"decision": "allow"}))
        return

    reason = match_protected(path)
    if reason is None:
        print(json.dumps({"decision": "allow"}))
        return

    print(json.dumps({
        "decision": "block",
        "reason": (
            f"Write would overwrite protected learning history ({reason}). "
            "To append, use Edit instead. If you truly mean to replace it, "
            "confirm with the user and remove/rename the file first."
        ),
    }))


if __name__ == "__main__":
    main()
