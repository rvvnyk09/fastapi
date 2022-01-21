from hashlib import algorithms_available
from jose import JWTError, jwt
from jose.constants import ALGORITHMS, Algorithms
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.param_functions import Depends
import schema,config

SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
    id: int = payload.get("user_id")
    
    print("id in oauth2 = ",id)
    print("id tpye in outh2 = ",type(id))
    token_data = schema.TokenData(id = id)

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_access_token(token)