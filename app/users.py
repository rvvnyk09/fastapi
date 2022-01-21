from pydantic import BaseModel
from fastapi import FastAPI, Request, Response, status, HTTPException, Body, APIRouter
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import query
from sqlalchemy.orm.session import Session
from passwordhasher import VerifyPassword
import models, schema, passwordhasher, oauth2
from database import engine, get_db

router = APIRouter()
   
@router.post("/createuser", response_model=schema.UserCreate_Response, status_code = status.HTTP_201_CREATED)
def CreateUser(payload: schema.UserCreate,db: Session = Depends(get_db)):
    payload_dict = payload.dict()
    print("1 ->",payload_dict)
    payload_dict["password"]=passwordhasher.hash(payload.password)
    print("2 ->",payload_dict)
    new_model = models.Users(**payload_dict)
    try:
        db.add(new_model)
        db.commit()
        db.refresh(new_model)
#        return{"message":f"{payload.email_address} has been created"}
        return(new_model)
    except :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "Invalid data")

@router.post("/loginuser",status_code = status.HTTP_202_ACCEPTED,response_model = schema.Token)
def LoginUser(payload: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):   
    findemail = db.query(models.Users).filter(payload.username == models.Users.email_address).first()
    if not findemail:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
#        payload_dict = payload.dict()
        print("payload.password = ",payload.password)
        hashedpass = passwordhasher.VerifyPassword(payload.password,findemail.password)
        print("hashedpass = ",hashedpass)
        print("findemail.password = ",findemail.password)
        if hashedpass:
            access_token = oauth2.create_access_token(data={"user_id": findemail.user_id})
            return{"access_token":access_token,"token_type": "bearer"}
        else:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)


