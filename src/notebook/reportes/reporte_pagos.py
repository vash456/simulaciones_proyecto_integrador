"""HU P05: genera las tres graficas de `pagos` en reportes/ e imprime conclusiones."""
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RAIZ_PROYECTO    = Path(__file__).resolve().parents[3]   # raiz del proyecto
RUTA_ENTRADA     = RAIZ_PROYECTO / "data" / "limpio" / "pagos_limpio.csv"
RUTA_CRUDO       = RAIZ_PROYECTO / "data" / "crudo"  / "pagos_sucio.csv"
CARPETA_REPORTES = RAIZ_PROYECTO / "reportes"


def contar_duplicados_id_externo(ruta_crudo=RUTA_CRUDO) -> int | None:
    """Calcula cuantas filas excedentes por id_externo repetido existian en el CSV crudo."""
    if not Path(ruta_crudo).is_file():
        return None
    df_crudo = pd.read_csv(ruta_crudo).drop_duplicates()
    return int(df_crudo.duplicated(subset=["id_externo"], keep="first").sum())


def graficar_transacciones_por_proveedor(df: pd.DataFrame, carpeta_reportes) -> pd.Series:
    """Grafica 1 (barras): transacciones por proveedor de pago."""
    conteo_proveedor = df["proveedor"].value_counts()
    ruta = os.path.join(carpeta_reportes, "pagos_grafica_1.png")
    conteo_proveedor.plot(kind="bar")
    plt.title("Transacciones por proveedor de pago")
    plt.xlabel("Proveedor")
    plt.ylabel("Cantidad de transacciones")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica 1 guardada en: {ruta}")
    return conteo_proveedor


def graficar_tendencia_mensual(df: pd.DataFrame, carpeta_reportes) -> pd.Series:
    """Grafica 2 (linea con marcadores): evolucion mensual de transacciones."""
    por_mes = df.groupby("mes")["id_pago"].count()
    ruta = os.path.join(carpeta_reportes, "pagos_grafica_2.png")
    por_mes.plot(kind="line", marker="o")
    plt.title("Evolución mensual de transacciones de pagos")
    plt.xlabel("Mes")
    plt.ylabel("Cantidad de transacciones")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica 2 guardada en: {ruta}")
    return por_mes


def graficar_top_usuarios_por_monto(df: pd.DataFrame, carpeta_reportes) -> pd.Series:
    """Grafica 3 (barras horizontales): los 10 usuarios con mayor inversion total."""
    top_inversionistas = df.groupby("id_usuario")["monto"].sum().nlargest(10)
    ruta = os.path.join(carpeta_reportes, "pagos_grafica_3.png")
    top_inversionistas.plot(kind="barh")
    plt.title("Top 10 usuarios con mayor inversión total (USD)")
    plt.xlabel("Monto total acumulado (USD)")
    plt.ylabel("ID de usuario")
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica 3 guardada en: {ruta}")
    return top_inversionistas


def imprimir_conclusiones(conteo_proveedor, por_mes, top_inversionistas, dups_ext) -> None:
    """Imprime en consola las conclusiones de negocio obtenidas del analisis de pagos."""
    prov_top     = conteo_proveedor.idxmax()
    prov_total   = int(conteo_proveedor.max())
    mes_top      = por_mes.idxmax()
    mes_total    = int(por_mes.max())
    usr_top      = top_inversionistas.idxmax()
    usr_monto    = round(float(top_inversionistas.max()), 2)

    print("\n=== CONCLUSIONES ===")
    print(f"- Pasarela mas utilizada: '{prov_top}' con {prov_total} transacciones.")
    print(f"- Mes con mayor volumen de compras: {mes_top} con {mes_total} transacciones.")
    print(f"- Usuario con mayor inversion: id_usuario={usr_top} con ${usr_monto} USD acumulados.")
    if dups_ext is not None:
        print(
            f"- Pagos duplicados por id_externo: se detectaron {dups_ext} filas excedentes. "
            "El backend de Spring Boot debe controlar la idempotencia (por ejemplo respondiendo "
            "409 Conflict o ignorando el webhook) para evitar acreditar amatistas dos veces."
        )
    else:
        print("- Duplicados por id_externo: no se encontro el CSV crudo para calcular el conteo exacto.")
    print(
        "- Integridad transaccional: la tabla `pagos` debe tener una restriccion UNIQUE sobre "
        "`id_externo` para bloquear desde la insercion cualquier pago duplicado proveniente "
        "de reintentos de pasarela."
    )


def generar_reporte(ruta_entrada=RUTA_ENTRADA, carpeta_reportes=CARPETA_REPORTES) -> None:
    """Lee el CSV limpio de pagos, genera las tres graficas y muestra las conclusiones."""
    if not Path(ruta_entrada).is_file():
        sys.exit(f"Error: no existe el archivo '{ruta_entrada}'.")
    df = pd.read_csv(ruta_entrada)
    os.makedirs(carpeta_reportes, exist_ok=True)
    conteo_proveedor   = graficar_transacciones_por_proveedor(df, carpeta_reportes)
    por_mes            = graficar_tendencia_mensual(df, carpeta_reportes)
    top_inversionistas = graficar_top_usuarios_por_monto(df, carpeta_reportes)
    dups_ext           = contar_duplicados_id_externo()
    imprimir_conclusiones(conteo_proveedor, por_mes, top_inversionistas, dups_ext)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    generar_reporte()
