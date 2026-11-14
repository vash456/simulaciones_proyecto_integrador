"""HU F01: simula 800 filas de la tabla `personajes` con Faker y las ensucia a proposito."""
import random

import pandas as pd
from faker import Faker

SEMILLA = 42
random.seed(SEMILLA)
Faker.seed(SEMILLA)
fake = Faker("es_CO")

# ------------------------------------------------------------------ Constantes
IDS_CATEGORIA = [1, 2, 3, 4, 5]
IDS_CREADOR = [101, 102, 103, 104, 105]
IDS_MODERADOR = [1, 2, 3]
ESTADOS_MODERACION = ["pendiente", "aprobado", "rechazado"]
CLASIFICACIONES_CONTENIDO = ["todo_publico", "adolescentes", "adultos"]
GENEROS = ["masculino", "femenino", "no_binario", "otro"]
MODOS_ANIMACION_PORTADA = ["estatico", "hover", "bucle"]

COLUMNAS = [
    "id_personaje", "cid", "id_categoria", "id_creador", "nombre", "descripcion_corta",
    "avatar_url", "publico", "clasificacion_contenido", "estado_moderacion",
    "motivo_rechazo", "id_moderador", "fecha_moderacion", "destacado", "orden_destacado",
    "version", "fecha_creacion", "es_oficial", "genero", "tags", "fecha_eliminacion",
    "motivo_eliminacion", "modo_animacion_portada", "avatar_animado_url",
]
COLUMNAS_ENTERAS = [
    "id_personaje", "id_categoria", "id_creador", "publico", "id_moderador", "destacado",
    "orden_destacado", "version", "es_oficial",
]
FMT_ISO = "%Y-%m-%d %H:%M:%S"
FMT_LATINO = "%d/%m/%Y %H:%M"


def _cid_unico(usados):
    """Crea un cid de 12 caracteres ('cid-' + 8 alfanumericos) que no se haya usado."""
    while True:
        cid = "cid-" + fake.lexify(text="????????", letters="abcdefghijklmnopqrstuvwxyz0123456789")
        if cid not in usados:
            usados.add(cid)
            return cid


def _fila_base(i, usados):
    """Genera una fila limpia con las 24 columnas y sus reglas de coherencia."""
    estado = random.choice(ESTADOS_MODERACION)
    moderado = estado in ("aprobado", "rechazado")
    destacado = random.choice([0, 1])
    eliminado = random.random() < 0.10
    creacion = fake.date_time_between(start_date="-1y", end_date="now")
    return {
        "id_personaje": i,
        "cid": _cid_unico(usados),
        "id_categoria": random.choice(IDS_CATEGORIA),
        "id_creador": random.choice(IDS_CREADOR),
        "nombre": fake.first_name(),
        "descripcion_corta": fake.sentence(nb_words=10),
        "avatar_url": fake.image_url(),
        "publico": random.choice([0, 1]),
        "clasificacion_contenido": random.choice(CLASIFICACIONES_CONTENIDO),
        "estado_moderacion": estado,
        "motivo_rechazo": fake.sentence(nb_words=6) if estado == "rechazado" else None,
        "id_moderador": random.choice(IDS_MODERADOR) if moderado else None,
        "fecha_moderacion": (fake.date_time_between(start_date="-6m", end_date="now").strftime(FMT_ISO)
                             if moderado else None),
        "destacado": destacado,
        "orden_destacado": random.randint(1, 50) if destacado else None,
        "version": 0,
        "fecha_creacion": creacion,
        "es_oficial": random.choice([0, 1]),
        "genero": random.choice(GENEROS),
        "tags": ", ".join(fake.words(nb=3)),
        "fecha_eliminacion": (fake.date_time_between(start_date=creacion, end_date="now").strftime(FMT_ISO)
                              if eliminado else None),
        "motivo_eliminacion": fake.sentence(nb_words=4) if eliminado else None,
        "modo_animacion_portada": random.choice(MODOS_ANIMACION_PORTADA),
        "avatar_animado_url": fake.image_url(),
    }


def _indices(n, proporcion):
    """Elige sin repetir round(n * proporcion) posiciones usando el `random` con semilla."""
    return random.sample(range(n), round(n * proporcion))


def generar_personajes(n=800):
    """Devuelve un DataFrame con n filas de `personajes` y errores sembrados a proposito."""
    random.seed(SEMILLA)   # garantiza el mismo resultado aunque se llame varias veces
    Faker.seed(SEMILLA)
    usados = set()
    filas = [_fila_base(i, usados) for i in range(1, n + 1)]

    # fecha_creacion: dos formatos mezclados
    for f in filas:
        formato = random.choice([FMT_ISO, FMT_LATINO])
        f["fecha_creacion"] = f["fecha_creacion"].strftime(formato)

    # Nulos: 20% en descripcion_corta, 10% en avatar_url
    for i in _indices(n, 0.20):
        filas[i]["descripcion_corta"] = None
    for i in _indices(n, 0.10):
        filas[i]["avatar_url"] = None

    # estado_moderacion y nombre: espacios sobrantes y mayusculas mezcladas
    for i in _indices(n, 0.15):
        e = filas[i]["estado_moderacion"]
        filas[i]["estado_moderacion"] = random.choice(
            [f" {e.upper()} ", f"{e} ", f" {e}", e.upper(), e.capitalize()])
    for i in _indices(n, 0.10):
        nom = filas[i]["nombre"]
        filas[i]["nombre"] = random.choice([f"  {nom} ", f"{nom} ", nom.upper(), nom.lower()])

    # 10% con el cid repetido (viola la unicidad): copia el cid de otra fila
    for i in _indices(n, 0.10):
        otra = random.choice([j for j in range(n) if j != i])
        filas[i]["cid"] = filas[otra]["cid"]

    # 5% de filas repetidas tal cual (se agregan al final; los id_personaje 1..n siguen presentes)
    repetidas = [dict(filas[i]) for i in _indices(n, 0.05)]
    df = pd.DataFrame(filas + repetidas, columns=COLUMNAS)

    # Enteros con nulos: tipo Int64 para que no se escriban como '10.0'
    for col in COLUMNAS_ENTERAS:
        df[col] = df[col].astype("Int64")
    return df


if __name__ == "__main__":
    df = generar_personajes()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())
