"""Revisa la simulación (HU F01) y la exportación (HU X01) de la tabla usuarios.

Uso:  python scripts/revisar_datos.py entrada.txt

Formatos de entrada admitidos (se detectan por contenido/extensión):
  - .csv / .txt  -> texto delimitado (se detecta coma, punto y coma o tabulador)
  - .json        -> lista de objetos (orient="records")
  - .xlsx        -> requiere pandas + openpyxl (única dependencia externa)
  - .txt con UNA sola línea que sea la ruta de otro archivo -> se sigue esa ruta
"""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

N_ESPERADO = 800

# Columnas de la HU: nombre -> (¿admite nulo?, longitud máxima o None)
COLUMNAS = {
    "id_usuario": (False, None),
    "uid": (False, 20),
    "nombre_usuario": (False, 50),
    "correo": (False, 100),
    "genero": (True, None),
    "contrasena_hash": (True, 255),
    "proveedor_auth": (False, 20),
    "id_plan": (False, None),
    "fecha_nacimiento": (True, None),
    "edad_verificada": (False, None),
    "terminos_aceptados": (False, None),
    "fecha_aceptacion_terminos": (True, None),
    "version_terminos": (True, 20),
    "amatistas_saldo": (False, None),
    "estado": (False, None),
    "intentos_fallidos": (False, None),
    "bloqueado_hasta": (True, None),
    "debe_cambiar_password": (False, None),
    "token_version": (False, None),
    "ultimo_acceso": (True, None),
    "fecha_registro": (True, None),
    "rol": (False, None),
    "avatar_url": (True, 255),
    "fecha_eliminacion": (True, None),
    "motivo_eliminacion": (True, 255),
}

FORMATO_ISO = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
FORMATO_LATINO = re.compile(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$")


def es_nulo(valor):
    """Devuelve True si el valor cuenta como nulo (None, vacío o 'nan'/'null')."""
    if valor is None:
        return True
    if isinstance(valor, float) and valor != valor:  # NaN
        return True
    return str(valor).strip().lower() in ("", "nan", "null", "none")


def leer_delimitado(ruta):
    """Lee un archivo de texto delimitado y devuelve (columnas, filas como dicts)."""
    texto = Path(ruta).read_text(encoding="utf-8-sig")
    try:
        dialecto = csv.Sniffer().sniff(texto[:5000], delimiters=",;\t|")
    except csv.Error:
        dialecto = csv.excel
    lector = csv.DictReader(texto.splitlines(), dialect=dialecto)
    filas = list(lector)
    return list(lector.fieldnames or []), filas


def leer_json(ruta):
    """Lee un JSON orient='records' y devuelve (columnas, filas)."""
    datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
    if not isinstance(datos, list):
        raise ValueError("El JSON debe ser una lista de objetos (orient='records').")
    columnas = list(datos[0].keys()) if datos else []
    return columnas, datos


def leer_excel(ruta):
    """Lee un .xlsx con pandas (dependencia opcional) y devuelve (columnas, filas)."""
    try:
        import pandas as pd
    except ImportError:
        sys.exit("Error: leer .xlsx requiere 'pip install pandas openpyxl'.")
    df = pd.read_excel(ruta)
    df = df.astype(object).where(df.notna(), None)
    return list(df.columns), df.to_dict(orient="records")


def cargar(ruta):
    """Elige el lector según la extensión; sigue la ruta si el .txt solo contiene una."""
    ruta = Path(ruta)
    if not ruta.exists():
        sys.exit(f"Error: no existe el archivo '{ruta}'.")
    ext = ruta.suffix.lower()
    if ext == ".txt":
        lineas = [l.strip() for l in ruta.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
        if len(lineas) == 1 and Path(lineas[0]).exists():
            return cargar(lineas[0])
    if ext == ".json":
        return leer_json(ruta)
    if ext in (".xlsx", ".xls"):
        return leer_excel(ruta)
    return leer_delimitado(ruta)


def fila(comprobacion, esperado, encontrado, ok):
    """Construye una fila de la tabla de resultados."""
    return (comprobacion, str(esperado), str(encontrado), "PASA" if ok else "FALLA")


def revisar(columnas, filas):
    """Ejecuta todas las comprobaciones y devuelve la lista de filas de la tabla."""
    r = []
    n = len(filas)
    r.append(fila("Número de filas", N_ESPERADO, n, n == N_ESPERADO))

    # Columnas: faltantes, sobrantes y cantidad
    faltan = [c for c in COLUMNAS if c not in columnas]
    sobran = [c for c in columnas if c not in COLUMNAS]
    r.append(fila("Número de columnas", len(COLUMNAS), len(columnas), len(columnas) == len(COLUMNAS)))
    r.append(fila("Columnas faltantes", "ninguna", ", ".join(faltan) or "ninguna", not faltan))
    r.append(fila("Columnas sobrantes", "ninguna", ", ".join(sobran) or "ninguna", not sobran))
    orden_ok = [c for c in columnas if c in COLUMNAS] == [c for c in COLUMNAS if c in columnas] and not faltan
    r.append(fila("Orden de columnas (HU)", "orden de la HU", "igual" if orden_ok else "distinto", orden_ok))

    # Duplicados exactos de fila (HU: ~5% repetidas tal cual)
    vistas = Counter(tuple(str(f.get(c)) for c in columnas) for f in filas)
    dup_exactos = sum(v - 1 for v in vistas.values() if v > 1)
    pct = 100 * dup_exactos / n if n else 0
    r.append(fila("Filas duplicadas exactas", "≈5% (3%–7%)", f"{dup_exactos} ({pct:.1f}%)", 3 <= pct <= 7))

    # Nulos y duplicados por columna
    for col, (admite_nulo, maximo) in COLUMNAS.items():
        if col not in columnas:
            r.append(fila(f"[{col}] nulos", "columna presente", "columna ausente", False))
            continue
        valores = [f.get(col) for f in filas]
        nulos = sum(es_nulo(v) for v in valores)
        no_nulos = [str(v).strip() for v in valores if not es_nulo(v)]
        dups = sum(c - 1 for c in Counter(no_nulos).values() if c > 1)

        if col == "motivo_eliminacion":
            p = 100 * nulos / n if n else 0
            r.append(fila(f"[{col}] nulos", "≈20% (15%–25%)", f"{nulos} ({p:.1f}%)", 15 <= p <= 25))
        elif admite_nulo:
            r.append(fila(f"[{col}] nulos", "permitidos (columna nula en BD)", nulos, True))
        else:
            r.append(fila(f"[{col}] nulos", 0, nulos, nulos == 0))

        if col == "correo":
            p = 100 * dups / n if n else 0
            r.append(fila(f"[{col}] duplicados", "≥10% repetidos", f"{dups} ({p:.1f}%)", p >= 10))
        else:
            r.append(fila(f"[{col}] duplicados", "sin criterio en la HU", dups, True))

        if maximo:
            largos = [len(v) for v in no_nulos]
            peor = max(largos) if largos else 0
            r.append(fila(f"[{col}] longitud máx.", f"≤{maximo}", peor, peor <= maximo))

    # Ensuciado de fecha_registro: deben convivir los dos formatos
    if "fecha_registro" in columnas:
        vals = [str(f.get("fecha_registro")).strip() for f in filas if not es_nulo(f.get("fecha_registro"))]
        iso = sum(bool(FORMATO_ISO.match(v)) for v in vals)
        lat = sum(bool(FORMATO_LATINO.match(v)) for v in vals)
        otros = len(vals) - iso - lat
        r.append(fila("fecha_registro: 2 formatos mezclados", "ISO>0, dd/mm/aaaa>0, otros=0",
                      f"ISO={iso}, dd/mm/aaaa={lat}, otros={otros}", iso > 0 and lat > 0 and otros == 0))

    # Ensuciado de estado: variantes con mayúsculas o espacios
    if "estado" in columnas:
        vals = [str(f.get("estado")) for f in filas if not es_nulo(f.get("estado"))]
        sucias = sum(v != v.strip() or v != v.lower() for v in vals)
        r.append(fila("estado: variantes sucias (espacios/mayúsculas)", ">0", sucias, sucias > 0))

    # id_usuario secuencial 1..800 (se compara el conjunto de valores únicos)
    if "id_usuario" in columnas:
        try:
            ids = {int(str(f.get("id_usuario")).strip()) for f in filas if not es_nulo(f.get("id_usuario"))}
            ok = ids == set(range(1, N_ESPERADO + 1))
            enc = f"{len(ids)} únicos, rango {min(ids)}-{max(ids)}" if ids else "sin valores"
        except ValueError:
            ok, enc = False, "valores no enteros"
        r.append(fila("id_usuario: entero secuencial", "1 a 800", enc, ok))

    return r


def imprimir_tabla(resultados):
    """Imprime los resultados como tabla Markdown y un resumen final."""
    print("| Comprobación | Esperado | Encontrado | Estado |")
    print("|---|---|---|---|")
    for c, e, f, s in resultados:
        print(f"| {c} | {e} | {f} | {s} |".replace("\n", " "))
    fallas = sum(s == "FALLA" for *_, s in resultados)
    print(f"\nResumen: {len(resultados) - fallas} PASA, {fallas} FALLA de {len(resultados)} comprobaciones.")


def main():
    """Punto de entrada: valida argumentos, carga el archivo y muestra la tabla."""
    if len(sys.argv) != 2:
        sys.exit("Uso: python scripts/revisar_datos.py entrada.txt")
    columnas, filas = cargar(sys.argv[1])
    imprimir_tabla(revisar(columnas, filas))


if __name__ == "__main__":
    main()
