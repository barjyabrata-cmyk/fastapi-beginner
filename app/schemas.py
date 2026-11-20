from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# create a schema for basemodel fro daat reciveing from client

class UserResponse(BaseModel):
        email:EmailStr
        id:int
        created_at:datetime
        
        class Config:
                orm_mode=True


class PostBase(BaseModel):
    title: str
    content:str
    published : bool=True
   # rating: Optional [int]=None

class Postcreate(PostBase):
    pass   

class Post(PostBase):
    title: str
    content:str
    published : bool
    created_at:datetime
    owner_id:int
    owner: UserResponse   # to get the user info as well as post detials , UserResponse class is written upper for these reason to use this here

# lower class is defined because when we track the response to user
# we must use pydantic model,but orm does not give dict so pydantoc model does not use that directly
# so we use this
    class Config:
        orm_mode=True

class UserPost(BaseModel):

        email:EmailStr
        password:str


class UserLogin(BaseModel):

        email:EmailStr
        password:str

class Token(BaseModel):
      access_token :str
      token_type :str

class TokenData(BaseModel):
      id : Optional[int]=None

class Vote(BaseModel):
      post_id : int
      dir : conint(le=1)    # to give input only o or 1 , for vote 1 and deleting vote 0
     
     
class PostOut(BaseModel):
      Post:Post
      votes: int

      class Config:
            orm_mode =True
      