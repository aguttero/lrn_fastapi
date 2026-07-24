from fastapi import FastAPI
import models
from database import engine, SessionLocal

app = FastAPI()

# --- CREATE SQLITE DB
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
