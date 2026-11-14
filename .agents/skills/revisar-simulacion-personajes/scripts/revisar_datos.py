#!/usr/bin/env python3
"""Revisa los archivos sucios de la tabla `personajes` contra las HU F01 (simulacion)
y X01 (exportacion) de Kaizen.

Uso:
    python scripts/revisar_datos.py personajes_sucio.csv
    (tambien acepta .xlsx y .json, y varios archivos a la vez)

Imprime una tabla Markdown: Comprobacion | Esperado | Encontrado | Estado.
Solo usa la libreria estandar; `openpyxl` se necesita unicamente para leer .xlsx.
Codigo de salida: 0 si todo PASA, 1 si alguna comprobacion FALLA, 2 si hay error de uso.
"""
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------- Criterios HU
COLUMNAS_HU = [
    "id_personaje", "cid", "id_categoria", "id_creador", "nombre", "descripcion_corta",
    "avatar_url", "publico", "clasificacion_contenido", "estado_moderacion",
    "motivo_rechazo", "id_moderador", "fecha_moderacion", "destacado", "orden_destacado",
    "version", "fecha_creacion", "es_oficial", "genero", "tags", "fecha_eliminacion",
    "motivo_eliminacion", "modo_animacion_portada", "avatar_animado_url",
]
FILAS_HU = 800
# Columnas con Nulo = No en la tabla (captura de phpMyAdmin): nunca deben tener nulos.
OBLIGATORIAS = [
    "id_personaje", "cid", "nombre", "publico", "clasificacion_contenido",
    "estado_moderacion", "destacado", "version", "es_oficial", "modo_animacion_portada",
]
ENTEROS = [
    "id_personaje", "id_categoria", "id_creador", "id_moderador", "orden_destacado",
    "version", "publico", "destacado", "es_oficial",
]
BINARIAS = ["publico", "destacado", "es_oficial"]
NULOS_HU = {"descripcion_corta": 0.20, "avatar_url": 0.10}   # proporcion esperada
TOLERANCIA = 0.03                                            # +/- 3 puntos porcentuales
RE_ISO = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
RE_LATINO = re.compile(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$")
RE_ENTERO = re.compile(r"^-?\d+$")
RE_MOJIBAKE = re.compile("[\u00c3\u00c2][\u0080-\u00bf\u00a0-\u00ff]")


# ------------------------------------------------------------------ Utilidades
def texto(valor):
    """Convierte cualquier valor leido a texto; None y cadena vacia significan nulo (None)."""
    if valor is None:
        return None
    if isinstance(valor, datetime):
        return valor.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(valor, bool):
        return "1" if valor else "0"
    cadena = str(valor)
    return None if cadena == "" else cadena


def pct(parte, total):
    """Devuelve 'n (x.x%)' para mostrar conteos junto a su porcentaje."""
    return f"{parte} ({(100 * parte / total) if total else 0:.1f}%)"


def lista_corta(items, maximo=8):
    """Une una lista en texto y la recorta si es muy larga."""
    items = list(items)
    if not items:
        return "ninguna"
    extra = f" (+{len(items) - maximo} mas)" if len(items) > maximo else ""
    return ", ".join(map(str, items[:maximo])) + extra


# --------------------------------------------------------------------- Lectura
def leer_csv(ruta, meta):
    """Lee un CSV exigiendo UTF-8; si no es valido lo anota en meta y reintenta en latin-1."""
    try:
        with open(ruta, encoding="utf-8", newline="") as f:
            lector = csv.DictReader(f)
            filas = list(lector)
            meta["utf8"] = True
    except UnicodeDecodeError:
        meta["utf8"] = False
        with open(ruta, encoding="latin-1", newline="") as f:
            lector = csv.DictReader(f)
            filas = list(lector)
    return list(lector.fieldnames or []), filas


def leer_json(ruta, meta):
    """Lee un JSON y comprueba que sea una lista de objetos (orient='records')."""
    crudo = Path(ruta).read_text(encoding="utf-8")
    datos = json.loads(crudo)
    meta["json_lista"] = isinstance(datos, list) and all(isinstance(d, dict) for d in datos)
    meta["json_sin_escapes"] = "\\u" not in crudo      # force_ascii=False
    meta["json_indentado"] = crudo.startswith("[\n  ")   # indent=2
    if not meta["json_lista"]:
        return [], []
    columnas = list(datos[0].keys()) if datos else []
    return columnas, datos


def leer_xlsx(ruta, meta):
    """Lee la primera hoja de un .xlsx con openpyxl y anota el nombre de las hojas."""
    try:
        from openpyxl import load_workbook
    except ImportError:
        sys.exit("Falta openpyxl para leer .xlsx: pip install openpyxl")
    libro = load_workbook(ruta, read_only=True, data_only=True)
    meta["hojas"] = libro.sheetnames
    hoja = libro[libro.sheetnames[0]]
    filas_xl = list(hoja.iter_rows(values_only=True))
    if not filas_xl:
        return [], []
    columnas = [str(c) for c in filas_xl[0]]
    return columnas, [dict(zip(columnas, fila)) for fila in filas_xl[1:]]


def leer_archivo(ruta):
    """Despacha la lectura segun la extension y devuelve (columnas, filas, meta)."""
    meta = {}
    ext = Path(ruta).suffix.lower()
    lectores = {".csv": leer_csv, ".json": leer_json, ".xlsx": leer_xlsx}
    if ext not in lectores:
        sys.exit(f"Extension no soportada: {ext} (use .csv, .xlsx o .json)")
    columnas, filas = lectores[ext](ruta, meta)
    return columnas, filas, meta


# --------------------------------------------------------------- Comprobaciones
def comprobar_exportacion(ruta, meta):
    """Comprueba lo que la HU X01 permite verificar mirando el archivo generado."""
    r = []
    ext = Path(ruta).suffix.lower()
    esperado = f"personajes_sucio{ext}"
    r.append(("Nombre del archivo", esperado, Path(ruta).name, Path(ruta).name == esperado))
    if "utf8" in meta:
        r.append(("CSV en UTF-8 valido", "si", "si" if meta["utf8"] else "no", meta["utf8"]))
    if "hojas" in meta:
        r.append(("Hoja de Excel", "personajes", lista_corta(meta["hojas"]),
                  meta["hojas"][:1] == ["personajes"]))
    if "json_lista" in meta:
        r.append(("JSON orient='records' (lista de objetos)", "si",
                  "si" if meta["json_lista"] else "no", meta["json_lista"]))
        r.append(("JSON con force_ascii=False", "sin \\uXXXX",
                  "sin escapes" if meta["json_sin_escapes"] else "con escapes",
                  meta["json_sin_escapes"]))
        r.append(("JSON con indent=2", "si",
                  "si" if meta["json_indentado"] else "no", meta["json_indentado"]))
    return r


def comprobar_estructura(columnas, filas):
    """Comprueba filas y columnas (HU F01: 800 filas y 24 columnas, en orden)."""
    n = len(filas)
    faltan = [c for c in COLUMNAS_HU if c not in columnas]
    sobran = [c for c in columnas if c not in COLUMNAS_HU]
    con_dups = int(FILAS_HU * 1.05)
    return [
        ("Filas", f"{FILAS_HU} (o {con_dups} si los duplicados exactos se anaden aparte)",
         str(n), n in (FILAS_HU, con_dups)),
        ("Cantidad de columnas", str(len(COLUMNAS_HU)), str(len(columnas)),
         len(columnas) == len(COLUMNAS_HU)),
        ("Columnas faltantes", "ninguna", lista_corta(faltan), not faltan),
        ("Columnas sobrantes", "ninguna", lista_corta(sobran), not sobran),
        ("Orden de columnas igual al de la HU", "si", "si" if columnas == COLUMNAS_HU else "no",
         columnas == COLUMNAS_HU),
    ]


def comprobar_columnas(columnas, filas):
    """Cuenta nulos y duplicados de cada columna y los compara con la regla de la HU."""
    r = []
    n = len(filas)
    for col in COLUMNAS_HU + [c for c in columnas if c not in COLUMNAS_HU]:
        if col not in columnas:
            r.append((f"Nulos / duplicados: {col}", "columna presente", "columna ausente", False))
            continue
        valores = [texto(f.get(col)) for f in filas]
        nulos = sum(v is None for v in valores)
        no_nulos = [v for v in valores if v is not None]
        dups = len(no_nulos) - len(set(no_nulos))
        encontrado = f"nulos={pct(nulos, n)}; duplicados={pct(dups, n)}"
        esperado, ok = "sin regla en la HU (informativo)", True
        if col in NULOS_HU:
            meta_p = NULOS_HU[col]
            esperado = f"nulos ~{meta_p:.0%} (+/-{TOLERANCIA:.0%})"
            ok = abs(nulos / n - meta_p) <= TOLERANCIA if n else False
        elif col in OBLIGATORIAS:
            esperado = "nulos=0 (columna NOT NULL)"
            ok = nulos == 0
        if col == "cid":
            esperado += "; duplicados >=7% (10% sembrado)"
            ok = ok and n > 0 and dups / n >= 0.10 - TOLERANCIA
        r.append((f"Nulos / duplicados: {col}", esperado, encontrado, ok))
    exactos = n - len({tuple(texto(f.get(c)) for c in columnas) for f in filas})
    r.append(("Filas duplicadas exactas", "~5% (3% a 7%)", pct(exactos, n),
              n > 0 and 0.03 <= exactos / n <= 0.07))
    return r


def comprobar_contenido(columnas, filas):
    """Comprueba tipos, formatos y suciedad sembrada a proposito (solo columnas presentes)."""
    r = []

    def col(nombre):
        return [texto(f.get(nombre)) for f in filas] if nombre in columnas else None

    # Enteros sin decimales (int(11), tinyint, bit)
    for nombre in ENTEROS:
        v = col(nombre)
        if v is None:
            continue
        malos = [x for x in v if x is not None and not RE_ENTERO.match(x)]
        ejemplo = f", ej. {lista_corta(sorted(set(malos)), 3)}" if malos else ""
        r.append((f"{nombre}: valores enteros", "solo enteros (sin '10.0' ni texto)",
                  f"{len(malos)} invalidos{ejemplo}", not malos))
    for nombre in BINARIAS:
        v = col(nombre)
        if v is None:
            continue
        malos = {x for x in v if x is not None and x not in ("0", "1")}
        r.append((f"{nombre}: solo 0 o 1", "0 / 1", lista_corta(sorted(malos)), not malos))

    # id_personaje 1..800
    ids = col("id_personaje")
    if ids is not None:
        validos = {int(x) for x in ids if x and RE_ENTERO.match(x)}
        rango = f"{min(validos)} a {max(validos)}" if validos else "sin valores"
        r.append(("id_personaje secuencial", f"1 a {FILAS_HU}",
                  f"{rango} ({len(validos)} distintos)",
                  validos == set(range(1, FILAS_HU + 1))))

    # Longitudes de varchar
    for nombre, limite in (("cid", 20), ("nombre", 100), ("genero", 30), ("modo_animacion_portada", 30)):
        v = col(nombre)
        if v is not None:
            largos = sum(x is not None and len(x) > limite for x in v)
            r.append((f"{nombre}: longitud <= {limite}", "0 excesos", f"{largos} excesos", largos == 0))

    # Fechas mezcladas en fecha_creacion
    fechas = col("fecha_creacion")
    if fechas is not None:
        iso = sum(bool(x and RE_ISO.match(x)) for x in fechas)
        lat = sum(bool(x and RE_LATINO.match(x)) for x in fechas)
        raros = sum(1 for x in fechas if x and not (RE_ISO.match(x) or RE_LATINO.match(x)))
        r.append(("fecha_creacion: dos formatos mezclados",
                  "'AAAA-MM-DD HH:MM:SS' y 'DD/MM/AAAA HH:MM'",
                  f"ISO={iso}, latino={lat}, otros={raros}", iso > 0 and lat > 0 and raros == 0))
        parseadas = []
        for x in fechas:
            for fmt in ("%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M"):
                try:
                    parseadas.append(datetime.strptime(x, fmt))
                    break
                except (TypeError, ValueError):
                    continue
        if parseadas:
            dias = (max(parseadas) - min(parseadas)).days
            r.append(("fecha_creacion: rango de ~1 anio (-1y a now)", "<= 366 dias",
                      f"{min(parseadas):%Y-%m-%d} a {max(parseadas):%Y-%m-%d} ({dias} dias)",
                      dias <= 366))

    # Suciedad sembrada en estado_moderacion y nombre
    for nombre in ("estado_moderacion", "nombre"):
        todos = col(nombre)
        if todos is None:
            continue
        v = [x for x in todos if x is not None]
        espacios = sum(x != x.strip() for x in v)
        if nombre == "nombre":   # un nombre "normal" va en Titulo; sucio = TODO MAYUS o todo minus
            mezcla = sum(x.strip().isupper() or x.strip().islower() for x in v)
        else:                    # los estados limpios van en minuscula
            mezcla = sum(x.strip() != x.strip().lower() for x in v)
        r.append((f"{nombre}: espacios sobrantes", "> 0 (ensuciado a proposito)", str(espacios), espacios > 0))
        r.append((f"{nombre}: mayusculas mezcladas", "> 0 (ensuciado a proposito)", str(mezcla), mezcla > 0))

    # Texto danado por codificacion
    danados = sum(
        1 for f in filas for c in columnas
        if isinstance(f.get(c), str) and RE_MOJIBAKE.search(f[c])
    )
    r.append(("Texto sin mojibake (Ã©, Ã­...)", "0 celdas", f"{danados} celdas", danados == 0))

    # Coherencia entre columnas (solo si existen)
    est, mot, mod = col("estado_moderacion"), col("motivo_rechazo"), col("id_moderador")
    if est is not None and mot is not None:
        incoh = sum((e is not None and e.strip().lower() == "rechazado") != (m is not None)
                    for e, m in zip(est, mot))
        r.append(("motivo_rechazo solo si fue rechazado", "0 incoherencias", str(incoh), incoh == 0))
    if est is not None and mod is not None:
        incoh = sum(e is not None and e.strip().lower() in ("aprobado", "rechazado") and m is None
                    for e, m in zip(est, mod))
        r.append(("id_moderador presente si fue moderado", "0 incoherencias", str(incoh), incoh == 0))
    dest, orden = col("destacado"), col("orden_destacado")
    if dest is not None and orden is not None:
        incoh = sum((d == "1") != (o is not None) for d, o in zip(dest, orden))
        r.append(("orden_destacado solo si destacado=1", "0 incoherencias", str(incoh), incoh == 0))
    fe, me = col("fecha_eliminacion"), col("motivo_eliminacion")
    if fe is not None and me is not None:
        incoh = sum((a is None) != (b is None) for a, b in zip(fe, me))
        r.append(("fecha_eliminacion y motivo_eliminacion juntos", "0 incoherencias", str(incoh), incoh == 0))
    return r


# ------------------------------------------------------------------- Impresion
def celda(valor):
    """Escapa las barras verticales para no romper la tabla Markdown."""
    return str(valor).replace("|", "\\|").replace("\n", " ")


def imprimir_tabla(resultados):
    """Imprime la tabla Markdown Comprobacion | Esperado | Encontrado | Estado."""
    print("| Comprobación | Esperado | Encontrado | Estado |")
    print("|---|---|---|---|")
    for comprobacion, esperado, encontrado, ok in resultados:
        print(f"| {celda(comprobacion)} | {celda(esperado)} | {celda(encontrado)} | "
              f"{'PASA' if ok else 'FALLA'} |")
    fallas = sum(not ok for *_, ok in resultados)
    print(f"\nResumen: {len(resultados) - fallas} PASA, {fallas} FALLA de {len(resultados)} comprobaciones.\n")
    return fallas


def revisar(ruta):
    """Ejecuta todas las comprobaciones sobre un archivo e imprime su tabla."""
    columnas, filas, meta = leer_archivo(ruta)
    resultados = (comprobar_exportacion(ruta, meta) + comprobar_estructura(columnas, filas)
                  + comprobar_columnas(columnas, filas) + comprobar_contenido(columnas, filas))
    print(f"### {Path(ruta).name}\n")
    return imprimir_tabla(resultados), (tuple(columnas), len(filas))


def main(argv):
    """Punto de entrada: revisa cada archivo recibido y devuelve el codigo de salida."""
    if len(argv) < 2:
        print("Uso: python scripts/revisar_datos.py personajes_sucio.csv [otro.xlsx otro.json]")
        return 2
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    total, formas = 0, []
    for ruta in argv[1:]:
        if not Path(ruta).is_file():
            print(f"No existe el archivo: {ruta}")
            return 2
        fallas, forma = revisar(ruta)
        total += fallas
        formas.append(forma)
    if len(formas) > 1:   # consistencia entre formatos exportados (HU X01: "el mismo DataFrame")
        iguales = len(set(formas)) == 1
        print("### Consistencia entre formatos\n")
        total += imprimir_tabla([("Mismas columnas y mismo numero de filas en todos los archivos",
                                  "si", "si" if iguales else "no", iguales)])
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
