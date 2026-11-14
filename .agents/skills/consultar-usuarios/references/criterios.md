hu consultas

Criterios de aceptación
El script src/consultas_usuarios.py existe y corre sin errores.

Lee data/limpio/usuarios_limpio.csv (el archivo LIMPIO, no el sucio).

Consulta 1 — Usuarios con estado activo: activos = df[df["estado"] == "ACTIVO"].

Consulta 2 — Usuarios con correo repetido: repetidos = df[df.duplicated(subset=["correo"], keep=False)].

Consulta 3 — Cuántos usuarios hay por estado: conteo = df["estado"].value_counts().

Consulta 4 — GROUPBY: cantidad de usuarios por rol: por_rol = df.groupby("rol")["id_usuario"].count().sort_values(ascending=False).

Consulta 5 — GROUPBY por mes: cuántos usuarios se registraron cada mes: por_mes = df.groupby("mes")["id_usuario"].count().

Al menos 2 de las cinco consultas usan groupby.

Cada consulta está en su propia función, con un print() que dice qué pregunta responde.

Cada resultado se guarda como data/limpio/usuarios_consulta_N.csv.

Al ejecutar el script se ven las cinco respuestas en consola, en orden.