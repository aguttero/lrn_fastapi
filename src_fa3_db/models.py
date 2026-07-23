from database import Base
# from sqlalchemy import ForeignKey
# from typing import List
from sqlalchemy.orm import Mapped, mapped_column


# class Users(Base):
#     __tablename__ = 'users'

#     id: Mapped [int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(unique=True, index=True)
#     username: Mapped[str] = mapped_column(unique=True, index=True))
#     first_name : Mapped [str]
#     last_name : Mapped [str]
#     hashed_password : Mapped [str]
#     is_active : Mapped[bool] = mapped_column(default=True)
#     role : Mapped [str]

#     def __repr__(self) -> str:
#         return (
#         f"User(id={self.id!r}, email={self.email!r}, username={self.username!r})"
#     )


class Todo(Base):
    __tablename__ = 'todos'

    # id = Column(Integer, primary_key=True, index=True)
    id: Mapped [int] = mapped_column(primary_key=True)
    title: Mapped [str]
    description: Mapped [str]
    priority : Mapped[int]
    complete : Mapped[bool] = mapped_column(default=False)
    # owner_id: Mapped[int] = mapped_column (ForeignKey("users.id"))

    def __repr__(self) -> str:
        return (
        f"Todo(id={self.id!r}, title={self.title!r}, complete={self.complete!r})"
    )
