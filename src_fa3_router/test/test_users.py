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
    assert response.json()['username'] == 'user3_test'
    assert response.json()['email'] == 'test3@email.com'
    assert response.json()['role'] == 'admin'

def test_change_pwd_success(test_user):
    response = client.put("/user/password", json={"password":"test_password", "new_password":"updated_password"})
    print(f"status message= {response.status_code}")
    print(f"response.json()={response.json()}")
    assert response.status_code == status.HTTP_202_ACCEPTED

def test_change_password_invalid(test_user):
    response = client.put("/user/password", json={"password":"wrong_password", "new_password":"updated_password"})
    print(f"status message= {response.status_code}")
    print(f"response.json()={response.json()}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()== {'detail': 'Error on password change'}
