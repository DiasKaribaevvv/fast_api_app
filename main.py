from typing import Optional

from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # if the user doesn't provide value it will be True OPTIONAL field
    rating: Optional[int] = None # in this field we can not provide any information to this field it will be empty

my_posts = []

def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_index(id: int):
    for index,post in enumerate(my_posts):
        if post["id"]==id:
            return index




# this is decorator
@app.get("/")
# this is function which decorator makes
async def root():
    return {"message":"hello world!"}

@app.get("/posts")
async def get_posts():
    return {"data":my_posts}

@app.get("/posts/{id}")
async def get_specific_post(id: int,response:Response):
    post= find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND #changing to not found if answer is empty
        # return {'message': f'post with id {id} not found'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} not found')
    return {"post":post}

@app.get("/posts/latest/")
async def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"latest":post}


@app.post("/createpost",status_code=status.HTTP_201_CREATED)
async def create_post(new_post:Post):
    # print(new_post.title,new_post.content,new_post.published,new_post.rating)
    # print(new_post.dict())
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"message":"post added"}

@app.delete("/posts/delete/{id}",status_code=status.HTTP_200_OK)
async def delete_post(id: int):

    index = find_index(id)
    my_posts.pop(index)

    return {"message":"post deleted!"}