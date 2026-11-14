# Proyecto Integrador — Simulación y Análisis de `personajes`

Pipeline en Python para simular datos sucios de la tabla `personajes` (24 columnas) con `Faker("es_CO")`, exportarlos en múltiples formatos, limpiarlos con `pandas`, responder consultas analíticas y generar reportes gráficos con `matplotlib`.

---

## Estructura del proyecto

```text
proyecto_integrador_simulaciones/
├── .agents/skills/                         # Skills locales instaladas para el workspace
├── data/
│   ├── crudo/                              # Datos sucios generados (CSV, XLSX, JSON)
│   │   ├── personajes_sucio.csv
│   │   ├── personajes_sucio.xlsx
│   │   └── personajes_sucio.json
│   └── limpio/                             # Datos limpios y resultados de consultas
│       ├── personajes_limpio.csv
│       └── personajes_consulta_1..5.csv
├── reportes/                               # Gráficas generadas (PNG, 120 dpi)
│   ├── personajes_grafica_1.png
│   ├── personajes_grafica_2.png
│   └── personajes_grafica_3.png
├── src/
│   └── notebook/
│       ├── main.py                         # Ejecuta las 5 etapas en orden
│       ├── simulaciones/
│       │   └── simular_personajes.py
│       ├── exportaciones/
│       │   └── exportar_personajes.py
│       ├── limpieza/
│       │   └── limpiar_personajes.py
│       ├── consultas/
│       │   └── consultas_personajes.py
│       └── reportes/
│           └── reporte_personajes.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Requisitos e instalación

Dependencias declaradas en `requirements.txt` (probado en Windows con Python `3.13.9` y `pandas` `2.3.3`):

- `pandas>=2,<3`
- `faker`
- `openpyxl`
- `matplotlib`

En PowerShell, desde la raíz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Cómo ejecutar

### Pipeline completo (recomendado)

Ejecuta en secuencia la simulación, exportación, limpieza, consultas y generación de gráficas:

```powershell
python src/notebook/main.py
```

### Ejecución por etapas (individual)

Cada módulo puede ejecutarse de forma independiente desde la raíz del repositorio:

```powershell
# 1. Simular 800 filas base (+ 5% duplicados exactos = 840) con semilla fija (42)
python src/notebook/simulaciones/simular_personajes.py

# 2. Exportar el DataFrame sucio a CSV, Excel (hoja 'personajes') y JSON en data/crudo/
python src/notebook/exportaciones/exportar_personajes.py

# 3. Limpiar data/crudo/personajes_sucio.csv y guardar data/limpio/personajes_limpio.csv
python src/notebook/limpieza/limpiar_personajes.py

# 4. Responder las 5 consultas sobre data/limpio/personajes_limpio.csv
python src/notebook/consultas/consultas_personajes.py

# 5. Generar las 3 gráficas en reportes/ e imprimir las conclusiones
python src/notebook/reportes/reporte_personajes.py
```

---

## Resumen de etapas

1. **Simulación (`simular_personajes.py`):** genera `800` registros base con las 24 columnas del esquema `personajes` usando `Faker.seed(42)` y `random.seed(42)`, e introduce suciedad controlada: fechas en formato ISO y `DD/MM/AAAA HH:MM`, `20%` de nulos en `descripcion_corta`, `10%` en `avatar_url`, espacios y mayúsculas mezcladas en `estado_moderacion` y `nombre`, `10%` de `cid` repetidos y `5%` de duplicados exactos (`840` filas en total).
2. **Exportación (`exportar_personajes.py`):** importa `generar_personajes()` y genera `personajes_sucio.csv`, `personajes_sucio.xlsx` y `personajes_sucio.json` dentro de `data/crudo/`.
3. **Limpieza (`limpiar_personajes.py`):** muestra diagnóstico antes y después (`shape`, `info`, nulos, duplicados), elimina `40` duplicados exactos y `75` filas excedentes por `cid` repetido, unifica `fecha_creacion` a `datetime`, normaliza `estado_moderacion` y `nombre`, rellena `descripcion_corta` con `"Sin descripcion"`, agrega la columna `mes` y exporta `data/limpio/personajes_limpio.csv` (`725` filas, `25` columnas, sin nulos en columnas obligatorias).
4. **Consultas (`consultas_personajes.py`):** responde 5 preguntas sobre los datos limpios (incluyendo 2 agrupaciones `groupby` por `id_categoria` y por `mes`) y guarda `personajes_consulta_1.csv` a `personajes_consulta_5.csv` en `data/limpio/`.
5. **Reportes (`reporte_personajes.py`):** genera 3 gráficas PNG en `reportes/` (`estado_moderacion`, creaciones por `mes` y top categorías) e imprime las conclusiones principales, incluyendo la justificación de la restricción `UNIQUE` sobre `cid`.
