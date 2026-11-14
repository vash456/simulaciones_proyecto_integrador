HU simulacion
Criterios de aceptación

Ubicación y ejecución:
 El script src/simular_personajes.py existe y corre con python src/simular_personajes.py sin errores.

Constantes declaradas al inicio:
 Se definen listas para las claves foráneas e índices categóricos observables en el esquema:

IDS_CATEGORIA: lista de IDs de categoría (ej. [1, 2, 3, 4, 5]).

IDS_CREADOR: lista de IDs de creadores (ej. [101, 102, 103, 104, 105]).

IDS_MODERADOR: lista de IDs de moderadores (ej. [1, 2, 3]).

ESTADOS_MODERACION: lista de estados (ej. ['pendiente', 'aprobado', 'rechazado']).

CLASIFICACIONES_CONTENIDO: clasificaciones (ej. ['todo_publico', 'adolescentes', 'adultos']).

GENEROS: opciones de género (ej. ['masculino', 'femenino', 'no_binario', 'otro']).

MODOS_ANIMACION_PORTADA: opciones del modo de animación (ej. ['estatico', 'hover', 'bucle'], predeterminado 'estatico').

Estructura exacta de 800 filas y 24 columnas:
 Se generan 800 filas cubriendo estrictamente los tipos de datos observados:

id_personaje: int(11) autoincremental / secuencial (1 a 800).

cid: varchar(20) alfanumérico único (longitud ≤20\le 20≤20, ej. fake.lexify(text='cid-????????')).

id_categoria: int(11) generado con random.choice(IDS_CATEGORIA) o None.

id_creador: int(11) generado con random.choice(IDS_CREADOR) o None.

nombre: varchar(100) generado con fake.first_name().

descripcion_corta: text generado con fake.sentence(nb_words=10) o None.

avatar_url: varchar(255) generado con fake.image_url() o None.

publico: tinyint(1) con valor 1 por defecto o random.choice([0, 1]).

clasificacion_contenido: varchar(255) generado con random.choice(CLASIFICACIONES_CONTENIDO).

estado_moderacion: varchar(255) generado con random.choice(ESTADOS_MODERACION).

motivo_rechazo: text generado con fake.sentence(nb_words=6) si fue rechazado, caso contrario None.

id_moderador: int(11) generado con random.choice(IDS_MODERADOR) si fue moderado, o None.

fecha_moderacion: datetime generado con fake.date_time_between(start_date="-6m", end_date="now") o None.

destacado: tinyint(1) con valor 0 por defecto o random.choice([0, 1]).

orden_destacado: int(11) con número entero si es destacado, o None.

version: int(11) con valor entero (0 por defecto).

fecha_creacion: datetime generado con fake.date_time_between(start_date="-1y", end_date="now").

es_oficial: bit(1) generado con random.choice([0, 1]).

genero: varchar(30) generado con random.choice(GENEROS) o None.

tags: text generado con etiquetas separadas por comas (ej. ", ".join(fake.words(nb=3))) o None.

fecha_eliminacion: datetime (None para personajes activos).

motivo_eliminacion: varchar(255) (None para personajes activos).

modo_animacion_portada: varchar(30) con 'estatico' por defecto o random.choice(MODOS_ANIMACION_PORTADA).

avatar_animado_url: varchar(500) generado con fake.image_url() o None.

Reproducibilidad:
 La semilla está fija: Faker.seed(42) y random.seed(42).

Reglas para ensuciar datos a propósito:

Fechas mezcladas: En fecha_creacion, alternar dos formatos: "2026-03-15 14:30:00" y "15/03/2026 14:30".

Nulos inducidos: Forzar un 20% de valores None en descripcion_corta y un 10% en avatar_url.

Variantes de texto y espacios: En estado_moderacion y nombre, introducir variantes como ' APROBADO ', 'pendiente ', 'RECHAZADO' y espacios en blanco al inicio o al final.

Clave única duplicada: 10% de registros con el identificador cid duplicado (o par repetido id_creador + nombre) para simular violación de unicidad.

Duplicados exactos: 5% de las filas duplicadas tal cual (filas completas repetidas).

Estructura modular:
 Todo se implementa en una función generar_personajes(n=800) que devuelve el DataFrame (return df), permitiendo su reutilización en pipelines de exportación o limpieza.

Salida de verificación:
 El bloque if __name__ == "__main__": únicamente imprime df.shape, df.head() y df.isna().sum().

HU Exportacion
Criterios de aceptación

El script src/exportar_personajes.py existe y corre sin errores con python src/exportar_personajes.py.

Importa la función del script anterior (from importlib import import_module o importando el módulo simular_personajes) y NO vuelve a copiar el código de generación.

Genera data/crudo/personajes_sucio.csv con df.to_csv(ruta, index=False, encoding="utf-8").

Genera data/crudo/personajes_sucio.xlsx con df.to_excel(ruta, index=False, sheet_name="personajes").

Genera data/crudo/personajes_sucio.json con df.to_json(ruta, orient="records", force_ascii=False, indent=2).

La carpeta se crea sola si no existe: os.makedirs("data/crudo", exist_ok=True).

Al final el script imprime la ruta y el tamaño (df.shape) de cada archivo generado.

requirements.txt incluye: pandas (versión 2.x), faker, openpyxl y matplotlib.

Los tres archivos quedan versionados en Git o, si pesan mucho, se documenta en el README cómo generarlos.
