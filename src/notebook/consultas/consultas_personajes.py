"""HU Q01: responde las cinco consultas sobre `personajes` y guarda personajes_consulta_N.csv."""
import os
import sys
from pathlib import Path

import pandas as pd

RAIZ_PROYECTO = Path(__file__).resolve().parents[3]   # raiz del proyecto
RUTA_ENTRADA = RAIZ_PROYECTO / "data" / "limpio" / "personajes_limpio.csv"
CARPETA_SALIDA = RAIZ_PROYECTO / "data" / "limpio"


def guardar_resultado(resultado, carpeta_salida, numero):
    """Guarda el DataFrame o Serie de la consulta N en data/limpio/personajes_consulta_N.csv."""
    os.makedirs(carpeta_salida, exist_ok=True)
    ruta = Path(carpeta_salida) / f"personajes_consulta_{numero}.csv"
    if isinstance(resultado, pd.Series):
        resultado.rename("cantidad").to_csv(ruta, index=True, encoding="utf-8")
    else:
        resultado.to_csv(ruta, index=False, encoding="utf-8")
    print(f"Guardado en: {ruta}\n")
    return ruta


def consulta_1_aprobados(df, carpeta_salida=CARPETA_SALIDA):
    """Consulta 1: obtiene los personajes aprobados por moderacion."""
    print("=== Consulta 1: ¿Cuáles personajes fueron aprobados por moderación? ===")
    aprobados = df[df["estado_moderacion"] == "APROBADO"]
    print(f"Total aprobados: {len(aprobados)}")
    print(aprobados[["id_personaje", "cid", "nombre", "estado_moderacion"]].head(10))
    guardar_resultado(aprobados, carpeta_salida, 1)
    return aprobados


def consulta_2_destacados(df, carpeta_salida=CARPETA_SALIDA):
    """Consulta 2: obtiene los personajes destacados ordenados por orden_destacado."""
    print("=== Consulta 2: ¿Cuáles son los personajes destacados ordenados por orden_destacado? ===")
    destacados = df[df["destacado"] == 1].sort_values("orden_destacado")
    print(f"Total destacados: {len(destacados)}")
    print(destacados[["id_personaje", "cid", "nombre", "destacado", "orden_destacado"]].head(10))
    guardar_resultado(destacados, carpeta_salida, 2)
    return destacados


def consulta_3_por_estado(df, carpeta_salida=CARPETA_SALIDA):
    """Consulta 3: cuenta cuántos personajes hay por estado de moderacion."""
    print("=== Consulta 3: ¿Cuántos personajes hay por estado de moderación? ===")
    conteo = df["estado_moderacion"].value_counts()
    print(conteo)
    guardar_resultado(conteo, carpeta_salida, 3)
    return conteo


def consulta_4_top_categorias(df, carpeta_salida=CARPETA_SALIDA):
    """Consulta 4 (GROUPBY): obtiene las 10 categorias con mas personajes."""
    print("=== Consulta 4 (GROUPBY): ¿Cuáles son las 10 categorías con más personajes? ===")
    top_categorias = df.groupby("id_categoria")["id_personaje"].count().nlargest(10)
    print(top_categorias)
    guardar_resultado(top_categorias, carpeta_salida, 4)
    return top_categorias


def consulta_5_por_mes(df, carpeta_salida=CARPETA_SALIDA):
    """Consulta 5 (GROUPBY por mes): cuenta cuántos personajes se crearon cada mes."""
    print("=== Consulta 5 (GROUPBY): ¿Cuántos personajes se crearon cada mes? ===")
    por_mes = df.groupby("mes")["id_personaje"].count()
    print(por_mes)
    guardar_resultado(por_mes, carpeta_salida, 5)
    return por_mes


def ejecutar_consultas(ruta_entrada=RUTA_ENTRADA, carpeta_salida=CARPETA_SALIDA):
    """Lee el CSV limpio, ejecuta las cinco consultas en orden y guarda sus resultados."""
    if not Path(ruta_entrada).is_file():
        sys.exit(f"Error: no existe el archivo '{ruta_entrada}'.")
    df = pd.read_csv(ruta_entrada)
    return [
        consulta_1_aprobados(df, carpeta_salida),
        consulta_2_destacados(df, carpeta_salida),
        consulta_3_por_estado(df, carpeta_salida),
        consulta_4_top_categorias(df, carpeta_salida),
        consulta_5_por_mes(df, carpeta_salida),
    ]


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ejecutar_consultas()
