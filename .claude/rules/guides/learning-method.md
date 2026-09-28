# Learning method

> Read when designing/walking a module. Defines *how* we learn — not *what*.
> The project mode (`breadth`) shifts the emphasis; the principles are shared.

## When to read

- `/plan` designs a module (tutor) — so the module is practice-first, not a lecture.
- `/go` runs the practice — so explanation is just-in-time, not a theory dump.
- The question "too much theory / stuck / boring" — check against the principles below.

## 1. Practice-first (the main one)

**EVERYTHING converts to practice.** This is the prime directive of the whole learning process. Theory, the mini-theory of §2, explanation, `/page`, Anki, recall — exist **only as a step toward action**, not as an end. Rules that make this ironclad:
- **Every piece of input → a hands-on step in the same session.** Explained a concept → immediately applied it to your task/built it/did it. No application → not covered.
- **What can't be turned into practice → not a module.** It goes to `docs/backlog.md` (depth) or `/anki` (if it's a recall atom). A module without a §3 applicable result isn't approved.
- **"Read/understood" is not a result.** The result is what you **did** and can show/repeat (an artifact, an action, a written breakdown — see module §3).

**A working result > complete understanding.** A module ends with a tangible artifact (module §3), not "read it". Understanding is gathered *around* practice, not before it.

- Build/do first and ask — then (if needed) read.
- **Productive failure (attempt before theory):** on a new topic the tutor first throws a challenge/question — the learner tries, errs, **then** theory lands on a felt problem. This beats "theory→practice". Don't hand over the solution before an honest attempt.
- No applicable result → this isn't a module, it's a note in `docs/backlog.md` (depth).
- The `/deploy` gate physically requires an artifact — protection against "studied and studied, nothing to show".

## 2. Learning through dialogue

Understanding is obtained by **talking with Claude**, not from a textbook.

- Each module has §8 "Break it down with me": the user asks "why this / what's it for / what is it" — the tutor explains **in plain terms**, not academically.
- Real-time help with snags: you throw an error/symptom — we work it out together (Hypothesis Journal at 3 failures).
- Explanation **on the fly**, tied to what's in your hands right now.

## 3. Just-in-time theory

Take exactly as much theory as the next step needs. No more.

- The theory in module §2 is deliberately compressed. It bloat → the extra goes to `docs/backlog.md`.
- Don't hand out a textbook where one fact is needed. "Drowning in theory" is Forbidden (CLAUDE.md §5).
- Dig into depth **later, by choice, without guilt** — that's what depth-backlog is for.

## 4. Verification ≠ self-assessment

"Got it?" is an unreliable signal (illusion of knowledge). Readiness is caught two ways:

- **§9 readiness criterion** — an observable sign (works / passes / I explain it without a hint).
- **`/exam`** — the examiner runs through what's been covered later (spaced retention), sceptically, without playing along. Gaps → a review module or a backlog note.

That's the role split: the tutor is on your side (helps), the examiner verifies (doesn't believe "yeah I got it").

**Проверка фактов ≠ уверенность модели.** «Помню так» — не источник. Источник факта = якорь с вердиктом чекера (`/fact-check`); уверенность модели источником не является. Сверка с якорями — на `/exam`; правила — [fact-checking.md](fact-checking.md).

**Verification/retention techniques (the examiner applies these in `/exam`):**
- **Spaced repetition.** A finished module is revisited on a growing interval: **+1d → +3d → +7d → +21d → +60d**. The `review-due` field in the module's meta; `/exam` raises what's due. Retained → the next interval; a gap → reset to +1d.
- **Teach-back (Feynman).** "Explain the topic from scratch, as if I don't know it." Where you stumble in the explanation is where the gap is (not where you "didn't recognize"). The strongest tool against the illusion of knowledge.
- **Confidence calibration.** Before verification — "how confident, 1–5?". Compare with the fact. "Confident, but couldn't" → a fat signal into the skill-map (self-deception costs more than an honest "I don't know").

## 5. Bridges — integration (especially in breadth)

Going wide across topics is good, but without links knowledge crumbles into **isolated islands**. So every module (except the first) is **linked to what's been covered** — a mandatory gate, not a wish.

- **Rests on (backward):** the module reuses the past — both the understanding and the **real artifact** of a previous module (not just "we recalled the theory", but physically took M{k}'s result and built it in).
- **Groundwork for the future (forward):** what this module gives the next ones.
- **Practical projects are always a bridge.** A prototype uses a previous module's artifact where possible. That's "seeing how topics combine".
- **External bridges (between projects):** if you're learning several subjects in parallel (separate course folders), a module links to another subject where possible. Free text in §Bridges, not enforced — but this is what turns separate courses into one picture of the world.
- **A capstone integrates** as much of what's been covered as possible — the final bridge; ideally it reaches into ≥1 other subject too.

This applies to **all** plans and modes. In the roadmap, bridges show as dependencies between modules; the tutor lays them in during design; the examiner checks the ability to **combine** topics, not just each in isolation.

## 6. Modes (`breadth`)

| Mode | Essence | Roadmap | Anti-boredom |
|-------|------|---------|------------|
| **breadth** | touch EVERYTHING fast, many small prototypes | a tour across areas, interleaved (each module a different area) | speed + variety |
| **depth** | mastery of one topic, building up | steps from base to hard | rising task difficulty |
| **mixed** | a wide tour + targeted deep dives | areas + marked "dig" branches | balance |

**breadth nuance:** modules go **interleaved** (not in blocks of one area) — so each is about something different. Depth is deliberately deferred to the backlog.
**depth nuance:** each module rests on the previous one; skipping a pre-module → `Blocked` or frame-check.

## 7. Tempo and WIP

- **One active module at a time.** The roadmap is a map, but we instantiate one at a time (minimum noise): the next after the current `/deploy`.
- Module size fits the rhythm (`—`): usually a module = several sessions = one prototype.
- Don't spawn modules in advance: defocus. A future idea → a roadmap checkmark or the backlog, not a new file.

## 8. Adapting the plan to difficulties

A plan isn't carved in stone. The system **accumulates what's stuck** and adjusts. Otherwise breadth blindly races on over a weak foundation.

- **Detects difficulty** — `examiner` (gaps at verification) and `/go` (practice snags: 3 consecutive failures / re-explaining the same thing). The signal → `docs/skill-map.md` (an aggregate of "where I'm weak now").
- **Adapts** — the `tutor` at `/plan` **reads the skill-map first** and adjusts: smaller steps · insert a pre-module / review module for what's sagging · more "break it down with me" on the weak spot · strengthen the bridge to a topic that won't hold · slow down. It records the correction (in the module + closes the "Open corrections" item in the skill-map).
- **The roadmap moves too:** an area is consistently stuck → the tutor proposes reordering/inserting a review rather than pushing through.
- Role split: the examiner **finds** the weakness (not on your side — honest), the tutor **fixes** the plan (on your side).

skill-map ≠ journal: the journal is a chronology of "what happened", the map is the current "where I'm weak". The map lives on; entries in it are updated/closed.

## 9. What the roles decide themselves (you only `/do`)

The user runs **one `/do`** and doesn't remember the skills. When and what to apply is decided by `tutor`/`examiner` on **concrete conditions** (not "when useful" — that's unreliable):

**tutor (during `/go`, `/plan`):**
- Explain in plain terms — along the practice (§8), always.
- **Productive-failure** — on a new topic, throw a challenge before theory.
- **`/page` (interactive)** — the concept is visual/spatial with ≥2 interacting parts, OR the learner failed to get it in words twice (dual coding).
- **`/anki` (deck)** — the topic has ≥~5 recall atoms (terms/formulas/pinouts).
- **Adapt the plan** — a weak spot in the skill-map (§8).

**examiner (triggered by `/do` when due):**
- *When* to verify is decided by `/do`: `review-due ≤ today` (spaced) OR a weak spot hasn't been probed in a while. Not the user.
- *How* — teach-back + confidence calibration, one at a time, without playing along.

`/do` runs the **whole cycle itself**: practice → when §6 is done and §9's criterion is met, it immediately carries through to `/deploy` (artifact + journal + Done, confirming the criterion with the learner). The user calls neither `/go` nor `/deploy`.

The commands `/page` `/anki` `/exam` `/plan` `/go` `/deploy` remain as a manual override, but normally **aren't needed** — `/do` + the roles initiate everything.

## 10. Method anti-patterns

| Anti-pattern | Why bad | Correct |
|--------------|-------------|-----------|
| A lecture instead of practice | we get stuck in theory, no result | practice-first, an artifact is mandatory |
| "Got it?" as done | illusion of knowledge | §9 criterion / `/exam` |
| The whole textbook at once | overload, boredom | just-in-time, depth to the backlog |
| 10 modules in advance | defocus | one active, the rest in the roadmap |
| The examiner hints | verification is nullified | fresh context, a sceptic |
| Island modules | breadth without links doesn't add up | §Bridges mandatory, the prototype uses the past |
| Pushing the plan while ignoring what's stuck | a weak foundation accrues debt | skill-map → the tutor adapts (§8) |

## 11. Усилители удержания (науки о памяти)

> Доказательные усилители кодирования. Применяет tutor в диалоге/сессиях; examiner — на проверках. Это метод, не опция: пункты 1 и 2 — жёсткие.

1. **«Сначала моя версия» (жёсткое, на ВСЕ вопросы, не только крючок).** Прежде чем tutor объясняет, ученик выдаёт свою гипотезу/прогноз — даже «не знаю, но думаю…». LLM обесценивает ответы; попытка до ответа — условие глубокого кодирования. Tutor спрашивает версию прежде отвечать (и на вопросы ученика: «как ты сам думаешь?»). На новой теме совпадает с productive failure (§1).
2. **Free recall после сессии (обязательный шаг).** После диалога и ДО сверки с материалами — ~10 минут выгрузки по памяти (вслух/на бумагу): «что осталось в голове». Только потом сверка, заполнение шпаргалки/заметок, правки. Инверсия «сначала вспомнил — потом сверил» вместо «записываю по горячему с опорой на диалог».
3. **Персональные аналогии.** Новое объясняется через домены ученика (профиль — roadmap: рынки/трейдинг, дроны/SDR/электроника, свои проекты) — аналогия в родную доменную сеть держится дольше универсальных примеров. Всегда с рамкой «аналогия кончается здесь» (за рамку следит checker — учительский слой).
4. **Генерация вопросов учеником.** После каждого модуля/эпохи ученик пишет 3 своих вопроса (не ответов) — метапоиск «что важно». Examiner включает их в прогоны; кривой вопрос = сигнал непонимания сути.
5. **Интерливинг в разминке.** Вопросы из разных прошлых тем вперемешку (эпохи + нити; модули разных треков), не «по вчерашнему». Ощущается хуже — работает лучше (desirable difficulty).
6. **Мета-правило системы:** время на обвязку/полировку системы ≤ 10% времени учёбы. Overengineering системы — анти-паттерн курса.

## 12. Разговорный слой (protégé effect)

> Рассказывание другому человеку — один из сильнейших способов кодирования. Слой лёгкий, добровольный, без принуждения собеседников.

**Разговорный набор (conversation kit)** — tutor/main прикладывает к контентному артефакту при `/deploy` (секция «Разговорный слой»):
- **2 хука-парадокса** — застольные, 60-секундная версия: факт-загадка, который естественно просят объяснить («почему земледелие сделало жизнь хуже — и победило?»).
- **1 вопрос к собеседнику** — «как думаешь, почему…?» (прогноз собеседника = тот же productive failure; его версия интересна сама по себе).
- **1 микро-объяснение на 60 секунд** — челлендж «расскажи сам»: версия для одного человека, без терминов.
- **Практические курсы (electro/radio):** «покажи-расскажи» — что из собранного показать и как объяснить (мост в курс общения: рассказ = практика).

Тон: любопытство, не лекция; не навязываться; реакция собеседника — данные («где не понял другой — там дыра у меня»).

**Петля:** после разговора — 1 строка в `docs/lecture-log.md` (фидбек-блок): «рассказал <тему> <кому> — что не получилось объяснить» → вывод для следующих лекций. Examiner может спрашивать на `/exam`: «объясни X так, как рассказывал <человеку>» — вариативность контекста.
