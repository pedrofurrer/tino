---
name: introspect
description: Consolidates the judgment lessons: measures recurrence, promotes, archives and prunes the index. Use with «run the introspection», in the periodic review or at a rethink milestone.
---

# Introspection — consolidating the agent's judgment

The judgment lessons live in the folder configured at installation
(`lessons/lesson-*.md`), indexed in the «Agent judgment» section (by default,
in the project's instructions, down to its END line). Format: frontmatter
(`validation: proposed | hypothesis | recurring | confirmed | graduated |
archived`, `scope`, `evidence: data | source | reality | user`) + a body
**Trigger / Original error / Principle / Application / Cases**, with cases
`- YYYY-MM-DD · origin|applied|recurrence — …`. The Trigger is written by
MECHANISM (act + input); the concrete forms illustrate, they do not limit;
a recurrence through a form not listed ⇒ reformulate by mechanism, do not
add the form to the list.

## Triggers (all three count)

1. **Periodic**: at the configured cadence (weekly recommended, merged with
   an existing review ritual).
2. **Manual**: the user invokes it whenever they want.
3. **By event**: in ANY session, if you detect a signal of a rethink
   milestone, propose running it right then (do not wait for the calendar):
   - an established premise of the project is refuted by reality;
   - an important result differs sharply from what was expected;
   - a hot recurrence of an error already filed;
   - ≥2 new lessons in a few days on the same axis.
   In autonomous sessions: record the recommendation and present it at the
   next contact.

## Procedure

1. **Read, incrementally**: `python3 scripts/lint_lessons.py --dir lessons --index CLAUDE.md --summary` lists every lesson
   with validation, scope, evidence, cases, applied cases, recurrence rate
   and last change; open in full only those that changed since the previous
   run or those a recurrence points to (reading them all does not scale: in
   the reference deployment there were 65 cards and ~340 KB). Add the
   project's recent record (logbook, changelog or equivalent). The
   introspection does not read past conversations or the agent's own memory.
2. **Recurrence** (the most valuable signal): did an error already filed
   repeat? → the trigger (badly formulated) or the application channel
   failed → REFORMULATE the lesson, do not just note the case. And ask first
   "what MOMENT do the recurrences share?": if they share the act, the input
   and the point of the work, the remedy is an instrument (verifier, hook,
   required field, ritual step with the command written out), recorded as
   `carried_to` in the card — not another line of text.
3. **Drafts**: lessons in `validation: proposed` (captured in autonomous
   work) are presented to the user for OK, correction or discarding. With
   OK, the card becomes `hypothesis` and ENTERS the index: its bullet
   (`- lesson-<slug> — <trigger → principle>`) and the END count.
4. **Cross-cutting patterns**: do several lessons point to a deeper bias? →
   propose consolidating them into a parent lesson (the children are
   archived with a link; nothing is deleted and their history is not
   rewritten).
5. **Promotion / demotion**: hypothesis → recurring (2+ cases) → confirmed
   (at least one `applied` case with an observable success). A lesson with
   `evidence: user` (only the user's word) does not go beyond recurring
   until data, a primary source or an observed outcome corroborates it. No
   recurrence or use in ~30 days → archive. Confirmed lessons with a
   frequent trigger → propose to the user their graduation to a permanent
   rule (`graduated`), with a DESTINATION that follows the card's `scope`:
   `<project>` → the project's instructions, guides or invariants (if there
   is a brain, lessons about reading sources or validating claims go to its
   SCHEMA); `cross-project` → the user's GLOBAL instructions, if their
   environment has them — rewritten without references to the project
   (neither its domain nor its tools), because those instructions load in
   every session of every project and only take generic rules; the card
   keeps the history. It is `cross-project` only if trigger and principle
   speak about the METHOD and would apply unchanged in another project.
   Never write into the global instructions outside this step or without
   OK.
6. **Additions and pruning of the index**: every active lesson has its
   bullet; the section stays within the current cap (≤20 bullets by
   default; recalibrated with measured use and the user's OK, recording why
   — the reference deployment raised it to 40 after measuring ~21 different
   lessons cited in 9 days). Archived lessons leave the index, not the disk.
   Graduated ones are compressed to a mention: they live in the
   instructions and no longer depend on the index. Mechanical hygiene: the
   section closes with «END OF LESSON INDEX — N entries» — `python3 scripts/lint_lessons.py --dir lessons --index CLAUDE.md`
   green when closing.
7. **Mini-report to the user** (3-5 lines): new or consolidated lessons,
   recurrences detected with their rate (recurrences / uses), promotions and
   graduations proposed. Record the run wherever the project records
   maintenance.

## Governance (hard)

- Every new lesson or substantial reformulation is PROPOSED to the user
  before filing (trigger + principle + what it rests on, 2-3 lines); without
  their OK it stays `proposed`. Adding a dated case to a card is a record,
  not a reformulation.
- Graduations to shared documents ALWAYS require their OK.
- Lessons never veto the user's decisions: they describe the agent's
  judgment, they do not take away the user's risk / benefit decisions.
