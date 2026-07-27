from typing import Annotated
import pydantic
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from starlette import status
from pydantic import BaseModel, Field
import models
from models import Todo
from database import engine, SessionLocal

app = FastAPI()

# --- CREATE SQLITE DB
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field (min_length=3)
    description: str = Field (min_length=3, max_length=100)
    priority: int = Field (gt=0, lt=6)
    complete: bool


@app.get("/",  status_code=status.HTTP_200_OK )
async def read_all(db: db_dependency):
    # SQLA V1
    # return db.query(Todo).all()
    # SQLA V2
    stmt = select(Todo)
    result = db.scalars(stmt).all()
    return result

@app.get("/pol")
async def pol():
    return  {"message": "pol ok!"}

@app.get ("/todo/{todo_id}", status_code=status.HTTP_200_OK )
async def read_todo_by_id(db: db_dependency, todo_id:int = Path(gt=0)):
    stmt = select(Todo).where(Todo.id == todo_id)
    found_record = db.scalar(stmt)

    # Exception Handling:
    if not found_record:
        raise HTTPException(status_code=404, detail="Item not found")

    return found_record

@app.post ("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo_item (db: db_dependency, todo_request: TodoRequest):
    # Pydantic V1
    # new_record = Todo(**todo_request.dict())

    # Pydantic V2
    new_record = Todo(**todo_request.model_dump())

    db.add(new_record)
    db.commit()

# SQLA BULK UPDATE:
@app.put ("/todobulk/{todo_id}", status_code=status.HTTP_200_OK)
async def bulk_update_todo_by_id (db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    # Convert incoming data to dictionary
    update_dict = todo_request.model_dump()

    # Build and execute the V2 update statement
    stmt = (update(Todo).where(Todo.id == todo_id).values(**update_dict))

    result = db.execute(stmt)
    db.commit()

    # Handle unexisisting record:
    print(f"row_count= {result.rowcount}")
    if result.rowcount == 0:
        raise HTTPException (status_code=404, detail="Item not found")

    # Return the updated record - C
    ret_txt = db.get(Todo, todo_id)
    print (f"bulk update return= {ret_txt}")
    return ret_txt

# SQLA MERGE UPDATE:
# Inserts if record not found
@app.put("/todomerge/{todo_id}", status_code=status.HTTP_202_ACCEPTED)
async def merge_update_todo_by_id(todo_request: TodoRequest, db: db_dependency,  todo_id: int = Path(gt=0)):
    # 1. Convert to dict and explicitly inject the URL's todo_id into it
    update_data = todo_request.model_dump()
    update_data["id"] = todo_id  # Ensures it targets the correct PK

    # 2. Create a temporary model instance (like your POST example)
    updated_record_instance = Todo(**update_data)

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

# SQLA BULK DELETE
@app.delete("/bkdeltodo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def bulk_delete_todo_by_id (db: db_dependency, todo_id:int = Path(gt=0)):
    stmt = delete(Todo).where(Todo.id == todo_id)
    result = db.execute(stmt)
    print(f"Buld Delete Result= {result} ")
    return result
