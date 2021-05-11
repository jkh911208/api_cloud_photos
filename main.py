from fastapi import FastAPI

import config
from api.v1.photo import photo_router
from api.v1.user import user_router
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

app.include_router(user_router, prefix="/api/v1/user")
app.include_router(photo_router, prefix="/api/v1/photo")

if __name__ == "__main__": 
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000,
                log_level="debug", reload=True)
