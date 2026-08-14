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

## Folder Structure Best Practice
La mejor práctica para organizar un proyecto de FastAPI basado en módulos es seguir una estructura orientada a características (feature-based) o por dominios. Esto agrupa los archivos por su funcionalidad de negocio en lugar de su tipo técnico, lo que facilita enormemente la escalabilidad.

mi_proyecto_fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Punto de entrada de la aplicación
│   ├── config.py                # Configuración y variables de entorno
│   ├── database.py              # Sesión y configuración de la base de datos
│   │
│   ├── core/                    # Funcionalidades compartidas en todo el sistema
│   │   ├── __init__.py
│   │   ├── security.py          # Hashing de contraseñas, tokens JWT
│   │   └── dependencies.py      # Dependencias globales (ej. obtener DB)
│   │
│   └── modules/                 # Directorio de módulos por características
│       ├── users/               # Módulo de Usuarios
│       │   ├── __init__.py
│       │   ├── router.py        # Endpoints (APIRouter)
│       │   ├── models.py        # Modelos ORM (SQLAlchemy, Tortoise, etc.)
│       │   ├── schemas.py       # Modelos Pydantic (Validación de datos)
│       │   ├── services.py      # Lógica de negocio pesada
│       │   └── dependencies.py  # Dependencias específicas del módulo
│       │
│       └── items/               # Módulo de Ítems (Ejemplo de otro dominio)
│           ├── __init__.py
│           ├── router.py
│           ├── models.py
│           ├── schemas.py
│           └── services.py
│
├── tests/                       # Pruebas unitarias y de integración
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
│
├── .env                         # Variables de entorno locales
├── .gitignore
├── README.md
└── requirements.txt             # o pyproject.toml / Pipfile

### Reglas Clave y Buenas Prácticas
* Agrupación por dominio: Mantén todo lo relacionado con una característica (users, products, orders) dentro de su propia carpeta. Si eliminas una característica, solo borras esa carpeta.
* Separación de Modelos y Schemas: Usa models.py estrictamente para la base de datos (ORM) y schemas.py para los modelos de Pydantic que validan la entrada y salida de la API.
* Lógica en Servicios: No satures los archivos router.py con lógica de negocio compleja ni consultas directas a la base de datos. Crea un archivo services.py para manejar esas operaciones.
* Enrutador Centralizado: Cada módulo exporta un APIRouter en su archivo router.py. Luego, todos estos enrutadores se importan e integran en el archivo app/main.py usando app.include_router().
* Uso de Imports Absolutos: Configura siempre tus imports desde la raíz del proyecto (ej. from app.modules.users.models import User) en lugar de usar paths relativos (from .models import User). Esto evita errores cuando el proyecto crece.


## PIP Deploy to Fastapi Cloud
pip install "fastapi[standard]"
pip freeze > requirements.txt
fastapi login
fastapi deploy


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

# Sync vs Async en FastAPI
FastAPI brilla justamente por su manejo nativo de programación asincrónica. Como ya conoces Python básico, piénsalo en términos de optimización de recursos y tiempos de espera de la CPU.

## 🌟 Concepto clave: El mozo del restaurante

* Sincrónico (def): Un mozo toma el pedido de una mesa, va a la cocina, espera a que cocinen el plato sin hacer nada más, y luego lo sirve. Las demás mesas esperan completamente bloqueadas.

* Asincrónico (async def): El mozo toma el pedido, lo deja en la cocina y, mientras los cocineros preparan la comida, atiende a otras mesas. Aprovecha el tiempo muerto de espera.

## ⏸️ Sincrónico en FastAPI
Se define con funciones estándar def. Bloquea el hilo de ejecución por cada solicitud entrante.

* Cuándo usarlo: Tareas puras de CPU que no involucran esperas externas.
* Ejemplos: Operaciones matemáticas complejas, manipulación de imágenes, parsing de JSON pesado.
* Código Junior:
```python
@app.get("/calcular")def calcular_impuesto(monto: float):
    # La CPU trabaja activamente sin parar
    return {"total": monto * 1.19}
```

## ⚡ Asincrónico en FastAPI
Se define con async def y libera el control usando la palabra clave await cuando hay operaciones de Entrada/Salida (I/O). [1] 

* Cuándo usarlo: Tareas bloqueantes por redes o discos donde la CPU se queda esperando una respuesta externa.
* Ejemplos: Consultas a bases de datos, llamadas a APIs de terceros (ej. Stripe o OpenAI), leer archivos grandes.
* Código Junior:
```python
@app.get("/perfil")async def obtener_usuario(user_id: int):
    # await pausa esta función y libera a FastAPI para atender otros requests
    usuario = await db.fetch_user(user_id) 
    return usuario
```

## 📈 Perspectiva de Negocio: ¿Por qué importa?

* Reducción de costos: Un solo servidor asincrónico con FastAPI puede procesar miles de solicitudes simultáneas que antes requerían múltiples servidores sincrónicos.
* Mejor experiencia de usuario: Tu aplicación no se "congela" para el Usuario B mientras el Usuario A está descargando un reporte pesado.
* Escalabilidad: Ideal para arquitecturas modernas de microservicios y consumo intensivo de APIs de Inteligencia Artificial.


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

# Cryptography standards
## Industry Comparison Matrix
you must implement the right cryptographic standards based on your industry's compliance laws.

Here is the direct blueprint of the hashing, password storage, and JWT standards required across major sectors.

| Industry | Password Hashing Standard | Data Encoding / Encryption | JWT Signing Algorithm | Compliance Framework |
|---|---|---|---|---|
| FinTech & Banking | Argon2id (or PBKDF2) | Base64URL / AES-GCM | Asymmetric (RS256 / ES256) | PCI-DSS & GLBA |
| Healthcare & HealthTech | Argon2id (or bcrypt) | Base64URL / AES-GCM | Asymmetric (RS256 / ES256) | HIPAA & HITECH |
| E-Commerce & Retail | bcrypt (or Argon2id) | Base64URL / AES-256 | Symmetric (HS256) ok for internal | PCI-DSS (v4.0) |
| SaaS & B2B Enterprise | Argon2id | Base64URL / AES-GCM | Asymmetric (RS256) preferred | SOC2 & ISO 27001 |

------------------------------
## 1. Password Storage (Hashing)
Never let your junior devs use fast algorithms like MD5, SHA-1, or SHA-256 for passwords. Attackers can guess billions of these per second. You need key-stretching, resource-intensive algorithms.

* 
* Argon2id: The gold standard for FinTech, SaaS, and Healthcare. It won the Password Hashing Competition. It uses both memory and CPU time, making hardware-accelerated attacks (like GPUs) useless.
* bcrypt: Perfect for E-Commerce and general startups. It is slow, highly secure, and has been a reliable industry standard for decades.
* PBKDF2: Still accepted by legacy banking compliance (PCI-DSS), but newer projects should favor Argon2id.
* Developer Tip for Your Team: Tell your junior dev to use a library like bcrypt or argon2-cffi and let the library handle the auto-generation of a unique salt for every single password.

### OWASP recommendations
The OWASP Cheat Sheet Series and RFC 9106 outline baseline parameters. However, as a business entrepreneur, your configurations must balance attack mitigation (security) against hardware costs and authentication delays (user experience) according to your industry’s threat profile
https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
https://datatracker.ietf.org/doc/html/rfc9106

### General Baseline (Global Standards)
Before looking at specific industries, your junior dev must apply these universal cryptographic constants across all applications: 
* Salt Length: Minimum 16 bytes (128 bits) generated by a cryptographically secure random number generator (CSPRNG).
* Hash Length: 32 bytes (256 bits) for the output string.
* Parallelism (\(p\)): Set equal to double the number of available CPU cores assigned to the auth process, though a baseline of \(p=1\) or \(p=4\) is common depending on the programming library's defaults.

### Industry-Specific Argon2id Parameter Profiles

#### 🏦 FinTech, Crypto, & Banking (High Defense Profile)
FinTech demands the highest possible defense against well-funded offline brute-force attacks using custom ASICs or massive GPU rigs. This configuration deliberate scales up memory to make parallel hardware cracking economically unfeasible. [9, 10] 

* Memory ($m$): 64 MiB ($65,536$ KiB) (or up to 256 MiB if hosted on dedicated auth hardware).
* Time / Iterations ($t$): 3 to 4 passes.
* Parallelism ($p$): 4 threads (adjust to match your core availability).
* Business Impact: Hashing will take roughly 200ms - 500ms per login. It prevents cheap automated brute-forcing but requires you to monitor API rate limits to block DoS (Denial of Service) attacks targeting your login endpoint. [4, 6, 8, 11] 

#### 🏥 Healthcare & HealthTech (Strict Compliance / HIPAA Profile)
Healthcare requires maximum defense while maintaining strict system availability and predictable server loads to ensure medical staff face no authentication lag. [12] 

* Memory ($m$): 46 MiB ($47,104$ KiB).
* Time / Iterations ($t$): 1 pass.
* Parallelism ($p$): 1 thread.
* Business Impact: This exact profile is highly favored because $t=1$ reduces CPU usage while the $46 \text{ MiB}$ RAM cost keeps it highly memory-hard. It offers an exceptional security-to-performance balance for systems handling protected health information (PHI). [4, 9, 13] 

#### 🛒 E-Commerce & Retail (High Concurrency / Low Latency Profile)
E-commerce platforms handle massive bursts of traffic (e.g., Black Friday deals). If a server spends too much RAM or time hashing a single login, the checkout funnel slows down, directly hurting your revenue.

* Memory ($m$): 19 MiB ($19,456$ KiB).
* Time / Iterations ($t$): 2 passes.
* Parallelism ($p$): 1 thread.
* Business Impact: This is the absolute minimum baseline recommended by OWASP. It keeps the execution time ultra-fast (often under 50ms), preventing your web servers from running out of RAM during high-volume consumer events. [4, 5] 

#### 💻 SaaS & B2B Enterprise (Balanced / Multi-Tenant Profile)
SaaS infrastructures must withstand B2B vendor security assessments (like SOC2 Type II) without breaking the bank on infrastructure scaling costs.

* Memory ($m$): 32 MiB ($32,768$ KiB).
* Time / Iterations ($t$): 3 passes.
* Parallelism ($p$): 2 threads.
* Business Impact: Provides clean middle-ground parameter settings that sail through enterprise security audits while preserving resources across multi-tenant database clusters.

------------------------------
### Summary Checklist for Code Reviews
When reviewing your junior dev’s pull request, look out for these pitfalls:

   1. Hardcoded Parameters: Ensure memory, time, and parallelism are kept in environment variables or configuration files, not hardcoded in application scripts. This makes future cryptographic upgrades easy. [7, 14] 
   2. Using Default Packages Blindly: Some older programming libraries default to Argon2i or Argon2d. Force your developer to explicitly pass Argon2id in the initialization code. [9] 

------------------------------
#### References

[1] [https://guides.adobe.com](https://guides.adobe.com/content/coldfusion-docs/en/docs/introduction-to-coldfusion/__references__/hash-and-verify-passwords-in-coldfusion.html)
[2] [https://theproductguy.in](https://theproductguy.in/blogs/argon2-tuning-guide/)
[3] [https://theproductguy.in](https://theproductguy.in/blogs/argon2-tuning-guide/)
[4] [https://community.bitwarden.com](https://community.bitwarden.com/t/argon2id-settings-higher-values-better/70073)
[5] [https://cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
[6] [https://www.reddit.com](https://www.reddit.com/r/crypto/comments/pk5bw6/rfc_9106_argon2_memoryhard_function_for_password/)
[7] [https://bellatorcyber.com](https://bellatorcyber.com/blog/best-password-hashing-algorithms-of-2023)
[8] [https://cryptopp-modern.com](https://cryptopp-modern.com/docs/api/kdf/argon2/)
[9] [https://arxiv.org](https://arxiv.org/html/2504.17121v2)
[10] [https://cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
[11] [https://www.reddit.com](https://www.reddit.com/r/cryptography/comments/1jwon09/what_are_the_recommended_argon2_parameters/)
[12] [https://www.appsecmaster.net](https://www.appsecmaster.net/blog/owasp-secure-coding-practices/)
[13] [https://crypto.stackexchange.com](https://crypto.stackexchange.com/questions/62043/argon2-memory-setting-lower-bound)
[14] [https://medium.com](https://medium.com/@felixtwoli21/why-developers-should-stop-hashing-passwords-and-start-using-kdfs-0be0da663393)
[15] [https://toolsana.com](https://toolsana.com/blog/password-hashing-2026-bcrypt-argon2-scrypt-pbkdf2-guide/)




------------------------------
## 2. JSON Web Tokens (JWT) Standards
JWTs are used for stateless authentication. In a business environment, how you sign these tokens dictates your system's architecture security.

* 
* Encoding standard: All JWTs inherently use Base64URL encoding for the Header and Payload. Remind your junior dev: Base64URL is for transmission, NOT for secrecy. Anyone can decode a JWT payload online. Never put plain social security numbers or credit cards inside it. [1] 
* Symmetric Signing (HS256): Uses a single secret key to both sign and verify tokens.
* Best for: E-Commerce or single-monolith SaaS apps.
   * Risk: If an attacker steals the secret key from any microservice, they can forge fake admin tokens.
* Asymmetric Signing (RS256 / ES256): Uses a private key to sign the token (held tightly by your Auth server) and a public key to verify it (shared with your microservices).
* Best for: FinTech, Healthcare, and Complex SaaS architectures.
   * Benefit: Even if a microservice is hacked, the attacker only gets the public verification key. They cannot forge new tokens. [2] 
* 

------------------------------
## 3. Data Encoding vs. Encryption
Junior developers frequently confuse encoding with encryption. Keep this rule clear in your code reviews:

* 
* Base64 / Base64URL: This is Encoding. It translates binary data into readable ASCII text for web URLs. It provides zero security.
* AES-256-GCM: This is Authenticated Encryption. Use this standard across all industries when you need to store sensitive data at rest (like medical notes under HIPAA or bank routing numbers) that you need to decrypt later.
* 

------------------------------
To help you guide your team on the next implementation steps, let me know:

* 
* What is the specific industry of your startup?
* What backend language or framework (e.g., Node.js, Python, Go) is your junior dev using?
* Will your system use a monolith architecture or distributed microservices?
* 


[1] [https://oasishack.medium.com](https://oasishack.medium.com/jwt-desde-0-b9ae18c8763d)
[2] [https://oasishack.medium.com](https://oasishack.medium.com/jwt-desde-0-b9ae18c8763d)


# JWT Tokens
## jwt decoder: jwt.io
## JWT en python
La forma moderna, oficial y recomendada por la documentación de FastAPI para generar JSON Web Tokens (JWT) en Python es utilizando la librería PyJWT.Si vienes de tutoriales antiguos (anteriores a 2024), notarás que casi todos usaban una librería llamada python-jose. Sin embargo, python-jose quedó completamente obsoleta y abandonada, por lo que todo el ecosistema moderno se migró a PyJWT

## pyjwt setup
pip install pyjwt
https://pyjwt.readthedocs.io/en/stable/

## JWT Code example:
#### pyjwt page:
```python
import jwt
encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
{'some': 'payload'}
```
https://pyjwt.readthedocs.io/en/stable/usage.html

#### Gemini 1
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

#### Gemini 2
```python
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

app = FastAPI()

# 1. Instanciamos el esquema de seguridad nativo
security_scheme = HTTPBearer()

SECRET_KEY = "tu_clave_secreta_super_segura"
ALGORITHM = "HS256"

class UserTokenData(BaseModel):
    username: str

# 2. Creamos la función de dependencia para validar el token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = credentials.credentials # Extrae el string del token
    try:
        # Validamos la firma y expiración de forma criptográfica usando PyJWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token no contiene el usuario (sub claim)",
            )
        return UserTokenData(username=username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

# 3. Protegemos la ruta inyectando la dependencia
@app.get("/users/me")
def read_current_user(current_user: UserTokenData = Depends(get_current_user)):
    return {"message": f"Hola, {current_user.username}. Tienes acceso."}
```

### PyJWT Exception handling
The modern equivalent of catching JWTError from python-jose depends on whether you want to catch all token failures or specifically isolate expiration versus malformed tokens.

In PyJWT, the modern approach uses jwt.exceptions.InvalidTokenError as the generic replacement for JWTError, alongside more specialized classes.

1. The Direct Replacement (Catch-All)To catch any validation failure—such as an invalid signature, malformed token structure, or an expired timestamp—use jwt.exceptions.InvalidTokenError

```python
import jwt

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
except jwt.exceptions.InvalidTokenError:
    # This catches expired tokens, bad signatures, and malformed structures
    raise HTTPException(status_code=401, detail="Invalid or expired token")
```

2. The Granular Approach (Best Practice)In modern API development, you usually want to give the client explicit feedback if a token is simply expired (so they know to use a refresh token) versus when a token is completely corrupted or forged.You can chain PyJWT's granular exceptions like this:

```python
import jwt
from fastapi import HTTPException, status

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    
except jwt.exceptions.ExpiredSignatureError:
    # Token is valid but past its 'exp' claim timestamp
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Token has expired"
    )
    
except jwt.exceptions.InvalidTokenError:
    # Catches DecodeError, InvalidSignatureError, etc.
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid token credentials"
    )
```

####PyJWT Exception Mapping Summary
Old python-jose Class | Modern PyJWT Equivalent | ReasonRaised
JWTError | jwt.exceptions.InvalidTokenError | Base class for decoding failures.
ExpiredSignatureError | jwt.exceptions.ExpiredSignatureError | Time limits (exp) exceeded.
JWTClaimsError | jwt.exceptions.InvalidIssuerError / InvalidAudienceError | Mismatch on iss or aud verification.

____
## Conceptos Clave para el Negocio y Arquitectura
 hay tres detalles cruciales que diferencian a un desarrollador junior de uno que entiende la arquitectura del negocio:
 * Sustitución de Librería: Asegúrate de instalar la correcta: pip install pyjwt. En tu código se importa simplemente como import jwt.
 * Timezones Explícitas: El uso de datetime.utcnow() fue marcado como obsoleto en las versiones recientes de Python. La forma moderna obliga a usar datetime.now(timezone.utc) para evitar errores de desincronización de horas si tu servidor está en un país y tu base de datos en otro.
 * El contenido del Payload: Al generar el token en la ruta /token que construimos antes, lo ideal es pasar únicamente datos de identificación que no cambien seguido (como el ID del usuario o su correo). Nunca pongas contraseñas ni datos sensibles dentro del JWT, ya que el token viaja cifrado pero es fácilmente legible (decodificable) por cualquiera que lo intercepte; la firma solo garantiza que nadie lo haya alterado.
