from fastapi import FastAPI

import config
from db import db

app = None
app = FastAPI(title="Save your photos api",
                description="API Docs for save your photos",
                version=0.1, debug=True)
if app is None:
    raise RuntimeError("Failed to initiate FastAPI")

@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

from models.User import *


@app.post("/")
async def read_root(data: UserInput):
    import uuid

    from schema.Users import Users
    data = data.dict()
    data["id"] = uuid.uuid4()
    user_id = await Users.create(**data)
    return {"id": user_id}

if __name__ == "__main__": 
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000,
                log_level="debug", reload=True)
