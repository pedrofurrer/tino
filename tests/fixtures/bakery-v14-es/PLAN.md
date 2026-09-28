# PLAN — Panadería Los Robles

> Última actualización: 2026-09-26 (cierre 01:10) · Presupuestos (líneas / KB, alarma al 80 %): PLAN 150/18 · ARQUITECTURA 200/30 · BITACORA 200/25 · bloque de instrucciones 20 líneas.
<!-- lint-topes: PLAN 120/150 14/18 | ARQUITECTURA 160/200 24/30 | BITACORA 160/200 20/25 | INSTRUCCIONES 200/300 12/20 | BLOQUE 20 -->

## F1 — Recetario 🔄
- ✅ Pan de campo y baguette escritas (`recetario/`).
- 🔄 Medialunas — quedamos en: es el producto que más se vende y no tiene receta escrita; próximo paso: entrevistar al panadero y redactar `recetario/medialunas.md`.

## F2 — Análisis de ventas 🔄
- ✅ `analisis/resumen_ventas.py` resume unidades e ingresos por mes y producto.
- 🔄 Comparación entre meses — quedamos en: decidido calcular precio medio PONDERADO por unidades (lección de criterio); próximo paso: agregar variación % mes a mes al script.
- ⏳ Detectar el producto que más crece (jun→sep).
- 💡 Gráfico simple de ventas por producto (idea aprobada, sin arrancar).

## Pendientes del USUARIO
- Confirmar si `datos/ventas-2026.csv` está completo (hoy tiene 5 días de muestra, no el año).

## Mantenimiento
- Introspección del criterio del agente: semanal, fusionada con la revisión periódica (última corrida: 2026-09-26 — 1 lección nueva, 0 reincidencias; próxima: 2026-10-03).
- Revisión periódica de la metodología: cada ~15 días — próxima 2026-10-10 (¿los documentos sirven a ESTE proyecto? ¿presupuestos bien calibrados?).
