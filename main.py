import logging
from time import time
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from jose import jwt

import config
from api.v1.feedback import feedback_router
from api.v1.photo import photo_router
from api.v1.user import user_router
from db import db
from schema.RequestLog import RequestLog

app = None
if config.PRODUCTION == True:
    app = FastAPI(docs_url=None, redoc_url=None)
elif config.PRODUCTION == False:
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

app.include_router(feedback_router, prefix="/api/v1/feedback")
app.include_router(user_router, prefix="/api/v1/user")
app.include_router(photo_router, prefix="/api/v1/photo")


# Define middleware
if config.PRODUCTION == True:
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        try:
            requested_time = jwt.decode(
                request.headers["X-Custom-Auth"], config.APP_SECRET)["timestamp"]
            arrival_time = int(time() * 1000)
            data = {
                "id": str(uuid4()),
                "headers": dict(request.headers),
                "requested_time": requested_time,
                "arrival_time": arrival_time,
                "time_difference": arrival_time - requested_time
            }
            await RequestLog.insert(**data)
        except Exception as err:
            logging.exception(err)
            data = {
                "id": str(uuid4()),
                "headers": dict(request.headers),
                "requested_time": 0,
                "arrival_time": int(time() * 1000),
                "time_difference": 0
            }
            await RequestLog.insert(**data)
            return JSONResponse({"error": "Not Authorized"}, 401)

        return await call_next(request)

gunicorn_logger = logging.getLogger('gunicorn.info')
logger.handlers = gunicorn_logger.handlers
if __name__ == "__main__":
    import uvicorn
    logger.setLevel(logging.DEBUG)
    uvicorn.run("main:app", host="0.0.0.0", port=5000,
                log_level="debug", reload=True)
else:
    logger.setLevel(gunicorn_logger.level)
