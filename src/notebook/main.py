"""Punto de entrada principal de los pipelines de `personajes` y `usuarios`."""
import os
import sys
from pathlib import Path

NOTEBOOK_DIR = Path(__file__).resolve().parent
if str(NOTEBOOK_DIR) not in sys.path:
    sys.path.insert(0, str(NOTEBOOK_DIR))

from consultas.consultas_personajes import ejecutar_consultas as ejecutar_consultas_personajes
from consultas.consultas_usuarios import ejecutar_consultas as ejecutar_consultas_usuarios
from exportaciones.exportar_personajes import exportar as exportar_personajes
from exportaciones.exportar_usuarios import exportar_usuarios
from limpieza.limpiar_personajes import ejecutar_limpieza as ejecutar_limpieza_personajes
from limpieza.limpiar_usuarios import limpiar_usuarios
from reportes.reporte_personajes import generar_reporte as generar_reporte_personajes
from reportes.reporte_usuarios import generar_reporte as generar_reporte_usuarios
from simulaciones.simular_personajes import generar_personajes
from simulaciones.simular_usuarios import generar_usuarios


def ejecutar_pipeline_personajes():
    """Ejecuta simulacion, exportacion, limpieza, consultas y reporte de `personajes`."""
    print("============================================================")
    print("PIPELINE 1: TABLA `personajes`")
    print("============================================================")

    print("1. Simulando tabla `personajes`...")
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


def ejecutar_pipeline_usuarios():
    """Ejecuta simulacion, exportacion, limpieza, consultas y reporte de `usuarios`."""
    print("\n============================================================")
    print("PIPELINE 2: TABLA `usuarios`")
    print("============================================================")

    print("1. Simulando tabla `usuarios` (HU F01)...")
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


def main():
    """Ejecuta en secuencia los pipelines completos de `personajes` y `usuarios`."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    ejecutar_pipeline_personajes()
    ejecutar_pipeline_usuarios()


if __name__ == "__main__":
    main()
