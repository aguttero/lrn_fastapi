fastapi
uvicorn? -> standard
pydantic

# DB
sqlalchemy

# passwords
passlib -> dead migrate to
    1. raw calls in bycript
    2. or pwdlib
bcrypt==4.0.1

2026 Reco 
bcrypt 5.0 -> sin passlib o pwdlib
Argon2id

## token Oauth
python-multipart -> password request form
from fastapi.security import OAuth2PasswordRequestForm

## JWT
pyjwt
https://pyjwt.readthedocs.io/en/stable/

## TESTING
pytest
pytest-asyncio to test async functions

### http requests
httpx2

bash
pytest -s to see prints from inside test_filename.py
pytest path/test_filename.py -s -v
pytest test/test_main.py -s -v

## Jinja2
pip install jinja2
