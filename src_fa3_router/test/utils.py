from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base
from models import Todo
import pytest
from fastapi.testclient import TestClient
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"
TEST_RAM_DATABASE_URL = "sqlite:///:memory:"

# engine = create_engine(TEST_DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool, echo=True)
engine = create_engine(TEST_DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool, echo=False)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# MOCK DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        print ("check point override get_db close")

# MOCK USER
def override_get_current_user():
    # return needs to match return format in get_current_user function in auth.py
    return {'username':'user3_test', 'id':1, 'user_role':'admin'}

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo_record = Todo(
        title = "Sample Title",
        description = "Sample Description",
        priority=5,
        complete=False,
        owner_id =1
    )
    # Create Record
    db = TestingSessionLocal()
    db.add(todo_record)
    db.commit()

    # Delete All Records in Todos table
    print("checkpoint test_todo before yield")
    yield todo_record
    db.execute(delete(Todo))
    print("checkpoint table Todo delete")
    db.commit()
