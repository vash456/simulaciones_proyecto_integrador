Criterios de aceptación

El script src/reporte_personajes.py existe y corre sin errores.

Lee data/limpio/personajes_limpio.csv.

Gráfica 1 (barras): personajes por estado de moderación. Usa conteo = df["estado_moderacion"].value_counts() y conteo.plot(kind="bar"). Se guarda en reportes/personajes_grafica_1.png.

Gráfica 2 (línea): personajes creados por mes. Usa por_mes = df.groupby("mes")["id_personaje"].count() y por_mes.plot(kind="line", marker="o"). Se guarda en reportes/personajes_grafica_2.png.

Gráfica 3 (barras horizontales): las 10 categorías con más personajes. Usa top_categorias = df.groupby("id_categoria")["id_personaje"].count().nlargest(10) y top_categorias.plot(kind="barh"). Se guarda en reportes/personajes_grafica_3.png.

Cada gráfica tiene plt.title(...), plt.xlabel(...), plt.ylabel(...) y plt.tight_layout() antes de plt.savefig(...).

Se usa plt.savefig(ruta, dpi=120) y luego plt.close(). No se usa plt.show(), para que el script no se quede esperando.

La carpeta se crea sola: os.makedirs("reportes", exist_ok=True).

El script imprime al final las conclusiones, que responden por lo menos:

Cuál es la categoría con más personajes y cuántos tiene.

En qué mes se crearon más personajes.

Cuántos personajes hay por estado de moderación y cuál predomina.

Cuántas filas se eliminaron en la limpieza por cid repetido (u otra clave duplicada). Debe explicar por qué la base de datos debe impedirlo con una restricción UNIQUE sobre cid.

Las tres imágenes quedan subidas al repositorio dentro de reportes/.