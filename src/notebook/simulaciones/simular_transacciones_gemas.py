"""HU HI-5: simula 800 filas de la tabla `transacciones_gemas` con Faker y las ensucia a propósito."""
import random
from pathlib import Path
import pandas as pd
from faker import Faker

SEMILLA = 42
random.seed(SEMILLA)
Faker.seed(SEMILLA)
fake = Faker("es_ES")

# ------------------------------------------------------------------ Constantes
MOTIVOS = [
    "compra",
    "bono_diario",
    "recompensa_personaje_publico",
    "gasto_mensaje",
    "ajuste_admin",
]

IDS_USUARIO = [1, 2, 3, 4, 5, 6, 7, 8, 9]

COLUMNAS = [
    "id_transaccion",
    "id_usuario",
    "cantidad",
    "motivo",
    "id_referencia",
    "fecha",
]


def generar_transacciones_gemas(n: int = 800) -> pd.DataFrame:
    """
    Genera un DataFrame con n transacciones base de transacciones_gemas
    ensuciadas a propósito según los criterios de la HU HI-5.
    """
    random.seed(SEMILLA)
    Faker.seed(SEMILLA)

    registros = []

    for i in range(1, n + 1):
        usuario = random.choice(IDS_USUARIO)
        motivo = random.choice(MOTIVOS)

        # Asignación coherente de signo según motivo
        if motivo == "gasto_mensaje":
            cantidad = -random.randint(5, 50)
        elif motivo == "bono_diario":
            cantidad = random.choice([20, 25, 50])
        elif motivo == "compra":
            cantidad = random.choice([100, 250, 500, 1000])
        elif motivo == "recompensa_personaje_publico":
            cantidad = random.choice([50, 100])
        else:  # ajuste_admin
            cantidad = random.choice([-50, 50, 100, 500])

        # Ensuciamiento: 5% de inconsistencias en balance
        if random.random() < 0.05:
            cantidad = -cantidad

        # Ensuciamiento: Variantes en motivo (mayúsculas, minúsculas, espacios)
        prob_motivo = random.random()
        if prob_motivo < 0.08:
            motivo_final = motivo.upper()
        elif prob_motivo < 0.16:
            motivo_final = f" {motivo} "
        elif prob_motivo < 0.22:
            motivo_final = motivo.capitalize()
        else:
            motivo_final = motivo

        # Ensuciamiento: id_referencia con al menos 25% nulos y espacios
        prob_ref = random.random()
        if prob_ref < 0.30:
            id_referencia = None
        elif prob_ref < 0.35:
            id_referencia = f" {random.randint(100, 5000)} "
        else:
            id_referencia = random.randint(100, 5000)

        # Fecha distribuida en el último año
        fecha_dt = fake.date_time_between(start_date="-1y", end_date="now")

        # Ensuciamiento: Mezcla de al menos dos formatos de fecha
        if random.random() < 0.50:
            fecha_str = fecha_dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            fecha_str = fecha_dt.strftime("%d/%m/%Y %H:%M")

        registros.append({
            "id_transaccion": i,
            "id_usuario": usuario,
            "cantidad": cantidad,
            "motivo": motivo_final,
            "id_referencia": id_referencia,
            "fecha": fecha_str,
        })

    df = pd.DataFrame(registros)

    # Ensuciamiento: 5% de filas duplicadas íntegramente
    n_duplicados = int(n * 0.05)
    filas_duplicadas = df.sample(n=n_duplicados, random_state=42)
    df = pd.concat([df, filas_duplicadas], ignore_index=True)

    return df


if __name__ == "__main__":
    df_resultado = generar_transacciones_gemas(800)
    print(f"Shape generado: {df_resultado.shape}")
    print(df_resultado.head(5))
