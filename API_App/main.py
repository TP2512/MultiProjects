import logging
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Annotated, Optional
from .database import engine
from . import models

# Example configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create logger instances
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

#uvicorn main:app --reload


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None

app = FastAPI()

posts_dict=[
    {"title":"AAA","content":"my name is anthony gonsalis","id":1},
    {"title":"DuaLipa","content":"Levitating","id":2}
]

def get_post(id):
    for post_ele in posts_dict:
        if post_ele["id"]==id:
            return post_ele
    return False


@app.get("/")
async def root():
    return {"message": "This is post blog api site"}


@app.get("/posts")
async def get_all_posts():
    return {"all posts":posts_dict}


@app.get("/posts/{id}")
async def get_post_by_id(id: int, response: Response):
    if not get_post(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id {id} not found"}
    return {f"got post of id:{id}":get_post(id)}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def post_one_post(post: Post):
    print(post)

    posts_dict.append(post.dict())
    return {f"new post added with id ":get_post(id)}


@app.patch("/posts/{id}")
async def patch_post_by_id(id: int, post:Post):
    if id not in posts_dict.keys():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    posts_dict[id] = post.dict()["title"]
    return {f"got post of id:{id} {posts_dict}":get_post(id)}


@app.put("/posts/{id}")
async def put_post_by_id(id: int, post:Post):
    if id not in posts_dict.keys():
        raise HTTPException(status_code=404, detail="Item not found")
    posts_dict[id] = post.dict()["title"]
    return {f"got post of id:{id} {posts_dict}": get_post(id)}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(id: int):
    if id not in posts_dict.keys():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no post with id {id} to delete")
    del posts_dict[id]
    print(posts_dict)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/posts",status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_posts():
    posts_dict.clear()
    print(posts_dict)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

