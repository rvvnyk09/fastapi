from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy.sql.sqltypes import TIMESTAMP, String

class PostIncoming(BaseModel):
    title: str
    content: Optional[str] = "No Content"
    published: Optional[bool] = False

    class Config:
        orm_mode = True

class GetPost(PostIncoming):
    user_id : int

    class Config:
        orm_mode = True

class PostCreate_Response(PostIncoming):
    id: int

    class Config:
        orm_mode = True 

class UserCreate(BaseModel):
    email_address: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserCreate_Response(BaseModel):
    email_address: EmailStr

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id: Optional[int] = None

class Token(BaseModel):
    access_token : str
    token_type : str