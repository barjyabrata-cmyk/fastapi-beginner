from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models,utils,oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login",response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm=Depends() ,
    db: Session = Depends(database.get_db)
):

  # oauth2passwordrequestform returns
  # username
  #password
  # without writing oaurth2form we also use user.credentials : user_login schemas where we use email
  # and when use oauth2 in postman use from data insted of raw body
  

  user = db.query(models.User).filter(models.User.email ==user_credentials.username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Credentials Incorrect")
  
  if not utils.verify(user_credentials.password,user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Credentials Incorrect")

  # craete a token and return toke


  # create access token

  access_token=oauth2.create_access_token(data={"user_id":user.id})

  return {"access_token": access_token,"token_type":"bearer"}


  
    
 