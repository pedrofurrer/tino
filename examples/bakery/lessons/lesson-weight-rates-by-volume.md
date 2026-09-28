---
name: lesson-weight-rates-by-volume
description: "averaging a price or rate across periods with different volumes → weight by volume (Σ value×volume / Σ volume); a plain mean needs a stated reason"
metadata:
  type: lesson
  validation: hypothesis
  scope: cross-project
  evidence: user        # the owner's correction; arithmetic, but not yet shown by a case where the two averages differ
  carried_to: ~
---

**Trigger**: I am about to average a per-unit figure (price, margin, rate,
cost per unit) over several periods or groups, and the volume behind each
one can differ. The forms illustrate, they do not limit.

**Original error**: 2026-09-28, June vs September average price per
product. Both the plain and the unit-weighted mean were computed, but the
answer presented the weighting as indifferent instead of
stating it as the definition. They matched only because no price changed
mid-month; with a mid-month change the plain mean would have been wrong.
The owner corrected it.

**Principle**: the average of a per-unit figure is the volume-weighted one:
total value / total volume. A plain mean is used only with a stated reason
why every period should count equally, and that reason is written down.

**Application**: in `data/sales-2026.csv`, a month's average price =
Σ(units × unit_price) / Σ units; name the method in the answer, even when
the plain and weighted means coincide.

**Cases**:
- 2026-09-28 · origin — June vs September price comparison; weighting presented as optional; corrected by the owner.
