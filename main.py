from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    isPublic: bool = True
    rate: Optional[int] = None

@app.get("/")
def root():
    return {"message": "Welcome to my first FastAPI application!"}

@app.get("/posts")
def posts():
    return {"data": "Here are your posts"}

@app.post("/createpost")
def create_post(payload: Post):
    return {"message": f"Post {payload.title} created successfully!"}