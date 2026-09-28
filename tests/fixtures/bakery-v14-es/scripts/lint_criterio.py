#!/usr/bin/env python3
"""Verificador de las lecciones de criterio y de su índice.

Plantilla del paquete `metacognicion` (v1.4). El instalador la copia al
proyecto receptor (p. ej. `scripts/lint_criterio.py`). Uso:

  python3 scripts/lint_criterio.py --dir criterio --indice criterio/INDICE.md
  python3 scripts/lint_criterio.py --dir <memoria>/criterio --indice <memoria>/MEMORY.md --tope 40
  python3 scripts/lint_criterio.py … --resumen   → una línea por lección (validación ·
                                                   ámbito · casos · última modificación),
                                                   para la introspección incremental

Chequeos sobre cada `leccion-*.md`: frontmatter con `name` igual al archivo,
`description` no vacía, `metadata.type: leccion`, `validacion` dentro del
conjunto admitido (propuesta · hipotesis · recurrente · confirmada · archivada ·
graduada · ejemplo), `ambito` presente; secciones Gatillo / Error original /
Principio / Aplicación / Casos (faltantes → aviso). Sobre el índice (la
sección cuyo encabezado contiene «Criterio del agente»): tope de líneas de
viñeta (`--tope`, 20 por defecto), ninguna lección en dos viñetas, ninguna
referencia a lección inexistente (falla), lecciones activas sin referencia
(aviso), línea «FIN DEL ÍNDICE DE CRITERIO — N entradas» con el conteo
exacto, sección dentro de las primeras `--posicion-max` líneas del archivo
(aviso) y archivo entero bajo `--lineas-max` / `--bytes-max` (200 / 25000,
el límite de carga de la memoria de agente en Claude Code; aviso al 90 %,
falla por encima). Exit 1 = falla; los avisos no fallan. Solo lectura.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

VALIDACIONES = {"propuesta", "hipotesis", "recurrente", "confirmada", "archivada", "graduada", "ejemplo"}
ACTIVAS = {"hipotesis", "recurrente", "confirmada"}
SECCIONES = ("Gatillo", "Error original", "Principio", "Aplicación", "Casos")
RE_FIN = re.compile(r"^FIN DEL ÍNDICE DE CRITERIO — (\d+) entradas\s*$", re.M)
RE_SLUG = re.compile(r"leccion-[a-z0-9-]+")

fallas: list[str] = []
avisos: list[str] = []


def frontmatter(texto: str) -> dict:
    """Parser mínimo: `clave: valor` de primer nivel y un nivel anidado bajo `metadata:`."""
    if not texto.startswith("---"):
        return {}
    partes = texto.split("---", 2)
    if len(partes) < 3:
        return {}
    fm: dict = {}
    padre = None
    for linea in partes[1].splitlines():
        if not linea.strip() or linea.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\s*)([A-Za-z_][\w-]*):\s*(.*)$", linea)
        if not m:
            continue
        sangria, clave, valor = len(m.group(1)), m.group(2), m.group(3).split(" #")[0].strip().strip('"').strip("'")
        if sangria == 0:
            padre = clave if valor == "" else None
            fm[clave] = valor if valor != "" else {}
        elif padre:
            fm[padre][clave] = valor
    return fm


def chequear_leccion(p: Path) -> dict:
    texto = p.read_text(encoding="utf-8")
    fm = frontmatter(texto)
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    if not fm:
        fallas.append(f"{p.name}: sin frontmatter")
    if fm.get("name") != p.stem:
        fallas.append(f"{p.name}: name «{fm.get('name')}» ≠ archivo «{p.stem}»")
    if not fm.get("description"):
        fallas.append(f"{p.name}: description vacía")
    if meta.get("type") != "leccion":
        avisos.append(f"{p.name}: metadata.type ≠ leccion")
    val = meta.get("validacion", "")
    if val not in VALIDACIONES:
        fallas.append(f"{p.name}: validacion «{val}» fuera de {sorted(VALIDACIONES)}")
    if not meta.get("ambito"):
        avisos.append(f"{p.name}: sin ambito")
    faltan = [s for s in SECCIONES if not re.search(r"\*\*" + re.escape(s) + r"\b", texto)]
    if faltan:
        avisos.append(f"{p.name}: sin sección(es) {', '.join(faltan)}")
    m = re.search(r"\*\*Casos\*\*.*", texto, re.S)
    casos = len(re.findall(r"^\s*- ", m.group(0), re.M)) if m else 0
    return {"slug": p.stem, "validacion": val, "ambito": meta.get("ambito", ""), "casos": casos,
            "heredero": meta.get("heredero", ""), "mtime": dt.datetime.fromtimestamp(p.stat().st_mtime)}


def chequear_indice(indice: Path, lecciones: dict, tope: int, posicion_max: int, lineas_max: int, bytes_max: int) -> None:
    texto = indice.read_text(encoding="utf-8")
    lineas = texto.split("\n")
    total_lineas, total_bytes = len(lineas) - (1 if texto.endswith("\n") else 0), indice.stat().st_size
    if total_lineas > lineas_max or total_bytes > bytes_max:
        fallas.append(f"{indice.name}: {total_lineas} líneas / {total_bytes} B supera el límite de carga ({lineas_max} / {bytes_max}) — lo que sigue NO se carga")
    elif total_lineas > 0.9 * lineas_max or total_bytes > 0.9 * bytes_max:
        avisos.append(f"{indice.name}: {total_lineas} líneas / {total_bytes} B, cerca del límite de carga ({lineas_max} / {bytes_max})")
    ini = next((i for i, l in enumerate(lineas) if l.startswith("#") and "criterio del agente" in l.lower()), None)
    if ini is None:
        fallas.append(f"{indice.name}: no encuentro la sección «Criterio del agente»")
        return
    fin = next((j for j in range(ini + 1, len(lineas)) if lineas[j].startswith("## ")), len(lineas))
    seccion = "\n".join(lineas[ini:fin])
    if ini + 1 > posicion_max:
        avisos.append(f"{indice.name}: la sección de criterio empieza en la línea {ini+1} (> {posicion_max}); debería ir primero — la cola del archivo es lo primero que se pierde")
    vinetas = [l for l in lineas[ini:fin] if l.startswith("- ")]
    if len(vinetas) > tope:
        fallas.append(f"índice: {len(vinetas)} viñetas > tope {tope}")
    vistos: dict[str, int] = {}
    for v in vinetas:
        for s in set(RE_SLUG.findall(v)):
            vistos[s] = vistos.get(s, 0) + 1
    for s, n in vistos.items():
        if n > 1:
            fallas.append(f"índice: {s} aparece en {n} viñetas")
    referidas = set(RE_SLUG.findall(seccion))
    for s in lecciones:  # una mención sin el prefijo «leccion-» (p. ej. una graduada comprimida a nombre) también cuenta
        if s not in referidas and re.search(r"(?<![\w-])" + re.escape(s[len("leccion-"):]) + r"(?![\w-])", seccion):
            referidas.add(s)
    for s in sorted(referidas - set(lecciones)):
        fallas.append(f"índice: referencia a {s}, que no existe en el directorio de lecciones")
    for s, d in sorted(lecciones.items()):
        if d["validacion"] in ACTIVAS and s not in referidas:
            avisos.append(f"{s} ({d['validacion']}) no está referida en el índice")
    m = RE_FIN.search(seccion)
    if not m:
        fallas.append("índice: sin línea «FIN DEL ÍNDICE DE CRITERIO — N entradas» al cierre de la sección")
    elif int(m.group(1)) != len(vinetas):
        fallas.append(f"índice: el FIN declara {m.group(1)} entradas y hay {len(vinetas)} viñetas")
    print(f"Índice: sección desde la línea {ini+1} · {len(vinetas)} viñetas (tope {tope}) · {len(referidas)} lecciones referidas · "
          f"archivo {total_lineas} líneas / {total_bytes} B (límite {lineas_max} / {bytes_max})")


def main() -> None:
    ap = argparse.ArgumentParser(description="Verificador de lecciones de criterio e índice.")
    ap.add_argument("--dir", default="criterio")
    ap.add_argument("--indice", default=None, help="archivo que contiene la sección «Criterio del agente» (default: <dir>/INDICE.md)")
    ap.add_argument("--tope", type=int, default=20)
    ap.add_argument("--posicion-max", type=int, default=40)
    ap.add_argument("--lineas-max", type=int, default=200)
    ap.add_argument("--bytes-max", type=int, default=25000)
    ap.add_argument("--resumen", action="store_true")
    a = ap.parse_args()
    d = Path(a.dir).expanduser()
    if not d.is_dir():
        sys.exit(f"✗ no encuentro el directorio de lecciones {d}")
    lecciones = {p.stem: chequear_leccion(p) for p in sorted(d.glob("leccion-*.md"))}
    if a.resumen:
        for s, x in sorted(lecciones.items(), key=lambda kv: kv[1]["mtime"], reverse=True):
            print(f"{x['mtime']:%Y-%m-%d %H:%M}  {x['validacion']:<11} {x['ambito']:<16} casos={x['casos']:<3} "
                  f"{'heredero=' + x['heredero'] + ' ' if x['heredero'] and x['heredero'] != '~' else ''}{s}")
        return
    indice = Path(a.indice).expanduser() if a.indice else d / "INDICE.md"
    if indice.exists():
        chequear_indice(indice, lecciones, a.tope, a.posicion_max, a.lineas_max, a.bytes_max)
    else:
        fallas.append(f"no encuentro el índice {indice}")
    conteo = {}
    for x in lecciones.values():
        conteo[x["validacion"]] = conteo.get(x["validacion"], 0) + 1
    print(f"Lecciones: {len(lecciones)} en {d} · " + " · ".join(f"{k} {v}" for k, v in sorted(conteo.items())))
    for av in avisos:
        print(f"  ⚠ {av}")
    for f in fallas:
        print(f"  ✗ {f}")
    if fallas:
        print(f"✗ {len(fallas)} falla(s)")
        sys.exit(1)
    print(f"✓ verde ({len(avisos)} aviso(s))")


if __name__ == "__main__":
    main()
