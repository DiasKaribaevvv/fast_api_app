from sqlalchemy import table

from app.database import engine,get_db
from sqlalchemy.orm import declarative_base, Session
from typing import List
from app import model
from app import schemas
from fastapi import FastAPI,Response,status,HTTPException,APIRouter
from fastapi.params import Depends



router =APIRouter(
    prefix='/posts',
    tags=["POSTS API"]
)

@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    post = db.query(model.Post).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    return post


@router.get("/{id}")
async def get_specific_post(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()

    # cursor.execute("""SELECT * FROM posts where id=%s""",(str(id)))
    # post = cursor.fetchone()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND #changing to not found if answer is empty
        # return {'message': f'post with id {id} not found'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    return post


@router.get("/posts/latest/")
async def get_latest_post():
    pass



@router.post("/createpost", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(new_post: schemas.PostBase, db: Session = Depends(get_db)):
    post = model.Post(**new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    text = 'hello'
    print(text.encode())
    # cursor.execute(f"""INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING *""",(new_post.title,new_post.content))
    # post = cursor.fetchone()
    # conn.commit()

    return post


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id)

    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id)))
    # delete_post_var = cursor.fetchone()
    # conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no post with id = {id}")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/update/{id}")
async def update_post(id: int, new_post: schemas.PostBase, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no post with id = {id}")

    post.update(new_post.dict())
    # print(new_post.dict())
    db.commit()

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

    return {"data": "updated"}