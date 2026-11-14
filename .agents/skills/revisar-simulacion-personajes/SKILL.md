---
name: revisar-simulacion-personajes
description: Revisa la simulación (HU F01) y la exportación (HU X01) de la tabla personajes del proyecto integrador contra los criterios de Kaizen, encuentra lo que está mal y entrega el código corregido. Úsala cuando alguien suba su script simular_personajes.py o exportar_personajes.py, suba los archivos personajes_sucio.csv, .xlsx o .json o pida revisar o corregir su simulación o su exportación de personajes.
---

# Revisar simulacion personajes

Revisa la simulación (HU F01) y la exportación (HU X01) de la tabla personajes del proyecto integrador contra los criterios de Kaizen, encuentra lo que está mal y entrega el código corregido. Trabaja en este orden y no te saltes pasos.

## Paso 1. Revisar lo que llegó

Revisa los scripts simular_personajes.py y exportar_personajes.py y, si existen, los archivos personajes_sucio.csv, .xlsx y .json. Puede llegar como archivo adjunto o como texto pegado en el chat: sirve igual. Si falta algo, pídelo en una sola pregunta.

## Paso 2. Consultar la guía

Lee `references/criterios.md`: tiene los criterios de aceptación de las HU F01 y X01 de la tabla personajes, copiados de Kaizen. No inventes reglas que no estén ahí.

## Paso 3. Procesar con el script

```bash
python scripts/revisar_datos.py personajes_sucio.csv
```

Cuenta las filas, revisa que estén las columnas que pide la HU y cuenta los nulos y los duplicados de cada columna. Usa las rutas reales de los archivos que subió la persona. Copia lo que imprime el script sin cambiar ningún resultado. Si no llegó el archivo que necesita el script, dilo y sigue con lo demás.

## Paso 4. Responder

Responde en español, en este orden:

1. Empieza con la conclusión: si la simulación y la exportación cumplen o no la HU.
2. Muestra una tabla por HU con cada criterio de references/criterios.md, su estado (PASA o FALLA) y el cambio mínimo.
3. Si llegaron los archivos de datos, copia también la tabla que imprime el script.
4. Explica cada FALLA con lo encontrado y lo esperado, en frases cortas.
5. Entrega simular_personajes.py y exportar_personajes.py corregidos y completos, cada uno en su propio bloque de código, listos para copiar en src/.
6. Termina con el siguiente paso: copiar el código en src/, ejecutarlo en tu computador, subir los cambios a GitHub y mover la tarjeta a Hecho en Kaizen.
