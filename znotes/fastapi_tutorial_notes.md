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
