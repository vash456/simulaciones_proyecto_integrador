#!/usr/bin/env python3
"""Genera las tres graficas de la HU G01 sobre `personajes` e imprime conclusiones.

Uso:
    python scripts/reporte_personajes.py data/limpio/personajes_limpio.csv
    python scripts/reporte_personajes.py personajes_limpio.csv [carpeta_reportes]
"""
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def cargar_limpio(ruta_entrada):
    """Lee el archivo CSV limpio con pandas y devuelve el DataFrame."""
    ruta = Path(ruta_entrada)
    if not ruta.is_file():
        sys.exit(f"Error: no existe el archivo '{ruta}'.")
    return pd.read_csv(ruta)


def contar_duplicados_cid(ruta_limpio):
    """Calcula cuantas filas excedentes por cid repetido existian en el CSV crudo."""
    entrada = Path(ruta_limpio)
    if entrada.parent.name == "limpio" and entrada.parent.parent.name == "data":
        ruta_crudo = entrada.parent.parent / "crudo" / "personajes_sucio.csv"
    else:
        ruta_crudo = Path("data") / "crudo" / "personajes_sucio.csv"
    if not ruta_crudo.is_file():
        return None
    df_crudo = pd.read_csv(ruta_crudo).drop_duplicates()
    return int(df_crudo.duplicated(subset=["cid"], keep="first").sum())


def graficar_estado_moderacion(df, carpeta_reportes):
    """Grafica 1 (barras): personajes por estado de moderacion."""
    conteo = df["estado_moderacion"].value_counts()
    ruta = os.path.join(carpeta_reportes, "personajes_grafica_1.png")
    conteo.plot(kind="bar")
    plt.title("Personajes por estado de moderación")
    plt.xlabel("Estado de moderación")
    plt.ylabel("Cantidad de personajes")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica 1 guardada en: {ruta}")
    return conteo


def graficar_creaciones_por_mes(df, carpeta_reportes):
    """Grafica 2 (linea): personajes creados por mes."""
    por_mes = df.groupby("mes")["id_personaje"].count()
    ruta = os.path.join(carpeta_reportes, "personajes_grafica_2.png")
    por_mes.plot(kind="line", marker="o")
    plt.title("Personajes creados por mes")
    plt.xlabel("Mes de creación")
    plt.ylabel("Cantidad de personajes")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica 2 guardada en: {ruta}")
    return por_mes


def graficar_top_categorias(df, carpeta_reportes):
    """Grafica 3 (barras horizontales): las 10 categorias con mas personajes."""
    top_categorias = df.groupby("id_categoria")["id_personaje"].count().nlargest(10)
    ruta = os.path.join(carpeta_reportes, "personajes_grafica_3.png")
    top_categorias.plot(kind="barh")
    plt.title("Top 10 categorías con más personajes")
    plt.xlabel("Cantidad de personajes")
    plt.ylabel("ID de categoría")
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica 3 guardada en: {ruta}")
    return top_categorias


def imprimir_conclusiones(conteo, por_mes, top_categorias, dups_cid):
    """Imprime en consola las conclusiones obtenidas de los datos y la limpieza."""
    cat_top = top_categorias.idxmax()
    cat_total = int(top_categorias.max())
    mes_top = por_mes.idxmax()
    mes_total = int(por_mes.max())
    estado_top = conteo.idxmax()
    estado_total = int(conteo.max())
    detalle_estados = ", ".join(f"{k}: {int(v)}" for k, v in conteo.items())

    print("\n=== CONCLUSIONES ===")
    print(f"- Categoría con más personajes: categoría {cat_top} con {cat_total} personajes.")
    print(f"- Mes con más personajes creados: {mes_top} con {mes_total} personajes.")
    print(f"- Personajes por estado de moderación: {detalle_estados}. Predomina {estado_top} ({estado_total}).")
    if dups_cid is not None:
        print(f"- Duplicados por cid: en la limpieza se eliminaron {dups_cid} filas excedentes por cid repetido.")
    else:
        print("- Duplicados por cid: no se encontró el CSV crudo para calcular el conteo exacto de filas eliminadas.")
    print(
        "- Integridad en base de datos: la tabla `personajes` debe tener una restricción UNIQUE sobre `cid` "
        "para impedir registros duplicados desde la inserción y garantizar que cada personaje tenga un "
        "identificador único."
    )


def generar_reporte(ruta_entrada, carpeta_reportes="reportes"):
    """Carga el CSV limpio, genera las tres graficas y muestra las conclusiones."""
    df = cargar_limpio(ruta_entrada)
    os.makedirs(carpeta_reportes, exist_ok=True)
    conteo = graficar_estado_moderacion(df, carpeta_reportes)
    por_mes = graficar_creaciones_por_mes(df, carpeta_reportes)
    top_categorias = graficar_top_categorias(df, carpeta_reportes)
    dups_cid = contar_duplicados_cid(ruta_entrada)
    imprimir_conclusiones(conteo, por_mes, top_categorias, dups_cid)


def main(argv):
    """Punto de entrada CLI: valida argumentos y genera el reporte grafico."""
    if len(argv) < 2:
        print("Uso: python scripts/reporte_personajes.py data/limpio/personajes_limpio.csv [carpeta_reportes]")
        return 2

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    ruta_entrada = argv[1]
    carpeta_reportes = argv[2] if len(argv) > 2 else "reportes"
    generar_reporte(ruta_entrada, carpeta_reportes)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))