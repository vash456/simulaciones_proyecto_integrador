"""
Punto de entrada principal del pipeline completo del proyecto integrador.

Ejecuta en orden los cuatro pipelines de simulacion disponibles:
  - Pipeline 1: `personajes`          (HU F01, X01, L01, Q01, G01)
  - Pipeline 2: `transacciones_gemas` (HU HI-5, HI-7, HI-8, HI-9, HI-10)
  - Pipeline 3: `usuarios`            (HU F01, X01, L01, Q01, G01)
  - Pipeline 4: `pagos`               (HU F01, X01, L01, Q01, G01)
"""
import os
import sys
from pathlib import Path

NOTEBOOK_DIR = Path(__file__).resolve().parent
if str(NOTEBOOK_DIR) not in sys.path:
    sys.path.insert(0, str(NOTEBOOK_DIR))

# --- Pipeline 1: personajes
from consultas.consultas_personajes import ejecutar_consultas as ejecutar_consultas_personajes
from exportaciones.exportar_personajes import exportar as exportar_personajes
from limpieza.limpiar_personajes import ejecutar_limpieza as ejecutar_limpieza_personajes
from reportes.reporte_personajes import generar_reporte as generar_reporte_personajes
from simulaciones.simular_personajes import generar_personajes

# --- Pipeline 2: transacciones_gemas
from consultas.consultas_transacciones_gemas import ejecutar_consultas as ejecutar_consultas_gemas
from exportaciones.exportar_transacciones_gemas import exportar as exportar_gemas
from limpieza.limpiar_transacciones_gemas import ejecutar_limpieza as ejecutar_limpieza_gemas
from reportes.reporte_transacciones_gemas import generar_reporte as generar_reporte_gemas
from simulaciones.simular_transacciones_gemas import generar_transacciones_gemas

# --- Pipeline 3: usuarios
from consultas.consultas_usuarios import ejecutar_consultas as ejecutar_consultas_usuarios
from exportaciones.exportar_usuarios import exportar_usuarios
from limpieza.limpiar_usuarios import limpiar_usuarios
from reportes.reporte_usuarios import generar_reporte as generar_reporte_usuarios
from simulaciones.simular_usuarios import generar_usuarios

# --- Pipeline 4: pagos
from consultas.consultas_pagos import ejecutar_consultas as ejecutar_consultas_pagos
from exportaciones.exportar_pagos import exportar_pagos
from limpieza.limpiar_pagos import ejecutar_limpieza as ejecutar_limpieza_pagos
from reportes.reporte_pagos import generar_reporte as generar_reporte_pagos
from simulaciones.simular_pagos import generar_pagos

SEPARADOR = "=" * 70


def ejecutar_pipeline_personajes():
    """Ejecuta simulacion, exportacion, limpieza, consultas y reporte de `personajes`."""
    print(f"\n{SEPARADOR}")
    print("  PIPELINE 1 - TABLA: personajes")
    print(SEPARADOR)

    print("\n1. Simulando tabla `personajes`...")
    df_sucio = generar_personajes()
    print(f"   Shape generado: {df_sucio.shape}\n")

    print("2. Exportando archivos sucios a data/crudo/...")
    rutas = exportar_personajes(df_sucio)
    for ruta in rutas:
        print(f"   - {ruta} ({os.path.getsize(ruta)} bytes)")

    print("\n3. Limpiando datos hacia data/limpio/...")
    df_limpio = ejecutar_limpieza_personajes()
    print(f"   Shape limpio final: {df_limpio.shape}\n")

    print("4. Ejecutando consultas sobre data/limpio/personajes_limpio.csv...")
    resultados = ejecutar_consultas_personajes()
    print(f"   Consultas completadas: {len(resultados)}\n")

    print("5. Generando graficas y conclusiones en reportes/...")
    generar_reporte_personajes()

    print(f"\n[OK] Pipeline `personajes` completado exitosamente.\n")


def ejecutar_pipeline_transacciones_gemas():
    """Ejecuta simulacion, exportacion, limpieza, consultas y reporte de `transacciones_gemas`."""
    print(f"\n{SEPARADOR}")
    print("  PIPELINE 2 - TABLA: transacciones_gemas")
    print(SEPARADOR)

    print("\n1. Simulando tabla `transacciones_gemas` (800 filas + 5% duplicados)...")
    df_sucio = generar_transacciones_gemas(800)
    print(f"   Shape generado: {df_sucio.shape}\n")

    print("2. Exportando archivos sucios a data/crudo/...")
    rutas = exportar_gemas(df_sucio)
    for ruta in rutas:
        print(f"   - {ruta} ({os.path.getsize(ruta)} bytes)")

    print("\n3. Limpiando datos hacia data/limpio/...")
    df_limpio = ejecutar_limpieza_gemas()
    print(f"   Shape limpio final: {df_limpio.shape}\n")

    print("4. Ejecutando consultas sobre data/limpio/transacciones_gemas_limpio.csv...")
    resultados = ejecutar_consultas_gemas(df_limpio)
    print(f"   Consultas completadas: {len(resultados)}\n")

    print("5. Generando graficas y conclusiones en reportes/...")
    generar_reporte_gemas(df_limpio)

    print(f"\n[OK] Pipeline `transacciones_gemas` completado exitosamente.\n")


def ejecutar_pipeline_usuarios():
    """Ejecuta simulacion, exportacion, limpieza, consultas y reporte de `usuarios`."""
    print(f"\n{SEPARADOR}")
    print("  PIPELINE 3 - TABLA: usuarios")
    print(SEPARADOR)

    print("\n1. Simulando tabla `usuarios` (HU F01)...")
    df_usuarios = generar_usuarios()
    print(f"   Shape generado: {df_usuarios.shape}")
    print(df_usuarios.head())
    print("\n   Nulos por columna:")
    print(df_usuarios.isna().sum())

    print("\n2. Exportando archivos sucios a data/crudo/ (HU X01)...")
    rutas = exportar_usuarios(df_usuarios)
    for formato, ruta in rutas.items():
        print(f"   - {formato.upper()}: {ruta} ({os.path.getsize(ruta)} bytes)")

    print("\n3. Limpiando datos hacia data/limpio/ (HU L01)...")
    df_limpio, ruta_limpio = limpiar_usuarios(ruta_entrada=rutas["csv"])

    print("\n4. Ejecutando consultas sobre data/limpio/usuarios_limpio.csv (HU Q01)...")
    resultados_consultas = ejecutar_consultas_usuarios(ruta_entrada=ruta_limpio)
    print(f"   Consultas completadas: {len(resultados_consultas['rutas'])}")

    print("\n5. Generando graficas y conclusiones en reportes/ (HU G01)...")
    rutas_graficas = generar_reporte_usuarios(ruta_entrada=ruta_limpio)
    print(f"   Graficas generadas: {len(rutas_graficas)}")

    print(f"\n[OK] Pipeline `usuarios` completado exitosamente.\n")


def ejecutar_pipeline_pagos():
    """Ejecuta simulacion, exportacion, limpieza, consultas y reporte de `pagos`."""
    print(f"\n{SEPARADOR}")
    print("  PIPELINE 4 - TABLA: pagos")
    print(SEPARADOR)

    print("\n1. Simulando tabla `pagos`...")
    df_pagos_sucio = generar_pagos()
    print(f"   Shape generado: {df_pagos_sucio.shape}\n")

    print("2. Exportando archivos sucios a data/crudo/...")
    rutas_pagos = exportar_pagos(df_pagos_sucio)
    for ruta in rutas_pagos:
        print(f"   - {ruta} ({os.path.getsize(ruta)} bytes)")

    print("\n3. Limpiando datos hacia data/limpio/...")
    df_pagos_limpio = ejecutar_limpieza_pagos()
    print(f"   Shape limpio final: {df_pagos_limpio.shape}\n")

    print("4. Ejecutando consultas sobre data/limpio/pagos_limpio.csv...")
    resultados_pagos = ejecutar_consultas_pagos()
    print(f"   Consultas completadas: {len(resultados_pagos)}\n")

    print("5. Generando graficas y conclusiones en reportes/...")
    generar_reporte_pagos()

    print(f"\n[OK] Pipeline `pagos` completado exitosamente.\n")


def main():
    """Ejecuta en secuencia los cuatro pipelines completos del proyecto integrador."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print(SEPARADOR)
    print("  PROYECTO INTEGRADOR - PIPELINE COMPLETO")
    print(SEPARADOR)

    ejecutar_pipeline_personajes()
    ejecutar_pipeline_transacciones_gemas()
    ejecutar_pipeline_usuarios()
    ejecutar_pipeline_pagos()

    print(SEPARADOR)
    print("  [OK] TODOS LOS PIPELINES COMPLETADOS EXITOSAMENTE")
    print(SEPARADOR + "\n")


if __name__ == "__main__":
    main()
