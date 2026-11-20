from .database import Base
from  sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String,ForeignKey
from sqlalchemy import Boolean,text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import  Relationship

# for posts

class Post(Base):
    __tablename__="posts"

    # define our colomn and their type for database

    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,primary_key=False,nullable=False)
    content=Column(String,primary_key=False,nullable=False)
    published=Column(Boolean,server_default='TRUE')
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner =Relationship("User")  # to get the user info , so relationship is useed here

# for users


class User(Base):
    __tablename__="users"

    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    id=Column(Integer,primary_key=True,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

# for like,votes

class Vote(Base):
    __tablename__="voters"
   
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)


