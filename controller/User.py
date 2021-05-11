import hashlib
import logging
import uuid

import config
from jose import jwt
from schema.Users import Users


class User():
    async def signup(self, data: dict) -> dict:
        logging.info("start sign up process")
        hash = hashlib.sha3_512()
        hash.update(data["password"].encode())
        data["password"] = hash.hexdigest()
        data["id"] = str(uuid.uuid4())
        data["status"] = 1
        logging.info("write to db")
        await Users.insert(**data)
        logging.info("return access token")
        return {"access_token": jwt.encode({"id": data["id"]}, config.SECRET), "token_type": "bearer"}

    async def login(self, data: dict) -> dict:
        logging.info("start login")
        user = await Users.get_by_username(data["username"])
        hash = hashlib.sha3_512()
        hash.update(data["password"].encode())
        if user["password"] == hash.hexdigest():
            logging.info("password match")
            return {"access_token": jwt.encode({"id": user["id"]}, config.SECRET), "token_type": "bearer"}