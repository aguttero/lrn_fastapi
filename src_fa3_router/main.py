from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, admin, users


app = FastAPI()

# --- CREATE SQLITE DB
models.Base.metadata.create_all(bind=engine)

# Dev Health Check
@app.get("/healthy")
def health_check():
    return {'status': 'OK Healthy'}

# --- Include routes
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
