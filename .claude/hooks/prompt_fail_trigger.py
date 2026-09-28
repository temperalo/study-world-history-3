#!/usr/bin/env python3
"""
UserPromptSubmit hook — deterministic `fail:` trigger.

A user message starting with `fail:` MUST produce an append to docs/claude-fails.md.
The rule lives in CLAUDE.md / workflow.md, but rules held "in the head" degrade after
compaction in long sessions — this hook re-injects the instruction at the exact moment
it applies. Shared across templates (single source at 999.claude/shared/hooks/).

Stdin-only (no file access) — chdir-to-root rule does not apply.
"""

from __future__ import annotations

import json
import re
import sys

INSTRUCTION = (
    "HARD TRIGGER `fail:` — сообщение начинается с `fail:`. Обязан append запись в "
    "docs/claude-fails.md БЕЗ уточняющих вопросов: `## YYYY-MM-DD — короткое название`, "
    "суть промаха 1-3 предложения, `**Должен был:**`, `**Контекст:**`. Если фраза "
    "короткая — восстановить детали из последнего шага сессии. Затем подтвердить: "
    "«записано в claude-fails.md»."
)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)
    prompt = data.get("prompt") or ""
    if re.match(r"^fail:\s*", prompt):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": INSTRUCTION,
            }
        }))
    sys.exit(0)


if __name__ == "__main__":
    main()
