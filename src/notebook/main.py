"""
Punto de entrada principal del pipeline completo del proyecto integrador.

Ejecuta en orden los dos pipelines de simulacion disponibles:
  - Pipeline 1: `personajes`         (tablas F01, X01, L01, Q01, G01)
  - Pipeline 2: `transacciones_gemas` (tablas HI-5, HI-7, HI-8, HI-9, HI-10)
"""
import os
import sys
from pathlib import Path

NOTEBOOK_DIR = Path(__file__).resolve().parent
if str(NOTEBOOK_DIR) not in sys.path:
    sys.path.insert(0, str(NOTEBOOK_DIR))

# ── Módulos Pipeline 1: personajes ──────────────────────────────────────────
from consultas.consultas_personajes import ejecutar_consultas
from exportaciones.exportar_personajes import exportar
from limpieza.limpiar_personajes import ejecutar_limpieza
from reportes.reporte_personajes import generar_reporte
from simulaciones.simular_personajes import generar_personajes

# ── Módulos Pipeline 2: transacciones_gemas ─────────────────────────────────
from exportaciones.exportar_transacciones_gemas import exportar as exportar_gemas
from limpieza.limpiar_transacciones_gemas import ejecutar_limpieza as ejecutar_limpieza_gemas
from consultas.consultas_transacciones_gemas import ejecutar_consultas as ejecutar_consultas_gemas
from reportes.reporte_transacciones_gemas import generar_reporte as generar_reporte_gemas
from simulaciones.simular_transacciones_gemas import generar_transacciones_gemas


SEPARADOR = "=" * 70


def pipeline_personajes():
    """Ejecuta simulacion, exportacion, limpieza, consultas y reporte de `personajes`."""
    print(f"\n{SEPARADOR}")
    print("  PIPELINE 1 — TABLA: personajes")
    print(SEPARADOR)

    print("\n1. Simulando tabla `personajes`...")
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
    print(f"   Consultas completadas: {len(resultados)}\n")

    print("5. Generando graficas y conclusiones en reportes/...")
    generar_reporte()

    print(f"\n[✓] Pipeline `personajes` completado exitosamente.\n")


def pipeline_transacciones_gemas():
    """Ejecuta simulacion, exportacion, limpieza, consultas y reporte de `transacciones_gemas`."""
    print(f"\n{SEPARADOR}")
    print("  PIPELINE 2 — TABLA: transacciones_gemas")
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

    print(f"\n[✓] Pipeline `transacciones_gemas` completado exitosamente.\n")


def main():
    """Ejecuta todos los pipelines del proyecto integrador en orden."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print(SEPARADOR)
    print("  PROYECTO INTEGRADOR — PIPELINE COMPLETO")
    print(SEPARADOR)

    pipeline_personajes()
    pipeline_transacciones_gemas()

    print(SEPARADOR)
    print("  [✓] TODOS LOS PIPELINES COMPLETADOS EXITOSAMENTE")
    print(SEPARADOR + "\n")


if __name__ == "__main__":
    main()
