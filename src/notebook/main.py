"""Punto de entrada principal del pipeline completo de `personajes` y `pagos`."""
import os
import sys
from pathlib import Path

NOTEBOOK_DIR = Path(__file__).resolve().parent
if str(NOTEBOOK_DIR) not in sys.path:
    sys.path.insert(0, str(NOTEBOOK_DIR))

# --- Pipeline personajes
from consultas.consultas_personajes import ejecutar_consultas
from exportaciones.exportar_personajes import exportar
from limpieza.limpiar_personajes import ejecutar_limpieza
from reportes.reporte_personajes import generar_reporte
from simulaciones.simular_personajes import generar_personajes

# --- Pipeline pagos
from consultas.consultas_pagos import ejecutar_consultas as ejecutar_consultas_pagos
from exportaciones.exportar_pagos import exportar_pagos
from limpieza.limpiar_pagos import ejecutar_limpieza as ejecutar_limpieza_pagos
from reportes.reporte_pagos import generar_reporte as generar_reporte_pagos
from simulaciones.simular_pagos import generar_pagos


def main():
    """Ejecuta simulacion, exportacion, limpieza, consultas y reporte grafico."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # ================================================================
    # PIPELINE 1: personajes
    # ================================================================
    print("=" * 60)
    print("PIPELINE 1: personajes")
    print("=" * 60)

    print("1. Simulando tabla `personajes`...")
    df_sucio = generar_personajes()
    print(f"   Shape generado: {df_sucio.shape}\n")

    print("2. Exportando archivos sucios a data/crudo/...")
    rutas = exportar(df_sucio)
    for ruta in rutas:
        print(f"   - {ruta} ({os.path.getsize(ruta)} bytes)")

    print("\n3. Limpiando datos hacia data/limpio/...")
    df_limpio = ejecutar_limpieza()
    print(f"   Shape limpio final: {df_limpio.shape}\n")

    print("4. Ejecutando consultas sobre data/limpio/personajes_limpio.csv...")
    resultados = ejecutar_consultas()
    print(f"Consultas completadas: {len(resultados)}\n")

    print("5. Generando graficas y conclusiones en reportes/...")
    generar_reporte()

    # ================================================================
    # PIPELINE 2: pagos
    # ================================================================
    print("\n" + "=" * 60)
    print("PIPELINE 2: pagos")
    print("=" * 60)

    print("1. Simulando tabla `pagos`...")
    df_pagos_sucio = generar_pagos()
    print(f"   Shape generado: {df_pagos_sucio.shape}\n")

    print("2. Exportando archivos sucios de pagos a data/crudo/...")
    rutas_pagos = exportar_pagos(df_pagos_sucio)
    for ruta in rutas_pagos:
        print(f"   - {ruta} ({os.path.getsize(ruta)} bytes)")

    print("\n3. Limpiando datos de pagos hacia data/limpio/...")
    df_pagos_limpio = ejecutar_limpieza_pagos()
    print(f"   Shape limpio final: {df_pagos_limpio.shape}\n")

    print("4. Ejecutando consultas sobre data/limpio/pagos_limpio.csv...")
    resultados_pagos = ejecutar_consultas_pagos()
    print(f"Consultas completadas: {len(resultados_pagos)}\n")

    print("5. Generando graficas y conclusiones de pagos en reportes/...")
    generar_reporte_pagos()


if __name__ == "__main__":
    main()
