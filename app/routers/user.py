from .. import models,schemas,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
     prefix ="/users",
     tags=["Users"]    # for grouping post and user in fastapi swagger ui
)

# to login user part

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)

def craete_user_table(UserPost:schemas.UserPost,db:Session =Depends(get_db)):

        # hash the password - user.password
    

        hashed_password=utils.hash(UserPost.password)
        UserPost.password=hashed_password
        new_users=models.User(**UserPost.dict())
        # here to add row data by user input
        # models.post because to import post from my models file
        db.add(new_users) # to add new post
        db.commit()       # to save this in the database
        db.refresh(new_users) # to return the wholw row data
        return new_users

@router.get('/{id}',response_model=schemas.UserResponse)

def get_users_id_in_database (id:int,db: Session=Depends(get_db)):
    user=db.query(models.UserPost).filter(models.UserPost.id ==id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NO_FOUND,detail="user with given id not found")

    return user