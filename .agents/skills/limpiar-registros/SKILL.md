---
name: limpiar-registros
description: Limpia los datos sucios de la tabla transacciones_gemas del proyecto integrador con pandas, siguiendo los criterios de la HU HI-8 de JIRA, y entrega el archivo limpio y el código. Úsala cuando alguien suba el archivo transacciones_gemas_sucio.csv (o registros_sucio.csv), pida limpiar los datos de transacciones_gemas o pregunte cómo hacer la HU HI-8 de limpieza.
---

# Limpiar registros (transacciones_gemas)

Limpia los datos sucios de la tabla transacciones_gemas del proyecto integrador con pandas, siguiendo los criterios de la HU HI-8 de JIRA, y entrega el archivo limpio y el código. Trabaja en este orden y no te saltes pasos.

## Paso 1. Revisar lo que llegó

Revisa el archivo transacciones_gemas_sucio.csv (o registros_sucio.csv). Si falta algo, pídelo en una sola pregunta.

## Paso 2. Consultar la guía

Lee `references/criterios.md`: tiene los criterios de aceptación de la HU HI-8 de la tabla transacciones_gemas, copiados de JIRA. No inventes reglas que no estén ahí.

## Paso 3. Procesar con el script

```bash
python scripts/limpiar_registros.py registros_sucio.csv
```

Lee registros_sucio.csv con pandas, imprime el diagnóstico (shape, info, nulos y duplicados), corrige cada error que piden los criterios, imprime el diagnóstico otra vez y guarda registros_limpio.csv. Usa las rutas reales de los archivos que subió la persona. Copia lo que imprime el script sin cambiar ningún resultado. Si no llegó el archivo que necesita el script, dilo y sigue con lo demás.

## Paso 4. Responder

Responde en español, en este orden:

1. Empieza con la conclusión en una frase.
2. Muestra el archivo registros_limpio.csv, el antes y después de la limpieza y el código de limpiar_registros.py.
3. Explica cada problema con el valor encontrado y el esperado.
4. Termina con el siguiente paso que debe dar la persona.
