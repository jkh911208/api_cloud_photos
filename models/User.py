import uuid
from random import randint

from pydantic import BaseModel


class UserInput(BaseModel):
    id=randint(-9999,9999)
    username: str
    password: str

    class Config:
        orm_mode = True

class UserReturn(BaseModel):
    id: str
    username: str
