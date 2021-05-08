import uvicorn
from fastapi import FastAPI

from models.User import User

app = FastAPI() 
@app.post("/", response_model=User) 
def create_user(user: User): 
    return user

if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=5000)
