import logging

from controller.User import User
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, StrictStr

user_router = APIRouter()
user_controller = User()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")


class SignUp(BaseModel):
    username: StrictStr
    password: StrictStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


@user_router.post("/signup", tags=["User"], summary="signup", response_model=Token, status_code=201)
async def signup(data: SignUp, response: Response):
    try:
        data = data.dict()
        result = await user_controller.signup(data)
        return result
    except Exception as err:
        logging.exception(err)
        response.status_code = 500
        return {"result": "INTERNAL ERROR"}


@user_router.post("/login", tags=["User"], summary="Login user", response_model=Token, status_code=200)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user_data = {
            "username": form_data.username,
            "password": form_data.password
        }
        result = await user_controller.login(user_data)
        return result
    except ValueError as err:
        response.status_code = 401
        return {"error": str(err)}
    except Exception as err:
        logging.exception(err)
        response.status_code = 500
        return {"result": "INTERNAL ERROR"}
