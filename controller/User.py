import hashlib
import uuid

import config
from jose import jwt
from schema.Users import Users


class User():
    async def signup(self, data: dict) -> dict:
        hash = hashlib.sha3_512()
        hash.update(data["password"].encode())
        data["password"] = hash.hexdigest()
        data["id"] = str(uuid.uuid4())
        data["status"] = 1
        await Users.insert(**data)
        return {"access_token": jwt.encode({"id": data["id"]}, config.SECRET), "token_type": "bearer"}

    async def login(self, data:dict) -> dict:
        user = await Users.get_by_username(data["username"])
        hash = hashlib.sha3_512()
        hash.update(data["password"].encode())
        if user["password"] == hash.hexdigest():
            return {"access_token": jwt.encode({"id": user["id"]}, config.SECRET), "token_type": "bearer"}
