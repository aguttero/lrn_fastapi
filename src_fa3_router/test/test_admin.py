from .utils import *
from routers.admin import get_current_user, get_db # these are in routers.auth.py but need to be imported from admin
from fastapi import status
from sqlalchemy import select
from models import Todo


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    print(f"status message= {response.status_code}")
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Sample Title', 'description': 'Sample Description', 'id': 1, 'priority': 5, 'owner_id': 1}]

def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/delete/1")
    print(f"status message= {response.status_code}")
    print(response.json())
    assert response.status_code == status.HTTP_202_ACCEPTED

    db = TestingSessionLocal()
    stmt = select(Todo).where(Todo.id == 1)
    found_record = db.scalar(stmt)
    assert found_record == None
    assert found_record is None

def test_admin_delete_item_not_found():
    response = client.delete("/admin/delete/999")
    print(f"status message= {response.status_code}")
    print(response.json())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item not found'}
