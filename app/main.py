from operator import index
from typing import List, Optional, Type
from fastapi import FastAPI, Request, Response, status, HTTPException, Body, APIRouter
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2
from pydantic import BaseModel
from pydantic.types import OptionalInt
from sqlalchemy.orm import query
from sqlalchemy.orm.session import Session
import random, psycopg2, models, schema, users, oauth2
from database import engine, get_db
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

posts_all = [{"Title":"Titanic","Description":"Film by SS","Rating":4,"id":1},{"Title":"Jurassic Park","Description":"Film by Hawking","Rating":5,"id":2}]

#conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="Nighthawk3")
#cur = conn.cursor()
#cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
#conn.commit()

@app.get("/alchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return {"data":posts}

@app.get("/")
def read_root():
    return {" This is a API World"}

@app.post("/createposts",response_model=schema.PostCreate_Response, response_model_exclude=["content","published"])
def create_posts(payload: schema.PostIncoming,db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    print(payload.dict())
    incoming_payload_dict = payload.dict()
    incoming_payload_dict["id"] = random.randrange(3,9999999)
    print("incoming_payload_dict = ",incoming_payload_dict)
    new_post = models.Posts(**incoming_payload_dict)
#    return {"Output":f"Name of the book you sent is {payload['Title']} Description is {payload['Description']}"}
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

#    posts_all.append(incoming_payload_dict)
#    return {"Output":f"The new model with base is {payload.Title}"}
#    return("It is created")
#    return new_post
    return new_post
 
def find_post(checkforid):

    query_post = db.query(models.Posts.id).filter(checkforid).all
    return query_post

#    for a in posts_all:
#        if a["id"] == checkforid:
#            return a

def find_index_post(checkforid):
    for i, a in enumerate(posts_all):
        if a["id"] == checkforid:
            return i

@app.get("/posts/{id}",response_model = schema.PostCreate_Response)
def get_id(id: int, db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
#    senddata = find_post(id)
    
    query_post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if get_current_user.id != query_post.user_id:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)

    if not query_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"{id} does not exist !!!")
    else:
        return query_post

@app.get("/postsbypayload",response_model = list[schema.GetPost]) 
def get_id(payload: schema.PostIncoming, db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user),title: Optional[str] = "",content: Optional[str] = ""):
#    senddata = find_post(id)
    
#    payload_dict = payload.dict()

    query_post = db.query(models.Posts).filter(models.Posts.title.contains(title)).filter(models.Posts.content.contains(content)).filter(models.Posts.user_id == get_current_user.id).all()

    print(query_post)

#    all_response = schema.GetPost(query_post)


#    if get_current_user.id != query_post.user_id:
#        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)

    if not query_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"{id} does not exist !!!")
    else:
        return query_post

@app.put("/updatepost/{id}")
def update_post(id: int, payload: schema.PostIncoming, db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    
    payload_dict = payload.dict()
    payload_dict["id"] = id

    select_post = db.query(models.Posts).filter(models.Posts.id == id)
    select_post_first = select_post.first()

    if get_current_user.id != select_post_first.user_id:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    
#    index = find_index_post(id)
#    print("index = ",index)

    if select_post_first != None:
#        posts_all[index] = payload_dict
#        print("posts_all",posts_all)
        update_post = select_post.update(payload_dict)
        db.commit()
        
    
    if not select_post_first:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"{id} does not exist !!!")
    else:
        return{"message":f"{id} update is successful !!"}

app.include_router(users.router)
