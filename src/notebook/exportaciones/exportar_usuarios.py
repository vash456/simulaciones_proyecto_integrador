import os
import sys
from importlib import import_module
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[3]
RUTA_NOTEBOOK = Path(__file__).resolve().parents[1]
if str(RUTA_NOTEBOOK) not in sys.path:
    sys.path.insert(0, str(RUTA_NOTEBOOK))

generar_usuarios = import_module("simulaciones.simular_usuarios").generar_usuarios


def exportar_usuarios(df=None):
    """Exporta el DataFrame de usuarios sucios a CSV, Excel y JSON en data/crudo/."""
    if df is None:
        df = generar_usuarios()

    carpeta_crudo = RAIZ_PROYECTO / "data" / "crudo"
    os.makedirs(carpeta_crudo, exist_ok=True)

    ruta_csv = carpeta_crudo / "usuarios_sucio.csv"
    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    print(f"{ruta_csv} -> {df.shape}")

    ruta_xlsx = carpeta_crudo / "usuarios_sucio.xlsx"
    df.to_excel(ruta_xlsx, index=False, sheet_name="usuarios")
    print(f"{ruta_xlsx} -> {df.shape}")

    ruta_json = carpeta_crudo / "usuarios_sucio.json"
    df.to_json(ruta_json, orient="records", force_ascii=False, indent=2)
    print(f"{ruta_json} -> {df.shape}")

    return {
        "csv": ruta_csv,
        "xlsx": ruta_xlsx,
        "json": ruta_json,
    }


if __name__ == "__main__":
    exportar_usuarios()
