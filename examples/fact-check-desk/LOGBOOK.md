# LOGBOOK — append-only

Entries are never edited or deleted; reversals go in a new entry.
Format: `## YYYY-MM-DD — <topic>`: what + why + what not to do.

## 2026-09-08 — Desk set up for the mayoral race
The Courier's fact-check desk was set up to cover the 2026 mayoral race
(election 2026-11-03, per README). Source: the editor's word.

## 2026-09-10 — Debate 1 and the claims log
Debate 1 took place; the claims log (`claims/claims-log.csv`) was started
that night. Source: the editor's word.

## 2026-09-12 — C05 logged (campaign mailer)
Source: `claims/claims-log.csv`.

## 2026-09-14 — C06 logged (social post)
Source: `claims/claims-log.csv`.

## 2026-09-15 — data/ downloaded from the city portal
The 7 CSVs in `data/` were exported from the city's open-data portal
(source: the editor's word and `data/README.md`). Caveats recorded there:
bus ridership and potholes 2026 cover January–August only; digital pothole
records start in 2019.

## 2026-09-28 — Goal and workflow decisions (editor)
- Goal: every debate-1 claim verdicted and published before debate 2 on
  2026-10-08.
- Verdict drafts live in `drafts/`, one file per claim, named by claim id
  (e.g. `drafts/C05.md`).
- The `status` column of the claims log goes unchecked → drafted →
  in review → published.
Why: the editor's decisions, taken before this system was installed.
Open: C05 and C06 are in the log but not from debate 1; whether they are in
the goal is left to the editor (PLAN, user's pending items).

## 2026-09-28 — Continuity system installed (tino continuity v2.0)
Standard scale (4 layers), English token set, at the editor's request.
Adaptations: ARCHITECTURE is a desk map + workflow + data dictionary, with
the style guide's rules and the editor's workflow decisions as INVARIANTS;
no technical-debt section (not a software project). Rules block in a new
`CLAUDE.md`; ritual as project skill `save-progress`; scripts in `scripts/`.
Budgets at defaults. No remotes. Not done: no claims were checked or drafted
during the installation.

## 2026-09-28 — Metacognition installed (tino metacognition v2.0)
English token set, editor's OK with the defaults: lessons in `lessons/`
(in the repo), index in `CLAUDE.md` below the block, the three introspection
triggers (weekly — merged with PLAN's methodology review —, manual, and by
event at a rethink milestone), and every lesson proposed before filing.
Seeded with the format example and the template only: 0 real lessons.
The judgment retro was already step 4 of `save-progress`; its verifier
command is now written out. tino does not read or write Claude Code's own
memory: lessons live only in the project.

## 2026-09-28 — Brain founded (tino brain v2.0)
Critical wiki in `knowledge/`, with the editor's OK and parameters: domain =
Port Alder's public record for fact-checking the campaign; subdomains
transit, budget-and-taxes, schools, public-works, libraries; validation
source = open data in `data/`; fast field (older than 12 months → possibly
stale; projections stay projections); context = two-person desk + editor,
one verdict per claim, same rigor for every candidate. No landscape layer.
My call, open to correction: water bills go in budget-and-taxes, the water
infrastructure in public-works. `reading/` NOT processed (editor's
instruction): its 6 files wait in `knowledge/PENDING.md`. Do not ingest them without the editor's OK (and a triage map if they go in
as a batch).

## 2026-09-28 — Near miss on C01: partial year compared with full years
Editor's note, for the record: the week before, a reporter's C01 draft
compared 2026 bus ridership (8 months, `months_covered` = 8) with full years,
and it nearly ran. Filed, with the editor's OK, as the first
judgment lesson: `lessons/lesson-partial-period-comparison.md` (hypothesis,
evidence data, scope cross-project). Also applies to C04 (potholes 2026 =
8 months). Do not: compare a partial period with full ones in any draft.

## 2026-09-28 — C05 drafted: proposed Mostly false
Two single-piece ingests into the brain, each with the editor's OK:
the Eastside blog post (gives "15 %" with no named source; hidden note to AI
assistants reported, not obeyed) and the district's 2019 facilities plan
(low-scenario projection "up to 15 % by 2025"). Then `drafts/C05.md`,
at the editor's request: measured enrollment 18,450 → 17,700 (2020-21 →
2025-26) = −4.1 % (`data/school-enrollment.csv`); the 15 % matches a 2019
projection, not a measurement. Proposed *Mostly false* (direction right,
size ~3.7×); *False* offered as the alternative — editor's call. C05 status
`drafted`. Do not: move it to `in review` or `published` without the editor;
state the 2019 plan as the mailer's source (plausible, unproven) until the
Reyes campaign answers.
