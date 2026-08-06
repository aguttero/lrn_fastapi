# POSTGRES APP Notes
## Setup Steps
check postgressapp.com
1. Download
2. Move to Apps folder, Open and click 'Initialize'
3. Configure your $PATH to use the included command line tools (optional):
```bash
sudo mkdir -p /etc/paths.d && echo /Applications/Postgres.app/Contents/Versions/latest/bin | sudo tee /etc/paths.d/postgresapp
```
4. default settings:
Host	localhost
Port	5432
User	your system user name
Database	same as user
Password	none
Connection URL	postgresql://localhost

5. Install a GUI -> pgAdmin 4 / Postico
6. How to connect -> See postgresapp.com
7. 


# Rowcount del Result
Sí, existen alternativas para obtener o validar la cantidad de filas afectadas en SQLAlchemy 2.0. La elección depende de si estás ejecutando consultas masivas (Bulk) o si necesitas interactuar con los datos modificados.
### 1. El método recomendado por el ORM: RETURNING con len()
La forma más robusta y alineada con la filosofía de SQLAlchemy 2.0 es usar la cláusula .returning() combinado con result.all(). Esto no solo te da el conteo, sino que te permite validar los datos reales de manera segura.

```python
from sqlalchemy import update
# 1. Agregas returning al final de la sentencia
stmt = update(Usuario).where(Usuario.activo == False).values(por_depurar=True).returning(Usuario.id)
result = await db.execute(stmt)
# 2. Obtienes todas las filas afectadas como una lista
filas_afectadas = result.all()
# 3. Calculas la cantidad de filas directamente
cantidad = len(filas_afectadas) 
```

* Ventaja: Funciona de manera idéntica y garantizada en cualquier motor de base de datos (PostgreSQL, SQLite, MySQL) porque no depende de cómo el driver implemente el cursor.

------------------------------
### 2. Operaciones masivas del ORM (session.execute con mapeo)
Si estás utilizando ejecuciones masivas del ORM pasando diccionarios (Bulk Updates), el objeto CursorResult sigue teniendo el atributo rowcount, pero puedes estructurar la consulta para que devuelva las entidades directamente.
Si usas el método heredado de SQLAlchemy 1.x a través de la sesión (solo si no has migrado completamente a las sentencias 2.0 estilo update()):
```python
# Estilo antiguo/transicional (devuelve directamente el conteo como entero)
cantidad = db.query(Usuario).filter(Usuario.activo == False).update({"por_depurar": True})
```

* 
* Nota importante: En SQLAlchemy 2.0 puro, el uso de db.query() está obsoleto en favor de select() y update(), por lo que se desaconseja esta opción para proyectos nuevos.
* 

------------------------------
### 3. Ejecución multifila (executemany) con rowcount agrupado
Si estás ejecutando una actualización pasando una lista de parámetros para actualizar múltiples registros individuales en un solo viaje a la base de datos:

```python
stmt = update(Usuario).where(Usuario.id == bindparam("b_id")).values(nombre=bindparam("b_nombre"))
valores = [
    {"b_id": 1, "b_nombre": "Juan"},
    {"b_id": 2, "b_nombre": "Pedro"}
]
result = await db.execute(stmt, valores)
cantidad = result.rowcount  # Devolverá la suma total de filas afectadas por toda la lista
```
------------------------------
### Tabla comparativa de enfoques

| Método | Capa | ¿Cuándo usarlo? | Ventaja principal |
|---|---|---|---|
| result.rowcount | Core | Actualizaciones rápidas donde no importan los datos modificados. | No consume memoria extra. |
| len(result.all()) + RETURNING | ORM / Core | Cuando necesitas verificar qué IDs o datos cambiaron exactamente. | 100% consistente entre bases de datos. |
| .update() en db.query() | ORM (v1.x) | Código antiguo en proceso de migración. | Devuelve un entero directamente. |
_____
## Setup de Gemini para aync: (no validado)
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

### 1. Definir la Base y el Motor
class Base(DeclarativeBase):
    pass

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL)

app = FastAPI()

### 2. ?? Evento de inicio para crear las tablas
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # AQUÍ se ejecuta el comando para crear la base de datos
        await conn.run_sync(Base.metadata.create_all)
