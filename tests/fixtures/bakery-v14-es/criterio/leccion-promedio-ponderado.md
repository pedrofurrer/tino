---
name: leccion-promedio-ponderado
description: "voy a resumir una tasa o un precio a partir de filas con volúmenes distintos → ponderar por el volumen (unidades), nunca promediar los promedios"
metadata:
  type: leccion
  validacion: hipotesis   # 1 caso, con OK del usuario (2026-09-26)
  ambito: panaderia-los-robles
  heredero: ~
---

**Gatillo**: estoy por calcular un «precio medio», una «tasa media» o cualquier
resumen de un cociente a partir de filas (productos, días) que tienen volúmenes
distintos — el ACTO es promediar; el INSUMO son filas con pesos desiguales.

**Error original** (2026-09-26): para el informe de septiembre promedié los
precios unitarios de los tres productos (3,70 · 2,30 · 5,00 → «precio medio
3,67») sin ponderar por unidades vendidas; el usuario señaló que las
medialunas pesan poco en unidades y el número no representaba la caja.

**Principio**: ponderá por el volumen que corresponde (unidades, ingresos,
días) y decí con qué ponderaste; si no hay volumen, mostrá la distribución,
no un promedio.

**Aplicación**: «precio medio ponderado por unidades: 3,63 (55·3,70 + 29·2,30 +
27·5,00) / 111» y no «promedio simple 3,67».

**Casos**:
- 2026-09-26 — informe de septiembre (BITACORA 2026-09-26, introspección inicial).
