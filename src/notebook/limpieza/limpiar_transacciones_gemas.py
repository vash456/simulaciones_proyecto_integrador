"""HU HI-8: limpia los datos sucios de `transacciones_gemas` y guarda data/limpio/transacciones_gemas_limpio.csv."""
import os
import sys
from pathlib import Path

import pandas as pd

RAIZ_PROYECTO = Path(__file__).resolve().parents[3]   # raiz del proyecto
RUTA_ENTRADA = RAIZ_PROYECTO / "data" / "crudo" / "transacciones_gemas_sucio.csv"
RUTA_SALIDA = RAIZ_PROYECTO / "data" / "limpio" / "transacciones_gemas_limpio.csv"


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


def limpiar_transacciones_gemas(df):
    """Aplica todas las reglas de limpieza de la HU HI-8 y devuelve el DataFrame limpio."""
    df = df.copy()
    filas_iniciales = len(df)

    # 1. Quitar duplicados exactos
    df = df.drop_duplicates()
    print(f"Filas eliminadas por duplicado exacto: {filas_iniciales - len(df)}")

    # 2. Estandarización de fechas
    df["fecha"] = pd.to_datetime(df["fecha"], format="mixed", dayfirst=True, errors="coerce")

    # 3. Normalización del motivo (ENUM)
    df["motivo"] = df["motivo"].astype(str).str.strip().str.lower().str.replace(" ", "_")

    # 4. Corrección de reglas lógicas de negocio (cantidad)
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    df.loc[(df["motivo"] == "gasto_mensaje") & (df["cantidad"] > 0), "cantidad"] = -df["cantidad"].abs()
    df.loc[(df["motivo"] != "gasto_mensaje") & (df["cantidad"] < 0), "cantidad"] = df["cantidad"].abs()

    # 5. Tratamiento de identificador de referencia
    df["id_referencia"] = pd.to_numeric(df["id_referencia"], errors="coerce").astype("Int64")

    # 6. Unicidad de clave primaria
    df = df.drop_duplicates(subset=["id_transaccion"], keep="first")

    # 7. Ingeniería de atributos temporales
    df["mes"] = df["fecha"].dt.to_period("M").astype(str)

    # 8. Mapeo de tipo de movimiento
    df["tipo_movimiento"] = df["cantidad"].apply(lambda x: "gasto" if x < 0 else "ingreso")

    filas_finales = len(df)
    print(f"Balance de filas: Iniciales={filas_iniciales}, Finales={filas_finales}, Removidas={filas_iniciales - filas_finales}")

    return df


def ejecutar_limpieza(ruta_entrada=RUTA_ENTRADA, ruta_salida=RUTA_SALIDA):
    """Carga crudo, diagnostica, limpia, vuelve a diagnosticar y guarda limpio."""
    df_crudo = pd.read_csv(ruta_entrada)
    imprimir_diagnostico(df_crudo, "Diagnóstico inicial de transacciones_gemas", incluir_info=True)

    df_limpio = limpiar_transacciones_gemas(df_crudo)
    imprimir_diagnostico(df_limpio, "Diagnóstico final de transacciones_gemas")

    os.makedirs(Path(ruta_salida).parent, exist_ok=True)
    df_limpio.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"Archivo limpio guardado en: {ruta_salida}\n")
    return df_limpio


if __name__ == "__main__":
    ejecutar_limpieza()
