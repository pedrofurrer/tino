# LOGBOOK — decisions and why (append-only)

Entries are never edited or deleted; a reversal goes in a new entry.

## 2026-06-01 — Sales CSV starts; recipe writing begins this month
Per the owner, recipe writing began in June 2026 (the day is not recorded)
with the country loaf and
the baguette, to get down on paper what lived only in the baker's head. The
weekly sales CSV was set up the same month (first week: 2026-06-01).

## 2026-06-26 — Country loaf standard: 72 % hydration
Bake log: 75 % (2026-06-12) spread on the peel, 2 of 12 too flat to sell;
80 % (2026-06-19) too slack to shape at our pace, 5 of 12 flat; 72 %
(2026-06-26) 0 of 12 rejected. Decision: 72 % is the standard.
Do NOT raise hydration without new trials in our own oven.

## 2026-07-20 — Seed rye added
Per the owner, the seed rye recipe was written in July; it first appears in
the sales CSV the week of 2026-07-20.

## 2026-08-14 — Seed rye bake time: 55 min
Bake log: 55 min is right; at 50 min the center stays gummy.

## 2026-09-04 — New flour supplier, to watch
Bake log: new mill's flour, same 11.5 % protein on the bag, but the dough
felt weaker. The mill's datasheet came with the delivery and was not read
then (it was ingested on 2026-09-28, below). No change made; watch the next
bakes (PLAN Phase 3).

## 2026-09-28 — Continuity system installed (tino continuity v2.0)
Standard scale (all 4 layers), English, at the owner's request. Adaptations:
ARCHITECTURE holds the CSV data dictionary and the invariants from the bake
log; `reading/` is declared outside material (the 80 % blog contradicts
invariant 1). Owner's word: croissants are the best seller and have no
written recipe. The CSV (2026-06-01 → 2026-09-14) says otherwise by units and revenue,
counting a box of six croissants as one unit, as the product name
"croissants x6" suggests (in single pieces, 2343 × 6 = 14058, the croissants
would lead): country loaf 4462 u / 15998.20, croissants x6 2343 u / 11453.80,
baguette 2875 u / 6519.90, seed rye 527 u / 2213.40. Left as an open
question in PLAN (the measure may be margin); the croissant recipe is the
top pending item either way.

## 2026-09-28 — Metacognition installed (tino metacognition v2.0)
Owner accepted the defaults: lessons in `lessons/` (versioned with the
project), index in CLAUDE.md below the block (always loaded), all three
introspection triggers, and every lesson proposed before filing. Periodic
introspection merged with the fortnightly methodology review in PLAN. The
save-progress ritual already carries the judgment-retro step (step 4), so it
was not changed. Seeded with the format example (`validation: example`)
and the template; no project lessons yet. The agent's own automatic memory
is not part of this system.

## 2026-09-28 — Brain founded (tino brain v2.0)
Owner's parameters: domain artisan bread baking and running a small bakery;
subdomains doughs-fermentation, baking, costs-pricing, sales-customers (one
sub-index each, plus sources); validation source `notes/bake-log.md` +
`data/sales-2026.csv`; validity ~5 years for techniques, ~12 months for
prices and costs; context a neighborhood bakery, two people, wood-fired
oven. No landscape layer (owner). Wiki in `knowledge/`, empty catalog.
`reading/` NOT processed, by the owner's instruction: both files queued in
PENDING. Gap noted: no cost data, so costs-pricing cannot reach ✅ yet.

## 2026-09-28 — June vs September sales; first judgment lesson
Weekly averages (September has 2 weeks in the CSV, June 5): country loaf
255.2 → 313.0 u/wk (+22.6 %, largest gain in units), croissants x6 123.2 →
173.5 (+40.8 %, the fastest growth among the products sold since June), baguette 185.2 → 178.5 (−3.6 %), seed rye
47.0 (July) → 68.0. Prices June → September: 3.50 → 3.70, 2.20 → 2.30,
4.80 → 5.00, seed rye 4.20 flat. Owner's correction: a month's average price
must be weighted by units (plain mean misleads when volumes vary). Filed
with OK as `lessons/lesson-weight-rates-by-volume.md` (hypothesis). Owner
did NOT approve writing the formula into ARCHITECTURE (only proposed).
Do not compare partial months by totals.

## 2026-09-28 — First brain ingest: datasheet filed, 80 % blog rejected
Owner's OK on both recommendations. Datasheet → card, concept and the
synthesis `knowledge/syntheses/country-loaf-hydration.md` (72 % ✅ with the
previous flour; open with the new one; supplier advises ≤70 % for hearth).
Blog → rejected (no data; our 80 % trial had 5 of 12 flat); raw copy kept.

## 2026-09-28 — 78 % hydration for the new flour: advised against
Owner asked whether to raise the country loaf to 78 % because the new flour
feels weaker. Agent advised no: it would break invariant 1, and the bake log does not
support it (78 % was never tried; with the previous flour, 75 % → 2/12 flat
and 80 % → 5/12), and the supplier points below 72 %, not
above. No change made; the decision stays the owner's. Next: count rejects
at 72 %, then a 70 vs 72 % trial if flat loaves return. A 78 % try, if the
owner wants it, is a logged one-batch trial, not a recipe change.
