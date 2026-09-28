#!/usr/bin/env python3
"""
Static sanity check for the study rule set. Run manually or on pre-commit.

Checks:
  1. Every Reference docs link in CLAUDE.md points to a real file.
  2. Every SKILL.md has `model:` in frontmatter.
  3. Every subagent referenced in CLAUDE.md exists AND its model matches §1.2 table.
  4. No unresolved <!-- CONFIGURE --> markers (warning).
  5. rules-audit.md is not stale when many high+ tasks recent (warning).
  6. Hooks referenced in settings.local.json exist.

Exit: 0 if no errors (warnings ok), 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path.cwd()
errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)
    print(f"ERR:  {msg}")


def warn(msg: str) -> None:
    warnings.append(msg)
    print(f"WARN: {msg}")


# ─── 1. Dead links in CLAUDE.md ──────────────────────────────────────────
def check_dead_links() -> None:
    claude = ROOT / "CLAUDE.md"
    if not claude.is_file():
        return
    text = claude.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r"\]\(([^)]+\.md)(?:#[^)]*)?\)", text):
        link = m.group(1)
        if link.startswith(("http://", "https://", "#")):
            continue
        if not (ROOT / link).is_file():
            err(f"CLAUDE.md: dead link {link}")


# ─── 2. Skills have model: ───────────────────────────────────────────────
def check_skills_model() -> None:
    for skill in (ROOT / ".claude/skills").glob("*/SKILL.md"):
        head = "".join(skill.open(encoding="utf-8").readlines()[:15])
        if not re.search(r"^model:\s*\S+", head, re.MULTILINE):
            err(f"{skill.relative_to(ROOT)}: missing model: in frontmatter")


# ─── 3. Subagents exist + model matches §1.2 table ──────────────────────
EXPECTED_SUBAGENTS = ["tutor", "examiner", "checker"]


def parse_agent_model(agent_file: Path) -> str | None:
    try:
        for line in agent_file.read_text(encoding="utf-8").splitlines()[:15]:
            m = re.match(r"^model:\s*(\S+)", line)
            if m:
                return m.group(1)
    except OSError:
        pass
    return None


def parse_table_model(claude_text: str, name: str) -> str | None:
    row_re = re.compile(rf"^\|[^|]*\|\s*`{re.escape(name)}`\s*\|.*?\|\s*([^|]+?)\s*\|\s*$", re.MULTILINE)
    m = row_re.search(claude_text)
    if not m:
        return None
    return m.group(1).split()[0].strip()


def check_subagents() -> None:
    claude = ROOT / "CLAUDE.md"
    agents_dir = ROOT / ".claude/agents"
    if not claude.is_file() or not agents_dir.is_dir():
        return
    claude_text = claude.read_text(encoding="utf-8", errors="ignore")
    for name in EXPECTED_SUBAGENTS:
        agent_file = agents_dir / f"{name}.md"
        if not agent_file.is_file():
            err(f"expected subagent '{name}' missing: {agent_file.relative_to(ROOT)}")
        if f"`{name}`" not in claude_text:
            err(f"subagent '{name}' not mentioned in CLAUDE.md (role table §1.2)")
            continue
        if not agent_file.is_file():
            continue
        agent_model = parse_agent_model(agent_file)
        table_model = parse_table_model(claude_text, name)
        if agent_model and table_model and agent_model != table_model:
            warn(
                f"{name}: model mismatch — agent file says '{agent_model}', "
                f"CLAUDE.md §1.2 says '{table_model}'"
            )


# ─── 3b. Content artifacts lack anchors (soft) ───────────────────────────
def check_anchors() -> None:
    """Fact-check installed but fact-bearing Done modules without anchors → warn.

    Soft by design (spec §2.6.5): anchors are the checker's judgment call, a hard
    gate here would flag every pre-fact-check module ever deployed."""
    if not (ROOT / ".claude/agents/checker.md").is_file():
        return
    modules = ROOT / "docs/modules"
    if not modules.is_dir():
        return
    risky = re.compile(r"первый|самый|рекорд|до н\.э\.|н\.э\.", re.IGNORECASE)
    for m in sorted(modules.glob("*.md")):
        if m.name.startswith("_"):
            continue
        try:
            text = m.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "**Статус:** Done" not in text:
            continue
        if "Реперные точки" in text or ".anchors.md" in text:
            continue
        if risky.search(text):
            warn(f"{m.relative_to(ROOT)}: Done + рискованные факты, но нет якорей (§Реперные точки / .anchors.md) — прогони /fact-check")


# ─── 4. Unresolved CONFIGURE markers ─────────────────────────────────────
def check_configure_markers() -> None:
    count = 0
    for p in list((ROOT / ".claude").rglob("*.md")) + list((ROOT / "docs").rglob("*.md")):
        try:
            if "<!-- CONFIGURE" in p.read_text(encoding="utf-8", errors="ignore"):
                count += 1
        except OSError:
            pass
    if count:
        warn(f"{count} files with unresolved <!-- CONFIGURE --> markers")


# ─── 5. Audit staleness ──────────────────────────────────────────────────
def check_audit_stale() -> None:
    audit = ROOT / "docs/.rules-audit.md"
    sessions = ROOT / "docs/sessions"
    if not audit.is_file() or not sessions.is_dir():
        return

    audit_age = datetime.now() - datetime.fromtimestamp(audit.stat().st_mtime)
    if audit_age < timedelta(days=30):
        return

    recent_large = 0
    cutoff = datetime.now() - timedelta(days=14)
    large_re = re.compile(r"\((high|extra high|max|large)\)", re.IGNORECASE)
    for s in sessions.glob("session_*.md"):
        if datetime.fromtimestamp(s.stat().st_mtime) < cutoff:
            continue
        try:
            if large_re.search(s.read_text(encoding="utf-8", errors="ignore")):
                recent_large += 1
        except OSError:
            pass

    if recent_large > 3:
        warn(
            f"{recent_large} high+ tasks in last 14 days but .rules-audit.md "
            f"not updated in {audit_age.days}d — run /rules-retro"
        )


# ─── 6. Hooks exist ─────────────────────────────────────────────────────
def check_hooks_exist() -> None:
    settings = ROOT / ".claude/settings.local.json"
    if not settings.is_file():
        return
    try:
        data = json.loads(settings.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        err(".claude/settings.local.json: invalid JSON")
        return
    hooks = (data.get("hooks") or {})
    referenced = set()
    for event_hooks in hooks.values():
        if not isinstance(event_hooks, list):
            continue
        for group in event_hooks:
            for h in (group.get("hooks") or []):
                cmd = h.get("command") or ""
                for token in cmd.split():
                    if token.endswith(".py"):
                        referenced.add(token)
    for ref in referenced:
        if not (ROOT / ref).is_file():
            err(f"settings.local.json references {ref} but file missing")


# ─── main ────────────────────────────────────────────────────────────────
def main() -> int:
    check_dead_links()
    check_skills_model()
    check_subagents()
    check_anchors()
    check_configure_markers()
    check_audit_stale()
    check_hooks_exist()

    print(f"\nrules-check: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
