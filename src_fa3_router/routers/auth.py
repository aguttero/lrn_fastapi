from fastapi import APIRouter
from pydantic import BaseModel
from models import User


# --- ROUTE from MAIN FastAPI APP
# remember to include this module in main.py
router = APIRouter()

class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name : str
    last_name : str
    password : str
    role : str


@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest):
    # No se puede usar el truco de User (**create_user_request.model_dump()) porque en el dict tengo 'password' y en DB model 'hashed_password'
    new_user_record = User(
        email= create_user_request.email,
        username= create_user_request.username,
        first_name= create_user_request.first_name,
        last_name= create_user_request.last_name,
        hashed_password= create_user_request.password,
        is_active= True,
        role= create_user_request.role
    )

    return new_user_record


    return {"user": "authenticated"}
