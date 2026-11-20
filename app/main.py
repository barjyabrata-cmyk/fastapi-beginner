from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas,utils
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session 
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware


 # models.Base.metadata.create_all(bind=engine)

app=FastAPI()

# for CORS to make it availble on any webfrom

# list of website to allow my api ,,,i mentio website like google,youtube,* means all

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# here published is optional if not given default value is true 
while True:
  try:
    conn= psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='msdcsk2007',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("DATABSE connected succesfully\n")
    break
  except Exception as error:
    print("failed database connection")
    print("Error",error)
    time.sleep(5)

my_posts=[{"title":"title of postv 1","content":"content of post 1","id":1},{"title":"favourite foods","content":"i like pizaa","id":2}]

def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
         return p
def find_index_posts(id):
     for i,p in enumerate (my_posts):
         if p['id'] == id:
             return i





         
app.include_router(post.router)   # it connects the post and user file in tthe router dircatory
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)








@app.get("/")    
# that is called 'get'http method...without it it is a normal function..not api call held
# '/' is the path operation
#@ is called decorator
async def root():
    return {"message":"dipayan chudir bhai  "}

# the code to connect  with database and get the data from the postgresql

@app.get("/arjya")
def get_posts():
   cursor.execute(""" SELECT * FROM posts """)
   post=cursor.fetchall()
   return {"data":post}

# note : if two function has same http method and path opetration then forst one is run
@app.post("/createposts")

def create_post(x : dict =Body(...)):

    # here  x is a varriable which is stroe the value in the body of postman...
    print(x)
    return {"message":f"title :{x['title']} content:{x['content']}"}


#using pydantic basemodel

@app.post("/xyz",status_code=status.HTTP_201_CREATED)

# HTTP_201.. - IS written just for make the stauts code 201 because it was universal code for created 


def create_new_post(new_post:schemas.Postcreate):

    # here  post is a varriable which is stroe the value in the body of postman...
   # print(new_post)

   post_dict=new_post.dict()

   post_dict['id']=randrange(0,10000)

   my_posts.append(post_dict)

   #   print(new_post.dict())

    # to make the pydantic model into a dictionary format 
   return {"message":post_dict}

@app.get("/xyz")

def view_posts():
    return {"data":my_posts}

#to retrive single post 

@app.get("/xyz/{id}")  #so url is this type of..id is reffered to the specefic post

#  note : "here the given id is always string type not ineteger type "
# this code is taken id and return the data realted to id
def view_post(id :int,response :Response):  # convert into int
    post=find_posts(id)

    if not post :
       # response.status_code=404
        #return {"message":f"post with {id} not given "}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    

    # the code is for if unkonwned id number is given it gives 404 error status
    # two codes make same error message but two different process
      
    return {"post details": post}


@app.delete("/xyz/{id}",status_code= status.HTTP_204_NO_CONTENT)

def delete_post(id:int):
    #deleting post
    #find the indx of the array that has required id
    #then delee it

    index=find_index_posts(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT) 

# put method to update the previous post

@app.put("/xyz/{id}")

def update_post(id:int,post:schemas.Postcreate):
    index=find_index_posts(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not exist")

    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {"data":post_dict}

# this code to insert new values in database and print this 

@app.post("/database",status_code=status.HTTP_201_CREATED)

def create_new_post_database(post:schemas.Postcreate):

    cursor.execute(""" INSERT INTO POSTS (title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    new_posts=cursor.fetchone()  # to print the new post in database with the help of post created body schema class

    conn.commit()  # to make changes in the database

    
    return {"data":new_posts}

# it is to print the data from the database from the given id

@app.get("/database/{id}")

def view_new_posts_id(id:str):  # str beacuse in database id stored in data fromat
    cursor.execute(""" SELECT * FROM posts WHERE id=%s """,(id))  # to print those row data where id given
    post=cursor.fetchone()  # fetchone to print the one row data
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found") # if wrong id given throw error
    return {"posts":post}


# it is to delete the data from database for specefic id

@app.delete("/database/{id}",status_code=status.HTTP_204_NO_CONTENT)

def delete_id_posts_database(id: str):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(id))
    deleted_post=cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# IT IS TO update the data in database with code

@app.put("/database/{id}")

def update_new_post_database( id :str,post:schemas.Postcreate):
    cursor.execute(""" UPDATE posts SET title=%s,content=%s,published=%s WHERE id =%s RETURNING *  """,(post.title,post.content,post.published,(id)))
    updated_posts=cursor.fetchone()
    conn.commit()

    if updated_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    return{"data":updated_posts}


# to check sqlalchemy 

@app.get("/getsqlalchemy")

def test_post(db:Session =Depends(get_db)):
    return{"message":"successfully done"}

