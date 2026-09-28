# PLAN — Los Robles Bakery

Last updated: 2026-09-28

States: ✅ done · 🔄 in progress · ⏳ pending · 💡 approved idea, not started <!-- tino:legend -->

## Phase 1 — Write the recipes down (`recipes/`)
- ✅ Country loaf (`recipes/country-loaf.md`), 72 % hydration — June 2026.
- ✅ Baguette (`recipes/baguette.md`) — June 2026.
- ✅ Seed rye (`recipes/seed-rye.md`) — July 2026.
- ⏳ **Croissants** — no written recipe yet, although the owner calls them
  the best seller (see LOGBOOK 2026-09-28). Next step: interview the baker
  (dough, butter, laminating folds, proof, bake) and write
  `recipes/croissants.md` in the same format as the others.

## Phase 2 — Sales analysis (`data/`, `analysis/`)
- ✅ Weekly sales CSV set up (June 2026) and monthly summary script
  (`analysis/sales_summary.py`). Data: 16 weeks, 2026-06-01 → 2026-09-14.
- ⏳ Add the September weeks after 2026-09-14 (September is partial today).
- ✅ June vs September comparison (2026-09-28): prices unit-weighted; units
  compared per week because September is partial (LOGBOOK).
- ⏳ Settle what "best seller" means (units, revenue or margin): by units
  and revenue the CSV puts the country loaf first, the croissants third in
  units (a box of six counted as one unit) and second in revenue; counted
  in single pieces, the croissants lead.

## Phase 3 — Open questions from the baking
- ⏳ New mill flour (delivery 2026-09-04) felt weaker at the same 11.5 %
  protein (spec ± 0.5; blend varies by harvest). Its datasheet advises up to
  70 % for hearth loaves; our standard is 72 %. State of the question:
  `knowledge/syntheses/country-loaf-hydration.md`. Next step: count rejects
  per batch at 72 % in the next bakes; flat loaves → 70 vs 72 % trial.
  Raising to 78 % was asked about and advised against (LOGBOOK 2026-09-28).
- ✅ `reading/` first ingest (2026-09-28): datasheet filed, 80 % blog
  rejected (owner's OK on both).

## User's pending items (only the owner or the baker can do these)
- Give the croissant recipe (the baker's head is the only source).
- Keep sending the weekly sales rows.

## Maintenance
- ⏳ Periodic methodology review + introspection (fortnightly; next:
  2026-10-12): does this continuity system serve the bakery? Propose
  adjustments, never impose them. Same session: skill `introspect` (lesson
  recurrence, drafts, pruning of the index in CLAUDE.md).
- ⏳ Brain content lint (skill `lint-brain`) every ~10 ingests; the
  verifier `python3 scripts/lint_index.py knowledge` counts them.

<!-- lint-budgets: PLAN 120/150 14.4/18 | ARCHITECTURE 160/200 24/30 | LOGBOOK 160/200 20/25 | INSTRUCTIONS 200/300 12/20 | BLOCK 20 -->
