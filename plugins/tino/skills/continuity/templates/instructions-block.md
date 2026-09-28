<!-- Block to insert into the project's instructions (CLAUDE.md /
AGENTS.md / equivalent), TRANSLATED into the project's language and WITHOUT
this comment. Placeholders: <RITUAL> = how the closing ritual is invoked
(skill "save-progress" — "guardar-avance" in the Spanish set — or, without
it, «follow rituals/save-progress.md»); <VERSION> = this skill's
version (CHANGELOG.md); <VERIFIER> and <ROTATOR> = the FULL commands of the
installed scripts (e.g. `python3 scripts/lint_continuity.py` and `python3
scripts/rotate_logbook.py`; without Python: "by hand"). Minimal scale (PLAN
only): item 1 becomes «read PLAN.md» and item 3 is dropped. Document names,
the INVARIANTS heading and the HTML marker on the last line come from the
token set (Spanish set: BITACORA.md, ARQUITECTURA.md, INVARIANTES) and are
not translated further: the scripts and the installer read them. At most 20
lines counted from the heading to the marker, both included: they are paid
in every session. -->

## Session continuity (MANDATORY)

1. **BEFORE changing** code, structure, content or configuration:
   read `PLAN.md` ("where we left off") and `ARCHITECTURE.md` (map and
   **INVARIANTS**); past decisions are looked up in `LOGBOOK.md`. If the
   change contradicts an invariant or a decision, **STOP and alert the user**.
2. **WHEN CLOSING a milestone or session** (or if the user asks): the full
   closing ritual (<RITUAL>).
3. `LOGBOOK.md` is **append-only**: entries are never edited or deleted;
   reversals go in a new entry.
4. Multi-session plans are resumed from `PLAN.md`, not from your assumptions.
5. Budgets (`lint-budgets` line in `PLAN.md`): measure BEFORE writing
   with `<VERIFIER> --margin`; if it does not fit, rotate with `<ROTATOR>`
   or compact by archiving FIRST, never by deleting. With another session
   active: touch only your own files and stage file by file.
<!-- tino: continuity v<VERSION> -->
