#!/usr/bin/env python3
"""Resuelve las cinco consultas de la HU Q01 sobre la tabla `usuarios`.

Uso:
    python scripts/consultas_usuarios.py usuarios_limpio.csv
"""
import sys
from pathlib import Path

import pandas as pd

CARPETA_SALIDA = Path("data/limpio")


def guardar_consulta(df_resultado, numero):
    """Guarda el resultado de la consulta N en data/limpio/usuarios_consulta_N.csv."""
    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)
    ruta = CARPETA_SALIDA / f"usuarios_consulta_{numero}.csv"
    df_resultado.to_csv(ruta, index=False, encoding="utf-8")
    print(f"Guardado en: {ruta}")
    return ruta


def consulta_1_usuarios_activos(df):
    """Consulta 1: filtra y muestra los usuarios con estado ACTIVO."""
    print("\n=== Consulta 1: ¿Cuántos y cuáles son los usuarios con estado activo? ===")
    activos = df[df["estado"] == "ACTIVO"]
    print(f"Total de usuarios activos: {len(activos)}")
    print(activos[["id_usuario", "nombre_usuario", "correo", "estado"]].head())
    guardar_consulta(activos, 1)
    return activos


def consulta_2_correos_repetidos(df):
    """Consulta 2: detecta y muestra usuarios que aún tengan correo repetido."""
    print("\n=== Consulta 2: ¿Cuántos usuarios tienen correo repetido? ===")
    repetidos = df[df.duplicated(subset=["correo"], keep=False)]
    print(f"Total de registros con correo repetido: {len(repetidos)}")
    if not repetidos.empty:
        print(repetidos[["id_usuario", "nombre_usuario", "correo"]].head())
    guardar_consulta(repetidos, 2)
    return repetidos


def consulta_3_conteo_por_estado(df):
    """Consulta 3: cuenta cuántos usuarios hay por cada estado."""
    print("\n=== Consulta 3: ¿Cuántos usuarios hay por estado? ===")
    conteo = df["estado"].value_counts()
    print(conteo)
    df_conteo = conteo.rename_axis("estado").reset_index(name="cantidad_usuarios")
    guardar_consulta(df_conteo, 3)
    return conteo


def consulta_4_usuarios_por_rol(df):
    """Consulta 4 (groupby): calcula la cantidad de usuarios por rol."""
    print("\n=== Consulta 4: ¿Cuántos usuarios hay por rol? (groupby) ===")
    por_rol = df.groupby("rol")["id_usuario"].count().sort_values(ascending=False)
    print(por_rol)
    df_rol = por_rol.reset_index(name="cantidad_usuarios")
    guardar_consulta(df_rol, 4)
    return por_rol


def consulta_5_usuarios_por_mes(df):
    """Consulta 5 (groupby): calcula cuántos usuarios se registraron cada mes."""
    print("\n=== Consulta 5: ¿Cuántos usuarios se registraron cada mes? (groupby) ===")
    por_mes = df.groupby("mes")["id_usuario"].count()
    print(por_mes)
    df_mes = por_mes.reset_index(name="cantidad_usuarios")
    guardar_consulta(df_mes, 5)
    return por_mes


def main(argv):
    """Punto de entrada: lee usuarios_limpio.csv y ejecuta las 5 consultas en orden."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if len(argv) != 2:
        print("Uso: python scripts/consultas_usuarios.py usuarios_limpio.csv")
        return 2

    ruta_entrada = Path(argv[1])
    if not ruta_entrada.is_file():
        print(f"Error: no existe el archivo '{ruta_entrada}'.")
        return 2

    df = pd.read_csv(ruta_entrada)
    consulta_1_usuarios_activos(df)
    consulta_2_correos_repetidos(df)
    consulta_3_conteo_por_estado(df)
    consulta_4_usuarios_por_rol(df)
    consulta_5_usuarios_por_mes(df)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))