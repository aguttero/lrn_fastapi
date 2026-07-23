from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

# 1. Definir la Base y el Motor
class Base(DeclarativeBase):
    pass

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL)

app = FastAPI()

# 2. Evento de inicio para crear las tablas
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # AQUÍ se ejecuta el comando para crear la base de datos
        await conn.run_sync(Base.metadata.create_all)
