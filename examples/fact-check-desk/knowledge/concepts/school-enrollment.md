# School enrollment (Port Alder public school district)

**Definition**: students enrolled in the city's public school district, per
school year (`data/school-enrollment.csv`, portal export of 2026-09-15).

## State of knowledge
- ✅ Measured enrollment, 2020-21 → 2025-26 (`data/school-enrollment.csv`):
  18,450 · 18,320 · 18,100 · 17,960 · 17,820 · 17,700. Change over the
  period: −750 students, **−4.1 %** (750 / 18,450). Every year is lower than
  the one before; the last year's drop is −0.7 % (120 / 17,820).
- The file does not cover years before 2020-21.
- 🔸 "Enrollment has fallen 15 percent" — circulating claim with no named source
  ([[cards/eastside-blog-schools]]; also C05 in the claims log).
  Contradicted by the measured series for the period it covers.
- 🔹 District projections, 2019 → 2025 ([[cards/school-facilities-plan-2019]]):
  high stable (± 1 %), baseline about −5 %, low "up to 15 %" (conditional).
  Projections, not measurements. The measured change (−3.4 % to 2024-25,
  −4.1 % to 2025-26, from a 2020-21 base) sits closest to the baseline.
- Origin of the circulating 15 %: a plausible origin is documented (the
  2019 low scenario); that it is the actual origin is unproven.
- Gap: no 2019 enrollment figure in `data/`, so the plan's base year cannot
  be compared like for like.

## Relations
- Claim C05 (claims log).
- [[cards/school-facilities-plan-2019]] — the district's own projections.

## Application
For any enrollment claim: compute it from `data/school-enrollment.csv` for
the period the speaker names; if no period is named, report the full series'
change and say the claim does not specify one.
