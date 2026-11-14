"""HU P03: limpia los datos sucios de `pagos` y guarda data/limpio/pagos_limpio.csv."""
import os
import sys
from pathlib import Path

import pandas as pd

RAIZ_PROYECTO = Path(__file__).resolve().parents[3]   # raiz del proyecto
RUTA_ENTRADA  = RAIZ_PROYECTO / "data" / "crudo"  / "pagos_sucio.csv"
RUTA_SALIDA   = RAIZ_PROYECTO / "data" / "limpio" / "pagos_limpio.csv"

# Columnas que NO pueden quedar nulas segun el esquema de la tabla `pagos`
OBLIGATORIAS = ["id_pago", "id_usuario", "monto", "proveedor", "id_externo", "fecha_pago"]

PROVEEDORES_VALIDOS = {"stripe", "apple", "google"}


def imprimir_diagnostico(df: pd.DataFrame, titulo: str, incluir_info: bool = False) -> None:
    """Imprime shape, nulos, duplicados exactos y opcionalmente df.info()."""
    print(f"\n=== {titulo} ===")
    print(f"df.shape: {df.shape}")
    if incluir_info:
        print("\ndf.info():")
        df.info()
    print("\ndf.isna().sum():")
    print(df.isna().sum())
    print(f"\nDuplicados exactos: {df.duplicated().sum()}\n")


def limpiar_pagos(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica todas las reglas de limpieza sobre el DataFrame sucio de pagos."""
    df = df.copy()
    filas_iniciales = len(df)

    # 1. Quitar duplicados exactos
    df = df.drop_duplicates()
    print(f"Filas eliminadas por duplicado exacto: {filas_iniciales - len(df)}")

    # 2. Convertir fecha_pago (dos formatos: ISO y DD/MM/AAAA HH:MM)
    df["fecha_pago"] = pd.to_datetime(
        df["fecha_pago"], format="mixed", dayfirst=True, errors="coerce"
    )

    # 3. Normalizar proveedor: strip + minusculas
    df["proveedor"] = (
        df["proveedor"]
        .astype("string")
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # 4. Rellenar concepto vacio
    df["concepto"] = df["concepto"].fillna("Paquete de Amatistas no especificado")

    # 5. Garantizar que monto sea numerico
    df["monto"] = pd.to_numeric(df["monto"], errors="coerce")

    # 6. Detectar id_externo duplicado (simula doble cobro / webhook duplicado)
    repetidos = df[df.duplicated(subset=["id_externo"], keep=False)]
    print(
        f"Filas con id_externo repetido: {len(repetidos)} "
        f"(duplicados a eliminar: {df.duplicated(subset=['id_externo']).sum()})"
    )
    df = df.drop_duplicates(subset=["id_externo"], keep="first")

    # 7. Garantizar cero nulos en columnas obligatorias
    cols_oblig = [c for c in OBLIGATORIAS if c in df.columns]
    df = df.dropna(subset=cols_oblig)

    # 8. Crear columna mes para agrupar despues
    df["mes"] = df["fecha_pago"].dt.to_period("M")

    return df


def ejecutar_limpieza(ruta_entrada=RUTA_ENTRADA, ruta_salida=RUTA_SALIDA) -> pd.DataFrame:
    """Lee el CSV crudo, imprime antes/despues, limpia y guarda pagos_limpio.csv."""
    if not Path(ruta_entrada).is_file():
        sys.exit(f"Error: no existe el archivo '{ruta_entrada}'.")

    df_sucio = pd.read_csv(ruta_entrada)
    imprimir_diagnostico(df_sucio, "ANTES DE LIMPIAR PAGOS", incluir_info=True)

    df_limpio = limpiar_pagos(df_sucio)

    imprimir_diagnostico(df_limpio, "DESPUES DE LIMPIAR PAGOS", incluir_info=False)
    print(f"Filas eliminadas en total: {len(df_sucio) - len(df_limpio)}")

    os.makedirs(Path(ruta_salida).parent, exist_ok=True)
    df_limpio.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"Archivo limpio guardado en: {ruta_salida}")
    return df_limpio


if __name__ == "__main__":
    ejecutar_limpieza()
