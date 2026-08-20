from fastapi import FastAPI
from fastapi import Request
import models
# import src_fa3_router.models as models
# from src_fa3_router.models import Base

from database import engine
from routers import auth, todos, admin, users
# Jinja Setup
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# FAVICON.ICO
from fastapi.responses import FileResponse


app = FastAPI()

# Mount Static Files:
app.mount("/static",StaticFiles(directory="static"), name="static")



# --- CREATE SQLITE DB
models.Base.metadata.create_all(bind=engine)
# Base.metadata.create_all(bind=engine)

# JINJA Template directory
templates = Jinja2Templates(directory="templates")

# FAVICON
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.svg")

#JINJA Test endpoint
@app.get("/")
def jinja_test(request: Request):
    # return templates.TemplateResponse("home.html", {'request':request})
    # return templates.TemplateResponse(name="home.html", request={"request":request})
    return templates.TemplateResponse(request,"home.html")


@app.get("/login")
def jinja_test_login(request: Request):
    # return templates.TemplateResponse(name="home.html", request={"request":request})
    return templates.TemplateResponse(request=request,name="login.html")
    # return templates.TemplateResponse(request,"login.html")


@app.get("/register")
def jinja_test_register(request: Request):
    # return templates.TemplateResponse(name="home.html", request={"request":request})
    return templates.TemplateResponse(request=request,name="register.html")
    # return templates.TemplateResponse(request,"login.html")

# END JINJA TEST ENDPOINT

# Dev Health Check
@app.get("/healthy")
def health_check():
    return {'status': 'OK Healthy'}

# --- Include routes
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
