"""HU P04: responde las cinco consultas sobre `pagos` y guarda pagos_consulta_N.csv."""
import os
import sys
from pathlib import Path

import pandas as pd

RAIZ_PROYECTO  = Path(__file__).resolve().parents[3]   # raiz del proyecto
RUTA_ENTRADA   = RAIZ_PROYECTO / "data" / "limpio" / "pagos_limpio.csv"
CARPETA_SALIDA = RAIZ_PROYECTO / "data" / "limpio"


def guardar_resultado(resultado, carpeta_salida, numero: int):
    """Guarda la Serie o DataFrame de la consulta N en data/limpio/pagos_consulta_N.csv."""
    os.makedirs(carpeta_salida, exist_ok=True)
    ruta = Path(carpeta_salida) / f"pagos_consulta_{numero}.csv"
    if isinstance(resultado, pd.Series):
        resultado.rename("cantidad").to_csv(ruta, index=True, encoding="utf-8")
    else:
        resultado.to_csv(ruta, index=False, encoding="utf-8")
    print(f"Guardado en: {ruta}\n")
    return ruta


def consulta_1_pagos_stripe(df: pd.DataFrame, carpeta_salida=CARPETA_SALIDA):
    """Consulta 1: obtiene los pagos procesados por Stripe."""
    print("=== Consulta 1: ¿Cuáles pagos fueron procesados por Stripe? ===")
    pagos_stripe = df[df["proveedor"] == "stripe"]
    print(f"Total pagos Stripe: {len(pagos_stripe)}")
    print(pagos_stripe[["id_pago", "id_usuario", "monto", "proveedor", "fecha_pago"]].head(10))
    guardar_resultado(pagos_stripe, carpeta_salida, 1)
    return pagos_stripe


def consulta_2_compradores_recurrentes(df: pd.DataFrame, carpeta_salida=CARPETA_SALIDA):
    """Consulta 2: identifica usuarios con mas de una compra (compradores recurrentes)."""
    print("=== Consulta 2: ¿Cuáles usuarios son compradores recurrentes? ===")
    recurrentes = df[df.duplicated(subset=["id_usuario"], keep=False)]
    print(f"Total transacciones de compradores recurrentes: {len(recurrentes)}")
    print(recurrentes[["id_pago", "id_usuario", "concepto", "monto"]].head(10))
    guardar_resultado(recurrentes, carpeta_salida, 2)
    return recurrentes


def consulta_3_volumen_por_proveedor(df: pd.DataFrame, carpeta_salida=CARPETA_SALIDA):
    """Consulta 3: cuenta el total de transacciones por proveedor de pago."""
    print("=== Consulta 3: ¿Cuántas transacciones tiene cada proveedor? ===")
    conteo_proveedor = df["proveedor"].value_counts()
    print(conteo_proveedor)
    guardar_resultado(conteo_proveedor, carpeta_salida, 3)
    return conteo_proveedor


def consulta_4_top_usuarios_por_monto(df: pd.DataFrame, carpeta_salida=CARPETA_SALIDA):
    """Consulta 4 (GROUPBY): los 10 usuarios con mayor inversion total acumulada."""
    print("=== Consulta 4 (GROUPBY): ¿Cuáles son los 10 usuarios con mayor inversión total? ===")
    top_inversionistas = df.groupby("id_usuario")["monto"].sum().nlargest(10)
    print(top_inversionistas)
    guardar_resultado(top_inversionistas, carpeta_salida, 4)
    return top_inversionistas


def consulta_5_por_mes(df: pd.DataFrame, carpeta_salida=CARPETA_SALIDA):
    """Consulta 5 (GROUPBY por mes): volumen de transacciones por mes."""
    print("=== Consulta 5 (GROUPBY): ¿Cuántas transacciones se realizaron cada mes? ===")
    por_mes = df.groupby("mes")["id_pago"].count()
    print(por_mes)
    guardar_resultado(por_mes, carpeta_salida, 5)
    return por_mes


def ejecutar_consultas(ruta_entrada=RUTA_ENTRADA, carpeta_salida=CARPETA_SALIDA):
    """Lee el CSV limpio de pagos, ejecuta las cinco consultas y guarda sus resultados."""
    if not Path(ruta_entrada).is_file():
        sys.exit(f"Error: no existe el archivo '{ruta_entrada}'.")
    df = pd.read_csv(ruta_entrada)
    return [
        consulta_1_pagos_stripe(df, carpeta_salida),
        consulta_2_compradores_recurrentes(df, carpeta_salida),
        consulta_3_volumen_por_proveedor(df, carpeta_salida),
        consulta_4_top_usuarios_por_monto(df, carpeta_salida),
        consulta_5_por_mes(df, carpeta_salida),
    ]


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ejecutar_consultas()
