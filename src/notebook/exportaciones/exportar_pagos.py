"""HU P02: exporta el DataFrame sucio de `pagos` a CSV, Excel y JSON en data/crudo/."""
import os
import sys
from importlib import import_module
from pathlib import Path

NOTEBOOK_DIR = Path(__file__).resolve().parents[1]   # src/notebook
RAIZ_PROYECTO = NOTEBOOK_DIR.parents[1]              # raiz del proyecto
if str(NOTEBOOK_DIR) not in sys.path:
    sys.path.insert(0, str(NOTEBOOK_DIR))

simular = import_module("simulaciones.simular_pagos")  # no se duplica el codigo de generacion

CARPETA = str(RAIZ_PROYECTO / "data" / "crudo")


def exportar_pagos(df, carpeta=CARPETA):
    """Guarda df en CSV, Excel y JSON y devuelve la lista de rutas generadas."""
    os.makedirs(carpeta, exist_ok=True)

    ruta_csv  = os.path.join(carpeta, "pagos_sucio.csv")
    ruta_xlsx = os.path.join(carpeta, "pagos_sucio.xlsx")
    ruta_json = os.path.join(carpeta, "pagos_sucio.json")

    df.to_csv(ruta_csv,  index=False, encoding="utf-8")
    df.to_excel(ruta_xlsx, index=False, sheet_name="pagos")
    df.to_json(ruta_json,  orient="records", force_ascii=False, indent=2)

    rutas = [ruta_csv, ruta_xlsx, ruta_json]
    for ruta in rutas:
        print(f"   {ruta} -> shape={df.shape}, {os.path.getsize(ruta)} bytes")
    return rutas


if __name__ == "__main__":
    datos = simular.generar_pagos()
    exportar_pagos(datos)
