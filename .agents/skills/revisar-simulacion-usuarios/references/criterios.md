HU simulacion
Criterios de aceptación

El script src/simular_usuarios.py existe y corre con python src/simular_usuarios.py sin errores.

Al inicio se declaran las constantes: GENEROS, ESTADOS, ROLES, PROVEEDORES_AUTH, IDS_PLAN.

Se generan 800 filas con estas 25 columnas:

#

Columna

Tipo en BD

Nulo

Predeterminado

1

id_usuario

int(11)

No

Ninguna

2

uid

varchar(20)

No

Ninguna

3

nombre_usuario

varchar(50)

No

Ninguna

4

correo

varchar(100)

No

Ninguna

5

genero

enum('masculino','femenino','otro')

Sí

NULL

6

contrasena_hash

varchar(255)

Sí

NULL

7

proveedor_auth

varchar(20)

No

email

8

id_plan

int(11)

No

1

9

fecha_nacimiento

date

Sí

NULL

10

edad_verificada

tinyint(1)

No

0

11

terminos_aceptados

tinyint(1)

No

1

12

fecha_aceptacion_terminos

datetime

Sí

NULL

13

version_terminos

varchar(20)

Sí

v1.0

14

amatistas_saldo

int(11)

No

50

15

estado

enum('activo','suspendido','baneado','eliminado'…)

No

activo

16

intentos_fallidos

int(11)

No

0

17

bloqueado_hasta

datetime

Sí

NULL

18

debe_cambiar_password

tinyint(1)

No

0

19

token_version

int(11)

No

1

20

ultimo_acceso

datetime

Sí

NULL

21

fecha_registro

datetime

Sí

current_timestamp()

22

rol

enum('usuario','moderador','admin','superadmin'…)

No

usuario

23

avatar_url

varchar(255)

Sí

NULL

24

fecha_eliminacion

datetime

Sí

NULL

25

motivo_eliminacion

varchar(255)

Sí

NULL

Generación (con las reglas de la historia original):

id_usuario: entero secuencial (1 a 800). (Reemplaza el UUID del ejemplo, porque aquí es int(11).)

uid: texto de máximo 20 caracteres. Debe respetar el límite de varchar(20).

nombre_usuario: fake.user_name(), máximo 50 caracteres.

correo: fake.email(), máximo 100 caracteres.

genero: random.choice(GENEROS), con algunos valores nulos permitidos por la BD.

contrasena_hash: texto simulado (nunca contraseñas reales).

proveedor_auth: random.choice(PROVEEDORES_AUTH).

id_plan: random.choice(IDS_PLAN).

fecha_nacimiento: fake.date_of_birth().

edad_verificada, terminos_aceptados, debe_cambiar_password: 0 o 1.

fecha_aceptacion_terminos, bloqueado_hasta, ultimo_acceso, fecha_eliminacion: fake.date_time_between(start_date="-1y", end_date="now").

version_terminos: texto tipo v1.0.

amatistas_saldo, intentos_fallidos, token_version: enteros.

estado: random.choice(ESTADOS).

fecha_registro: fake.date_time_between(start_date="-1y", end_date="now").

rol: random.choice(ROLES).

avatar_url: fake.image_url().

motivo_eliminacion: fake.sentence(nb_words=10).

La semilla está fija: Faker.seed(42) y random.seed(42).

Ensuciado a propósito:

fecha_registro: dos formatos mezclados: "2026-03-15 14:30:00" y "15/03/2026 14:30".

motivo_eliminacion: 20% en None (nulos).

estado: variantes como 'activo', 'ACTIVO', ' Suspendido '.

correo: 10% repetido entre filas distintas, con mayúsculas mezcladas y espacios sobrantes.

5% de las filas repetidas tal cual (duplicados exactos).

Estructura del script:

Todo se arma en una función generar_usuarios(n=800) que devuelve el DataFrame (return df), para importarla desde el script de exportación.

El bloque if __name__ == "__main__": solo imprime df.shape, df.head() y df.isna().sum().

HU Exportacion
Criterios de aceptación

El script src/exportar_usuarios.py existe y corre sin errores.

Importa la función del script anterior (from importlib import import_module o renombrando el módulo) y NO vuelve a copiar el código de generación.

Genera data/crudo/usuarios_sucio.csv con df.to_csv(ruta, index=False, encoding="utf-8").

Genera data/crudo/usuarios_sucio.xlsx con df.to_excel(ruta, index=False, sheet_name="usuarios").

Genera data/crudo/usuarios_sucio.json con df.to_json(ruta, orient="records", force_ascii=False, indent=2).

La carpeta se crea sola si no existe: os.makedirs("data/crudo", exist_ok=True).

Al final el script imprime la ruta y el tamaño (df.shape) de cada archivo generado.

requirements.txt incluye: pandas (versión 2.x), faker, openpyxl y matplotlib.

Los tres archivos quedan versionados en Git (o, si pesan mucho, se documenta en el README cómo generarlos).
