from datetime import datetime
from pydantic import BaseModel
from typing import Annotated

class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []

external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}

def say_hello(name: Annotated[str, "this is just metadata"]) -> str:
    return f"Hello {name}"

user = User(**external_data)
print(user)
print(user.id)
print ("- - -")
print (say_hello("Nombre"))
print ("- - -")
print (say_hello(external_data.get('id')))
print ("- - -")
print (say_hello(user.name))
