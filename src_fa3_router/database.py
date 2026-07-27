from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
# from sqlalchemy.ext.declarative import declarative_base


# Database setup
DATABASE_URL = 'sqlite:///./todosapp2.db'
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False}, echo=True)

# engine = create_async_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLA V1
# Base = DeclarativeBase()

# SQLA V2
class Base(DeclarativeBase):
    """SQLAlchemy declarative base."""
    pass
