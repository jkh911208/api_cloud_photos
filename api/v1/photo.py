from controller.Photo import Photo
from fastapi import APIRouter, Depends, File, Response, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, StrictInt, StrictStr

photo_router = APIRouter()
photo_controller = Photo()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")

@photo_router.post("/", tags=["Photo"], summary="upload single photo", status_code=201)
async def upload_media(file: UploadFile = File(...)):
    await photo_controller.upload_media(file)
    return {"filename": file.filename}