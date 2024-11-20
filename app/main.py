
from fastapi import FastAPI,Response,status,HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time



from . import model
from .database import engine
from .routers import post,user,auth


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
app.include_router(auth.router)

# this is decorator
@app.get("/")
# this is function which decorator makes
async def root():
    return {"message":"hello world!"}

