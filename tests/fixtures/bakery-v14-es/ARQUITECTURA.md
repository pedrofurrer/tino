# ARQUITECTURA — Panadería Los Robles

## Piezas
- `datos/ventas-2026.csv` — ventas diarias por producto. Fuente primaria (muestra: jun–sep 2026).
- `analisis/resumen_ventas.py` — resumen mensual (solo biblioteca estándar; `python3 analisis/resumen_ventas.py [csv]`).
- `recetario/*.md` — una receta por archivo, kebab-case sin acentos.
- `scripts/lint_continuidad.py` · `scripts/rotar_bitacora.py` — verificador de topes y rotador de la bitácora (continuidad).
- `criterio/` + `scripts/lint_criterio.py` — lecciones de criterio e índice (metacognición).
- `conocimiento/` + `scripts/lint_indice.py` — wiki crítica de panadería artesanal (cerebro).

## Diccionario de datos (`ventas-2026.csv`)
| columna | tipo | notas |
|---|---|---|
| fecha | AAAA-MM-DD | un registro por producto y día |
| producto | texto | «pan de campo», «baguette», «medialunas x6» |
| unidades | entero | unidades vendidas |
| precio_unitario | decimal con punto | precio del día |

## INVARIANTES
1. El CSV es la única fuente de verdad de ventas: no se edita a mano ni se «recuerdan» números fuera de él.
2. Fechas ISO y decimales con punto; el script no hace conversiones.
3. `BITACORA.md` es append-only.

## Deuda técnica
- El CSV es una muestra: cualquier conclusión sobre tendencias lleva la etiqueta «muestra de 5 días».
