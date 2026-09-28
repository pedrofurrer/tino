#!/usr/bin/env python3
"""Verificador de continuidad — topes e integridad de los documentos vivos.

Plantilla del paquete `continuidad` (v1.4). El instalador la copia al proyecto
receptor (p. ej. `scripts/lint_continuidad.py`) y deja en PLAN.md la línea
máquina-legible de topes, con este formato (alarma/tope en líneas y
alarma/tope en KB, KB = 1000 bytes):

  <!-- lint-topes: PLAN 120/150 14/18 | ARQUITECTURA 160/200 24/30 | BITACORA 160/200 20/25 | INSTRUCCIONES 200/300 12/20 | BLOQUE 20 -->

INSTRUCCIONES es el archivo de instrucciones del agente (CLAUDE.md, AGENTS.md…;
se detecta solo, o se fija con el tramo `INSTRUCCIONES=<archivo>`); BLOQUE es
el tope en líneas del bloque «Continuidad entre sesiones» dentro de él. Sin
línea de topes se usan estos mismos valores por defecto.

Uso, desde la raíz del proyecto:
  python3 scripts/lint_continuidad.py            → verifica; exit 1 si hay EXCESO o falla
  python3 scripts/lint_continuidad.py --margen   → bytes y líneas que todavía caben en
                                                   cada documento: medir ANTES de redactar;
                                                   si no cabe, rotar o compactar ANTES.

Chequeos: 1) topes por documento → OK / ALARMA (avisa) / EXCESO (falla);
2) el archivo de instrucciones entero y el bloque de continuidad (solo
ALARMA: se pagan en toda sesión; la dieta la decide el usuario); 3) marcador
de versión del sistema en el bloque; 4) «al filo»: un documento en ALARMA con
menos del 3 % del tope libre ⇒ ESCALADA (proponer al usuario partición tipo
índice o recalibración; nunca de oficio); 5) si ARQUITECTURA tiene una
sección «## INVARIANTES» numerada, la numeración es creciente y sin repetir
(un hueco avisa; un desorden falla: nunca se renumera).
Solo lectura; sin dependencias fuera de la biblioteca estándar.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path.cwd()
DEFAULTS = {  # doc: (alarma_lineas, tope_lineas, alarma_kb, tope_kb)
    "PLAN": (120, 150, 14.0, 18.0),
    "ARQUITECTURA": (160, 200, 24.0, 30.0),
    "BITACORA": (160, 200, 20.0, 25.0),
    "INSTRUCCIONES": (200, 300, 12.0, 20.0),
}
BLOQUE_DEFAULT = 20
CANDIDATOS_INSTRUCCIONES = ("CLAUDE.md", "AGENTS.md", "GEMINI.md", ".cursorrules")
RE_MARCADOR = re.compile(r"<!--\s*suite-agentica:\s*continuidad\s+v[\d.]+\s*-->|Sistema:\s*continuidad\s+v[\d.]+")
RE_BLOQUE = re.compile(r"^#{2,3} .*continuidad", re.M | re.I)
AL_FILO = 0.03  # fracción del tope

fallas: list[str] = []
alarmas: list[str] = []


def parsear_topes():
    topes = dict(DEFAULTS)
    bloque = BLOQUE_DEFAULT
    instrucciones = None
    plan = RAIZ / "PLAN.md"
    if not plan.exists():
        alarmas.append("PLAN.md no existe: se usan los presupuestos por defecto")
        return topes, bloque, instrucciones
    m = re.search(r"<!--\s*lint-topes:\s*(.+?)\s*-->", plan.read_text(encoding="utf-8"))
    if not m:
        alarmas.append("PLAN.md sin línea «<!-- lint-topes: … -->»: se usan los presupuestos por defecto")
        return topes, bloque, instrucciones
    for tramo in m.group(1).split("|"):
        tramo = tramo.strip()
        if not tramo or re.match(r"\S+-particion\s+\S+$", tramo):
            continue  # tramos propios de otras variantes del lint: se ignoran
        mb = re.match(r"BLOQUE\s+(\d+)$", tramo)
        mi = re.match(r"INSTRUCCIONES=(\S+)$", tramo)
        md = re.match(r"(\S+)\s+(\d+)/(\d+)\s+(\d+(?:[.,]\d+)?)/(\d+(?:[.,]\d+)?)$", tramo)
        if mb:
            bloque = int(mb.group(1))
        elif mi:
            instrucciones = mi.group(1)
        elif md:
            doc, al, tl, ak, tk = md.groups()
            topes[doc] = (int(al), int(tl), float(ak.replace(",", ".")), float(tk.replace(",", ".")))
        else:
            alarmas.append(f"tramo ilegible en lint-topes: {tramo!r}")
    return topes, bloque, instrucciones


def archivo_instrucciones(fijado: str | None) -> Path | None:
    if fijado:
        return RAIZ / fijado
    for c in CANDIDATOS_INSTRUCCIONES:
        if (RAIZ / c).exists():
            return RAIZ / c
    return None


def medir(path: Path) -> tuple[int, int]:
    texto = path.read_text(encoding="utf-8")
    return texto.count("\n") + (0 if texto.endswith("\n") or not texto else 1), path.stat().st_size


def ruta_doc(doc: str, instrucciones: str | None) -> Path | None:
    if doc == "INSTRUCCIONES":
        return archivo_instrucciones(instrucciones)
    return RAIZ / f"{doc}.md"


def chequear_topes(topes, instrucciones) -> bool:
    exceso = False
    for doc, (al, tl, ak, tk) in topes.items():
        path = ruta_doc(doc, instrucciones)
        if not path or not path.exists():
            if doc != "INSTRUCCIONES":
                alarmas.append(f"{doc}.md no existe")
            continue
        lineas, tam = medir(path)
        tope_b, alarma_b = int(tk * 1000), int(ak * 1000)
        if lineas > tl or tam > tope_b:
            estado = "EXCESO"
        elif lineas > al or tam > alarma_b:
            estado = "ALARMA"
        else:
            estado = "OK    "
        nota = ""
        if doc == "INSTRUCCIONES":
            if estado == "EXCESO":
                estado, nota = "ALARMA", " (solo aviso: se paga en toda sesión; la dieta la decide el usuario)"
        elif estado == "EXCESO":
            exceso = True
        if estado == "ALARMA" and doc != "INSTRUCCIONES" and (tope_b - tam) < AL_FILO * tope_b:
            nota += " · ESCALADA: al filo del tope → PROPONER al usuario partición tipo índice o recalibración"
        print(f"  {estado}  {path.name}: {lineas} líneas (alarma {al} / tope {tl}) · "
              f"{tam/1000:.1f} KB (alarma {ak} / tope {tk}){nota}")
        if estado == "ALARMA":
            alarmas.append(f"{path.name} en ALARMA{nota}")
    return exceso


def chequear_bloque(instrucciones: str | None, tope_bloque: int) -> None:
    path = archivo_instrucciones(instrucciones)
    if not path or not path.exists():
        alarmas.append("no encuentro el archivo de instrucciones del agente (CLAUDE.md / AGENTS.md…)")
        return
    texto = path.read_text(encoding="utf-8")
    m = RE_BLOQUE.search(texto)
    if not m:
        alarmas.append(f"{path.name}: no encuentro el bloque «Continuidad entre sesiones»")
        return
    resto = texto[m.end():]
    fin = re.search(r"^## ", resto, re.M)
    bloque = texto[m.start(): m.end() + (fin.start() if fin else len(resto))].rstrip("\n")
    n = bloque.count("\n") + 1
    estado = "OK    " if n <= tope_bloque else "ALARMA"
    print(f"  {estado}  bloque de continuidad en {path.name}: {n} líneas (tope {tope_bloque})")
    if n > tope_bloque:
        alarmas.append(f"bloque de continuidad de {n} líneas > {tope_bloque}")
    if RE_MARCADOR.search(bloque) or RE_MARCADOR.search(texto):
        print(f"  OK      marcador de versión presente ({RE_MARCADOR.search(texto).group(0).strip()})")
    else:
        alarmas.append(f"{path.name}: sin marcador de versión «<!-- suite-agentica: continuidad vX.Y -->» (el instalador no podrá detectar la versión)")


def chequear_invariantes() -> None:
    arq = RAIZ / "ARQUITECTURA.md"
    if not arq.exists():
        return
    m = re.search(r"^## INVARIANTES.*?(?=^## |\Z)", arq.read_text(encoding="utf-8"), re.M | re.S)
    if not m:
        return
    numeros = [int(n) for n in re.findall(r"^(\d+)\.\s", m.group(0), re.M)]
    if not numeros:
        return
    if numeros != sorted(numeros) or len(numeros) != len(set(numeros)):
        fallas.append(f"INVARIANTES: numeración desordenada o repetida {numeros} (nunca se renumera)")
        return
    huecos = sorted(set(range(1, max(numeros) + 1)) - set(numeros))
    if huecos:
        alarmas.append(f"INVARIANTES: faltan los números {huecos} (¿se borró una invariante? dejá un tombstone)")
    print(f"  OK      INVARIANTES: {len(numeros)} numeradas, creciente y sin repetir")


def margen(topes, instrucciones) -> None:
    print("── margen de escritura (medir ANTES de redactar) ──")
    for doc, (al, tl, ak, tk) in topes.items():
        path = ruta_doc(doc, instrucciones)
        if not path or not path.exists():
            continue
        lineas, tam = medir(path)
        libre = int(tk * 1000) - tam
        estado = f"caben {libre} B" if libre >= 0 else f"EXCESO: sobran {-libre} B"
        print(f"  {path.name}: {tam} B → {estado} (tope {int(tk*1000)} B) · {lineas}/{tl} líneas → caben {tl - lineas}")


def main() -> None:
    topes, bloque, instrucciones = parsear_topes()
    if "--margen" in sys.argv:
        margen(topes, instrucciones)
        return
    print("── lint_continuidad ──")
    exceso = chequear_topes(topes, instrucciones)
    chequear_bloque(instrucciones, bloque)
    chequear_invariantes()
    for a in alarmas:
        print(f"  ⚠ {a}")
    for f in fallas:
        print(f"  ✗ {f}")
    if exceso or fallas:
        print("RESULTADO: ❌ EXCESO o falla — archivar/reparar ANTES del commit de cierre.")
        sys.exit(1)
    if alarmas:
        print("RESULTADO: ⚠️  ALARMA — compactar en esta sesión si se puede (no bloquea).")
        sys.exit(0)
    print("RESULTADO: ✅ todo dentro de presupuesto.")


if __name__ == "__main__":
    main()
