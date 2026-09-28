#!/usr/bin/env python3
"""Monthly sales summary: units and revenue per product."""
import collections
import csv
import sys

totals = collections.defaultdict(lambda: [0, 0.0])
path = sys.argv[1] if len(sys.argv) > 1 else "data/sales-2026.csv"
with open(path, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        key = (row["week_starting"][:7], row["product"])
        units = int(row["units"])
        totals[key][0] += units
        totals[key][1] += units * float(row["unit_price"])
for (month, product), (units, revenue) in sorted(totals.items()):
    print(f"{month}  {product:<14} {units:>5} u  {revenue:>9.2f}")
