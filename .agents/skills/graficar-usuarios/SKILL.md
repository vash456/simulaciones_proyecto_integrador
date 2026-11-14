---
name: graficar-usuarios
description: Crea las tres gráficas de la HU G01 de la tabla usuarios del proyecto integrador con matplotlib, escribe las conclusiones y entrega las imágenes y el código. Úsala cuando alguien suba el archivo usuarios_limpio.csv y pida gráficas, pida el reporte o las conclusiones de usuarios o pregunte cómo hacer la HU G01 con matplotlib.
---

# Graficar usuarios

Crea las tres gráficas de la HU G01 de la tabla usuarios del proyecto integrador con matplotlib, escribe las conclusiones y entrega las imágenes y el código. Trabaja en este orden y no te saltes pasos.

## Paso 1. Revisar lo que llegó

Revisa el archivo usuarios_limpio.csv. Si falta algo, pídelo en una sola pregunta.

## Paso 2. Consultar la guía

Lee `references/criterios.md`: tiene los criterios de aceptación de la HU G01 de la tabla usuarios, con las tres gráficas y las preguntas de las conclusiones, copiados de Kaizen. No inventes reglas que no estén ahí.

## Paso 3. Procesar con el script

```bash
python scripts/reporte_usuarios.py usuarios_limpio.csv
```

Lee usuarios_limpio.csv, crea las tres gráficas de la HU con título, nombre en los dos ejes y tight_layout, las guarda en reportes/ con dpi=120 y plt.close(), y al final imprime las conclusiones. Usa las rutas reales de los archivos que subió la persona. Copia lo que imprime el script sin cambiar ningún resultado. Si no llegó el archivo que necesita el script, dilo y sigue con lo demás.

## Paso 4. Responder

Responde en español, en este orden:

1. Muestra las tres gráficas.
2. Entrega los tres archivos PNG para descargar.
3. Escribe las conclusiones que imprimió el script, respondiendo las preguntas de la HU.
4. Entrega el código completo de scripts/reporte_usuarios.py en un bloque, listo para copiar en src/reporte_usuarios.py.
5. Termina con el siguiente paso: copiar el código en src/, ejecutarlo en tu computador, subir los cambios a GitHub y mover la tarjeta a Hecho en Kaizen.
