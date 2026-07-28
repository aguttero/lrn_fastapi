# FastAPI udemy complete course 2026 coding with roby
## Documentation
https://fastapi.tiangolo.com/

## Architecture
Popular:
1. web server - Front End (Node / Next)
2. Fast API Server - Backend logic
3. dependencies:
  - Fast API
  - Uvicorn -> Web Server

Fast Dev and prototype:
Fast API can also work as a full stack app

## installation PIP
python3 -m venv .venv
pip install fastapi ?standard? for production?
pip install "uvicorn[standard]" -> web server production version

## run server
### uvicorn command
uvicorn python_file:app --reload -> reload allows for refresh in code and auto reload of web server

### fastapi prod and dev start:
* Requires pip install "fastapi[standard]"
1. Prod
fastapi run python_file.py -> prod
2. dev
fastapi dev python_file.py -> dev

# Standard HTTP Status Codes
## 1xx Information Response: Request Processing
## 2xx Success: Req Successfully complete
## 3xx Redirection: Further action must be complete
## 4xx Client errors: An error was caused by the client
## 5xx Server errors: An error ocurred on the server

# SQLA 2 Tutorial DB Setup
## 1. create engine
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

## 2. Use Session as connection model
https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-query-usage


# Sampple SQLA DB Setup
## Sync configuration 
1. Declare Models
  from typing import List, Optional
  from sqlalchemy import ForeignKey, 
  from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

  class Base(DeclarativeBase)
    pass
  class User(Base):
    __tablename__ = "user_table"
    id: Mapped[int] = mapped_column(primary_key = True)

    def __repr__(self) -> str:
      return f"user.id={self.id!r} ... "

2. Create an Engine
  from sqlalchemy import create_engine
  engine = create_engine("sqlite:///./filename.db", echo=True)

3. Create Table DDL
  Base.metadata.create_all(bind=engine)

# SQLA Sync vs Async
La diferencia fundamental entre el código síncrono y el asíncrono radica en cómo el programa maneja el tiempo de espera cuando realiza tareas lentas, como consultar una base de datos o llamar a una API externa.
Aquí tienes la explicación detallada de cada enfoque:
------------------------------
## 1. Código Síncrono (Secuencial o Bloqueante)
El código se ejecuta en orden estricto, línea por línea. Si una línea de código tarda en responder, todo el programa se detiene y espera a que termine antes de pasar a la siguiente instrucción. [1, 2, 3, 4] 

* Metáfora: Imagina que vas a un restaurante donde solo hay un camarero. Él toma tu pedido, va a la cocina, se queda parado esperando a que el cocinero prepare tu comida, te la sirve y recién ahí pasa a atender al siguiente cliente de la fila.
* Pros: Es muy fácil de escribir, leer y depurar porque el flujo de lógica es predecible. [5, 6] 
* Contras: Poco eficiente para servidores web. Si un usuario hace una consulta lenta a la base de datos, los demás usuarios tendrán que esperar a que esa consulta termine para que el servidor responda sus peticiones.

------------------------------
## 2. Código Asíncrono (No Bloqueante)
Permite que el programa inicie una tarea larga y, en lugar de quedarse congelado esperando el resultado, continúe ejecutando otras tareas pendientes. Cuando la tarea larga finaliza, el programa regresa a ella para procesar el resultado. [7, 8, 9] 

* Metáfora: En un restaurante eficiente, el camarero toma tu pedido, lo pasa a la cocina y va inmediatamente a atender a otras mesas mientras tu comida se cocina. Cuando tu plato está listo, el camarero regresa para servírtelo.
* Pros: Permite que un solo servidor maneje miles de peticiones simultáneas con muy pocos recursos, ya que el procesador nunca está "ocioso" esperando respuestas de la base de datos o de la red.
* Contras: El código es más complejo de estructurar. Requiere entender conceptos como async, await y promesas, y si cometes un error, puede ser más difícil de depurar. [10, 11, 12] 

------------------------------
## Resumen Comparativo

| Característica | Síncrono | Asíncrono |
|---|---|---|
| Flujo | Bloqueante (Línea por línea) | No bloqueante (Multitarea) |
| Tiempo de espera | Desperdiciado (El hilo se congela) | Aprovechado (Atiende otras tareas) |
| Complejidad | Baja y fácil de entender | Media-Alta (async/await) |
| Ideal para... | Scripts simples, tareas de CPU intensivas (cálculos matemáticos, procesamiento de imágenes) | Aplicaciones web (FastAPI, Node.js), APIs, apps con mucho tráfico y consultas a bases de datos |

## En el contexto de FastAPI y SQLAlchemy

* Síncrono: Usas def en tus rutas y SessionLocal() normal. Cada petición bloquea un hilo del servidor.
* Asíncrono: Usas async def en tus rutas y AsyncSessionLocal(). Mientras la base de datos busca la información, el servidor FastAPI queda libre para recibir y procesar peticiones de otros usuarios.

¿Estás evaluando cuál de los dos enfoques elegir para la arquitectura de tu API actual? Cuéntame qué tipo de base de datos usarás y cuántos usuarios estimas que consumirán tu aplicación para ayudarte a decidir.

# SQLA Return data: db.get() vs db.refresh():
 db.get() vs db.refresh():The Big DifferenceWhile both can result in a SQL query, they serve opposite purposes:db.get() tries to avoid the database: It prefers to use the local memory cache to save time. It only hits the database if it absolutely has to.db.refresh() forces a database lookup: It completely ignores the local memory cache. It deliberately wipes out whatever is in your Python memory and pulls a fresh copy straight from the database columns.

# SQLA Delete record
To delete a record in SQLAlchemy V2, you have two primary methods: fetching the record first and deleting it via the session, or using the modern V2 bulk delete() statement

# SQLA Scalar, Scalars, one, all, etc

In SQLAlchemy V2, choosing between scalar(), scalars(), and scalar_one() depends entirely on how many rows you expect the database to return, and how you want your app to handle missing or duplicate data.
First, understand what "scalar" means: It tells SQLAlchemy to unpack the raw database row tuple and give you the individual Python object (like a Todo instance) directly.
Here is the exact guide on when to use each method when running a select().where() query:
------------------------------
## 1. db.scalars(statement)

* What it returns: An iterable collection (a stream of multiple objects).
* When to use it: When your query can return zero, one, or many rows. This is your default choice for fetching lists.
* Example: Getting all completed todos. [1, 2, 3, 4] 

statement = select(Todo).where(Todo.completed == True)results = db.scalars(statement).all()  # Returns a List[Todo] (could be empty)

## 2. db.scalar(statement)

* What it returns: A single object, or None.
* When to use it: When you are looking for a specific item that might not exist, or you only care about the first match. If the database finds multiple rows, it safely returns the first one without crashing.
* Example: Fetching a user by email, or a todo by ID where you want to handle a missing item manually. [5, 6, 7, 8] 

statement = select(Todo).where(Todo.id == todo_id)todo = db.scalar(statement)  # Returns a Todo instance OR None
if not todo:
    raise HTTPException(status_code=404)

## 3. db.scalars(statement).one()

* What it returns: A single object. [9] 
* When to use it: When the item must exist, and it is a critical error if it doesn't. [10] 
* The Catch:
* If 0 rows are found, it raises a NoResultFound exception.
   * If 2 or more rows are found, it raises a MultipleResultsFound exception. [11, 12] 
* Example: Internal system lookups where data integrity guarantees the row is there.

try:
    statement = select(Todo).where(Todo.id == todo_id)
    todo = db.scalars(statement).one()except NoResultFound:
    print("This should never happen based on our database logic!")

## 4. db.scalars(statement).one_or_none()

* What it returns: A single object, or None.
* When to use it: When a duplicate row is a severe database error, but a missing row is completely normal.
* The Catch: It returns None safely if 0 rows are found, but it will still raise a MultipleResultsFound exception if more than one row matches your criteria.
* Example: Checking if a unique username is taken during registration. [13, 14, 15, 16] 

statement = select(User).where(User.username == "john_doe")user = db.scalars(statement).one_or_none()
if user:
    raise HTTPException(status_code=400, detail="Username already taken")

------------------------------
## Summary Cheat Sheet

| Method | 0 Rows Found | 1 Row Found | 2+ Rows Found | Best Use Case |
|---|---|---|---|---|
| db.scalars(...).all() | Returns [] | Returns [Obj] | Returns [Obj, Obj] | Fetching lists or search results. |
| db.scalar(...) | Returns None | Returns Obj | Returns First Obj (ignores rest) | Standard FastAPI GET by ID lookups. |
| db.scalars(...).one() | ❌ Crashes | Returns Obj | ❌ Crashes | Strict lookups where data must exist. |
| db.scalars(...).one_or_none() | Returns None | Returns Obj | ❌ Crashes | Checking unique constraints (e.g., registration). |


# Password handling
## bcrypt

Starting in bcrypt 5.0.0, the library officially added native support for Python 3.14 and free-threaded (GIL-less) Python 3.14. This version also introduces strict error handling that blocks a silent security flaw.
bcrypt builds rely on a Rust-based cryptographic engine backend under the hood

In Python 3.14, you should call the library natively. Do not use passlib or other wrappers, which are completely broken on modern bcrypt versions

## Critical 3.14 Upgrades & Best Practices

* 
* Handling the 72-Byte Limit Explicitly: In older versions of bcrypt, text longer than 72 bytes was silently truncated. Starting in modern versions, passing a password longer than 72 bytes raises a ValueError. If your users choose massive passphrases, you must pre-hash the password using hashlib.sha256 before feeding it to bcrypt. [1] 
* Work Factor (Rounds): The default is 12. If your server runs on strong, dedicated modern hardware, test if you can bump this to 13 or 14. Your goal is to target a hashing time of roughly 250ms to 500ms per login request to keep things snappy but secure. [7, 8, 9, 10, 11] 
* Free-Threaded Python 3.14: If you are experimenting with Python 3.14's experimental free-threaded binaries (concurrency without the Global Interpreter Lock), bcrypt >= 5.0.0 ships with full, stable wheel support explicitly compiled to avoid concurrency crashes. [1, 12] 

## sample code
```python
import bcrypt

def hash_user_password(plain_password: str) -> str:
    # 1. Encode text to bytes (bcrypt strictly requires byte strings)
    password_bytes = plain_password.encode('utf-8')
    
    # 2. Generate a salt with a modern cost factor (12 is the production standard)
    salt = bcrypt.gensalt(rounds=12)
    
    # 3. Hash the password and decode the resulting bytes to a UTF-8 string for DB storage
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_user_password(plain_password: str, stored_hash: str) -> bool:
    # Convert string inputs back to bytes for verification
    password_bytes = plain_password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')
    
    # Securely verify (avoids timing attacks)
    return bcrypt.checkpw(password_bytes, hash_bytes)
```

## Cantidad de rounds de Salt
El "Punto Caramelo" (Sweet Spot)El estándar de la industria busca que el proceso de hash tarde entre 100 y 300 milisegundos. Es un pestañeo para un humano, pero una eternidad para una computadora que intenta hackearte.A día de hoy, los valores recomendados son:
* rounds=12: Es el valor por defecto actual en la mayoría de librerías modernas y el balance ideal para servidores web estándar.
* rounds=13 o 14: Ideal si manejas datos extremadamente sensibles (finanzas, salud) y tienes servidores potentes.

## Ejemplo para medir tiempo en python
Puedes usar este pequeño truco de código para ver cuánto tarda tu propia computadora en procesar diferentes rounds:

```python
import bcrypt
import time

password = b"super_secret"

for r in:
    inicio = time.time()
    bcrypt.hashpw(password, bcrypt.gensalt(rounds=r))
    fin = time.time()
    print(f"Rounds {r} tardó: {fin - inicio:.4f} segundos")
```
## Oauth2
pip install python-multipart -> password request form
from fastapi.security import OAuth2PasswordRequestForm
la especificación oficial de OAuth2 exige estrictamente que las credenciales de inicio de sesión (username y password) se envíen codificadas como datos de formulario (application/x-www-form-urlencoded), en lugar de un objeto JSON tradicional. Como Python no puede procesar formularios web de forma nativa, FastAPI necesita la librería externa python-multipart en el ecosistema para interpretar esa petición.

```python
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

@app.post("/token")
async def login(
    # 'Annotated' junto con 'Depends' es la sintaxis moderna de FastAPI
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    # El formulario te provee los campos limpios de forma automática
    usuario = form_data.username
    password_plana = form_data.password

    # Aquí agregarías tu lógica de negocio (buscar en DB y verificar hash con bcrypt)
    if usuario != "admin" or password_plana != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario o contraseña incorrectos"
        )
        
    # Retornas el token en el formato JSON que exige la especificación OAuth2
    return {"access_token": "tu_jwt_token_generado", "token_type": "bearer"}
```

### Resumen para tu perspectiva de Negocio
* Instalación Si instalas FastAPI mediante el comando moderno de entornos virtuales (uv add "fastapi[standard]"), el módulo python-multipart ya viene incluido automáticamente. 
Si usas una instalación mínima, debes agregarlo manualmente con pip install python-multipart.
* Documentación Interactiva Avanzada: Al usar OAuth2PasswordRequestForm, FastAPI habilita de forma automática el botón "Authorize" con el candado en la interfaz de Swagger UI (/docs). Esto permite a tus desarrolladores o clientes probar las rutas protegidas directamente desde el navegador de manera muy profesional.
* Rigidez del Estándar: Aunque como desarrollador junior de Python prefieras enviar JSON (porque es más cómodo de estructurar con Pydantic), romperías la compatibilidad con herramientas universales de autenticación si no utilizas el formato de formulario (multipart/form-data o x-www-form-urlencoded)

# JWT Tokens
## jwt decoder: jwt.io
## JWT en python
La forma moderna, oficial y recomendada por la documentación de FastAPI para generar JSON Web Tokens (JWT) en Python es utilizando la librería PyJWT.Si vienes de tutoriales antiguos (anteriores a 2024), notarás que casi todos usaban una librería llamada python-jose. Sin embargo, python-jose quedó completamente obsoleta y abandonada, por lo que todo el ecosistema moderno se migró a PyJWT

## pyjwt setup
pip install pyjwt
https://pyjwt.readthedocs.io/en/stable/

## JWT Code example:
```python
import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any

# 1. Parámetros de configuración del negocio
SECRET_KEY = "tu_clave_secreta_super_segura_y_larga" # Guardar en variables de entorno
ALGORITHM = "HS256" # El estándar simétrico más común
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

def create_access_token(data: dict) -> str:
    """Genera un token JWT firmado de forma moderna."""
    # Copiamos los datos para no modificar el diccionario original
    payload = data.copy()
    
    # IMPORTANTE: Definir la expiración usando zona horaria UTC explícita (estándar moderno)
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Añadimos los 'claims' (propiedades estándar del protocolo JWT)
    payload.update({
        "exp": expiracion,                 # Expiración (Expiration time)
        "iat": datetime.now(timezone.utc)  # Cuándo fue creado (Issued at)
    })
    
    # Generamos y firmamos el token usando PyJWT
    token_firmado = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return token_firmado
```
## Conceptos Clave para el Negocio y Arquitectura
 hay tres detalles cruciales que diferencian a un desarrollador junior de uno que entiende la arquitectura del negocio:
 * Sustitución de Librería: Asegúrate de instalar la correcta: pip install pyjwt. En tu código se importa simplemente como import jwt.
 * Timezones Explícitas: El uso de datetime.utcnow() fue marcado como obsoleto en las versiones recientes de Python. La forma moderna obliga a usar datetime.now(timezone.utc) para evitar errores de desincronización de horas si tu servidor está en un país y tu base de datos en otro.
 * El contenido del Payload: Al generar el token en la ruta /token que construimos antes, lo ideal es pasar únicamente datos de identificación que no cambien seguido (como el ID del usuario o su correo). Nunca pongas contraseñas ni datos sensibles dentro del JWT, ya que el token viaja cifrado pero es fácilmente legible (decodificable) por cualquiera que lo intercepte; la firma solo garantiza que nadie lo haya alterado.
