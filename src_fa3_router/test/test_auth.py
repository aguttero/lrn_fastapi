from .utils import *
from routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user # these are in routers.auth.py
from  datetime import timedelta
import jwt
# import pytest_asyncio # to be able to use pytest-asyncio for the async functions called directly by pytest. fastapy async endpoints don't need this
import pytest # to be able to use pytest-asyncio for the async functions called directly by pytest. fastapy async endpoints don't need this
from fastapi import HTTPException

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

def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)
    print (f"expires_delta= {expires_delta}")

    token = create_access_token(username, user_id, role, expires_delta)
    print (f"token= {token}")
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature':False})
    # decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # skipping signature verification tests only logic and avoids expired token errors or validation if token signatures validates against an external service
    print (f"decoded_token= {decoded_token}")
    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role
    # assert decoded_token['exp'] == expires_delta ## THIS WONT WORK JWT['exp'] stores a UNIX TimeStamp

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    print (f"user= {user}")
    assert user == {'username': 'testuser', 'id': 1, 'user_role': 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=token)

    print (f"exc_info= {exc_info}")
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'Could not validate user'
