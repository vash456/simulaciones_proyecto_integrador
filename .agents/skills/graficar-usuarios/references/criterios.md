Criterios de aceptación

El script src/reporte_usuarios.py existe y corre sin errores.

Lee data/limpio/usuarios_limpio.csv.

Gráfica 1 — Barras: usuarios por estado: conteo.plot(kind="bar"), guardada en reportes/usuarios_grafica_1.png.

Gráfica 2 — Línea: usuarios registrados por mes: por_mes.plot(kind="line", marker="o"), guardada en reportes/usuarios_grafica_2.png.

Gráfica 3 — Barras horizontales: usuarios por rol: por_rol.plot(kind="barh"), guardada en reportes/usuarios_grafica_3.png.

Cada gráfica tiene plt.title(...), plt.xlabel(...), plt.ylabel(...) y plt.tight_layout() antes de plt.savefig(...).

Se usa plt.savefig(ruta, dpi=120) y luego plt.close() (no plt.show(), para que el script no se quede esperando).

La carpeta se crea sola: os.makedirs("reportes", exist_ok=True).

El script imprime al final las conclusiones, respondiendo por lo menos:

Cuál es el rol con más usuarios y cuántos tiene.

En qué mes hubo más registros.

Cuántos usuarios con correo repetido se encontraron y por qué el back debe bloquearlos (por ejemplo, con 409 Conflict al registrar un correo ya existente).

Las tres imágenes quedan subidas al repositorio dentro de reportes/.