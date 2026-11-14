"""HU G01: genera las tres graficas de `personajes` en reportes/ e imprime conclusiones."""
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RAIZ_PROYECTO = Path(__file__).resolve().parents[3]   # raiz del proyecto
RUTA_ENTRADA = RAIZ_PROYECTO / "data" / "limpio" / "personajes_limpio.csv"
RUTA_CRUDO = RAIZ_PROYECTO / "data" / "crudo" / "personajes_sucio.csv"
CARPETA_REPORTES = RAIZ_PROYECTO / "reportes"


def contar_duplicados_cid(ruta_crudo=RUTA_CRUDO):
    """Calcula cuantas filas excedentes por cid repetido existian en el CSV crudo."""
    if not Path(ruta_crudo).is_file():
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
        print("- Duplicados por cid: no se encontró el CSV crudo para calcular el conteo exacto.")
    print(
        "- Integridad en base de datos: la tabla `personajes` debe tener una restricción UNIQUE sobre `cid` "
        "para impedir registros duplicados desde la inserción y garantizar un identificador único."
    )


def generar_reporte(ruta_entrada=RUTA_ENTRADA, carpeta_reportes=CARPETA_REPORTES):
    """Lee el CSV limpio, genera las tres graficas y muestra las conclusiones."""
    if not Path(ruta_entrada).is_file():
        sys.exit(f"Error: no existe el archivo '{ruta_entrada}'.")
    df = pd.read_csv(ruta_entrada)
    os.makedirs(carpeta_reportes, exist_ok=True)
    conteo = graficar_estado_moderacion(df, carpeta_reportes)
    por_mes = graficar_creaciones_por_mes(df, carpeta_reportes)
    top_categorias = graficar_top_categorias(df, carpeta_reportes)
    dups_cid = contar_duplicados_cid()
    imprimir_conclusiones(conteo, por_mes, top_categorias, dups_cid)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    generar_reporte()
