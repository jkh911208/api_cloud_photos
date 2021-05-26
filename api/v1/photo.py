import logging

import config
from controller.Photo import Photo
from fastapi import APIRouter, Depends, File, Response, UploadFile
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

photo_router = APIRouter()
photo_controller = Photo()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")


@photo_router.post("/", tags=["Photo"], summary="upload single photo", status_code=201)
async def upload_media(
        response: Response,
        md5: str = Form(...),
        size: str = Form(...),
        creationTime: str = Form(...),
        height: str = Form(...),
        width: str = Form(...),
        file: UploadFile = File(...),
        token: str = Depends(oauth2_scheme)):
    try:
        token = jwt.decode(token, config.SECRET)
        data = {
            "creation_time": int(creationTime),
            "md5": md5,
            "size": int(size),
            "height": int(height),
            "width": int(width)
        }
        return await photo_controller.upload_media(file, token["id"], data)
    except Exception as err:
        logging.exception(err)
        response.status_code = 500
        return {"result": "INTERNAL ERROR"}


@photo_router.get("/{filename}", tags=["Photo"], summary="get single photo", status_code=200)
async def get_image(response: Response, filename: str, token: str = Depends(oauth2_scheme)):
    try:
        token = jwt.decode(token, config.SECRET)
        return await photo_controller.get_image(filename, token["id"])
    except Exception as err:
        logging.exception(err)
        response.status_code = 500
        return {"result": "INTERNAL ERROR"}


@photo_router.get("/list/{created}", tags=["Photo"], summary="get list of photos", status_code=200)
async def get_photo_list(response: Response, created: int = 0, token: str = Depends(oauth2_scheme)):
    try:
        token = jwt.decode(token, config.SECRET)
        return await photo_controller.get_photo_list(created, token["id"])
    except Exception as err:
        logging.exception(err)
        response.status_code = 500
        return {"result": "INTERNAL ERROR"}
