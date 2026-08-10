from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base
from main import app

SQLA_DATABASE_URL = "sqlite:///./test.db"
SQLA_RAM_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLA_DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool, echo=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
