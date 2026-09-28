---
name: lesson-partial-period-comparison
description: "Comparing period totals when one side may be incomplete → check months covered; exclude, match months, or label partial; never set it against full years"
metadata:
  type: lesson
  validation: hypothesis
  scope: cross-project
  evidence: data
  carried_to: ~
---

**Trigger**: I am about to compare, rank or compute a change between totals
that each aggregate a period — a year, a school year, "last year", "on
record", "since I took office" — and one side may be incomplete. Concrete
forms (they illustrate, they do not limit): a `months_covered` below 12, a
year still in progress, a "to date" figure, a first year of records that
starts mid-year.

**Original error**: in the week before 2026-09-28 (the editor's account; exact
date not given), a reporter's draft for C01 compared 2026 bus ridership,
which covers only eight months, with full years, and it nearly ran. What makes it wrong is in the data itself:
`data/bus-ridership.csv` has `months_covered` = 8 for 2026, and
`data/README.md` says 2026 covers January to August only. Style guide rule 3 says "a partial year is not a year", and the draft broke
it anyway: the failure was not checking coverage at the moment of comparing.

**Principle**: before comparing, check that both sides cover a period of
the same length. A partial period is excluded, compared only with the same
months of other periods, or labeled "partial" wherever it appears — never
set against full periods as if it were one.

**Application**: C01 — 2026 is 3.58 M boardings over 8 months; it is not
set next to 2025's 5.05 M over 12. The latest full year is 2025. `data/` has
no monthly figures, so a same-months comparison is not possible with what
the desk has. Same trap in C04: 2026 potholes are 7,900 over 8 months.
If it recurs: the remedy is an instrument (a mandatory "period covered"
column in each draft's arithmetic table), not more text.

**Cases**:
- 2026-09-28 · origin — recorded on the editor's note: C01 reporter draft, the week before, compared 8-month 2026 ridership with full years; caught before publication.
