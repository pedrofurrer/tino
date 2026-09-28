# PROTOCOL — The agent's metacognition (judgment lessons)

> v2.0 (2026-09-28). Portable core: any LLM agent working with a user can
> apply it, in projects of any kind (code, analysis, writing, running a
> business). Adapting it to a given environment is covered in "Anchoring by
> environment", at the end. Language: the artifacts this protocol creates in
> a project are written in THAT project's language.
> Created by Pedro Furrer Mendizabal.

## What it is and why it works

An LLM agent does not learn between sessions: its weights do not change with
use and every session starts the same. What CAN improve cumulatively is the
context it starts with and the rituals that make it consult that context.
This protocol turns "learning from experience" into context engineering:
**capture** the moments when the agent's judgment was corrected (by the
user, by the data, by reality), **distill** the underlying way of thinking —
not the one-off fact —, **keep it in view** at the moment of acting,
**apply it** verifiably and **measure** whether it recurs. The fragile link
is retrieval at the right moment; that is where the design invests, not in
accumulating text.

## The unit: a judgment lesson

One file per lesson (`lesson-<slug>.md`), in this format:

```markdown
---
name: lesson-<slug>
description: "<trigger → principle compressed into one line>"   # goes to the index
metadata:
  type: lesson
  validation: proposed   # proposed | hypothesis | recurring | confirmed | graduated | archived
  scope: <project>       # <project> | cross-project
  evidence: user         # what the correction rests on: data | source | reality | user
  carried_to: ~          # optional: the instrument that enforces it (channel 4)
---
**Trigger**: a concrete situation recognizable BEFORE acting, written by
MECHANISM (the act + the input that sets it off); concrete forms illustrate,
they do not limit — a recurrence through a form not listed ⇒ reformulate, do not list.
**Original error**: what was done or proposed and why it was wrong (date + case).
**Principle**: the distilled rule, as an actionable imperative.
**Application**: what applying it well looks like (the contrast with the error).
**Cases**: `- YYYY-MM-DD · origin|applied|recurrence — …`; added over time (append).
```

**Graded validation**: `proposed` (a draft without the user's OK; it does
not enter the index) → `hypothesis` (1 case, with OK) → `recurring` (2+
cases) → `confirmed` (at least one `applied` case with an observable
success) → `graduated` (promoted to a permanent rule: it lives in the
instructions; the card keeps the history). `archived` leaves the index, not
the disk. A hypothesis is considered; it does not govern.

**Evidence** (what the correction rests on): `data` (a measurement or a
record), `source` (a primary source that was opened), `reality` (the
observed outcome that refuted the prediction) or `user` (only their word). A
correction can be wrong, and filing it makes it persistent: a
lesson with `evidence: user` does not go beyond `recurring` until data, a
source or an observed outcome corroborates it. It is not distrusting the
user: it is not turning into a rule what nobody verified.

**Threshold rule**: file the PATTERN, not the fact. If you cannot formulate
a trigger recognizable in advance (when exactly should this fire next
time?), it is not a lesson: it goes to the project's normal record.
Deliberately low volume: a few good lessons > many generic ones.

## Capture (3 moments)

Signals: the user corrects an analysis or strategy and the correction
reveals a pattern; reality or the data refute a prediction of the agent;
the user brings a better strategy; the agent notices a better way too late
(inefficiency). Moments:

1. **In session**: when the signal appears, the agent PROPOSES the distilled
   lesson (trigger + principle + what it rests on, 2-3 lines) and writes it
   only with the user's OK, incorporating their corrections: the card and
   its line in the index, with the END count (a lesson outside the index is
   not "in view"; the verifier warns about it).
2. **When closing** (if the project has a closing ritual): a retro step —
   were there corrections, failed predictions, better strategies,
   inefficiencies? → propose lesson(s) or declare "no lessons".
3. **Autonomous work**: save as `validation: proposed` and present it for OK
   at the next contact. Nothing is filed for good without OK.

**The environment's own memory** (e.g. Claude Code's automatic memory):
tino does not read or write it. Lessons are captured in the session, with
the user's OK, and live in the project, where the user can review them.

## Application (4 channels — this is where it is won or lost)

1. **Index always in context**: one line per lesson (trigger → principle) in
   a text the agent loads BY ITSELF in every session. By default, a section
   below the rules block, in the project's instructions: any agent loads it,
   the subagents that load those instructions see it, and it travels with
   the repo. Alternative, at the user's choice: a `lessons/INDEX.md` — which
   is no longer "always in context" but read on
   demand: the channel weakens, and it is worth knowing. Budget: ≤20 lines by
   default, recalibrated with measured use (if the index is cited daily with
   many live lessons, the cap rises with the user's OK and the reason is
   recorded); the introspection prunes. Mechanical hygiene: the section
   closes with an END line with the count (without the END line seen, the
   index has not been read); the verifier `lint_lessons.py` measures it.
2. **Cited pre-delivery check**: before delivering a SUBSTANTIAL deliverable
   (report, strategy, plan, text for third parties), go through the index;
   if a lesson applies, apply it and cite it in one line at the end
   ("Judgment applied: <lesson>"). The citation makes use verifiable. It
   does not apply to quick answers (it would be noise).
3. **Graduation to a hard rule**: a `confirmed` lesson with a frequent
   trigger is proposed to the user for promotion to the permanent rules.
   The DESTINATION follows the card's `scope`: `<project>` → that project's
   instructions, guides or invariants; `cross-project` → the user's GLOBAL
   instructions, if their environment has them (they load in every session
   of every project, so they only take generic formulations): the rule is
   rewritten without references to the project of origin — neither its
   domain nor its tools — and the card remains the only carrier of the
   history and the cases. A lesson is `cross-project` only if trigger and
   principle speak about the METHOD (how things are verified, measured,
   decided) and would apply unchanged in another project; if it needs the
   domain to be understood, it is `<project>`. The best lessons stop
   depending on memory: they become system — each one in its proper layer.
4. **Instrument (the mechanical channel)**: a `recurring` or `confirmed`
   lesson whose recurrences share a MOMENT (the same act, with the same
   input, at the same point of the work) does not need more text: it needs a
   control that fires at that moment without depending on the agent's
   memory — a verifier run before the step, a hook that stops the command, a
   required field in the template, a ritual step with the command written
   out. The card records its `carried_to` and the introspection asks, at
   every recurrence, "what moment do the cases share?" before reformulating
   the trigger. Measured in the reference deployment: three recurrences in
   48 hours sharing one moment (the start of an assignment) did not fail
   because of the wording but because of the channel, and were solved with a
   pre-flight script, not with another line of text.

## Introspection (the consolidation ritual)

**Triggers**: (a) periodic — weekly recommended, ideally merged with an
existing review ritual; (b) manual — whenever the user asks; (c) **by
event** — the agent proposes it at once at a "rethink milestone": an
established premise is refuted by reality; an important result differs
sharply from what was expected; a hot recurrence of an error already filed;
≥2 new lessons in a few days on the same axis. The aim of the event trigger:
learn while the experience is fresh and do not let a broken assumption keep
governing decisions until the next periodic run.

**Procedure**: 1) read — incrementally: the verifier
(`lint_lessons.py --summary`) lists every lesson with validation, scope,
evidence, cases, applied cases, recurrence rate (recurrences over uses) and
last change, and only the lessons that changed since the previous run, or
that a recurrence points to, are opened in full — plus the project's recent
record; 2) **recurrence**
(the most valuable signal): if a filed error repeated, the trigger or the
application channel failed → REFORMULATE the lesson, and if the recurrences
share a MOMENT → an instrument (channel 4), not just text; 3) present
pending `proposed` drafts; 4) cross-cutting patterns: several lessons
pointing to a deeper bias → propose consolidating them into a parent lesson
(the children are archived with a link, not deleted, and their history is
not rewritten); 5) promotion / demotion by cases and evidence; no
recurrence or use in ~30 days → archive; 6) prune the index (current cap;
≤20 by default) and its mechanical hygiene (END line with the count:
verifier green);
7) a mini-report to the user (3-5 lines, with the recurrence rate of the
lessons that had one) and a record of the run wherever the project records
maintenance.

## Governance (hard)

- Every new lesson or substantial reformulation is PROPOSED before filing;
  without the user's OK it stays `proposed`.
- Graduations to shared documents ALWAYS require their OK.
- Lessons describe the agent's judgment; they never veto the user's
  decisions or take away risk / benefit decisions, which are theirs alone.

## Anti-theater defenses (why this does not degenerate)

The main risk is not technical: it is producing cards that sound deep and do
not change behavior, raising N=1 to law and applying it where it does not
belong, or turning into a rule a correction nobody verified. Six built-in
defenses: a mandatory trigger in advance (no trigger, no lesson); declared
evidence (a lesson resting on a single word does not reach confirmed);
citation in use (evidence of application, not declamation); recurrence
measured over uses in every introspection; graded validation (a hypothesis
does not govern); low volume and pruning (the index has a budget).

## Fixed tokens

The verifier reads a few names and markers, so they stay fixed in every
language. There are two sets; the verifier accepts both, in any mix. The
installer writes the Spanish set for a Spanish-language project and the
English set for any other language; a 1.x project keeps the set it has.

| Item | English set | Spanish set (1.x) |
|---|---|---|
| Lessons folder and files | `lessons/` · `lesson-<slug>.md` | `criterio/` · `leccion-<slug>.md` |
| Seeded files | `TEMPLATE-lesson.md` · `lesson-example-gatekeeper.md` | `PLANTILLA-leccion.md` · `leccion-ejemplo-gatekeeper.md` |
| `metadata.type` | `lesson` | `leccion` |
| Validation key and values | `validation`: `proposed` · `hypothesis` · `recurring` · `confirmed` · `graduated` · `archived` · `example` | `validacion`: `propuesta` · `hipotesis` · `recurrente` · `confirmada` · `graduada` · `archivada` · `ejemplo` |
| Scope key and cross-project value | `scope` · `cross-project` | `ambito` · `transversal` |
| Evidence key and values | `evidence`: `data` · `source` · `reality` · `user` | `evidencia`: `dato` · `fuente` · `realidad` · `usuario` |
| Instrument key | `carried_to` | `heredero` |
| Sections | **Trigger** · **Original error** · **Principle** · **Application** · **Cases** | **Gatillo** · **Error original** · **Principio** · **Aplicación** · **Casos** |
| Case types | `origin` · `applied` · `recurrence` | `origen` · `aplicada` · `reincidencia` |
| Block and index headings | `Agent judgment` · `Lesson index` | `Criterio del agente` · `Índice de lecciones` |
| Index closing line | `END OF LESSON INDEX — N entries` | `FIN DEL ÍNDICE DE CRITERIO — N entradas` |
| Ritual and script | `introspect` · `lint_lessons.py` | `introspeccion` · `lint_criterio.py` |

Shared by both sets: the version marker `<!-- tino: metacognition vX.Y -->`
and the index bullet `- <file stem> — <trigger → principle>`.

## Integration with the other components (detect, do not couple)

- **Continuity** installed → the closing ritual includes the judgment retro
  and the introspection merges with the periodic review; runs are recorded
  where the project records maintenance (PLAN).
- **Brain** (critical wiki) installed → its lint suggests signals for the
  introspection (the agent's error patterns when filing); lessons about how
  to read sources or validate claims are natural candidates to graduate into
  the wiki's conventions (its SCHEMA), with OK.
Without either of them, this protocol works fully on its own.

## Anchoring by environment (the 3 primitives)

The system only needs three primitives; here is the map by environment:

| Primitive | Claude Code / Cowork (tino plugin) | Agents with Agent Skills (Codex, Cursor, GitHub Copilot, Gemini CLI…) | Agent without skills |
|---|---|---|---|
| 1. Persistent place for lessons | `lessons/` in the repo | `lessons/` in the repo | `lessons/` in the repo |
| 2. Instructions loaded in every session | block + index in the project's CLAUDE.md | block + index in AGENTS.md (or the file that agent loads) | block + index in its system instructions |
| 3. Periodic ritual | project skill `introspect` in `.claude/skills/` (if that write is denied: as in the last column) (+ the retro in the closing ritual if there is one) | the same skill: several read `.claude/skills/` or `.agents/skills/` (check their documentation) | `rituals/introspect.md`, read on demand: the block points to it and the user asks for it |
| (aid) Lessons and index verifier | the project's `lint_lessons.py` (Python 3) | same | same; without Python, review by hand |

The introspection works from the project's own record (its lessons, its
logbook or changelog); it does not read past conversations or the agent's
memory. Nothing in this protocol depends on a provider.
