"""HU HI-10: genera las tres gráficas de `transacciones_gemas` en reportes/ e imprime conclusiones."""
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RAIZ_PROYECTO = Path(__file__).resolve().parents[3]   # raiz del proyecto
RUTA_ENTRADA = RAIZ_PROYECTO / "data" / "limpio" / "transacciones_gemas_limpio.csv"
CARPETA_REPORTES = RAIZ_PROYECTO / "reportes"


def graficar_frecuencia_motivo(df, carpeta_reportes=CARPETA_REPORTES):
    """Gráfica 1 (barras): frecuencia de operaciones por tipo de motivo."""
    conteo = df["motivo"].value_counts()
    ruta = os.path.join(carpeta_reportes, "transacciones_gemas_grafica_1.png")

    plt.figure(figsize=(9, 5))
    colores = ["#2b5c8f", "#3c8dbc", "#00a65a", "#dd4b39", "#f39c12"]
    barras = plt.bar(conteo.index, conteo.values, color=colores[:len(conteo)], edgecolor="black", alpha=0.85)

    plt.title("Frecuencia de Operaciones por Tipo de Motivo", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Motivo de Transacción", fontsize=11, fontweight="bold")
    plt.ylabel("Cantidad de Operaciones", fontsize=11, fontweight="bold")
    plt.xticks(rotation=20, ha="right", fontsize=9)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width() / 2.0, altura + (max(conteo.values) * 0.01),
                 f"{int(altura)}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica 1 guardada en: {ruta}")
    return conteo


def graficar_actividad_mensual(df, carpeta_reportes=CARPETA_REPORTES):
    """Gráfica 2 (línea temporal): cantidad de transacciones registradas por mes."""
    actividad_mes = df.groupby("mes").size().reset_index(name="total_transacciones")
    actividad_mes = actividad_mes.sort_values(by="mes")
    ruta = os.path.join(carpeta_reportes, "transacciones_gemas_grafica_2.png")

    plt.figure(figsize=(10, 5))
    plt.plot(actividad_mes["mes"], actividad_mes["total_transacciones"],
             marker="o", color="#1b7837", linewidth=2.2, markersize=6, label="Transacciones")

    plt.title("Actividad Mensual de Transacciones de Amatistas", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Período (Año - Mes)", fontsize=11, fontweight="bold")
    plt.ylabel("Cantidad de Transacciones Registradas", fontsize=11, fontweight="bold")
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc="upper left")

    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica 2 guardada en: {ruta}")
    return actividad_mes


def graficar_saldos_usuario(df, carpeta_reportes=CARPETA_REPORTES):
    """Gráfica 3 (barras horizontales): balance neto de amatistas por usuario (1 al 9)."""
    saldos = df.groupby("id_usuario")["cantidad"].sum().reset_index()
    saldos = saldos.sort_values(by="cantidad", ascending=True)
    ruta = os.path.join(carpeta_reportes, "transacciones_gemas_grafica_3.png")

    etiquetas_usuarios = [f"Usuario #{u}" for u in saldos["id_usuario"]]

    plt.figure(figsize=(9, 6))
    colores = ["#2171b5" if x >= 0 else "#cb181d" for x in saldos["cantidad"]]
    barras = plt.barh(etiquetas_usuarios, saldos["cantidad"], color=colores, edgecolor="black", alpha=0.85)

    plt.title("Balance Acumulado de Amatistas por Usuario", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Saldo Acumulado (Gemas / Amatistas)", fontsize=11, fontweight="bold")
    plt.ylabel("Usuario Registrado (ID)", fontsize=11, fontweight="bold")
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    for barra in barras:
        ancho = barra.get_width()
        pos_x = ancho + (max(abs(saldos["cantidad"])) * 0.015) if ancho >= 0 else ancho - (max(abs(saldos["cantidad"])) * 0.08)
        plt.text(pos_x, barra.get_y() + barra.get_height() / 2.0,
                 f"{int(ancho):,}", va="center", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica 3 guardada en: {ruta}")
    return saldos


def imprimir_conclusiones(df):
    """Imprime las conclusiones de negocio para transacciones_gemas requeridas por HU HI-10."""
    conteo_motivos = df["motivo"].value_counts()
    motivo_top = conteo_motivos.index[0]
    total_top = conteo_motivos.iloc[0]

    transacciones_ingreso = len(df[df["cantidad"] > 0])
    transacciones_gasto = len(df[df["cantidad"] < 0])
    total_gemas_ingresadas = df[df["cantidad"] > 0]["cantidad"].sum()
    total_gemas_gastadas = df[df["cantidad"] < 0]["cantidad"].sum()
    predominio = "INGRESOS" if transacciones_ingreso >= transacciones_gasto else "GASTOS"

    actividad_mes = df.groupby("mes").size()
    mes_pico = actividad_mes.idxmax()
    transacciones_pico = actividad_mes.max()

    saldos_usuario = df.groupby("id_usuario")["cantidad"].sum()
    usuario_mayor_saldo = saldos_usuario.idxmax()
    mayor_saldo = saldos_usuario.max()
    usuario_menor_saldo = saldos_usuario.idxmin()
    menor_saldo = saldos_usuario.min()
    usuarios_negativos = (saldos_usuario < 0).sum()

    estado_balances = (
        f"Se detectaron {usuarios_negativos} usuario(s) con balance neto negativo:"
        if usuarios_negativos > 0 else
        "Todos los usuarios registrados presentan solvencia y balance neto positivo:"
    )

    print("\n" + "=" * 80)
    print("  CONCLUSIONES DE NEGOCIO — TABLA `transacciones_gemas`")
    print("=" * 80)
    print(f"""
1. PATRÓN DE TRANSACCIONES Y MOTIVOS:
   - Motivo más frecuente: '{motivo_top}' con {total_top} operaciones ({(total_top / len(df) * 100):.1f}% del total).
   - Predominio del sistema: {predominio}.
     * Operaciones de ingreso: {transacciones_ingreso} (+{total_gemas_ingresadas:,} amatistas).
     * Operaciones de gasto  : {transacciones_gasto} ({total_gemas_gastadas:,} amatistas).

2. ACTIVIDAD TEMPORAL Y PICO DE USO:
   - Mayor pico mensual: '{mes_pico}' con {transacciones_pico} transacciones registradas.

3. DISTRIBUCIÓN DE SALDOS Y CRITICIDAD DE @Transactional:
   - {estado_balances}
     * Mayor balance: Usuario #{usuario_mayor_saldo} ({mayor_saldo:,} amatistas).
     * Menor balance: Usuario #{usuario_menor_saldo} ({menor_saldo:,} amatistas).
     * Cuentas en saldo negativo: {usuarios_negativos}.
   - Justificación de @Transactional en Backend:
     Garantiza atomicidad y aislamiento (ACID) en débitos y compras de amatistas. Si una
     operación intenta reducir el saldo por debajo de 0 (nuevoSaldo < 0) o falla una llamada
     concurrente, @Transactional aplica un rollback automático evitando pérdidas o inconsistencias.
""")
    print("=" * 80 + "\n")


def generar_reporte(df=None, ruta_entrada=RUTA_ENTRADA, carpeta_reportes=CARPETA_REPORTES):
    """Genera las tres gráficas e imprime las conclusiones analíticas."""
    os.makedirs(carpeta_reportes, exist_ok=True)
    if df is None:
        df = pd.read_csv(ruta_entrada)

    graficar_frecuencia_motivo(df, carpeta_reportes)
    graficar_actividad_mensual(df, carpeta_reportes)
    graficar_saldos_usuario(df, carpeta_reportes)
    imprimir_conclusiones(df)


if __name__ == "__main__":
    generar_reporte()
