#!/usr/bin/env python3
"""Verificador determinista del índice partido de la wiki (portada + sub-índices).

Plantilla del paquete `cerebro` (v1.4). El instalador la copia al proyecto
receptor (p. ej. `scripts/lint_indice.py`), ajusta CARPETA por defecto y, si
tradujo los índices a otro idioma, traduce también los MARCADORES de abajo
(cabecera, líneas FIN y operaciones del LOG). Uso:
`python3 lint_indice.py [carpeta-de-la-wiki]`.

Convierte la desincronización portada↔sub-índices↔disco de riesgo silencioso
en falla visible. Chequea:
  1. Portada↔disco: los [[INDICE-*]] enlazados en la portada son exactamente
     los archivos INDICE-*.md existentes; línea FIN de portada con el conteo.
  2. Por sub-índice: contador de cabecera == entradas reales == contador de la
     línea FIN; FIN presente y última línea no vacía; tamaño bajo ALARMA
     (140 líneas / 35 KB → proponer al usuario partición de 2º nivel) y TOPE
     (170 líneas / 45 KB ≈ 21k tokens; una lectura se trunca hacia ~25k).
     KB = 1000 bytes, la misma unidad que la documentación.
  3. Bijección disco↔índice: cada .md de las carpetas de contenido aparece
     exactamente UNA vez en el conjunto de sub-índices (0 huérfanas, 0
     duplicadas, 0 rotas); las entradas de fuentes se chequean por existencia.
  4. Lint de CONTENIDO pendiente: cuenta en LOG.md las ingestas (y cosechas)
     posteriores al último `lint` registrado y avisa a partir de
     INGESTAS_AVISO. Este verificador mide la FORMA de la wiki; el lint de
     contenido (contradicciones, vigencias, lagunas) es otro ritual.

Solo lectura. Exit 0 = verde (las alarmas avisan, no fallan); 1 = falla.
Lo corren los tres rituales (ingesta / cosecha / lint) al cerrar.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# ── Configuración (el instalador ajusta esto) ────────────────────────────
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("conocimiento")
PORTADA = "INDICE.md"
PREFIJO_SUB = "INDICE-"
DIRS_CONTENIDO = ("sintesis", "conceptos", "fichas", "mercado")
ALARMA_LINEAS, TOPE_LINEAS = 140, 170
ALARMA_BYTES, TOPE_BYTES = 35_000, 45_000  # KB = 1000 bytes
LOG, INGESTAS_AVISO = "LOG.md", 10
# Marcadores (traducir junto con los índices si el proyecto no es en español)
RE_FIN_PORTADA = r"^FIN DEL ÍNDICE \(portada\) — (\d+) sub-índices\s*$"
RE_CABECERA = r"^> Entradas: (\d+)\."
RE_FIN_SUB = r"^FIN DEL SUB-ÍNDICE · .+ — (\d+) entradas\s*$"
PREFIJO_FIN_SUB = "FIN DEL SUB-ÍNDICE"
RE_LOG = r"^## \[(\d{4}-\d{2}-\d{2})\] (\S+) \|"   # ## [AAAA-MM-DD] operacion | Título
OPS_INGESTA, OP_LINT = ("ingesta", "cosecha"), "lint"
# ─────────────────────────────────────────────────────────────────────────

fallas: list[str] = []
avisos: list[str] = []


def entradas(texto: str) -> list[str]:
    return [m.group(1).strip()
            for m in re.finditer(r"^- \[\[([^\]|#]+)\]\]", texto, re.M)]


def ingestas_desde_ultimo_lint() -> tuple[int, str]:
    """(ingestas+cosechas posteriores al último lint, fecha del último lint o '')."""
    log = CARPETA / LOG
    if not log.exists():
        return 0, ""
    ops = re.findall(RE_LOG, log.read_text(encoding="utf-8"), re.M)
    ultimo = max((i for i, (_, op) in enumerate(ops) if op == OP_LINT), default=-1)
    n = sum(1 for _, op in ops[ultimo + 1:] if op in OPS_INGESTA)
    return n, (ops[ultimo][0] if ultimo >= 0 else "")


def chequear_tamano(nombre: str, n_lineas: int, n_bytes: int) -> None:
    kb = n_bytes / 1000
    if n_lineas > TOPE_LINEAS or n_bytes > TOPE_BYTES:
        fallas.append(f"{nombre}: {n_lineas} líneas / {kb:.1f} KB supera el TOPE "
                      f"({TOPE_LINEAS} líneas / {TOPE_BYTES // 1000} KB) — partición "
                      f"de 2º nivel impostergable (proponer al usuario YA)")
    elif n_lineas > ALARMA_LINEAS or n_bytes > ALARMA_BYTES:
        avisos.append(f"{nombre}: {n_lineas} líneas / {kb:.1f} KB supera la ALARMA "
                      f"({ALARMA_LINEAS} líneas / {ALARMA_BYTES // 1000} KB) — "
                      f"proponer al usuario la partición de 2º nivel de ese subdominio")


if not (CARPETA / PORTADA).exists():
    print(f"✗ no encuentro {CARPETA / PORTADA} (pasá la carpeta de la wiki como argumento)")
    sys.exit(1)

# --- 1. portada ↔ disco --------------------------------------------------
portada = CARPETA / PORTADA
tx_portada = portada.read_text(encoding="utf-8")
subs_disco = sorted(CARPETA.glob(f"{PREFIJO_SUB}*.md"))
declarados = set(re.findall(r"\[\[(" + re.escape(PREFIJO_SUB) + r"[^\]|#]+)\]\]", tx_portada))
en_disco = {p.stem for p in subs_disco}
for s in sorted(declarados - en_disco):
    fallas.append(f"portada declara [[{s}]] pero {s}.md no existe")
for s in sorted(en_disco - declarados):
    fallas.append(f"{s}.md existe pero la portada no lo enlaza")
m_fin_p = re.search(RE_FIN_PORTADA, tx_portada, re.M)
if not m_fin_p:
    fallas.append("portada sin línea FIN (formato: ver RE_FIN_PORTADA)")
elif int(m_fin_p.group(1)) != len(subs_disco):
    fallas.append(f"portada: el FIN declara {m_fin_p.group(1)} sub-índices, hay {len(subs_disco)} en disco")

# --- 2. por archivo ------------------------------------------------------
vistos: dict[str, list[str]] = {}
for p in [portada] + subs_disco:
    tx = p.read_text(encoding="utf-8")
    lineas = tx.splitlines()
    chequear_tamano(p.name, len(lineas), p.stat().st_size)
    if p == portada:
        continue
    ent = entradas(tx)
    m_cab = re.search(RE_CABECERA, tx, re.M)
    m_fin = re.search(RE_FIN_SUB, tx, re.M)
    if not m_cab:
        fallas.append(f"{p.name}: sin contador de cabecera (formato: ver RE_CABECERA)")
    elif int(m_cab.group(1)) != len(ent):
        fallas.append(f"{p.name}: la cabecera declara {m_cab.group(1)} entradas, hay {len(ent)}")
    if not m_fin:
        fallas.append(f"{p.name}: sin línea FIN (formato: ver RE_FIN_SUB)")
    else:
        if int(m_fin.group(1)) != len(ent):
            fallas.append(f"{p.name}: el FIN declara {m_fin.group(1)} entradas, hay {len(ent)}")
        ultima = next((l for l in reversed(lineas) if l.strip()), "")
        if not ultima.startswith(PREFIJO_FIN_SUB):
            fallas.append(f"{p.name}: la línea FIN no es la última no vacía (hay contenido después del FIN)")
    for t in ent:
        vistos.setdefault(t, []).append(p.name)

# --- 3. bijección disco ↔ índice -----------------------------------------
paginas_disco = {f"{d}/{f.stem}" for d in DIRS_CONTENIDO
                 if (CARPETA / d).exists() for f in (CARPETA / d).glob("*.md")}
for t, dondes in sorted(vistos.items()):
    if len(dondes) > 1:
        fallas.append(f"entrada duplicada: [[{t}]] aparece en {', '.join(dondes)}")
    raiz = t.split("/", 1)[0]
    if raiz in DIRS_CONTENIDO:
        if t not in paginas_disco:
            fallas.append(f"entrada rota: [[{t}]] (en {dondes[0]}) no existe en disco")
    elif raiz == "fuentes":
        base = CARPETA / t
        existe = (base.with_suffix(".md").exists() or base.exists()
                  or (base.parent.exists() and any(base.parent.glob(base.name + ".*"))))
        if not existe:
            fallas.append(f"entrada de fuentes rota: [[{t}]] (en {dondes[0]}) sin archivo en disco")
    else:
        fallas.append(f"entrada fuera de las carpetas conocidas: [[{t}]] (en {dondes[0]})")
for pag in sorted(paginas_disco - set(vistos)):
    fallas.append(f"página huérfana de índice: {pag}.md no está en ningún sub-índice")

# --- reporte -------------------------------------------------------------
print(f"Índice de la wiki: portada + {len(subs_disco)} sub-índices · "
      f"{sum(len(v) for v in vistos.values())} entradas · "
      f"{len(paginas_disco)} páginas de contenido en disco")
n_ing, f_lint = ingestas_desde_ultimo_lint()
print(f"Ingestas desde el último lint de contenido: {n_ing}" + (f" (último lint: {f_lint})" if f_lint else " (sin lint registrado en el LOG)"))
if n_ing >= INGESTAS_AVISO:
    avisos.append(f"{n_ing} ingestas sin lint de CONTENIDO — proponer al usuario correr el lint (el verde de arriba mide solo la forma)")
for a in avisos:
    print(f"⚠ ALARMA: {a}")
if fallas:
    print(f"✗ {len(fallas)} falla(s):")
    for f in fallas:
        print(f"  ✗ {f}")
    sys.exit(1)
print("✓ verde: portada↔disco, contadores, FIN, topes y bijección OK")
