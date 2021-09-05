import logging

import config
from controller.Feedback import Feedback
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel, StrictStr

feedback_router = APIRouter()
feedback_controller = Feedback()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")


class Feedback(BaseModel):
    feedback: StrictStr

    class Config:
        orm_mode = True


@feedback_router.post("", tags=["Feedback"], summary="create new feedback", status_code=201)
async def get_photo_list(data: Feedback, response: Response, token: str = Depends(oauth2_scheme)):
    try:
        token = jwt.decode(token, config.SECRET)
        data = data.dict()
        data["owner"] = token["id"]
        await feedback_controller.new_feedback(data)
    except Exception as err:
        logging.exception(err)
        response.status_code = 500
        return {"result": "INTERNAL ERROR"}
