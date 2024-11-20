from .. import model,schemas,database,utils,oauth2
from .. database import get_db
from sqlalchemy.orm import declarative_base, Session
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from fastapi import status,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["AUTH API"],

)


@router.post('/login')
async def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials")

    if not utils.password_verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")


    access_token = oauth2.create_access_token({'user_id':user.id})

    return {'access_token':access_token,"token_type":"bearer"}