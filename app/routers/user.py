from .. import model,schemas,database,utils
from .. database import get_db
from sqlalchemy.orm import declarative_base, Session
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from fastapi import status,APIRouter

router =APIRouter(
    prefix='/user',
    tags=['USER API']
)

@router.post('/signup',response_model=schemas.UserResponse,status_code=status.HTTP_201_CREATED)
async def create_user(user:schemas.User,db:Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    return new_user


@router.get('/{id}',response_model=schemas.UserResponse)
async def get_specific_user(id: int,db:Session = Depends(get_db)):
    specific_user = db.query(model.User).filter(model.User.id == id).one_or_none()
    if not specific_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No user with id: {id}")
    return specific_user