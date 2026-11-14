#!/usr/bin/env python3
"""Limpia los datos sucios de la tabla `usuarios` segun los criterios de la HU L01.

Uso:
    python scripts/limpiar_usuarios.py usuarios_sucio.csv
"""
import sys
from pathlib import Path

import pandas as pd

COLUMNAS_OBLIGATORIAS = [
    "id_usuario", "uid", "nombre_usuario", "correo", "proveedor_auth",
    "id_plan", "edad_verificada", "terminos_aceptados", "amatistas_saldo",
    "estado", "intentos_fallidos", "debe_cambiar_password", "token_version", "rol",
]
RUTA_SALIDA = Path("data/limpio/usuarios_limpio.csv")


def mostrar_diagnostico(df, titulo, completo=True):
    """Imprime el diagnostico del DataFrame (forma, info, nulos y duplicados)."""
    print(f"\n=== {titulo} ===")
    print("Shape:", df.shape)
    if completo:
        print("\nInfo:")
        df.info()
        print("\nDuplicados exactos:", df.duplicated().sum())
    print("\nNulos por columna:")
    print(df.isna().sum())


def limpiar_datos(df):
    """Aplica las reglas de limpieza de la HU L01 y devuelve el DataFrame limpio."""
    df = df.copy()

    # 1. Eliminar filas duplicadas exactas
    df = df.drop_duplicates()

    # 2. Convertir fecha_registro unificando formatos ISO y latino
    df["fecha_registro"] = pd.to_datetime(
        df["fecha_registro"], format="mixed", dayfirst=True, errors="coerce"
    )

    # 3. Unificar formato de estado
    df["estado"] = df["estado"].str.strip().str.upper().str.replace(" ", "_")

    # 4. Rellenar motivos de eliminacion vacios
    df["motivo_eliminacion"] = df["motivo_eliminacion"].fillna("Sin motivo")

    # 5. Normalizar correo, detectar usuarios repetidos y dejar solo el primero
    df["correo"] = df["correo"].str.strip().str.lower()
    repetidos = df[df.duplicated(subset=["correo"], keep=False)]
    print(f"\nRegistros con correo repetido detectados: {len(repetidos)}")
    df = df.drop_duplicates(subset=["correo"], keep="first")

    # 6. Crear columna mes para agrupaciones posteriores
    df["mes"] = df["fecha_registro"].dt.to_period("M")

    return df


def verificar_post_limpieza(df):
    """Verifica que no queden nulos en columnas obligatorias ni duplicados exactos."""
    obligatorias_presentes = [c for c in COLUMNAS_OBLIGATORIAS if c in df.columns]
    nulos_obligatorios = int(df[obligatorias_presentes].isna().sum().sum())
    duplicados_exactos = int(df.duplicated().sum())
    print(f"\nNulos en columnas obligatorias: {nulos_obligatorios}")
    print(f"Duplicados exactos restantes: {duplicados_exactos}")


def guardar_limpio(df, ruta_salida):
    """Crea la carpeta de destino si no existe y guarda el CSV limpio en UTF-8."""
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"\nArchivo limpio guardado en: {ruta_salida}")


def main(argv):
    """Punto de entrada: lee el CSV sucio, diagnostica, limpia y guarda el resultado."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if len(argv) != 2:
        print("Uso: python scripts/limpiar_usuarios.py usuarios_sucio.csv")
        return 2

    ruta_entrada = Path(argv[1])
    if not ruta_entrada.is_file():
        print(f"Error: no existe el archivo '{ruta_entrada}'.")
        return 2

    df_sucio = pd.read_csv(ruta_entrada)
    filas_iniciales = len(df_sucio)
    mostrar_diagnostico(df_sucio, "DIAGNOSTICO INICIAL (ANTES DE LIMPIAR)", completo=True)

    df_limpio = limpiar_datos(df_sucio)
    filas_eliminadas = filas_iniciales - len(df_limpio)

    mostrar_diagnostico(df_limpio, "DIAGNOSTICO FINAL (DESPUES DE LIMPIAR)", completo=False)
    print(f"\nFilas eliminadas en total: {filas_eliminadas}")
    verificar_post_limpieza(df_limpio)

    guardar_limpio(df_limpio, RUTA_SALIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))