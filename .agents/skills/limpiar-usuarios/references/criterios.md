hu limpieza
Criterios de aceptación

El script src/limpiar_usuarios.py existe y corre sin errores.

Lee data/crudo/usuarios_sucio.csv con pd.read_csv().

Al inicio imprime el diagnóstico: df.shape, df.info(), df.isna().sum() y df.duplicated().sum().

Quitar los duplicados exactos con df.drop_duplicates().

Convertir la fecha (aunque venga en dos formatos): df["fecha_registro"] = pd.to_datetime(df["fecha_registro"], format="mixed", dayfirst=True, errors="coerce").

Unificar el estado: df["estado"] = df["estado"].str.strip().str.upper().str.replace(" ", "_").

Rellenar los motivos de eliminación vacíos: df["motivo_eliminacion"] = df["motivo_eliminacion"].fillna("Sin motivo").

Detectar los usuarios repetidos: repetidos = df[df.duplicated(subset=["correo"], keep=False)] e imprimir cuántos son.

Dejar solo el primer registro de cada correo: df = df.drop_duplicates(subset=["correo"], keep="first").

Crear la columna mes para agrupar después: df["mes"] = df["fecha_registro"].dt.to_period("M").

Al final vuelve a imprimir df.shape y df.isna().sum(), y muestra cuántas filas se eliminaron.

Guarda el resultado en data/limpio/usuarios_limpio.csv con df.to_csv(ruta, index=False, encoding="utf-8").

Después de limpiar no queda NINGÚN nulo en las columnas obligatorias ni ningún duplicado exacto.