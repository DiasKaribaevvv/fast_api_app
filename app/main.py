from fileinput import close
from multiprocessing.sharedctypes import synchronized
from select import error
from typing import Optional

from exceptiongroup import catch
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session, sessionmaker

from . import model
from . import database
from .database import engine, SessionLocal

model.Base.metadata.create_all(bind=engine)
app = FastAPI()
Session = SessionLocal()


def get_db():
    db= SessionLocal()

    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # if the user doesn't provide value it will be True OPTIONAL field
    #rating: Optional[int] = None # in this field we can not provide any information to this field it will be empty



while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi_app', user='karik', password='oper2022',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connnected!')
        break
    except Exception as error:
        print("Connecting to database failed", error)
        time.sleep(3)



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

    post = Session.query(model.Post).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    return {"data":post}

@app.get("/posts/{id}")
async def get_specific_post(id: int,response:Response):

    post = Session.query(model.Post).filter(model.Post.id == id).first()

    # cursor.execute("""SELECT * FROM posts where id=%s""",(str(id)))
    # post = cursor.fetchone()
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
    post = model.Post(**new_post.dict())
    Session.add(post)
    Session.commit()
    Session.refresh(post)


    # cursor.execute(f"""INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING *""",(new_post.title,new_post.content))
    # post = cursor.fetchone()
    # conn.commit()

    return {"message":post}

@app.delete("/posts/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):

    post = Session.query(model.Post).filter(model.Post.id == id)


    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id)))
    # delete_post_var = cursor.fetchone()
    # conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is no post with id = {id}")
    Session.delete(post)
    Session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/update/{id}")
async def update_post(id: int,new_post : Post):
    post = Session.query(model.Post).filter(model.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is no post with id = {id}")
    
    post.update(new_post.dict())
    # print(new_post.dict())
    Session.commit()
    
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s where id = %s returning *""",(post.title,post.content,str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    # if not post.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is no post with id = {id}")

    # post.update(new_post.dict(),synchronize_session=False)

    # # post_dict = post.dict()
    # # post_dict["id"]=id
    # # my_posts[index]=post_dict
    # Session.commit()

    return {"data":"updated"}