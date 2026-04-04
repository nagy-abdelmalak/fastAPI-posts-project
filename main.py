from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# using a scheme to get post data easily and validated in the target value type
class Post(BaseModel):
    title: str
    content: str
    isPublic: bool = True
    rate: Optional[int] = None

# the root of the web app
@app.get("/")
def root():
    return {"message": "Welcome to my first FastAPI application!"}

# a sub page of the app
@app.get("/posts")
def posts():
    return {"data": "Here are your posts"}

# first post http request (expecting data from user in certain format to create and save correctly)
@app.post("/createpost")
def create_post(payload: Post):
    return {"message": f"Post {payload.title} created successfully!"}