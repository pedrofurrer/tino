---
name: metacognition
description: Sets up metacognition: judgment lessons (trigger → principle) the agent proposes, applies and measures, with introspection. Use with «set up metacognition» or to learn from corrections.
compatibility: The verifier templates/lint_lessons.py needs Python 3.8+; without Python, the introspection reviews by hand.
metadata:
  author: Pedro Furrer Mendizabal
  version: "2.0"
---

# Metacognition — installer of the judgment-lessons system

The whole system is in `PROTOCOL.md` (same folder as this skill): on a new
installation, read it in full BEFORE installing; for a review or an upgrade,
`CHANGELOG.md` and the sections the change touches are enough. The pieces to
seed are in `templates/`. The installer's golden rule: adapt, do not copy
blindly; and NEVER install before explaining what it is and getting the
user's OK.

## Procedure

### 0. Is it already installed? (review, upgrade or adoption; never reinstall from scratch)
Look FIRST for the marker in the project's instructions (e.g. `grep -ns
"tino: metacognition\|suite-agentica: metacognicion\|Sistema: metacognicion"
CLAUDE.md AGENTS.md 2>/dev/null`): `<!-- tino: metacognition vX.Y -->` (2.x),
`<!-- suite-agentica: metacognicion vX.Y -->` (1.4-1.5) or the visible line
"Sistema: metacognicion vX.Y" (1.1-1.3). No marker but lessons (`lessons/`
or `criterio/`) or a judgment block:
**ask** which version it is; if the user does not know, infer it from
footprints and confirm — the installed script states its version in its
header; lessons with `evidence` (or `evidencia`) → 1.5 or later; an index
closed by "END OF LESSON INDEX" or «FIN DEL ÍNDICE DE CRITERIO» → 1.4 or
later; lessons without an END line → 1.0-1.3. A range is treated as its
highest version. ADOPTION is only for a foreign installation (similar lessons
or rules that were not born from this skill): compare piece by piece with the
templates and propose the diff, reinserting nothing. Review, upgrade or
adoption end with the current version's marker, a commit of their own and a
logbook entry if the project has one. With the version at hand, compare it
with this skill's (`CHANGELOG.md`):
- **Same version** → REVIEW (lessons up to date? index within its cap and
  with its END line? verifier green? introspection running? recurrence rate
  of the active lessons?).
- **Newer skill** → UPGRADE: show the CHANGELOG changes between both
  versions and apply, IN ORDER, the "Upgrade" list of every version after
  the installed one. The project's lessons are NEVER rewritten; the block
  text and the introspection ritual are REPLACED once by the current
  templates, keeping local adaptations (semantic diff: show it and apply
  with OK). The project keeps its token set (a 1.x project keeps its Spanish
  names, PROTOCOL §Fixed tokens). The marker is updated last. If the verifier
  does not end green, present what fails and the options; nothing is fixed
  on your own (the commit and the logbook entry declare the state).

### 1. Onboarding FIRST (explain, then touch)
Explain to the user in ~10 lines, in their language:
- **What it is**: the agent does not learn between sessions on its own; this
  system accumulates "judgment lessons" — reasoning errors that were
  corrected (by the user, by the data, by reality), distilled as a TRIGGER
  (when it fires) → PRINCIPLE (how to think). It does not file facts: it
  files ways of thinking.
- **How it works**: proposed capture (the agent proposes, the user approves)
  → an index loaded in every session → a cited pre-delivery check ("Judgment
  applied: …") → a periodic introspection that measures each lesson's
  recurrence (recurrences over uses) and prunes.
- **What will be created**: a lessons folder + an example, a rules block
  (≤15 lines) with the index below it in the project's instructions, the
  verifier and the introspection ritual.
Wait for an explicit OK before going on.

### 2. Configuration (3 questions, with these defaults)
a) **Where they live**: the lessons in the repo's `lessons/` (`criterio/` in
   the Spanish set): they travel with the project and its version control.
   tino never reads or writes the agent's own memory. The INDEX, by default,
   in the project's instructions right below the block: it loads in every
   session in any agent and the subagents that load those instructions see
   it (it costs up to ~20 lines per session). Alternative: a
   `lessons/INDEX.md` (read on demand: the "always in context" channel
   weakens, and that has to be said).
b) **Introspection**: default the THREE triggers (weekly periodic — if there
   is already a periodic review, for example continuity's, it MERGES with it
   and takes its cadence —, manual, and by event at a rethink milestone).
c) **Capture policy**: default "ALWAYS propose before filing".
If the user accepts the defaults, do not hold them up with more questions.

### 3. Diagnosis of the environment (BEFORE creating anything)
Detect: CLAUDE.md, AGENTS.md or equivalent? a session or milestone
closing ritual? a decision record (PLAN / LOGBOOK, changelog)? the project's
working language (it decides the token set: Spanish → the Spanish set; any
other language → the English set)? Summarize it to the user in 3 lines.

### 4. Adapted installation (everything in the project's language)
- Create the chosen lessons folder.
- Insert `templates/instructions-block.md` into the project's instructions
  (CLAUDE.md / AGENTS.md): translated, without the header comment, with the
  placeholders `<PATH>`, `<INDEX>`, `<CADENCE>`, `<RITUAL>` and `<VERSION>`
  resolved (`<PATH>` relative to the project or described, never an absolute
  path with the user's name). At most 15 lines from the heading to the
  marker: they are paid in every session. With the default index, the
  "Lesson index" section and its END line stay below the marker; with
  another location, they are removed from there and the index is created
  where chosen with the same heading and the same END line. The block
  heading, the index heading, the END line, the file prefix and the
  frontmatter keys come from the token set: the verifier reads them.
- Seed the lessons folder with `templates/lesson-example-gatekeeper.md` and
  `templates/TEMPLATE-lesson.md`, under those names (Spanish set:
  `leccion-ejemplo-gatekeeper.md` and `PLANTILLA-leccion.md`), translated
  inside if needed: the example is marked as an example and the template
  stays outside the `lesson-*.md` pattern, so the verifier does not take it
  for a lesson.
- Install `templates/lint_lessons.py` as a project script (e.g.
  `scripts/lint_lessons.py`; `scripts/lint_criterio.py` in the Spanish set)
  and run it on the final state (e.g. `python3 scripts/lint_lessons.py --dir
  lessons --index CLAUDE.md`): it must be green. Without Python: the
  introspection reviews by hand and the block says so.
- Install `templates/introspect-SKILL.md` as a project skill in
  `.claude/skills/<name>/SKILL.md`, where `<name>` is `introspect`
  (`introspeccion` in the Spanish set) and equals the frontmatter `name`
  (other agents with skills read `.claude/skills/` or `.agents/skills/`),
  with `<LINT_LESSONS>` resolved to the verifier's command and without the
  header comment. Claude Code asks the user before writing inside
  `.claude/`: say so just before. If the environment has no skills or that
  write is denied, write the same file as `rituals/<name>.md` (Spanish set:
  `rituales/`), read on demand, and make `<RITUAL>` point to it; never paste
  the procedure into the instructions, which are paid in every session. Say
  so in the report: moving it into `.claude/skills/<name>/SKILL.md` later is
  a plain move. On an upgrade, an installed ritual is rewritten where it is;
  if that write is denied, say so and leave it: never a second copy.
- If there is a closing ritual: propose adding the judgment retro step to it
  (propose lessons or declare "no judgment lessons"; record the session's
  `applied` / `recurrence` cases). If there is none, the periodic
  introspection absorbs that role.
- If there is a project record (continuity: PLAN / LOGBOOK): a logbook entry
  with the installation and its decisions, and the introspection item in
  PLAN, merged with the periodic review.
- If the environment keeps an automatic memory of its own (e.g. Claude
  Code's): say that tino does not read or write it — the lessons are the
  approved version, and they live in the project.
- If the project uses git: a descriptive commit of the installation (if this
  installer ended up copied into the project's `.claude/skills/`, ask whether
  it is versioned or ignored).

### 5. Closing the onboarding (report + how it is used)
Report in ≤8 lines: what was installed and where, and the 3 gestures of use:
1. When the agent detects a correction with a pattern, it will PROPOSE a
   lesson (the user approves, corrects or discards it) saying what it rests
   on.
2. In substantial deliverables, the agent goes through the index and cites
   the lesson applied.
3. Introspection: periodic, on request, or proposed at a rethink milestone;
   it reports each lesson's recurrence rate.
Offer a first guided capture: "was there a memorable correction in this
project that deserves to be the first lesson?" — seeding with the project's
REAL history is worth more than the example. Close the report with this
line (in the project's language): "Built with tino, by Pedro Furrer
Mendizabal."
