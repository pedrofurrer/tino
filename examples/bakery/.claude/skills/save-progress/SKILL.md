---
name: save-progress
description: Closing ritual that saves the progress (PLAN, LOGBOOK, ARCHITECTURE, commit) within the budgets. Use with «save progress», when closing the session or, proactively, after a milestone.
---

# Save progress — persistence ritual

Run ALL the steps, in order. The goal: a future session can resume exactly
from here without losing context or overwriting anything.

## 0. Measure before writing
- `python3 scripts/lint_continuity.py --margin`: how much fits in each capped document. If what you
  are about to write does not fit: rotate (`python3 scripts/rotate_logbook.py`, dry run first; check
  where each live part went) or compact by archiving BEFORE writing.
- Is another session or subagent working on the project? Then touch only
  your own things, re-read and write in the same step, do not rotate or
  compact what is someone else's, and stage file by file when committing.

## 1. PLAN.md
- Update the states (✅/🔄/⏳/💡) of what was worked on in the session.
- Tasks 🔄 half done: "where we left off: <exact point>" + a concrete next
  step. Add new tasks or ideas agreed with the user.
- Correct what the session made stale (a task already done, a source
  already read).
- Refresh the last-updated date.

## 2. LOGBOOK.md (append-only — NEVER delete or edit entries)
- One entry per decision or finding, headed `## YYYY-MM-DD — <topic>` (the
  rotator goes by that date): WHAT was done or decided + WHY + what NOT to do
  (if it applies).
- Include the user's reasons (stated preferences, options they rejected).
- Every figure, date and quotation comes from its source (the data, the
  file, the user's own words), not from memory; what only the user said is
  written as their word.

## 3. ARCHITECTURE.md (if the structure changed or a statement went stale)
- New or modified pieces and automations → update.
- New critical rules → INVARIANTS section.
- New rules → the PROJECT's instructions (or INVARIANTS). Never the user's
  global or personal instructions, if their environment has them: those are
  paid in every session of every project and only take generic rules; a
  rule gets there only through graduation (introspection ritual, with OK).
- Fragilities found → technical debt.

## 4. Judgment retro (only if metacognition is installed)
- Were there user corrections that reveal a pattern, refuted predictions,
  better strategies, inefficiencies? → PROPOSE the lesson (trigger +
  principle + what it rests on) or declare "no judgment lessons". With the
  user's OK: the card (`hypothesis`), its bullet in the lesson index and the
  count of its END line; without OK, `proposed`.
- If a lesson was applied or recurred in the session, add the case to its
  card (`- YYYY-MM-DD · applied — …` or `· recurrence — …`): it is a record,
  not a reformulation.

## 5. Budgets and compaction (check ALWAYS)
- Run `python3 scripts/lint_continuity.py`: OK / ALARM / EXCESS against PLAN's budgets (lines AND
  bytes). EXCESS → COMPACT by archiving (the rotator for the logbook; closed
  PLAN sections down to 1-3 lines + a pointer), never by deleting. Leave a
  note of what was archived. A document that closes at the edge of its cap
  session after session → propose to the user a split or a recalibration.
- If metacognition is installed and there were new lessons or added cases:
  its lessons verifier (`lint_lessons.py`) green.
- If the brain (critical wiki) is installed and there were operations on the
  wiki: its verifier green, its LOG up to date, and large operations (a
  batch ingest, a schema change) also in the LOGBOOK.

## 6. Version control
- Stage FILE BY FILE, never "everything modified": first the tree's state
  (`git status --short`); whatever changed that you did NOT touch in this
  session belongs to another session or a subagent — it is not added or
  committed; then `git add <file> …` with only your own and another
  `git status --short` to see that exactly that is staged.
- Check what goes in BEFORE committing: no secrets, heavy data or generated
  files (if they show up, exclude them, do not force them).
- A descriptive commit in the project's language: what + why (never "misc
  changes"). No push to remotes unless the user asks.

## 7. Confirmation to the user
- Summarize in 3-5 lines what was recorded and where, and whether anything
  is left 🔄 with its "where we left off". If something done in the session
  CONTRADICTS an invariant of ARCHITECTURE.md, say so explicitly now.
