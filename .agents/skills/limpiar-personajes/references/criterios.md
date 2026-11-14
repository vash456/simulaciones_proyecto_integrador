hu limpieza
Criterios de aceptación

El script src/limpiar_personajes.py existe y corre sin errores.

Lee data/crudo/personajes_sucio.csv con pd.read_csv().

Al inicio imprime el diagnóstico: df.shape, df.info(), df.isna().sum() y df.duplicated().sum().

Quita los duplicados exactos con df.drop_duplicates().

Convierte la fecha de creación, aunque venga en dos formatos: df["fecha_creacion"] = pd.to_datetime(df["fecha_creacion"], format="mixed", dayfirst=True, errors="coerce").

Unifica el estado de moderación: df["estado_moderacion"] = df["estado_moderacion"].str.strip().str.upper().str.replace(" ", "_").

Quita los espacios sobrantes de nombre con df["nombre"] = df["nombre"].str.strip().

Rellena las descripciones vacías: df["descripcion_corta"] = df["descripcion_corta"].fillna("Sin descripcion").

Detecta los cid repetidos: repetidos = df[df.duplicated(subset=["cid"], keep=False)], e imprime cuántos son.

Deja solo la primera aparición de cada cid: df = df.drop_duplicates(subset=["cid"], keep="first").

Crea la columna mes para agrupar después: df["mes"] = df["fecha_creacion"].dt.to_period("M").

Al final vuelve a imprimir df.shape y df.isna().sum(), y muestra cuántas filas se eliminaron.

Guarda el resultado en data/limpio/personajes_limpio.csv con df.to_csv(ruta, index=False, encoding="utf-8").

Después de limpiar no queda ningún nulo en las columnas obligatorias ni ningún duplicado exacto.

Las columnas obligatorias son las que en la captura tienen Nulo = No: id_personaje, cid, nombre, publico, clasificacion_contenido, estado_moderacion, destacado, version, es_oficial y modo_animacion_portada.

Las demás columnas aceptan NULL en la tabla, así que pueden conservar nulos.