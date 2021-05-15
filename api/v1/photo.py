import config
from controller.Photo import Photo
from fastapi import APIRouter, Depends, File, Response, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel, EmailStr, StrictInt, StrictStr

photo_router = APIRouter()
photo_controller = Photo()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")


@photo_router.post("/", tags=["Photo"], summary="upload single photo", status_code=201)
async def upload_media(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    token = jwt.decode(token, config.SECRET)
    return await photo_controller.upload_media(file, token["id"])

@photo_router.get("/{filename}", tags=["Photo"], summary="get single photo", status_code=200)
async def get_image(filename: str, token: str = Depends(oauth2_scheme)):
    token = jwt.decode(token, config.SECRET)
    return await photo_controller.get_image(filename, token["id"])

@photo_router.get("/list/{skip}", tags=["Photo"], summary="get list of photos", status_code=200)
async def get_photo_list(skip: int = 0, token: str = Depends(oauth2_scheme)):
    token = jwt.decode(token, config.SECRET)
    return await photo_controller.get_photo_list(skip, token["id"])
