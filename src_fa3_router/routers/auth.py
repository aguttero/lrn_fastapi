from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from models import User
import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
# from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import jwt
from datetime import timedelta, datetime, timezone

# Fastapi 2 Jinja integration setup
from fastapi import Request
from fastapi.templating import Jinja2Templates


# --- ROUTE from MAIN FastAPI APP
# remember to include this module in main.py
router = APIRouter(prefix='/auth', tags=['auth'])

# JWT Config
# Generated with
# openssl rand -hex 32
SECRET_KEY = "3ad1d79be2cf2be4f56a15be94eb4c6e429ce8e9878fa6807908ac30a0df731d"
ALGORITHM = "HS256"

# Oauth Config
# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token") -> calls the api endpoint
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token") #added auth/ after adding prefix setting to router


# --- Pydantic class defintion
class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name : str
    last_name : str
    password : str
    role : str


class Token(BaseModel):
    access_token: str
    token_type: str

# --- DB session definition
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="templates")

### Pages ###

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse(request,"login.html")

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse(request,"register.html")

### Endpoints ###
def hash_pwd (plain_pwd: str) -> str:
    pwd_bytes = plain_pwd.encode('utf-8')
    salt = bcrypt.gensalt(rounds=4)
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_bytes.decode('utf-8')

def authenticate_user(username: str, password: str, db): #db -> Session already created inside api endpoint
    # fetch user
    stmt = select(User).where(User.username == username)
    found_user_record = db.scalar(stmt)   #scalar returns first or none.

    if not found_user_record:
        return False
    pwd_bytes = password.encode('utf-8')
    hash_bytes = found_user_record.hashed_password.encode('utf-8')
    if not bcrypt.checkpw(pwd_bytes, hash_bytes):
        return False
    # return True
    return found_user_record

# JWT Encoding
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# JWT Decoding
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            print("raise error -> get_current_user inside try: - user missing data")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

        return {'username': username, 'id': user_id, 'user_role': user_role}
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')




# @router.post("/auth", status_code=status.HTTP_201_CREATED) # removed /auth after adding prefix setting to router, to avoid the /auth/auth
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    # No se puede usar el truco de User (**create_user_request.model_dump()) porque en el dict tengo 'password' y en DB model 'hashed_password'
    new_user_record = User(
        email= create_user_request.email,
        username= create_user_request.username,
        first_name= create_user_request.first_name,
        last_name= create_user_request.last_name,
        hashed_password= hash_pwd(create_user_request.password),
        is_active= True,
        role= create_user_request.role
    )
    db.add(new_user_record)
    db.commit()

    # --- DB.Refresh fuerza un nuevo select en la DB
    db.refresh(new_user_record)
    # print (f"new_record= {new_user_record}")
    # return {"user": "authenticated"}
    return new_user_record

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    # TEST CODE
    user = form_data.username
    plain_pwd = form_data.password
    print(f"usuario= {user}")
    print(f"pwd= {plain_pwd}")
    # END TEST CODE
    user = authenticate_user(form_data.username, form_data.password, db)
    print (f"User={user}")
    if not user:
        # return 'Failed Authentication'
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
