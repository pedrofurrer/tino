# CHANGELOG — metacognition

Author: Pedro Furrer Mendizabal. Each version lists ONLY the changes that
affect a project that has the system installed, and ends with its
**Upgrade** list: what the installer applies, in order, when it brings a
project from an earlier version (step 0). The block text and the
introspection ritual are replaced once, by the current version's. The
project's lessons are NEVER rewritten.

## v2.0 — 2026-09-28
- Published in English as part of the tino plugin (Claude Code and Cowork)
  and as a standalone Agent Skill. English is now the source language; the
  artifacts are still written in the project's language.
- Two token sets (PROTOCOL §Fixed tokens): English (`lessons/`,
  `lesson-*.md`, `validation: confirmed`, **Trigger** … **Cases**, `END OF
  LESSON INDEX — N entries`), and the Spanish set of 1.x, which the
  installer also writes for Spanish-language projects. The verifier accepts
  both, in any mix, and its summary shows each value as written.
- Verifier in the English set: `lint_lessons.py`, with English messages; the
  1.x flags keep working as aliases (`--indice`, `--tope`, `--resumen`,
  `--posicion-max`, `--lineas-max`); by default it takes `lessons/` (or
  `criterio/`) and its `INDEX.md` (or `INDICE.md`).
- Fix: the cases are counted from the same **Cases** label that marks the
  section (before, a longer label such as «**Casos de X**:» passed the
  section check but gave «0 dated cases»).
- Seeded files renamed in the English set: `TEMPLATE-lesson.md` (outside the
  `lesson-*.md` pattern) and `lesson-example-gatekeeper.md`.
- The lessons and their index live only in the project. tino no longer
  reads or writes the agent's own memory: the 1.x options of keeping them in
  the agent's memory (or the index in its `MEMORY.md`) and the
  introspection's review of the automatic memory as an inbox are gone, and
  the introspection works from the project's own record, never from past
  conversations.
- The verifier's load limits (`--position-max`, `--lines-max`,
  `--bytes-max`) are explicit options, each one applied on its own; there
  are no longer automatic limits for a file named `MEMORY.md`.
- Ritual fallback: where the environment has no skills or the write into
  `.claude/` is denied (Claude Code asks before writing there), the
  introspection goes to `rituals/introspect.md` (Spanish set: `rituales/`),
  read on demand and pointed to by the block, instead of a section of the
  instructions, which is paid in every session.
- **Upgrade** (from any 1.x version): (a) keep the project's token set — a 1.x
  project keeps its Spanish names (folder, prefix, keys, values, headings, END
  line, ritual and script file names); nothing is renamed and no lesson is
  rewritten; (b) replace the CONTENT of the installed verifier with
  `templates/lint_lessons.py`, keeping its file name; (c) if the lessons or
  the index still live in the agent's memory, outside the project: tino 2.0
  does not read them there — ask the user to copy that folder into the project
  (as `criterio/`) and continue from the copy, with the index moved to the
  project's instructions; (d) replace the block text with the current
  template, in the project's language (semantic diff, with OK), with the
  location already decided; (e) replace the introspection ritual (semantic
  diff, with OK), keeping its installed name; (f) if there is a closing
  ritual, its judgment retro adds the bullet to the index and the typed cases,
  and its budgets step runs this verifier; (g) run the verifier: lessons
  without `evidence` show up in a single warning and gain it when the
  introspection touches them — nothing is rewritten in bulk; (h) an
  introspection that 1.x left as a section of the instructions: propose moving
  it (with OK) to `.claude/skills/`, or to `rituals/` if that write is denied;
  (i) marker `<!-- tino: metacognition v2.0 -->`.

## 1.x history (Spanish-only releases)
- **v1.5 — 2026-09-26**: the index moves by default to the project's
  instructions (it loads in every session in any agent and subagents see
  it); typed cases (origin, applied, recurrence) and the recurrence rate per
  lesson; an `evidence` field (a lesson resting only on the user's word does
  not go beyond recurring until corroborated); `confirmed` requires an
  applied case; the automatic memory is reviewed as an inbox; a 12-line
  block; the verifier ends the index at its END line and handles quoted
  values, multi-line descriptions and invisible characters.
- **v1.4 — 2026-09-26**: the fourth application channel, the
  **instrument** (a recurring lesson whose recurrences share a moment is
  enforced by a mechanical control, recorded as `heredero`); index first in
  the loaded file, closed by its END line; the verifier `lint_criterio.py`
  with `--resumen`; HTML version marker.
- **v1.3 — 2026-09-02**: the Trigger is written by MECHANISM (act + input);
  the index cap can be recalibrated with measured use; graduation with a
  DESTINATION by scope (project rules, or the user's global instructions
  rewritten generically).
- **v1.2 — 2026-07-18**: the author's credit added; no functional changes.
- **v1.1 — 2026-07-18**: the installed version is recorded in the project;
  upgrade mode in step 0.
- **v1.0 — 2026-07-17**: foundation — installer with onboarding and 3
  configuration questions, provider-agnostic protocol (judgment lessons +
  introspection), templates.
