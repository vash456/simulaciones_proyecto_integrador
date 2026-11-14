"""HU HI-9: responde las cinco consultas sobre `transacciones_gemas` y guarda transacciones_gemas_consulta_N.csv."""
import os
import sys
from pathlib import Path

import pandas as pd

RAIZ_PROYECTO = Path(__file__).resolve().parents[3]   # raiz del proyecto
RUTA_ENTRADA = RAIZ_PROYECTO / "data" / "limpio" / "transacciones_gemas_limpio.csv"
CARPETA_SALIDA = RAIZ_PROYECTO / "data" / "limpio"


def guardar_resultado(resultado, carpeta_salida, numero):
    """Guarda el DataFrame o Serie de la consulta N en data/limpio/transacciones_gemas_consulta_N.csv."""
    os.makedirs(carpeta_salida, exist_ok=True)
    ruta = Path(carpeta_salida) / f"transacciones_gemas_consulta_{numero}.csv"
    if isinstance(resultado, pd.Series):
        resultado.rename("cantidad").to_csv(ruta, index=True, encoding="utf-8")
    else:
        resultado.to_csv(ruta, index=False, encoding="utf-8")
    print(f"Guardado en: {ruta}\n")
    return ruta


def consulta_1_compras(df, carpeta_salida=CARPETA_SALIDA):
    """Consulta 1 — Recargas por compra: filtra y extrae transacciones con motivo == 'compra'."""
    print("=== Consulta 1: Recargas por compra (motivo == 'compra') ===")
    res = df[df["motivo"] == "compra"]
    print(f"Total compras: {len(res)} | Total amatistas: +{res['cantidad'].sum():,}")
    print(res[["id_transaccion", "id_usuario", "cantidad", "motivo", "id_referencia", "fecha"]].head(10))
    guardar_resultado(res, carpeta_salida, 1)
    return res


def consulta_2_gastos(df, carpeta_salida=CARPETA_SALIDA):
    """Consulta 2 — Egresos por consumo de mensajes: filtra y extrae transacciones con motivo == 'gasto_mensaje'."""
    print("=== Consulta 2: Egresos por consumo de mensajes (motivo == 'gasto_mensaje') ===")
    res = df[df["motivo"] == "gasto_mensaje"]
    print(f"Total mensajes debitados: {len(res)} | Total amatistas: {res['cantidad'].sum():,}")
    print(res[["id_transaccion", "id_usuario", "cantidad", "motivo", "id_referencia", "fecha"]].head(10))
    guardar_resultado(res, carpeta_salida, 2)
    return res


def consulta_3_conteo_motivo(df, carpeta_salida=CARPETA_SALIDA):
    """Consulta 3 — Conteo por motivo: obtiene la frecuencia de transacciones agrupadas por motivo."""
    print("=== Consulta 3: Frecuencia de transacciones por motivo (value_counts) ===")
    conteo = df["motivo"].value_counts().reset_index()
    conteo.columns = ["motivo", "total_transacciones"]
    conteo["porcentaje"] = (conteo["total_transacciones"] / len(df) * 100).round(2)
    print(conteo)
    guardar_resultado(conteo, carpeta_salida, 3)
    return conteo


def consulta_4_saldos_usuario(df, carpeta_salida=CARPETA_SALIDA):
    """Consulta 4 — GROUPBY por usuario (Saldos): agrupa por id_usuario y calcula balance acumulado ordenado."""
    print("=== Consulta 4: Balance acumulado por usuario (GROUPBY id_usuario) ===")
    res = (
        df.groupby("id_usuario")["cantidad"]
        .agg(saldo_acumulado="sum", total_movimientos="count")
        .reset_index()
        .sort_values(by="saldo_acumulado", ascending=False)
    )
    print(res)
    guardar_resultado(res, carpeta_salida, 4)
    return res


def consulta_5_flujo_mensual(df, carpeta_salida=CARPETA_SALIDA):
    """Consulta 5 — GROUPBY por mes (Flujo temporal): agrupa por mes y calcula conteo y balance neto."""
    print("=== Consulta 5: Flujo temporal por mes (GROUPBY mes) ===")
    res = (
        df.groupby("mes")["cantidad"]
        .agg(total_transacciones="count", balance_neto="sum")
        .reset_index()
        .sort_values(by="mes")
    )
    print(res)
    guardar_resultado(res, carpeta_salida, 5)
    return res


def ejecutar_consultas(df=None, ruta_entrada=RUTA_ENTRADA, carpeta_salida=CARPETA_SALIDA):
    """Ejecuta secuencialmente las cinco consultas de la HU HI-9."""
    if df is None:
        df = pd.read_csv(ruta_entrada)

    resultados = [
        consulta_1_compras(df, carpeta_salida),
        consulta_2_gastos(df, carpeta_salida),
        consulta_3_conteo_motivo(df, carpeta_salida),
        consulta_4_saldos_usuario(df, carpeta_salida),
        consulta_5_flujo_mensual(df, carpeta_salida),
    ]
    return resultados


if __name__ == "__main__":
    ejecutar_consultas()
