---
name: undo
description: Откатить последнее изменение/коммит безопасно (git)
allowed-tools: Bash
model: haiku
---

1. Show `git diff --stat` + `git log --oneline -3`.
2. Pick: uncommitted → `git stash`. Unpushed commit → `git reset --soft HEAD~1`. Pushed → `git revert HEAD`.
3. **Ask confirmation** before undo.

## Protected paths

`docs/journal.md`, `artifacts/**` — это история обучения, восстановить нельзя. Если откат затрагивает их (в diff/коммите) — **явно назвать** и спросить отдельно, не откатывать молча.
