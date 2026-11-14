---
name: limpiar-personajes
description: Limpia los datos sucios de la tabla personajes del proyecto integrador con pandas, siguiendo los criterios de la HU L01 de Kaizen, y entrega el archivo limpio y el código. Úsala cuando alguien suba el archivo personajes_sucio.csv, pida limpiar los datos de personajes o pregunte cómo hacer la HU L01 de limpieza de personajes.
---

# Limpiar personajes

Limpia los datos sucios de la tabla personajes del proyecto integrador con pandas, siguiendo los criterios de la HU L01 de Kaizen, y entrega el archivo limpio y el código. Trabaja en este orden y no te saltes pasos.

## Paso 1. Revisar lo que llegó

Revisa el archivo personajes_sucio.csv. Si falta algo, pídelo en una sola pregunta.

## Paso 2. Consultar la guía

Lee `references/criterios.md`: tiene los criterios de aceptación de la HU L01 de la tabla personajes, copiados de Kaizen. No inventes reglas que no estén ahí.

## Paso 3. Procesar con el script

```bash
python scripts/limpiar_personajes.py personajes_sucio.csv
```

Lee personajes_sucio.csv con pandas, imprime el diagnóstico (shape, info, nulos y duplicados), corrige cada error que piden los criterios, imprime el diagnóstico otra vez y guarda personajes_limpio.csv. Usa las rutas reales de los archivos que subió la persona. Copia lo que imprime el script sin cambiar ningún resultado. Si no llegó el archivo que necesita el script, dilo y sigue con lo demás.

## Paso 4. Responder

Responde en español, en este orden:

1. Empieza con la conclusión en una frase.
2. Muestra el archivo personajes_limpio.csv, el antes y después de la limpieza y el código de limpiar_personajes.py.
3. Explica cada problema con el valor encontrado y el esperado.
4. Termina con el siguiente paso que debe dar la persona.
