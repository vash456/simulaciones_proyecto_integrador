---
name: consultar-registros
description: Responde las cinco consultas de la HU HI-9 sobre la tabla transacciones_gemas del proyecto integrador con pandas y entrega los resultados y el código. Úsala cuando alguien suba el archivo transacciones_gemas_limpio.csv (o registros_limpio.csv), pida hacer las consultas de transacciones_gemas o pregunte cómo hacer la HU HI-9 con groupby.
---

# Consultar registros (transacciones_gemas)

Responde las cinco consultas de la HU HI-9 sobre la tabla transacciones_gemas del proyecto integrador con pandas y entrega los resultados y el código. Trabaja en este orden y no te saltes pasos.

## Paso 1. Revisar lo que llegó

Revisa el archivo transacciones_gemas_limpio.csv (o registros_limpio.csv). Si falta algo, pídelo en una sola pregunta.

## Paso 2. Consultar la guía

Lee `references/criterios.md`: tiene los criterios de aceptación de la HU HI-9 de la tabla transacciones_gemas, con las cinco consultas, copiados de JIRA. No inventes reglas que no estén ahí.

## Paso 3. Procesar con el script

```bash
python scripts/consultas_registros.py registros_limpio.csv
```

Lee registros_limpio.csv y resuelve las cinco consultas de la HU, cada una en su propia función y al menos dos con groupby; imprime el título y el resultado de cada una y guarda registros_consulta_N.csv. Usa las rutas reales de los archivos que subió la persona. Copia lo que imprime el script sin cambiar ningún resultado. Si no llegó el archivo que necesita el script, dilo y sigue con lo demás.

## Paso 4. Responder

Responde en español, en este orden:

1. Empieza con una frase que resuma lo más importante que muestran los datos.
2. Muestra cada consulta con su pregunta y su resultado, en orden.
3. Entrega los cinco archivos registros_consulta_N.csv para descargar.
4. Entrega el código completo de scripts/consultas_registros.py en un bloque, listo para copiar en src/notebook/consultas/.
5. Termina con el siguiente paso: copiar el código en src/, ejecutarlo en tu computador, subir los cambios a GitHub y mover la tarjeta a Hecho en JIRA.
