from .. import models,schemas,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import  List,Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)




# to see the data from database using sqlalchemy

@router.get("/",response_model=List[schemas.PostOut]) # list because it returns all the post
def test_sqlalachemy(db:Session=Depends(get_db),current_user: int =Depends(oauth2.get_current_user),limit:int=5,skip:int=0,search:Optional[str]=""):  # here limit is query paramater,means it gives me first 10 posts at first

# pagination : means instead of returning huge data , gives it in small chunks of data in one time
# here limit is query paramater,means it gives me first 10 posts at first 
# skip: is used to skip posts ,like if i want to show post with skipping first 10
# search is used find polsts by given titles ,not fully same,but some words same 

  #  posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  
    # to recieve the data drom the database and show the all posts from our database 

    # now we return our post with owner ,id,vote count all using sql joins


    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts



#  to add new row in database

@router.post("/",status_code=status.HTTP_201_CREATED)

def create_new_row_database(post:schemas.Postcreate,db:Session =Depends(get_db),current_user: int =Depends(oauth2.get_current_user)): # user_id part is for authentication purpose

     #new_posts=models.Post(title=post.title,content=post.content,published=post.published)
    
    # without writing the whole big thing we write shortly


    new_posts=models.Post(owner_id=current_user.id,**post.dict())
    # here to add row data by user input
    # models.post because to import post from my models file
    db.add(new_posts) # to add new post
    db.commit()       # to save this in the database
    db.refresh(new_posts) # to return the wholw row data
    return new_posts


# to view post by given id

@router.get("/{id}",response_model=schemas.PostOut)

def view_xyz_qrm_database(id:int,db:Session=Depends(get_db),user_id : int =Depends(oauth2.get_current_user)):


    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    # first() is requied  to view only first post where id matches

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post was not found")
    # whe we use our response_model we return only oost instead of {"message":post}
    return post
# to delete the post by id

@router.delete("/{id}")

def delete_post_id_database(id:int, db:Session=Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
   
    if  post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post was not found")

    # Now put authorization in delete functionality that the usder with proper id ,owner_id can delete post

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid authorization")

    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")

def update_post_id_database(id:int,post:schemas.Postcreate, db:Session=Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post_first=post_query.first()
   
    if  post_first ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post was not found")

    if post_first.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid authorization")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {"data":post_query.first()}