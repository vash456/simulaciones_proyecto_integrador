---
name: consultar-usuarios
description: Responde las cinco consultas de la HU Q01 sobre la tabla usuarios del proyecto integrador con pandas y entrega los resultados y el código. Úsala cuando alguien suba el archivo usuarios_limpio.csv, pida hacer las consultas de usuarios o pregunte cómo hacer la HU Q01 con groupby.
---

# Consultar usuarios

Responde las cinco consultas de la HU Q01 sobre la tabla usuarios del proyecto integrador con pandas y entrega los resultados y el código. Trabaja en este orden y no te saltes pasos.

## Paso 1. Revisar lo que llegó

Revisa el archivo usuarios_limpio.csv. Si falta algo, pídelo en una sola pregunta.

## Paso 2. Consultar la guía

Lee `references/criterios.md`: tiene los criterios de aceptación de la HU Q01 de la tabla usuarios, con las cinco consultas, copiados de Kaizen. No inventes reglas que no estén ahí.

## Paso 3. Procesar con el script

```bash
python scripts/consultas_usuarios.py usuarios_limpio.csv
```

Lee usuarios_limpio.csv y resuelve las cinco consultas de la HU, cada una en su propia función y al menos dos con groupby; imprime el título y el resultado de cada una y guarda usuarios_consulta_N.csv. Usa las rutas reales de los archivos que subió la persona. Copia lo que imprime el script sin cambiar ningún resultado. Si no llegó el archivo que necesita el script, dilo y sigue con lo demás.

## Paso 4. Responder

Responde en español, en este orden:

1. Empieza con una frase que resuma lo más importante que muestran los datos.
2. Muestra cada consulta con su pregunta y su resultado, en orden.
3. Entrega los cinco archivos usuarios_consulta_N.csv para descargar.
4. Entrega el código completo de scripts/consultas_usuarios.py en un bloque, listo para copiar en src/consultas_usuarios.py.
5. Termina con el siguiente paso: copiar el código en src/, ejecutarlo en tu computador, subir los cambios a GitHub y mover la tarjeta a Hecho en Kaizen.
