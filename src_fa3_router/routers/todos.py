from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status
# from starlette import status
from models import Todo
from database import SessionLocal
from .auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        print("checkpoint get_db")
        yield db
    finally:
        db.close()

# Dependency Config
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)] # add from .auth import get_current_user

class TodoRequest(BaseModel):
    title: str = Field (min_length=3)
    description: str = Field (min_length=3, max_length=100)
    priority: int = Field (gt=0, lt=6)
    complete: bool

# Fetch Proof of Life
@router.get("/pol")
async def pol():
    return  {"message": "pol ok!"}

# Fetch all items by authorized user
@router.get("/",  status_code=status.HTTP_200_OK )
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    # SQLA V1
    # return db.query(Todo).all()
    # SQLA V2
    # stmt = select(Todo)
    stmt = select(Todo).where(Todo.owner_id == user.get('id'))
    result = db.scalars(stmt).all()
    return result

# Fetch Item by id
@router.get ("/todo/{todo_id}", status_code=status.HTTP_200_OK )
async def read_todo_by_id(user: user_dependency ,db: db_dependency, todo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    stmt = select(Todo).where(Todo.id == todo_id, Todo.owner_id == user.get('id'))
    found_record = db.scalar(stmt)

    # Exception Handling:
    if not found_record:
        print("record not found")
        raise HTTPException(status_code=404, detail="Item not found")

    return found_record

# Create item
@router.post ("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo_item (user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    # Pydantic V1
    # new_record = Todo(**todo_request.dict())
    # Pydantic V2
    new_record = Todo(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(new_record)
    db.commit()

    # --- DB.Refresh fuerza un nuevo select en la DB -> para devolver la data en el return a FastAPI
    # db.refresh(new_record)
    # print (f"new_record= {new_record}")
    # return new_record

# Update Item with user authorzation
# SQLA BULK UPDATE:
@router.put ("/todobulk/{todo_id}", status_code=status.HTTP_200_OK)
async def bulk_update_todo_by_id (user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    # Convert incoming data to dictionary
    update_dict = todo_request.model_dump()

    # Build and execute the V2 update statement
    stmt = (update(Todo).where(Todo.id == todo_id, Todo.owner_id == user.get('id')).values(**update_dict))

    result = db.execute(stmt)
    db.commit()

    # Handle unexisisting record:
    print(f"row_count= {result.rowcount}")
    if result.rowcount == 0:
        raise HTTPException (status_code=404, detail="Item not found")

    # Return the updated record - Consumes a select transaction
    # ret_txt = db.get(Todo, todo_id)
    # print (f"bulk update return= {ret_txt}")
    #return ret_txt
    return result # para que pase data significativa hay que usar RETURNING en SQLA STMT

# Update V2 with user Authoriztion - PENDING
# SQLA MERGE UPDATE:
# Inserts if record not found
@router.put("/todomerge/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
async def merge_update_todo_by_id(todo_request: TodoRequest, db: db_dependency,  todo_id: int = Path(gt=0)):

    # 1. Convert to dict and explicitly inject the URL's todo_id into it
    update_dict = todo_request.model_dump()
    update_dict["id"] = todo_id  # Ensures it targets the correct PK

    # 2. Create a temporary model instance (like your POST example)
    updated_record_instance = Todo(**update_dict)

    # 3. Merge it into the session.
    # SQLAlchemy looks up the ID, updates the fields, and returns the managed object.
    try:
        merged_todo = db.merge(updated_record_instance)
        db.commit()
    except Exception:
        raise HTTPException(status_code=404, detail="Update failed")

    # print (f"merged_todo= {merged_todo}")
    # db refresh geenrates a query to the DB - consumes resources - TO use it is a design decision
    db.refresh(merged_todo)
    return merged_todo


# Update V3 - Only one field, without previous fetch
# Gemini Sample Code:

async def update_sample(todo_request: TodoRequest, db: db_dependency, todo_id: int = Path (gt=0)):
    stmt = (
        update(Todo)
        .where(Todo.id == todo_id)
        .values(complete = todo_request.complete)  # <--- Solo modificas este campo
    )

    # 2. Ejecutar la sentencia
    result = db.execute(stmt)

    # 3. Validar si el registro existía (opcional pero recomendado)
    if result.rowcount == 0:
        return {"error": "Item no encontrado"}

    # 4. Confirmar la transacción
    db.commit()

    return {"status": "success", "message": "Teléfono actualizado"}

# SQLA BULK DELETE with user authorization
@router.delete("/bulkdeltodo/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
async def bulk_delete_todo_by_id (user: user_dependency, db: db_dependency, todo_id:int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    stmt = delete(Todo).where(Todo.id == todo_id, Todo.owner_id == user.get('id'))
    result = db.execute(stmt)
    print(f"Bulk Delete Result= {result} ")
    db.commit()

    #  Check if row was actually deleted (handles 404)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item deleted succesfully"}



# SQLA FETCH and DELETE
@router.delete("/fetchdeltodo/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
async def fetch_delete_todo_by_id (db: db_dependency, todo_id:int = Path(gt=0)):

    # Fetch record
    fetched_record = db.get(Todo, todo_id)

    # Handle 404
    if not fetched_record:
        raise HTTPException(status_code=404, detail="Item not found")

    # Delete the object from session and commit
    db.delete(fetched_record)
    db.commit()

    return {"message": "Item deleted succesfully"}
