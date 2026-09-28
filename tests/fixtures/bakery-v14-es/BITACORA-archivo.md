# BITÁCORA — Archivo histórico (entradas rotadas)

> Movidas desde BITACORA.md por presupuesto de tamaño. Mismo carácter
> append-only: nunca se edita ni se borra.

<!-- rotado desde BITACORA.md el 2026-09-26 (v1.4): entradas íntegras — herederos verificados: PLAN §Mantenimiento · ARQUITECTURA §Piezas · commit 8b697bf -->

## 2026-09-26 — Instalación del sistema de continuidad (v1.4)
- Qué: se instalaron las 4 capas (PLAN, BITACORA, ARQUITECTURA; bloque en CLAUDE.md; git ya existía; ritual `guardar-avance`) con escala ESTÁNDAR.
- Por qué: el proyecto tiene dos frentes (recetario + análisis) y va a durar meses; el mínimo (solo PLAN) dejaría sin registrar las decisiones sobre datos.
- Adaptación al dominio: ARQUITECTURA = diccionario de datos del CSV + estructura del recetario (no hay "sistema" que mapear).
- Qué NO hacer: no editar `datos/ventas-2026.csv` a mano (es la fuente primaria); no reescribir recetas ya validadas por el panadero sin su OK.

