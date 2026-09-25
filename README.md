# API RESTful — Sistema de votaciones

API para registrar votantes y candidatos, emitir un único voto por votante y consultar los resultados de la votación.

La base de datos es PostgreSQL. Los endpoints quedan protegidos con JWT: antes de usar el resto de la API hay que pedir un token de acceso.

## Documentación de la API

URL base en local: `http://127.0.0.1:8000`

Las rutas funcionan con barra final y sin ella (`/voters` y `/voters/`).

### Autenticación

| Método | Ruta | Descripción |
| --- | --- | --- |
| POST | `/auth/token` | Entrega `access` y `refresh` |
| POST | `/auth/token/refresh` | Entrega un `access` nuevo a partir del `refresh` |

Cuerpo para pedir el token:

```json
{
  "username": "admin",
  "password": "administrator1"
}
```

El login usa el campo `username`, no el correo. El correo `admin@gmail.com` queda guardado en la cuenta.

El `access` dura 12 horas. El `refresh` dura 1 día. El resto de endpoints exige la cabecera:

```http
Authorization: Bearer <access>
```

Sin esa cabecera la API responde `401`.

La cuenta `admin` se crea al ejecutar las migraciones. Quien revise el proyecto puede usarla después de migrar; no hace falta crearla a mano.

### Votantes

| Método | Ruta | Descripción |
| --- | --- | --- |
| POST | `/voters` | Registra un votante |
| GET | `/voters` | Lista los votantes |
| GET | `/voters/{id}` | Detalle de un votante |
| DELETE | `/voters/{id}` | Elimina un votante |

Cuerpo de registro:

```json
{
  "name": "Ana Ruiz",
  "email": "ana@example.com"
}
```

`name` y `email` son obligatorios. El correo debe ser único. `has_voted` inicia en `false` y la API no permite enviarlo: se actualiza al votar.

Un votante se puede eliminar aunque ya haya votado. En ese caso se quita su voto y el conteo del candidato baja en 1.

### Candidatos

| Método | Ruta | Descripción |
| --- | --- | --- |
| POST | `/candidates` | Registra un candidato |
| GET | `/candidates` | Lista los candidatos |
| GET | `/candidates/{id}` | Detalle de un candidato |
| DELETE | `/candidates/{id}` | Elimina un candidato |

Cuerpo de registro:

```json
{
  "name": "Carlos Mesa",
  "party": "Partido Verde"
}
```

`name` es obligatorio. `party` es opcional. `votes` inicia en `0` y la API no permite enviarlo: se incrementa al recibir un voto.

Un candidato se puede eliminar aunque ya tenga votos. Los votos asociados se quitan y esos votantes quedan otra vez con `has_voted` en `false`.

### Votos

| Método | Ruta | Descripción |
| --- | --- | --- |
| POST | `/votes` | Emite un voto |
| GET | `/votes` | Lista los votos emitidos |
| GET | `/votes/statistics` | Estadísticas de la votación |

Cuerpo para votar:

```json
{
  "voter_id": 1,
  "candidate_id": 1
}
```

No existe una ruta para eliminar un voto por sí solo.

`GET /votes/statistics` responde con el total de votos por candidato, el porcentaje de cada uno y el total de votantes que ya votaron:

```json
{
  "votes_by_candidate": [
    {
      "candidate_id": 1,
      "name": "Carlos Mesa",
      "party": "Partido Verde",
      "votes": 1,
      "percentage": 100.0
    }
  ],
  "voters_who_voted": 1
}
```

### Reglas de validación

- Una persona no puede ser votante y candidato a la vez. La comparación es por nombre, sin distinguir mayúsculas.
- Cada votante emite un solo voto.
- `voter_id` y `candidate_id` deben existir.
- Al votar, `has_voted` del votante pasa a `true` y `votes` del candidato aumenta en 1.

Si una regla no se cumple, la API responde `400`. Si el id no existe en un GET o DELETE de detalle, responde `404`. Un registro correcto responde `201`. Un DELETE correcto responde `204`.

### Filtros y paginación

`GET /voters` y `GET /candidates` devuelven páginas de 10 registros. La respuesta tiene `count`, `next`, `previous` y `results`.

Parámetros:

- `page`: número de página.
- `page_size`: cantidad por página, hasta 100.
- Votantes: `name`, `email` y `has_voted` (`true` o `false`).
- Candidatos: `name` y `party`.

`name`, `email` y `party` buscan una parte del texto y no distinguen mayúsculas. Se pueden combinar con la paginación, por ejemplo `GET /voters?name=ana&page_size=5`.

## Ejecutar el proyecto en local

Requisitos: Python 3 y PostgreSQL instalados en la máquina.

1. Clona el repositorio y entra en la carpeta del proyecto.

2. Crea y activa un entorno virtual.

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Linux o macOS:

```bash
python -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. En PostgreSQL crea una base de datos. Puedes hacerlo desde pgAdmin o con `psql`:

```sql
CREATE DATABASE voting_db;
```

El nombre debe coincidir con `DB_NAME`. El usuario de `DB_USER` debe poder conectarse a esa base.

5. En la raíz del proyecto, junto a `manage.py`, crea un archivo `.env`. Ese archivo no se sube al repositorio. Usa este formato y cambia la contraseña por la de tu instalación de PostgreSQL:

```env
DB_NAME=voting_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

6. Aplica las migraciones. Este paso también crea el usuario `admin`:

```bash
python manage.py migrate
```

7. Inicia el servidor:

```bash
python manage.py runserver
```

La API queda en `http://127.0.0.1:8000`.

## Uso en Postman

### Obtener el token

1. Crea una petición `POST` a `http://127.0.0.1:8000/auth/token`.
2. Abre la pestaña **Body**, elige **raw** y el tipo **JSON**.
3. Escribe:

```json
{
  "username": "admin",
  "password": "administrator1"
}
```

4. Pulsa **Send**.
5. En la respuesta copia el valor de `access`. Conserva también `refresh` por si el `access` vence.

### Usar el access token en las demás peticiones

1. Crea la petición que necesites, por ejemplo `GET http://127.0.0.1:8000/voters`.
2. Abre la pestaña **Authorization**.
3. En **Type** elige **Bearer Token**.
4. Pega el `access` en **Token**.
5. Pulsa **Send**.

Postman envía la cabecera `Authorization: Bearer <access>`. Repite esos cuatro pasos en cada petición a votantes, candidatos, votos y estadísticas.

Si el `access` ya venció, haz `POST http://127.0.0.1:8000/auth/token/refresh` con este cuerpo y usa el `access` nuevo:

```json
{
  "refresh": "<refresh>"
}
```

### Ejemplos de peticiones

Con el token ya configurado en Authorization:

**Registrar un votante.** `POST http://127.0.0.1:8000/voters`

Body, raw, JSON:

```json
{
  "name": "Ana Ruiz",
  "email": "ana@example.com"
}
```

**Registrar un candidato.** `POST http://127.0.0.1:8000/candidates`

```json
{
  "name": "Carlos Mesa",
  "party": "Partido Verde"
}
```

**Emitir un voto.** `POST http://127.0.0.1:8000/votes`

Usa los `id` devueltos al crear el votante y el candidato:

```json
{
  "voter_id": 1,
  "candidate_id": 1
}
```

**Listar y filtrar.** `GET http://127.0.0.1:8000/voters?name=ana&page=1&page_size=10`

**Ver estadísticas.** `GET http://127.0.0.1:8000/votes/statistics`

**Consultar o eliminar un registro.** `GET` o `DELETE` a `http://127.0.0.1:8000/voters/1` y `http://127.0.0.1:8000/candidates/1`. Estas peticiones no llevan body.
