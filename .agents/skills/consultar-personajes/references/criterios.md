hu consultas
Criterios de aceptación

El script src/consultas_personajes.py existe y corre sin errores.

Lee data/limpio/personajes_limpio.csv (el archivo LIMPIO, no el sucio).

Consulta 1: personajes aprobados por moderación: aprobados = df[df["estado_moderacion"] == "APROBADO"].

Consulta 2: personajes destacados: destacados = df[df["destacado"] == 1].sort_values("orden_destacado").

Consulta 3: cuántos personajes hay por estado de moderación: conteo = df["estado_moderacion"].value_counts().

Consulta 4 (GROUPBY): las 10 categorías con más personajes: top_categorias = df.groupby("id_categoria")["id_personaje"].count().nlargest(10).

Consulta 5 (GROUPBY por mes): cuántos personajes se crearon cada mes: por_mes = df.groupby("mes")["id_personaje"].count().

Al menos 2 de las cinco consultas usan groupby.

Cada consulta está en su propia función, con un print() que dice qué pregunta responde.

Cada resultado se guarda como data/limpio/personajes_consulta_N.csv.

Al ejecutar el script se ven las cinco respuestas en consola, en orden.
