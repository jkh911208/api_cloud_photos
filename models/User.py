import uuid
from random import randint

from pydantic import BaseModel


class UserInput(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class UserReturn(BaseModel):
    id: str
    username: str
