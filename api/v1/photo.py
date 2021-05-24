import logging

import config
from controller.Photo import Photo
from fastapi import APIRouter, Depends, File, Request, Response, UploadFile
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

photo_router = APIRouter()
photo_controller = Photo()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")


@photo_router.post("/", tags=["Photo"], summary="upload single photo", status_code=201)
async def upload_media(response: Response, request: Request, file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    try:
        token = jwt.decode(token, config.SECRET)
        form = await request.form()
        data = {
            "creation_time": int(form["creationTime"]),
            "md5": form["md5"],
            "size": int(form["size"]),
            "height": int(form["height"]),
            "width": int(form["width"])
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
