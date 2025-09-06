Usuario root → root / password123

Usuario app → juan / MYSQL_PASSWORD

Base de datos → mydb

Host (si corres FastAPI fuera del contenedor) → localhost

Host (si corres FastAPI en otro contenedor del mismo docker-compose) → db

⚠️ Importante: si levantas FastAPI en el mismo docker-compose.yml, la conexión debe usar db como host (porque así se llama el servicio).


2. Mantener el engine, sesiones y modelos

Necesitas database.py, models.py y schemas.py, porque:

database.py tiene la configuración de conexión y sesiones (engine, async_session).

models.py define cómo SQLAlchemy interpreta tu tabla (Pelicula).

schemas.py define las validaciones y respuestas de FastAPI (entrada/salida).