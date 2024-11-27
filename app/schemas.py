from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # if the user doesn't provide value it will be True OPTIONAL field

    #rating: Optional[int] = None # in this field we can not provide any information to this field it will be empty


class PostResponse(BaseModel):
    title: str
    content: str
    published: bool = True
    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email:EmailStr
    created_date: datetime

    class Config:
        orm_mode = True

class UserLoginResponse(BaseModel):

    email:EmailStr
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None