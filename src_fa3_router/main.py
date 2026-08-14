from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import Request
import models
# import src_fa3_router.models as models
# from src_fa3_router.models import Base

from database import engine
from routers import auth, todos, admin, users

app = FastAPI()
# --- CREATE SQLITE DB
models.Base.metadata.create_all(bind=engine)
# Base.metadata.create_all(bind=engine)

# JINJA Template directory
templates = Jinja2Templates(directory="templates")

#JINJA Test endpoint
@app.get("/")
def jinja_test(request: Request):
    # return templates.TemplateResponse("home.html", {'request':request})
    # return templates.TemplateResponse(name="home.html", request={"request":request})
    return templates.TemplateResponse(request,"home.html")

# Dev Health Check
@app.get("/healthy")
def health_check():
    return {'status': 'OK Healthy'}

# --- Include routes
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
