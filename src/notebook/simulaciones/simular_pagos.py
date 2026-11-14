"""HU P01: simula 800 filas de la tabla `pagos` con Faker y las ensucia a proposito."""
import random
import uuid

import pandas as pd
from faker import Faker

SEMILLA = 42
random.seed(SEMILLA)
Faker.seed(SEMILLA)
fake = Faker("es_CO")

# ------------------------------------------------------------------ Constantes
IDS_USUARIO = list(range(1, 11))          # enteros del 1 al 10
PROVEEDORES  = ["stripe", "apple", "google"]
CONCEPTOS    = [
    "100 Amatistas",
    "500 Amatistas",
    "1500 Amatistas",
    "Suscripcion Mensual",
]
MONTOS = {
    "100 Amatistas":    0.99,
    "500 Amatistas":    3.99,
    "1500 Amatistas":   9.99,
    "Suscripcion Mensual": 4.99,
}

FMT_ISO    = "%Y-%m-%d %H:%M:%S"
FMT_LATINO = "%d/%m/%Y %H:%M"

COLUMNAS = [
    "id_pago", "id_usuario", "monto", "proveedor",
    "id_externo", "concepto", "fecha_pago",
]


# ------------------------------------------------------------------ Helpers
def _id_externo(proveedor: str) -> str:
    """Genera un id_externo simulado con prefijo segun la pasarela."""
    token = uuid.uuid4().hex[:12]
    prefijos = {"stripe": "ch_", "apple": "APL_", "google": "GPA."}
    return prefijos.get(proveedor, "EXT_") + token


def _fila_base(i: int) -> dict:
    """Genera una fila limpia con las 7 columnas de pagos."""
    concepto   = random.choice(CONCEPTOS)
    proveedor  = random.choice(PROVEEDORES)
    fecha      = fake.date_time_between(start_date="-1y", end_date="now")
    return {
        "id_pago":    i,
        "id_usuario": random.choice(IDS_USUARIO),
        "monto":      MONTOS[concepto],
        "proveedor":  proveedor,
        "id_externo": _id_externo(proveedor),
        "concepto":   concepto,
        "fecha_pago": fecha,
    }


def _indices(n: int, proporcion: float) -> list:
    """Elige sin repetir round(n * proporcion) posiciones con la semilla fijada."""
    return random.sample(range(n), round(n * proporcion))


# ------------------------------------------------------------------ Generador principal
def generar_pagos(n: int = 800) -> pd.DataFrame:
    """Devuelve un DataFrame con n filas de `pagos` y errores sembrados a proposito."""
    random.seed(SEMILLA)
    Faker.seed(SEMILLA)

    filas = [_fila_base(i) for i in range(1, n + 1)]

    # --- Ensuciado 1: fecha_pago con dos formatos mezclados
    for f in filas:
        fmt = random.choice([FMT_ISO, FMT_LATINO])
        f["fecha_pago"] = f["fecha_pago"].strftime(fmt)

    # --- Ensuciado 2: 20% de concepto = None (nulos)
    for i in _indices(n, 0.20):
        filas[i]["concepto"] = None

    # --- Ensuciado 3: proveedor con variantes de formato y espacios
    variantes = {
        "stripe": [" STRIPE ", "Stripe", "STRIPE", "stripe"],
        "apple":  ["Apple", "APPLE", " apple ", "apple"],
        "google": ["Google", "GOOGLE", " Google ", "google"],
    }
    for i in _indices(n, 0.15):
        prov = filas[i]["proveedor"]
        filas[i]["proveedor"] = random.choice(variantes.get(prov, [prov]))

    # --- Ensuciado 4: 10% con id_externo duplicado (simula webhook duplicado)
    idx_dup_ext = _indices(n, 0.10)
    for i in idx_dup_ext:
        otra = random.choice([j for j in range(n) if j != i])
        filas[i]["id_externo"] = filas[otra]["id_externo"]

    # --- Ensuciado 5: 5% de filas repetidas tal cual al final
    repetidas = [dict(filas[i]) for i in _indices(n, 0.05)]
    df = pd.DataFrame(filas + repetidas, columns=COLUMNAS)

    return df


if __name__ == "__main__":
    df = generar_pagos()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())
