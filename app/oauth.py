#!/usr/bin/env python
from jose import JWTError,jwt
from datetime import datetime, timedelta
from . import schemas
from .config import settings
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')
# Needed Inputs
# Secret key
# Algorithm
#Expriation time
S_KEY=settings.s_key
ALGO=settings.varify_pass_algo
ATE_MINUTES=300000000

def create_access_token(data: dict):
    to_encode= data.copy()
    # utcnow is essential for currect time
    expire = datetime.utcnow() + timedelta(minutes=ATE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode,S_KEY,algorithm=ALGO)
    return encode_jwt

def verify_access_token(token: str, cred_exception):
    try:
        payload = jwt.decode(token,S_KEY,algorithms=[ALGO])
        id: str = payload.get("user_id")

        if id is None:
            raise cred_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise cred_exception
    return token_data
def get_current_user(token: str = Depends(oauth2_schema)):
    cred_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    # following suggestion maybe flowed
   # query database for id, then compare it with token.id
   # then, raise 403 if not in db, else return token
    return verify_access_token(token,cred_exception)
