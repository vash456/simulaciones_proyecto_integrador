#!/usr/bin/env python3
"""Limpia los datos sucios de la tabla `personajes` siguiendo los criterios de la HU L01.

Uso:
    python scripts/limpiar_personajes.py data/crudo/personajes_sucio.csv
    python scripts/limpiar_personajes.py personajes_sucio.csv [ruta_salida.csv]
"""
import os
import sys
from pathlib import Path

import pandas as pd

# Columnas con Nulo = No en el esquema de la tabla `personajes`
OBLIGATORIAS = [
    "id_personaje",
    "cid",
    "nombre",
    "publico",
    "clasificacion_contenido",
    "estado_moderacion",
    "destacado",
    "version",
    "es_oficial",
    "modo_animacion_portada",
]


def cargar_datos(ruta_entrada):
    """Lee el archivo CSV sucio con pandas y devuelve el DataFrame cargado."""
    ruta = Path(ruta_entrada)
    if not ruta.is_file():
        sys.exit(f"Error: no existe el archivo '{ruta}'.")
    return pd.read_csv(ruta)


def imprimir_diagnostico(df, titulo, incluir_info=False):
    """Imprime forma, duplicados exactos, nulos por columna y opcionalmente df.info()."""
    print(f"=== {titulo} ===")
    print(f"df.shape: {df.shape}")
    if incluir_info:
        print("\ndf.info():")
        df.info()
    print("\ndf.isna().sum():")
    print(df.isna().sum())
    print(f"\nDuplicados exactos (df.duplicated().sum()): {df.duplicated().sum()}\n")


def resolver_ruta_salida(ruta_entrada, ruta_salida=None):
    """Determina la ruta de salida en data/limpio/personajes_limpio.csv por defecto."""
    if ruta_salida:
        return Path(ruta_salida)
    entrada = Path(ruta_entrada)
    if entrada.parent.name == "crudo" and entrada.parent.parent.name == "data":
        return entrada.parent.parent / "limpio" / "personajes_limpio.csv"
    return Path("data") / "limpio" / "personajes_limpio.csv"


def limpiar_personajes(df):
    """Aplica todas las reglas de limpieza de la HU L01 y devuelve el DataFrame limpio."""
    df = df.copy()
    filas_iniciales = len(df)

    # 1. Quitar duplicados exactos
    df = df.drop_duplicates()
    tras_exactos = len(df)
    print(f"Filas eliminadas por duplicado exacto: {filas_iniciales - tras_exactos}")

    # 2. Convertir fecha_creacion aunque venga en dos formatos (ISO y DD/MM/AAAA HH:MM)
    df["fecha_creacion"] = pd.to_datetime(
        df["fecha_creacion"], format="mixed", dayfirst=True, errors="coerce"
    )

    # 3. Unificar estado_moderacion (sin espacios, en MAYUSCULAS y con guion bajo)
    df["estado_moderacion"] = (
        df["estado_moderacion"].astype("string").str.strip().str.upper().str.replace(" ", "_", regex=False)
    )

    # 4. Quitar espacios sobrantes de nombre
    df["nombre"] = df["nombre"].astype("string").str.strip()

    # 5. Rellenar descripciones vacias
    df["descripcion_corta"] = df["descripcion_corta"].fillna("Sin descripcion")

    # 6. Detectar cid repetidos e imprimir cuantos son, luego dejar solo la primera aparicion
    repetidos = df[df.duplicated(subset=["cid"], keep=False)]
    print(f"Filas involucradas en cid repetido: {len(repetidos)} "
          f"(duplicados excedentes a eliminar: {df.duplicated(subset=['cid']).sum()})")
    df = df.drop_duplicates(subset=["cid"], keep="first")

    # 7. Conservar columnas enteras nullable como Int64 (evita '1.0' al exportar)
    for col in ("id_categoria", "id_creador", "id_moderador", "orden_destacado"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # 8. Garantizar cero nulos en columnas obligatorias (Nulo = No)
    cols_oblig = [c for c in OBLIGATORIAS if c in df.columns]
    antes_oblig = len(df)
    df = df.dropna(subset=cols_oblig)
    if len(df) < antes_oblig:
        print(f"Filas eliminadas por nulo en columnas obligatorias: {antes_oblig - len(df)}")

    # 9. Crear la columna mes para agrupar despues
    df["mes"] = df["fecha_creacion"].dt.to_period("M")

    return df


def validar_limpieza(df):
    """Verifica que no queden nulos en columnas obligatorias ni duplicados exactos."""
    cols_oblig = [c for c in OBLIGATORIAS if c in df.columns]
    nulos_oblig = df[cols_oblig].isna().sum()
    nulos_oblig = nulos_oblig[nulos_oblig > 0]
    dups_exactos = int(df.duplicated().sum())
    dups_cid = int(df.duplicated(subset=["cid"]).sum()) if "cid" in df.columns else 0
    print("=== Validacion post-limpieza ===")
    print(f"Nulos en columnas obligatorias: {dict(nulos_oblig) if not nulos_oblig.empty else 'ninguno'}")
    print(f"Duplicados exactos restantes: {dups_exactos}")
    print(f"Duplicados de cid restantes: {dups_cid}\n")


def guardar_limpio(df, ruta_salida):
    """Crea la carpeta destino si no existe y exporta el DataFrame limpio a CSV UTF-8."""
    os.makedirs(ruta_salida.parent, exist_ok=True)
    df.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"Archivo limpio guardado en: {ruta_salida}")


def main(argv):
    """Punto de entrada: diagnostica, limpia, valida y guarda el archivo limpio."""
    if len(argv) < 2:
        print("Uso: python scripts/limpiar_personajes.py data/crudo/personajes_sucio.csv [salida.csv]")
        return 2

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    ruta_entrada = argv[1]
    ruta_salida = resolver_ruta_salida(ruta_entrada, argv[2] if len(argv) > 2 else None)

    df_sucio = cargar_datos(ruta_entrada)
    imprimir_diagnostico(df_sucio, "DIAGNOSTICO ANTES DE LIMPIAR", incluir_info=True)

    df_limpio = limpiar_personajes(df_sucio)

    imprimir_diagnostico(df_limpio, "DIAGNOSTICO DESPUES DE LIMPIAR", incluir_info=True)
    print(f"Total de filas eliminadas: {len(df_sucio) - len(df_limpio)} "
          f"(de {len(df_sucio)} a {len(df_limpio)})\n")

    validar_limpieza(df_limpio)
    guardar_limpio(df_limpio, ruta_salida)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))