# Criterios de Aceptación: Transacciones de Gemas

## HU HI-5 Simular 800 filas de transacciones_gemas con Faker y ensuciarlas a propósito

### Criterios de Aceptación:
- **Ejecución del script**: El script `src/notebook/simulaciones/simular_transacciones_gemas.py` existe y se ejecuta sin errores de sintaxis o runtime.
- **Constantes del dominio**: Se declaran `MOTIVOS` e `IDS_USUARIO = [1, 2, 3, 4, 5, 6, 7, 8, 9]` al inicio del archivo.
- **Estructura de columnas**: Se generan 800 filas con las columnas: `id_transaccion`, `id_usuario`, `cantidad`, `motivo`, `id_referencia`, `fecha`.
- **Lógica de generación limpia base**: `id_transaccion` correlativo 1..N; `id_usuario` con `random.choice(IDS_USUARIO)`; `motivo` con `random.choice(MOTIVOS)`; `cantidad` coherente con el motivo; `id_referencia` entero o None; `fecha` datetime.
- **Ensuciamiento controlado de `motivo`**: Al menos el 8% en mayúsculas, el 8% con espacios extra, el 6% capitalize; el resto en minúsculas limpias.
- **Ensuciamiento de `id_referencia`**: Al menos 25% de nulos y hasta 5% con strings con espacios.
- **Ensuciamiento de `fecha`**: Mezcla de al menos dos formatos (`%Y-%m-%d %H:%M:%S` y `%d/%m/%Y %H:%M`).
- **Duplicados exactos**: Se añade ~5% de filas duplicadas íntegramente al final, resultando en 840 filas.
- **Semilla reproducible**: `random.seed(42)` y `Faker.seed(42)`.

## HU HI-7 Exportar los datos sucios de transacciones_gemas a CSV, Excel y JSON

### Criterios de Aceptación:
- **Ejecución del script**: El script `src/notebook/exportaciones/exportar_transacciones_gemas.py` existe y se ejecuta sin errores.
- **Exportación a CSV**: Guarda `data/crudo/transacciones_gemas_sucio.csv` con `df.to_csv(..., index=False, encoding="utf-8")`.
- **Exportación a Excel**: Guarda `data/crudo/transacciones_gemas_sucio.xlsx` con `df.to_excel(..., index=False, sheet_name="transacciones_gemas")`.
- **Exportación a JSON**: Guarda `data/crudo/transacciones_gemas_sucio.json` con `df.to_json(..., orient="records", force_ascii=False, indent=2)`.
- **Creación de carpeta**: Asegura `data/crudo/` con `os.makedirs(..., exist_ok=True)`.
- **Trazabilidad**: Imprime en consola la ruta y dimensiones de cada archivo generado.

## HU HI-8 Limpiar los datos de transacciones_gemas con pandas

### Criterios de Aceptación:
- **Ejecución del script**: El script `src/notebook/limpieza/limpiar_transacciones_gemas.py` existe y se ejecuta sin errores.
- **Carga de datos crudos**: Carga `data/crudo/transacciones_gemas_sucio.csv` con `pd.read_csv()`.
- **Diagnóstico inicial**: Imprime `df.shape`, `df.info()`, `df.isna().sum()`, `df.duplicated().sum()`.
- **Eliminación de duplicados exactos**: `df.drop_duplicates()`.
- **Estandarización de fechas**: `pd.to_datetime(df["fecha"], format="mixed", dayfirst=True, errors="coerce")`.
- **Normalización del motivo (ENUM)**: `df["motivo"].str.strip().str.lower().str.replace(" ", "_")`.
- **Corrección lógica de cantidad**: Débitos de `gasto_mensaje` negativos; créditos de los demás motivos positivos.
- **Tratamiento de `id_referencia`**: `pd.to_numeric(..., errors="coerce").astype("Int64")`.
- **Unicidad de clave primaria**: `df.drop_duplicates(subset=["id_transaccion"], keep="first")`.
- **Ingeniería temporal**: `df["mes"] = df["fecha"].dt.to_period("M").astype(str)`.
- **Tipo de movimiento**: `df["tipo_movimiento"]` con valores `"ingreso"` o `"gasto"` según el signo de `cantidad`.
- **Exportación limpia**: Guarda en `data/limpio/transacciones_gemas_limpio.csv`.
- **Verificación final**: Imprime `df.shape`, `df.isna().sum()` y balance de filas removidas.

## HU HI-9 Cinco consultas sobre transacciones_gemas con pandas (incluye groupby)

### Criterios de Aceptación:
- **Ejecución del script**: El script `src/notebook/consultas/consultas_transacciones_gemas.py` existe y se ejecuta sin errores.
- **Insumo limpio**: Lee exclusivamente `data/limpio/transacciones_gemas_limpio.csv`.
- **Consulta 1 — Recargas por compra**: Filtra `motivo == "compra"`.
- **Consulta 2 — Egresos por mensajes**: Filtra `motivo == "gasto_mensaje"`.
- **Consulta 3 — Conteo por motivo**: `df["motivo"].value_counts()`.
- **Consulta 4 — GROUPBY por usuario (Saldos)**: `df.groupby("id_usuario")["cantidad"].agg(saldo_acumulado="sum", ...)` ordenado descendentemente.
- **Consulta 5 — GROUPBY por mes (Flujo temporal)**: `df.groupby("mes")["cantidad"].agg(total_transacciones="count", balance_neto="sum")`.
- **Requisito de agregación**: Al menos 2 consultas usan `groupby()`.
- **Modularidad**: Cada consulta en función independiente con docstring en español.
- **Exportación analítica**: Genera `data/limpio/transacciones_gemas_consulta_1.csv` a `...consulta_5.csv`.

## HU HI-10 Tres gráficas y conclusiones de transacciones_gemas con matplotlib

### Criterios de Aceptación:
- **Ejecución del script**: El script `src/notebook/reportes/reporte_transacciones_gemas.py` existe y se ejecuta sin errores ni bloqueos interactivos.
- **Carga de datos**: Lee `data/limpio/transacciones_gemas_limpio.csv`.
- **Gráfica 1 — Barras (Frecuencia por motivo)**: Total de operaciones por tipo de movimiento; guardada en `reportes/transacciones_gemas_grafica_1.png`.
- **Gráfica 2 — Línea temporal (Actividad mensual)**: Transacciones por mes con `marker="o"`; guardada en `reportes/transacciones_gemas_grafica_2.png`.
- **Gráfica 3 — Barras horizontales (Saldos por usuario)**: Balance neto por `id_usuario` (1 al 9); guardada en `reportes/transacciones_gemas_grafica_3.png`.
- **Formato**: Cada figura tiene `plt.title()`, `plt.xlabel()`, `plt.ylabel()`, `plt.tight_layout()`, `plt.savefig(dpi=120)` y `plt.close()`.
- **Creación automática de carpeta**: `os.makedirs("reportes", exist_ok=True)`.
- **Conclusiones de negocio**: Imprime cuál es el motivo más recurrente, el mes pico y distribución de saldos con justificación de `@Transactional`.
- **Persistencia**: Las tres imágenes `.png` quedan en `reportes/`.
