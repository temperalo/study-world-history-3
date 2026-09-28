# Session log

**When:** после практики (`Практика` — каждая задача в `/go`) и после `/deploy` модуля; экзамен (`Проверь меня`) тоже логируем. Разовый `Вопрос` / `Объясни` без артефакта — don't log.
**File:** `docs/sessions/session_YYMMDD.md` — one per day. Append. **YYMMDD** (не DDMMYY) — чтобы файлы сортировались хронологически.

**Format:**

    ### HH:MM–HH:MM (scale) — Label: short request
    **Что собрал:** артефакт в `artifacts/` (файл/демо/ссылка) или «—»
    **Что понял:** ключевой инсайт ≤300 chars
    **Что не вышло / грабли:** затыки, Hypothesis Journal — кратко, или «—»
    **Agents used:** tutor, examiner (comma-separated; — if main only)
    **Failed attempts:** (if changed approach — briefly why)
    **Result:** ✅ / ❌ / ⏳
    **Commit:** `hash msg` / —
    **Модуль:** M{n} статус (In progress / Done) + journal-запись (да/нет)

Scale: `small` | `medium` | `large`

**Observability — `Agents used`:**
- Обязательное поле, если была делегация через Task (tutor или examiner).
- «—» означает что main-agent делал всё сам (low effort или fallback).
- `/rules-retro` использует это поле для статистики: какие роли реально срабатывают (tutor vs examiner), какие комбо повторяются.

**Cross-session:** read today's log to know what's done.
