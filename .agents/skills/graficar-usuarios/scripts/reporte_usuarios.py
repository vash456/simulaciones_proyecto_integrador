#!/usr/bin/env python3
"""Genera las tres graficas y conclusiones de la HU G01 sobre la tabla `usuarios`.

Uso:
    python scripts/reporte_usuarios.py usuarios_limpio.csv
"""
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

CARPETA_REPORTES = Path("reportes")


def graficar_usuarios_por_estado(df, carpeta_salida):
    """Genera la grafica 1 de barras con la cantidad de usuarios por estado."""
    conteo = df["estado"].value_counts()
    plt.figure(figsize=(8, 5))
    conteo.plot(kind="bar", color="steelblue")
    plt.title("Cantidad de usuarios por estado")
    plt.xlabel("Estado")
    plt.ylabel("Cantidad de usuarios")
    plt.xticks(rotation=0)
    plt.tight_layout()
    ruta = carpeta_salida / "usuarios_grafica_1.png"
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica 1 guardada en: {ruta}")
    return ruta


def graficar_usuarios_por_mes(df, carpeta_salida):
    """Genera la grafica 2 de linea con los registros de usuarios por mes."""
    por_mes = df.groupby("mes")["id_usuario"].count().sort_index()
    plt.figure(figsize=(10, 5))
    por_mes.plot(kind="line", marker="o", color="darkorange")
    plt.title("Usuarios registrados por mes")
    plt.xlabel("Mes de registro")
    plt.ylabel("Cantidad de usuarios")
    plt.xticks(rotation=45)
    plt.tight_layout()
    ruta = carpeta_salida / "usuarios_grafica_2.png"
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica 2 guardada en: {ruta}")
    return por_mes, ruta


def graficar_usuarios_por_rol(df, carpeta_salida):
    """Genera la grafica 3 de barras horizontales con la cantidad de usuarios por rol."""
    por_rol = df.groupby("rol")["id_usuario"].count().sort_values(ascending=True)
    plt.figure(figsize=(8, 5))
    por_rol.plot(kind="barh", color="seagreen")
    plt.title("Cantidad de usuarios por rol")
    plt.xlabel("Cantidad de usuarios")
    plt.ylabel("Rol")
    plt.tight_layout()
    ruta = carpeta_salida / "usuarios_grafica_3.png"
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f"Gráfica 3 guardada en: {ruta}")
    return por_rol.sort_values(ascending=False), ruta


def imprimir_conclusiones(df, por_rol, por_mes):
    """Imprime las conclusiones clave requeridas por la HU G01."""
    rol_top = por_rol.index[0]
    total_rol_top = int(por_rol.iloc[0])

    mes_top = por_mes.idxmax()
    total_mes_top = int(por_mes.max())

    repetidos = int(df.duplicated(subset=["correo"], keep=False).sum())

    print("\n=== Conclusiones del reporte de usuarios ===")
    print(f"1. Rol con más usuarios: '{rol_top}' con {total_rol_top} usuarios.")
    print(f"2. Mes con más registros: {mes_top} con {total_mes_top} usuarios registrados.")
    print(
        f"3. Usuarios con correo repetido en el archivo analizado: {repetidos} "
        "(si el archivo ya pasó por limpieza será 0; en origen crudo existían duplicados). "
        "El backend debe validar unicidad y bloquear correos duplicados con HTTP 409 Conflict "
        "al registrar un correo ya existente, evitando cuentas duplicadas y fallos de integridad."
    )


def main(argv):
    """Punto de entrada: lee usuarios_limpio.csv, genera las 3 graficas e imprime conclusiones."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if len(argv) != 2:
        print("Uso: python scripts/reporte_usuarios.py usuarios_limpio.csv")
        return 2

    ruta_entrada = Path(argv[1])
    if not ruta_entrada.is_file():
        print(f"Error: no existe el archivo '{ruta_entrada}'.")
        return 2

    os.makedirs(CARPETA_REPORTES, exist_ok=True)
    df = pd.read_csv(ruta_entrada)

    graficar_usuarios_por_estado(df, CARPETA_REPORTES)
    por_mes, _ = graficar_usuarios_por_mes(df, CARPETA_REPORTES)
    por_rol, _ = graficar_usuarios_por_rol(df, CARPETA_REPORTES)
    imprimir_conclusiones(df, por_rol, por_mes)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))