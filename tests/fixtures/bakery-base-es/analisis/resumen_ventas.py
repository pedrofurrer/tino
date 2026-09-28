#!/usr/bin/env python3
"""Resumen mensual de ventas: unidades e ingresos por producto."""
import csv, collections, sys
tot = collections.defaultdict(lambda: [0, 0.0])
with open(sys.argv[1] if len(sys.argv) > 1 else "datos/ventas-2026.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        k = (r["fecha"][:7], r["producto"])
        tot[k][0] += int(r["unidades"]); tot[k][1] += int(r["unidades"]) * float(r["precio_unitario"])
for (mes, prod), (u, ing) in sorted(tot.items()):
    print(f"{mes}  {prod:<16} {u:>4} u  {ing:>8.2f}")
