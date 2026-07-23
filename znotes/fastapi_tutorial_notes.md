# FastAPI udemy complete course 2026 coding with roby
## Documentation
https://fastapi.tiangolo.com/

## Architecture
Popular:
1. web server - Front End (Node / Next)
2. Fast API Server - Backend logic
3. dependencies:
  - Fast API
  - Uvicorn -> Web Server

Fast Dev and prototype:
Fast API can also work as a full stack app

## installation PIP
python3 -m venv .venv
pip install fastapi
pip install "uvicorn[standard]" -> web server production version

## run server
### uvicorn command
uvicorn python_file:app --reload -> reload allows for refresh in code and auto reload of web server

### fastapi prod and dev start:
* Requires pip install "fastapi[standard]"
1. Prod
fastapi run python_file.py -> prod
2. dev
fastapi dev python_file.py -> dev

# Standard HTTP Status Codes
## 1xx Information Response: Request Processing
## 2xx Success: Req Successfully complete
## 3xx Redirection: Further action must be complete
## 4xx Client errors: An error was caused by the client
## 5xx Server errors: An error ocurred on the server
