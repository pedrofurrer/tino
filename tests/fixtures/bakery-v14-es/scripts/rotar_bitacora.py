#!/usr/bin/env python3
"""Rotación mecánica de la bitácora — mueve las entradas más viejas al archivo.

Plantilla del paquete `continuidad` (v1.4). Sin `--ejecutar` es un ENSAYO:
muestra qué entradas rotaría y cuánto libera, sin tocar nada.

  python3 scripts/rotar_bitacora.py                      → ensayo: la entrada más vieja
  python3 scripts/rotar_bitacora.py --n 3                → ensayo: las 3 más viejas
  python3 scripts/rotar_bitacora.py --hasta 2026-09-20   → ensayo: todas las anteriores a esa fecha
  python3 scripts/rotar_bitacora.py --n 3 --ejecutar --herederos "PLAN §F6 · memoria proyecto-x · commit abc123"

Reglas: (1) nada se borra — las entradas se MUEVEN íntegras al archivo, bajo un
marcador HTML con la fecha y los herederos; (2) `--ejecutar` exige
`--herederos`: el texto donde el operador declara que la parte VIVA de cada
entrada ya rige desde otro lado (PLAN, ARQUITECTURA, memoria, scripts,
commit) — el script mueve, la verificación es humana; (3) la cabecera de la
bitácora recibe (o extiende) la línea «Índice de rotaciones» con la fecha y
la línea del archivo donde quedaron.
Una entrada es todo lo que va desde un encabezado `## AAAA-MM-DD …` hasta el
siguiente `## `. La antigüedad sale de la fecha del encabezado; a igual
fecha, la que está más arriba. La cabecera (lo anterior al primer `## `)
nunca se rota. Sin dependencias fuera de la biblioteca estándar.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

RE_ENTRADA = re.compile(r"^## (\d{4}-\d{2}-\d{2})(.*)$")
CABECERA_ARCHIVO = ("# BITÁCORA — Archivo histórico (entradas rotadas)\n\n"
                    "> Movidas desde BITACORA.md por presupuesto de tamaño. Mismo carácter\n"
                    "> append-only: nunca se edita ni se borra.\n")


def partir(texto: str):
    lineas = texto.split("\n")
    idx = [i for i, l in enumerate(lineas) if l.startswith("## ")]
    if not idx:
        return lineas, []
    cab = lineas[: idx[0]]
    entradas = []
    for k, i in enumerate(idx):
        j = idx[k + 1] if k + 1 < len(idx) else len(lineas)
        m = RE_ENTRADA.match(lineas[i])
        entradas.append({"ini": i, "fin": j, "fecha": m.group(1) if m else "0000-00-00",
                         "titulo": lineas[i][3:].strip(), "lineas": lineas[i:j]})
    return cab, entradas


def etiqueta(titulo: str) -> str:
    m = re.search(r"\(([^)]{1,30})\)", titulo)
    return m.group(1) if m else re.sub(r"[*`]", "", titulo)[:40]


def main() -> None:
    ap = argparse.ArgumentParser(description="Rotación mecánica de la bitácora (ensayo por defecto).")
    ap.add_argument("--bitacora", default="BITACORA.md")
    ap.add_argument("--archivo", default="BITACORA-archivo.md")
    ap.add_argument("--n", type=int, default=1, help="cuántas entradas (las más viejas)")
    ap.add_argument("--hasta", help="rotar todas las anteriores a AAAA-MM-DD (ignora --n)")
    ap.add_argument("--ejecutar", action="store_true", help="sin esto es solo un ensayo")
    ap.add_argument("--herederos", default="", help="dónde rige ya la parte viva de cada entrada (obligatorio con --ejecutar)")
    a = ap.parse_args()

    bit, arc = Path(a.bitacora), Path(a.archivo)
    if not bit.exists():
        sys.exit(f"no encuentro {bit}")
    texto = bit.read_text(encoding="utf-8")
    cab, entradas = partir(texto)
    if not entradas:
        sys.exit("la bitácora no tiene entradas «## AAAA-MM-DD …»")
    orden = sorted(range(len(entradas)), key=lambda k: (entradas[k]["fecha"], k))
    if a.hasta:
        elegidas = [k for k in orden if entradas[k]["fecha"] < a.hasta]
    else:
        elegidas = orden[: max(0, a.n)]
    if not elegidas:
        print("nada que rotar con ese criterio."); return
    bytes_lib = sum(len("\n".join(entradas[k]["lineas"])) + 1 for k in elegidas)
    print(f"{'ROTACIÓN' if a.ejecutar else 'ENSAYO'} — {len(elegidas)} entrada(s) más vieja(s) de {len(entradas)}; libera ≈{bytes_lib} B "
          f"(bitácora hoy: {bit.stat().st_size} B):")
    for k in sorted(elegidas):
        e = entradas[k]
        print(f"  · {e['fecha']} [{etiqueta(e['titulo'])}] {len(e['lineas'])} líneas / {len(chr(10).join(e['lineas']))} B — {e['titulo'][:70]}")
    if not a.ejecutar:
        print("Ensayo: nada se tocó. Verificá que la parte VIVA de cada entrada ya rija en otro lado y repetí con "
              "--ejecutar --herederos \"…\".")
        return
    if not a.herederos.strip():
        sys.exit("--ejecutar exige --herederos \"<dónde rige la parte viva>\" — la verificación es humana.")

    hoy = dt.date.today().isoformat()
    etiquetas = ", ".join(etiqueta(entradas[k]["titulo"]) for k in sorted(elegidas))
    arc_txt = arc.read_text(encoding="utf-8") if arc.exists() else CABECERA_ARCHIVO
    if not arc_txt.endswith("\n"):
        arc_txt += "\n"
    linea_marcador = arc_txt.count("\n") + 2
    bloque = (f"\n<!-- rotado desde {bit.name} el {hoy} ({etiquetas}): entradas íntegras — "
              f"herederos verificados: {a.herederos.strip()} -->\n\n")
    for k in sorted(elegidas):
        cuerpo = "\n".join(entradas[k]["lineas"]).rstrip("\n") + "\n\n"
        bloque += cuerpo
    arc.write_text(arc_txt + bloque, encoding="utf-8")

    quitar = set(elegidas)
    nuevas = list(cab)
    for k, e in enumerate(entradas):
        if k not in quitar:
            nuevas.extend(e["lineas"])
    # índice de rotaciones en la cabecera
    viñeta = f"rotación del **{hoy}** ({etiquetas} al archivo **:{linea_marcador}**; herederos en el marcador)"
    for i, l in enumerate(nuevas[: len(cab)]):
        if l.startswith("> **Índice de rotaciones**"):
            nuevas[i] = l.rstrip() + " · " + viñeta
            break
    else:
        ultimo = max((i for i, l in enumerate(nuevas[: len(cab)]) if l.startswith(">")), default=len(cab) - 1)
        nuevas[ultimo + 1: ultimo + 1] = [">", f"> **Índice de rotaciones** — {viñeta}"]
    salida = "\n".join(nuevas)
    salida = re.sub(r"\n{3,}", "\n\n", salida)
    bit.write_text(salida, encoding="utf-8")
    print(f"Hecho: {len(elegidas)} entrada(s) → {arc.name} :{linea_marcador} · bitácora {bit.stat().st_size} B. "
          f"Revisá el diff antes de confirmar.")


if __name__ == "__main__":
    main()
