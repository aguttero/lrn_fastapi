from .utils import *
from routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM # these are in routers.auth.py
from  datetime import timedelta
import jwt

app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'test_password', db)
    print (f"authenticated_user= {authenticated_user}")
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user('WrongUserName', 'test_password', db)
    print (f"non_existent_user= {non_existent_user}")
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, 'wrong_password', db)
    print (f"wrong_password_user= {wrong_password_user}")
    assert wrong_password_user is False
