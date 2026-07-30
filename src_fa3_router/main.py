from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, admin, users


app = FastAPI()

# --- CREATE SQLITE DB
models.Base.metadata.create_all(bind=engine)

# --- Include routes
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
