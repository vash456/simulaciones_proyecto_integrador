"""HU L01: limpia los datos sucios de `personajes` y guarda data/limpio/personajes_limpio.csv."""
import os
import sys
from pathlib import Path

import pandas as pd

RAIZ_PROYECTO = Path(__file__).resolve().parents[3]   # raiz del proyecto
RUTA_ENTRADA = RAIZ_PROYECTO / "data" / "crudo" / "personajes_sucio.csv"
RUTA_SALIDA = RAIZ_PROYECTO / "data" / "limpio" / "personajes_limpio.csv"

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


def imprimir_diagnostico(df, titulo, incluir_info=False):
    """Imprime shape, nulos, duplicados exactos y opcionalmente df.info()."""
    print(f"=== {titulo} ===")
    print(f"df.shape: {df.shape}")
    if incluir_info:
        print("\ndf.info():")
        df.info()
    print("\ndf.isna().sum():")
    print(df.isna().sum())
    print(f"\nDuplicados exactos: {df.duplicated().sum()}\n")


def limpiar_personajes(df):
    """Aplica todas las reglas de limpieza de la HU L01 y devuelve el DataFrame limpio."""
    df = df.copy()
    filas_iniciales = len(df)

    # 1. Quitar duplicados exactos
    df = df.drop_duplicates()
    print(f"Filas eliminadas por duplicado exacto: {filas_iniciales - len(df)}")

    # 2. Convertir fecha_creacion (dos formatos: ISO y DD/MM/AAAA HH:MM)
    df["fecha_creacion"] = pd.to_datetime(
        df["fecha_creacion"], format="mixed", dayfirst=True, errors="coerce"
    )

    # 3. Unificar estado_moderacion y limpiar espacios en nombre
    df["estado_moderacion"] = (
        df["estado_moderacion"].astype("string").str.strip().str.upper().str.replace(" ", "_", regex=False)
    )
    df["nombre"] = df["nombre"].astype("string").str.strip()

    # 4. Rellenar descripciones vacias
    df["descripcion_corta"] = df["descripcion_corta"].fillna("Sin descripcion")

    # 5. Detectar cid repetidos e imprimir cuantos son; conservar primera aparicion
    repetidos = df[df.duplicated(subset=["cid"], keep=False)]
    print(f"Filas con cid repetido: {len(repetidos)} "
          f"(duplicados a eliminar: {df.duplicated(subset=['cid']).sum()})")
    df = df.drop_duplicates(subset=["cid"], keep="first")

    # 6. Conservar columnas enteras nullable como Int64 (evita '1.0' al guardar)
    for col in ("id_categoria", "id_creador", "id_moderador", "orden_destacado"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # 7. Garantizar cero nulos en columnas obligatorias
    cols_oblig = [c for c in OBLIGATORIAS if c in df.columns]
    df = df.dropna(subset=cols_oblig)

    # 8. Crear la columna mes para agrupar despues
    df["mes"] = df["fecha_creacion"].dt.to_period("M")

    return df


def ejecutar_limpieza(ruta_entrada=RUTA_ENTRADA, ruta_salida=RUTA_SALIDA):
    """Lee el CSV crudo, imprime antes/despues, limpia y guarda personajes_limpio.csv."""
    if not Path(ruta_entrada).is_file():
        sys.exit(f"Error: no existe el archivo '{ruta_entrada}'.")

    df_sucio = pd.read_csv(ruta_entrada)
    imprimir_diagnostico(df_sucio, "ANTES DE LIMPIAR", incluir_info=True)

    df_limpio = limpiar_personajes(df_sucio)

    imprimir_diagnostico(df_limpio, "DESPUES DE LIMPIAR", incluir_info=False)
    print(f"Filas eliminadas en total: {len(df_sucio) - len(df_limpio)}")

    os.makedirs(Path(ruta_salida).parent, exist_ok=True)
    df_limpio.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"Archivo limpio guardado en: {ruta_salida}")
    return df_limpio


if __name__ == "__main__":
    ejecutar_limpieza()
