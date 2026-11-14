"""HU HI-7: exporta el DataFrame sucio de `transacciones_gemas` a CSV, Excel y JSON en data/crudo/."""
import os
import sys
from importlib import import_module
from pathlib import Path

NOTEBOOK_DIR = Path(__file__).resolve().parents[1]   # src/notebook
RAIZ_PROYECTO = NOTEBOOK_DIR.parents[1]              # raiz del proyecto
if str(NOTEBOOK_DIR) not in sys.path:
    sys.path.insert(0, str(NOTEBOOK_DIR))

simular = import_module("simulaciones.simular_transacciones_gemas")

CARPETA = str(RAIZ_PROYECTO / "data" / "crudo")


def exportar(df, carpeta=CARPETA):
    """Guarda df en los tres formatos y devuelve la lista de rutas generadas."""
    os.makedirs(carpeta, exist_ok=True)
    ruta_csv = os.path.join(carpeta, "transacciones_gemas_sucio.csv")
    ruta_xlsx = os.path.join(carpeta, "transacciones_gemas_sucio.xlsx")
    ruta_json = os.path.join(carpeta, "transacciones_gemas_sucio.json")

    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    df.to_excel(ruta_xlsx, index=False, sheet_name="transacciones_gemas")
    df.to_json(ruta_json, orient="records", force_ascii=False, indent=2)

    return [ruta_csv, ruta_xlsx, ruta_json]


if __name__ == "__main__":
    datos = simular.generar_transacciones_gemas()
    for ruta in exportar(datos):
        print(f"{ruta} -> df.shape={datos.shape}, {os.path.getsize(ruta)} bytes")
