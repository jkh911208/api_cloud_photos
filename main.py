import hashlib
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import config
from api.v1.photo import photo_router
from api.v1.user import user_router
from db import db

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

app.include_router(user_router, prefix="/api/v1/user")
app.include_router(photo_router, prefix="/api/v1/photo")


# Define middleware
if config.PRODUCTION == True:
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        if "Authorization" not in request.headers:
            try:
                session_id = request.headers["sessionId"]
                before_result = session_id+"cloudpho"
                print(before_result)
                hash_alg = hashlib.sha256()
                hash_alg.update(before_result.encode())
                hash_result = hash_alg.hexdigest()
                if hash_result != request.headers["X-Custom-Auth"]:
                    return JSONResponse({"error": "Not Authorized"}, 401)
            except Exception as err:
                logging.exception(err)
                return JSONResponse({"error": "Not Authorized"}, 401)

        response = await call_next(request)
        return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000,
                log_level="debug", reload=True)
