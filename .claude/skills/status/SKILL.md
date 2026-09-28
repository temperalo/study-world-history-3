---
name: status
description: Снимок состояния учёбы — активный модуль, прогресс по доске и roadmap
allowed-tools: Bash, Read, Grep, Glob
model: haiku
---

Read-only снимок. Ничего не пишет, не правит.

Собрать:
- **Активный модуль** — `docs/modules/*.md` со `**Статус:** In progress`: slug + прогресс шагов (отмеченные `[x]` из N в §6).
- **Done count** — сколько модулей `Done` (из `docs/plans/plans-done.md`).
- **Roadmap progress** — из `docs/roadmap.md`: модулей X/N · областей X/M.
- **Blocked** — модули со `**Статус:** Blocked`: slug + чего не хватает (причина из файла, обычно §4 материалы / пред-модуль).
- **Last /exam** — последняя дата `/exam` (из `docs/flow.md` или `docs/journal.md`).
- **Git** — `git branch --show-current && git status --short`.

Result: ветка | uncommitted | активный модуль + шаги | Done X | roadmap X/N модулей · X/M областей | Blocked (что нужно) | last exam.
