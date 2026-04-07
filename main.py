from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# using a scheme to get post data easily and validated in the target value type
class Post(BaseModel):
    title: str
    content: str
    isPublic: bool = True
    rate: Optional[int] = None

saved_posts = [{"title": "Post 1", "content": "Content 1", "id": 1},
               {"title": "Post 2", "content": "Content 2", "id": 2}]

def find_post(id: int):
    for p in saved_posts:
        if p["id"] == id:
            return p

# the root of the web app
@app.get("/")
def root():
    return {"message": "Welcome to my first FastAPI application!"}

# a sub page of the app to display the posts
@app.get("/posts")
def posts():
    return {"data": saved_posts}

@app.get("/posts/{id}")
def post(id: int):
    return find_post(id)

# first post http request to create posts (expecting data from user in certain format to create and save correctly)
@app.post("/posts")
def create_post(payload: Post):
    post_dict = payload.dict()
    post_dict["id"] = randrange(0, 10000000)
    saved_posts.append(post_dict)
    return {"data": post_dict}