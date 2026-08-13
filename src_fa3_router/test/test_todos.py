# from main import app ### THIS ONE NEEDS TO BE IN UTILS AND NOT HERE ####
from sqlalchemy import select
from routers.todos import get_current_user, get_db # these are in routers.auth.py
from fastapi import status
from models import Todo
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# TESTs
def test_read_all_authenticated(test_todo):
    response = client.get("/")
    print(f"status message= {response.status_code}")
    print(f"response.json()={response.json()}")
    assert response.status_code == status.HTTP_200_OK
    # assert response.json() == []
    assert response.json() == [{'complete':False, 'title' : 'Sample Title', 'description': 'Sample Description', 'priority':5, 'owner_id':1, 'id':1 }]

def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1") # "/todd/{todo_id}"
    print(f"status message= {response.status_code}")
    print(f"response.json()={response.json()}")
    assert response.status_code == status.HTTP_200_OK
    # It should return a single object and not a list as in previous test read_all
    assert response.json() == {'complete':False, 'title' : 'Sample Title', 'description': 'Sample Description', 'priority':5, 'owner_id':1, 'id':1 }

# TEST single get authentication ok but item not found
def test_read_one_authenticated_not_found():
    response = client.get("/todo/999") # "/todd/{todo_id}"
    # print(f"status message= {response.raise_for_status()}")
    print(f"status message= {response.status_code}")
    print(f"response.json()={response.json()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Item not found'}

# TEST an iteam creation
def test_create_todo(test_todo):
    request_data = {
        'title':'Test Todo',
        'description': 'Test Description',
        'priority': 5,
        'complete': False
    }

    response = client.post('/todo/',json=request_data)
    print(f"status message= {response.status_code}")
    print(f"response.json()={response.json()}")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.status_code == 201

    db = TestingSessionLocal()
    stmt = select(Todo).where(Todo.id == 2)  # Todo.id == 1 es el record creado 'test_todo'
    found_record = db.scalar(stmt)
    print(f"Found record = {found_record}")
    assert found_record.title == 'Test Todo'
    assert found_record.title == request_data.get('title')
    assert found_record.description == 'Test Description'
    assert found_record.description == request_data.get('description')
    assert found_record.priority == 5
    assert found_record.priority == request_data.get('priority')
    assert found_record.complete == False
    assert found_record.complete == request_data.get('complete')

# TEST UPDATE
def test_update_item(test_todo):
    request_data = {
        'title':'Updated Todo already saved',
        'description': 'Updated Test Description',
        'priority': 4,
        'complete': True
    }
    response = client.put("/todobulk/1", json=request_data)
    print(f"status message= {response.status_code}")
    print(f"response.json()={response.json()}")
    assert response.status_code == 200
    assert response.status_code == status.HTTP_200_OK

    db = TestingSessionLocal()
    stmt = select(Todo).where(Todo.id == 1)  # Todo.id == 1 es el record creado 'test_todo'
    found_record = db.scalar(stmt)
    print(f"Found record = {found_record}")
    assert found_record.title == request_data.get('title')
    assert found_record.description == request_data.get('description')
    assert found_record.priority == request_data.get('priority')
    assert found_record.complete == request_data.get('complete')

def test_update_item_not_found(test_todo):
    request_data = {
        'title':'Updated Todo already saved',
        'description': 'Updated Test Description',
        'priority': 4,
        'complete': True
    }
    response = client.put("/todobulk/999", json=request_data)
    print(f"status message= {response.status_code}")
    print(f"response.json()={response.json()}")
    assert response.status_code == 404
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Item not found'}

# TEST DELETE
def test_delete_todo(test_todo):
    response = client.delete('/bulkdeltodo/1')
    print(f"status message= {response.status_code}")
    print(f"response.json()={response.json()}")
    assert response.status_code == 202
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json() == {'message':'Item deleted succesfully'}

    db = TestingSessionLocal()
    stmt = select(Todo).where(Todo.id == 1)  # Todo.id == 1 es el record creado 'test_todo'
    found_record = db.scalar(stmt)
    print(f"Found record = {found_record}")
    assert found_record is None
    assert not found_record

def test_delete_todo_not_found(test_todo):  #puedo pasar el test_todo o no en este caso
    response = client.delete('/bulkdeltodo/999')
    print(f"status message= {response.status_code}")
    print(f"response.json()={response.json()}")
    assert response.status_code == 404
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Item not found'}
