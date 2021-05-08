from pydantic import BaseModel


class User(BaseModel):
    name: str

    class Config:
        orm_mode = True
