from .utils import *
from routers.users import get_current_user, get_db # these are in routers.auth.py
from fastapi import status
from sqlalchemy import select
from models import Todo, User

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_get_user_info(test_user):
    response = client.get("/user")
    print(f"status message= {response.status_code}")
    print(f"response.json()={response.json()}")
    assert response.status_code == status.HTTP_200_OK
