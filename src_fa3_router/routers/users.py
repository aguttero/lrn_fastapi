from fastapi import APIRouter, Depends, status, HTTPException, Path
from database import SessionLocal
from typing import Annotated
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from .auth import get_current_user
from models import User


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

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    stmt = select(User).where(User.id == user.get('id'))
    found_record = db.scalar(stmt)

    # Exception Handling:
    if not found_record:
         raise HTTPException(status_code=404, detail="Item not found")

    return found_record

# @router.delete("/delete/{item_id}", status_code=status.HTTP_202_ACCEPTED)
# async def delete_item_by_id (user: user_dependency, db: db_dependency, item_id: int = Path(gt=0)):
#     if user is None or user.get('user_role') != 'admin':
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

#     stmt = delete(Todo).where(Todo.id == item_id)
#     result = db.execute(stmt)
#     print(f"Delete Result= {result}")
#     db.commit()

#     #  Check if row was actually deleted (handles 404)
#     if result.rowcount == 0:
#         raise HTTPException(status_code=404, detail="Item not found")

#     # return {"message": "Item deleted succesfully"}
#     return result
