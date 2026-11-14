import sys
from pathlib import Path

import pandas as pd

RAIZ_PROYECTO = Path(__file__).resolve().parents[3]
RUTA_ENTRADA_DEFECTO = RAIZ_PROYECTO / "data" / "crudo" / "usuarios_sucio.csv"
RUTA_SALIDA_DEFECTO = RAIZ_PROYECTO / "data" / "limpio" / "usuarios_limpio.csv"

COLUMNAS_OBLIGATORIAS = [
    "id_usuario", "uid", "nombre_usuario", "correo", "proveedor_auth",
    "id_plan", "edad_verificada", "terminos_aceptados", "amatistas_saldo",
    "estado", "intentos_fallidos", "debe_cambiar_password", "token_version", "rol",
]


def mostrar_diagnostico(df, titulo, completo=True):
    """Imprime el diagnostico del DataFrame (shape, info, nulos y duplicados)."""
    print(f"\n--- {titulo} ---")
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

    # 1. Quitar duplicados exactos
    df = df.drop_duplicates()

    # 2. Unificar formato de fecha_registro (ISO y latino)
    df["fecha_registro"] = pd.to_datetime(
        df["fecha_registro"], format="mixed", dayfirst=True, errors="coerce"
    )

    # 3. Unificar formato de estado
    df["estado"] = df["estado"].str.strip().str.upper().str.replace(" ", "_")

    # 4. Rellenar motivos de eliminacion vacios
    df["motivo_eliminacion"] = df["motivo_eliminacion"].fillna("Sin motivo")

    # 5. Normalizar correo, detectar repetidos y dejar solo el primer registro
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


def limpiar_usuarios(ruta_entrada=None, ruta_salida=None):
    """Lee el CSV crudo, imprime diagnosticos, limpia segun HU L01 y guarda el CSV limpio."""
    entrada = Path(ruta_entrada) if ruta_entrada else RUTA_ENTRADA_DEFECTO
    salida = Path(ruta_salida) if ruta_salida else RUTA_SALIDA_DEFECTO

    if not entrada.is_file():
        raise FileNotFoundError(f"No existe el archivo de entrada: {entrada}")

    df_sucio = pd.read_csv(entrada)
    filas_iniciales = len(df_sucio)
    mostrar_diagnostico(df_sucio, "DIAGNOSTICO INICIAL (ANTES DE LIMPIAR)", completo=True)

    df_limpio = limpiar_datos(df_sucio)
    filas_eliminadas = filas_iniciales - len(df_limpio)

    mostrar_diagnostico(df_limpio, "DIAGNOSTICO FINAL (DESPUES DE LIMPIAR)", completo=False)
    print(f"\nFilas eliminadas en total: {filas_eliminadas}")
    verificar_post_limpieza(df_limpio)

    salida.parent.mkdir(parents=True, exist_ok=True)
    df_limpio.to_csv(salida, index=False, encoding="utf-8")
    print(f"\nArchivo limpio guardado en: {salida}")

    return df_limpio, salida


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ruta_arg = sys.argv[1] if len(sys.argv) > 1 else None
    limpiar_usuarios(ruta_entrada=ruta_arg)
