from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # if the user doesn't provide value it will be True OPTIONAL field
    rating: Optional[int] = None # in this field we can not provide any information to this field it will be empty

# this is decorator
@app.get("/")
# this is function which decorator makes
async def root():
    return {"message":"hello world!"}

@app.get("/posts")
async def get_posts():
    return {"post":"your post"}

@app.post("/createpost")
async def create_post(new_post:Post):
    print(new_post.title,new_post.content,new_post.published,new_post.rating)
    return {"message":"post added"}