from fileinput import close
from multiprocessing.sharedctypes import synchronized
from select import error
from typing import Optional,List
from exceptiongroup import catch
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session, sessionmaker

from . import model,schemas,utils
from .database import engine, SessionLocal, get_db
from .routers import post,user


model.Base.metadata.create_all(bind=engine)
app = FastAPI()




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


app.include_router(post.router)
app.include_router(user.router)

# this is decorator
@app.get("/")
# this is function which decorator makes
async def root():
    return {"message":"hello world!"}

