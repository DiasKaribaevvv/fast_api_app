from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, column, ForeignKey
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String, nullable=False)
    published =Column(Boolean,default=True)
    created_date = Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_date = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))