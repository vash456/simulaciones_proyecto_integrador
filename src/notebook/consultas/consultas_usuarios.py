import sys
from pathlib import Path

import pandas as pd

RAIZ_PROYECTO = Path(__file__).resolve().parents[3]
CARPETA_LIMPIO = RAIZ_PROYECTO / "data" / "limpio"
RUTA_ENTRADA_DEFECTO = CARPETA_LIMPIO / "usuarios_limpio.csv"


def guardar_consulta(df_resultado, numero, carpeta_salida=CARPETA_LIMPIO):
    """Guarda el resultado de la consulta N en data/limpio/usuarios_consulta_N.csv."""
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    ruta = carpeta_salida / f"usuarios_consulta_{numero}.csv"
    df_resultado.to_csv(ruta, index=False, encoding="utf-8")
    print(f"Guardado en: {ruta}")
    return ruta


def consulta_1_usuarios_activos(df):
    """Consulta 1: filtra y muestra los usuarios con estado ACTIVO."""
    print("\n--- Consulta 1: ¿Cuántos y cuáles son los usuarios con estado activo? ---")
    activos = df[df["estado"] == "ACTIVO"]
    print(f"Total de usuarios activos: {len(activos)}")
    print(activos[["id_usuario", "nombre_usuario", "correo", "estado"]].head())
    ruta = guardar_consulta(activos, 1)
    return activos, ruta


def consulta_2_correos_repetidos(df):
    """Consulta 2: detecta y muestra usuarios que aún tengan correo repetido."""
    print("\n--- Consulta 2: ¿Cuántos usuarios tienen correo repetido? ---")
    repetidos = df[df.duplicated(subset=["correo"], keep=False)]
    print(f"Total de registros con correo repetido: {len(repetidos)}")
    if not repetidos.empty:
        print(repetidos[["id_usuario", "nombre_usuario", "correo"]].head())
    ruta = guardar_consulta(repetidos, 2)
    return repetidos, ruta


def consulta_3_conteo_por_estado(df):
    """Consulta 3: cuenta cuántos usuarios hay por cada estado."""
    print("\n--- Consulta 3: ¿Cuántos usuarios hay por estado? ---")
    conteo = df["estado"].value_counts()
    print(conteo)
    df_conteo = conteo.rename_axis("estado").reset_index(name="cantidad_usuarios")
    ruta = guardar_consulta(df_conteo, 3)
    return conteo, ruta


def consulta_4_usuarios_por_rol(df):
    """Consulta 4 (groupby): calcula la cantidad de usuarios por rol."""
    print("\n--- Consulta 4: ¿Cuántos usuarios hay por rol? (groupby) ---")
    por_rol = df.groupby("rol")["id_usuario"].count().sort_values(ascending=False)
    print(por_rol)
    df_rol = por_rol.reset_index(name="cantidad_usuarios")
    ruta = guardar_consulta(df_rol, 4)
    return por_rol, ruta


def consulta_5_usuarios_por_mes(df):
    """Consulta 5 (groupby): calcula cuántos usuarios se registraron cada mes."""
    print("\n--- Consulta 5: ¿Cuántos usuarios se registraron cada mes? (groupby) ---")
    por_mes = df.groupby("mes")["id_usuario"].count()
    print(por_mes)
    df_mes = por_mes.reset_index(name="cantidad_usuarios")
    ruta = guardar_consulta(df_mes, 5)
    return por_mes, ruta


def ejecutar_consultas(ruta_entrada=None):
    """Lee usuarios_limpio.csv y ejecuta las 5 consultas de la HU Q01 en orden."""
    entrada = Path(ruta_entrada) if ruta_entrada else RUTA_ENTRADA_DEFECTO
    if not entrada.is_file():
        raise FileNotFoundError(f"No existe el archivo limpio de entrada: {entrada}")

    df = pd.read_csv(entrada)
    r1, p1 = consulta_1_usuarios_activos(df)
    r2, p2 = consulta_2_correos_repetidos(df)
    r3, p3 = consulta_3_conteo_por_estado(df)
    r4, p4 = consulta_4_usuarios_por_rol(df)
    r5, p5 = consulta_5_usuarios_por_mes(df)

    return {
        "activos": r1,
        "repetidos": r2,
        "por_estado": r3,
        "por_rol": r4,
        "por_mes": r5,
        "rutas": [p1, p2, p3, p4, p5],
    }


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ruta_arg = sys.argv[1] if len(sys.argv) > 1 else None
    ejecutar_consultas(ruta_entrada=ruta_arg)
