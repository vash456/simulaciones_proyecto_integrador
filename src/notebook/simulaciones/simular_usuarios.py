import random
import pandas as pd
from faker import Faker

Faker.seed(42)
random.seed(42)
fake = Faker("es_CO")

GENEROS = ["masculino", "femenino", "otro"]
ESTADOS = ["activo", "suspendido", "baneado", "eliminado"]
ROLES = ["usuario", "moderador", "admin", "superadmin"]
PROVEEDORES_AUTH = ["email", "google"]
IDS_PLAN = [1, 2, 3]


def generar_usuarios(n=800):
    """Genera n filas simuladas de la tabla `usuarios` con suciedad controlada."""
    Faker.seed(42)
    random.seed(42)
    fake_local = Faker("es_CO")
    registros = []

    for i in range(1, n + 1):
        fecha_nac = fake_local.date_of_birth(minimum_age=18, maximum_age=65).strftime("%Y-%m-%d")
        fecha_acep = fake_local.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
        bloqueado = fake_local.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
        ultimo_acc = fake_local.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
        fecha_reg_dt = fake_local.date_time_between(start_date="-1y", end_date="now")
        fecha_elim = fake_local.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")

        registros.append({
            "id_usuario": i,
            "uid": fake_local.bothify(text="usr_????####????####")[:20],
            "nombre_usuario": fake_local.user_name()[:50],
            "correo": fake_local.email()[:100],
            "genero": None if random.random() < 0.10 else random.choice(GENEROS),
            "contrasena_hash": f"sim_hash_{fake_local.sha256()}"[:255],
            "proveedor_auth": random.choice(PROVEEDORES_AUTH),
            "id_plan": random.choice(IDS_PLAN),
            "fecha_nacimiento": fecha_nac,
            "edad_verificada": random.choice([0, 1]),
            "terminos_aceptados": random.choice([0, 1]),
            "fecha_aceptacion_terminos": fecha_acep,
            "version_terminos": random.choice(["v1.0", "v1.1", "v2.0"]),
            "amatistas_saldo": random.randint(0, 500),
            "estado": random.choice(ESTADOS),
            "intentos_fallidos": random.randint(0, 5),
            "bloqueado_hasta": bloqueado,
            "debe_cambiar_password": random.choice([0, 1]),
            "token_version": random.randint(1, 5),
            "ultimo_acceso": ultimo_acc,
            "fecha_registro": fecha_reg_dt,
            "rol": random.choice(ROLES),
            "avatar_url": fake_local.image_url()[:255],
            "fecha_eliminacion": fecha_elim,
            "motivo_eliminacion": fake_local.sentence(nb_words=10)[:255],
        })

    df = pd.DataFrame(registros)

    # 1. fecha_registro con dos formatos mezclados
    latino = df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")
    iso = df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df["fecha_registro"] = iso
    idx_lat = df.sample(frac=0.30, random_state=42).index
    df.loc[idx_lat, "fecha_registro"] = latino.loc[idx_lat]

    # 2. 20% de nulos en motivo_eliminacion
    idx_motivo = df.sample(frac=0.20, random_state=42).index
    df.loc[idx_motivo, "motivo_eliminacion"] = None

    # 3. Variantes de mayúsculas y espacios en estado
    idx_estado = df.sample(frac=0.20, random_state=43).index
    df.loc[idx_estado, "estado"] = df.loc[idx_estado, "estado"].map(
        lambda x: random.choice([x.upper(), f" {x.capitalize()} ", f" {x.upper()} "])
    )

    # 4. 10% de correo repetido con mayúsculas mezcladas y espacios sobrantes
    n_correo_rep = max(1, int(n * 0.10))
    idx_correo = df.sample(n=n_correo_rep, random_state=44).index
    correos_base = df.drop(idx_correo)["correo"].sample(n=10, random_state=44).tolist()
    df.loc[idx_correo, "correo"] = [
        random.choice([f"  {c.upper()} ", f" {c.capitalize()}  "])[:100]
        for c in (random.choice(correos_base) for _ in range(n_correo_rep))
    ]

    # 5. 5% de filas duplicadas exactas (manteniendo n filas)
    n_dup = max(1, int(n * 0.05))
    idx_origen = df.sample(n=n_dup, random_state=45).index
    idx_destino = df.drop(idx_origen).sample(n=n_dup, random_state=46).index
    df.loc[idx_destino] = df.loc[idx_origen].values

    return df


if __name__ == "__main__":
    df = generar_usuarios()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())
