# Proyecto Integrador — Simulación y Análisis (`personajes` y `usuarios`)

Pipeline en Python para simular datos sucios de las tablas `personajes` (24 columnas) y `usuarios` (25 columnas) con `Faker("es_CO")`, exportarlos en múltiples formatos, limpiarlos con `pandas`, responder consultas analíticas y generar reportes gráficos con `matplotlib`.

---

## Estructura del proyecto

```text
simulaciones_proyecto_integrador/
├── .agents/skills/                         # Skills locales instaladas para el workspace
├── data/
│   ├── crudo/                              # Datos sucios generados (CSV, XLSX, JSON)
│   │   ├── personajes_sucio.{csv,xlsx,json}
│   │   └── usuarios_sucio.{csv,xlsx,json}
│   └── limpio/                             # Datos limpios y resultados de consultas
│       ├── personajes_limpio.csv
│       ├── personajes_consulta_1..5.csv
│       ├── usuarios_limpio.csv
│       └── usuarios_consulta_1..5.csv
├── reportes/                               # Gráficas generadas (PNG, 120 dpi)
│   ├── personajes_grafica_1..3.png
│   └── usuarios_grafica_1..3.png
├── src/
│   └── notebook/
│       ├── main.py                         # Ejecuta los pipelines de personajes y usuarios
│       ├── simulaciones/
│       │   ├── simular_personajes.py
│       │   └── simular_usuarios.py
│       ├── exportaciones/
│       │   ├── exportar_personajes.py
│       │   └── exportar_usuarios.py
│       ├── limpieza/
│       │   ├── limpiar_personajes.py
│       │   └── limpiar_usuarios.py
│       ├── consultas/
│       │   ├── consultas_personajes.py
│       │   └── consultas_usuarios.py
│       └── reportes/
│           ├── reporte_personajes.py
│           └── reporte_usuarios.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Requisitos e instalación

Dependencias declaradas en `requirements.txt` (`pandas>=2,<3`, `faker`, `openpyxl`, `matplotlib`):

En PowerShell, desde la raíz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Cómo ejecutar

### Pipeline completo (recomendado)

Ejecuta en secuencia las 5 etapas para `personajes` y luego para `usuarios`:

```powershell
python src/notebook/main.py
```

### Ejecución por etapas (individual)

Cada módulo puede ejecutarse de forma independiente desde la raíz del repositorio:

#### Tabla `personajes`
```powershell
python src/notebook/simulaciones/simular_personajes.py
python src/notebook/exportaciones/exportar_personajes.py
python src/notebook/limpieza/limpiar_personajes.py
python src/notebook/consultas/consultas_personajes.py
python src/notebook/reportes/reporte_personajes.py
```

#### Tabla `usuarios`
```powershell
python src/notebook/simulaciones/simular_usuarios.py
python src/notebook/exportaciones/exportar_usuarios.py
python src/notebook/limpieza/limpiar_usuarios.py
python src/notebook/consultas/consultas_usuarios.py
python src/notebook/reportes/reporte_usuarios.py
```

---

## Resumen de etapas

### 1. Tabla `personajes`
1. **Simulación (`simular_personajes.py`):** genera `800` registros base con 24 columnas usando semilla `42` (`840` filas con 5 % de duplicados exactos).
2. **Exportación (`exportar_personajes.py`):** exporta `personajes_sucio.{csv,xlsx,json}` en `data/crudo/`.
3. **Limpieza (`limpiar_personajes.py`):** elimina duplicados exactos y `cid` repetidos, unifica fechas/textos, rellena nulos y genera `data/limpio/personajes_limpio.csv` (`725` filas, `25` columnas).
4. **Consultas (`consultas_personajes.py`):** responde 5 consultas (2 con `groupby`) y guarda `personajes_consulta_1..5.csv`.
5. **Reportes (`reporte_personajes.py`):** genera 3 gráficas PNG en `reportes/` e imprime conclusiones.

### 2. Tabla `usuarios`
1. **Simulación (`simular_usuarios.py`):** genera `800` filas con 25 columnas usando `Faker.seed(42)` y `random.seed(42)`, con fechas mezcladas, ~20 % de nulos en `motivo_eliminacion`, variantes en `estado`, ~10 % de `correo` repetido con mayúsculas/espacios y 5 % de duplicados exactos.
2. **Exportación (`exportar_usuarios.py`):** importa `generar_usuarios()` y genera `usuarios_sucio.csv`, `usuarios_sucio.xlsx` (hoja `usuarios`) y `usuarios_sucio.json` en `data/crudo/`.
3. **Limpieza (`limpiar_usuarios.py`):** elimina duplicados exactos y correos duplicados normalizados, unifica `fecha_registro` y `estado`, rellena `motivo_eliminacion` con `"Sin motivo"`, crea `mes` y exporta `data/limpio/usuarios_limpio.csv` (`681` filas, `26` columnas).
4. **Consultas (`consultas_usuarios.py`):** responde 5 consultas (incluyendo `groupby` por `rol` y por `mes`) y guarda `usuarios_consulta_1..5.csv`.
5. **Reportes (`reporte_usuarios.py`):** genera `usuarios_grafica_1..3.png` en `reportes/` e imprime las conclusiones sobre rol mayoritario, mes pico y validación `409 Conflict` para correos duplicados.
