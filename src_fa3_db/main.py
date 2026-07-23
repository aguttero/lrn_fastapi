from fastapi import FastAPI
import models
from database import engine

app = FastAPI()

# --- CREATE SQLITE DB
models.Base.metadata.create_all(bind=engine)
