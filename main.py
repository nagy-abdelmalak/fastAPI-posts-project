from fastapi import FastAPI, Response, status, HTTPException
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

def find_post_index(id: int):
    for i, p in enumerate(saved_posts):
        if p["id"] == id:
            return i

# the root of the web app
@app.get("/")
def root():
    return {"message": "Welcome to my first FastAPI application!"}

# a sub page of the app to display the posts
@app.get("/posts")
def posts():
    return {"data": saved_posts}

# first post http request to create posts (expecting data from user in certain format to create and save correctly)
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    post_dict = payload.model_dump()
    post_dict["id"] = randrange(0, 10000000)
    saved_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def post(id: int):
    post = find_post(id)
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")
    saved_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")
    post_dict = post.model_dump()
    post_dict["id"] = id
    saved_posts[index] = post_dict
    return {"message" : "Updated successfully!"}

