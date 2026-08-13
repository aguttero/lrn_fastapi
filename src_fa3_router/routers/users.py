from fastapi import APIRouter, Depends, status, HTTPException, Path
from pydantic import BaseModel, Field
from database import SessionLocal
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from .auth import get_current_user
from models import User
import bcrypt

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency Config
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)] # add from .auth import get_current_user

# Pydantic Class Definition
class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6 )



# Get user info in DB record
@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependency, db: db_dependency):
    # print (f"User= {user}")
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    stmt = select(User).where(User.id == user.get('id'))
    found_record = db.scalar(stmt)

    # User Not found Exception Handling:
    if not found_record:
         raise HTTPException(status_code=404, detail="Item not found")

    return found_record

# Update user password
# Validate current password
# Allow to update password (FETCH AND UPDATE)
# Usa FETCH and UPDATE si necesitas hacer validaciones complejas con los datos viejos del usuario
# antes de guardarlo.

@router.put ('/password', status_code=status.HTTP_202_ACCEPTED)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):

    # User not found Exception
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    stmt = select(User).where(User.id == user.get('id'))
    user_record = db.scalar(stmt)

    # print(f"User_record.hash = {user_record.hashed_password}")

    # User Password verification
    #if not passowrd verify():
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error on password change')

    old_pwd_txt = user_verification.password
    new_pwd_txt = user_verification.new_password

    old_pwd_bytes = old_pwd_txt.encode('utf-8')
    old_hash_btyes = user_record.hashed_password.encode('utf-8')

    # validate old password
    if not bcrypt.checkpw(old_pwd_bytes, old_hash_btyes):
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail='Error on password change')

    # else update password
    # can call hast_pwd (pwd_txt) -> str hash from .auth.py
    new_pwd_bytes = new_pwd_txt.encode('utf-8')
    salt = bcrypt.gensalt(rounds=4)
    new_hash_bytes = bcrypt.hashpw(new_pwd_bytes, salt)
    new_hash_txt = new_hash_bytes.decode('utf-8')

    # Update new hash in DB
    # como ya trajimos el record con un select el update se puede hacer simple:
    user_record.hashed_password = new_hash_txt
    db.commit()

    return {'message': 'transaction ok'}


# UPDATE sin FETCH - SAMPLE GEMINI
# mejor rendimiento, ejecuta cambio directamente en la base de datos en un solo viaje
# sin necesidad de traer el registro primero.
from sqlalchemy import update

async def actualizar_telefono_usuario(db: db_dependency, usuario_id: int, nuevo_nombre: str):
    # 1. Construir la sentencia UPDATE apuntando a un solo campo (.values)
    stmt = (
        update(User)
        .where(User.id == usuario_id)
        .values(first_name=nuevo_nombre)  # <--- Solo modificas este campo
    )

    # 2. Ejecutar la sentencia
    result = db.execute(stmt)

    # 3. Validar si el registro existía (opcional pero recomendado)
    if result.rowcount == 0:
        return {"error": "Usuario no encontrado"}

    # 4. Confirmar la transacción
    db.commit()

    return {"status": "success", "message": "Teléfono actualizado"}
