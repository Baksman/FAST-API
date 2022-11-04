from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from . import schema,models
from sqlalchemy.orm import Session
from .config import settings
from .database import  get_db

SECRET_KEY = "0495Y3U2345Y4923847509384YRTGHJKFHKJQYEKDHBSHD"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000000
ACCESS_TOKEN_EXPIRE_DAYS = 100

oauth2_scheme =  OAuth2PasswordBearer(tokenUrl = 'login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.access_expire)
    to_encode.update({"exp": expire})
    jwtToken = jwt.encode(to_encode, SECRET_KEY, algorithm=settings.algorithm)
    return jwtToken

def get_current_user(token: str=Depends(oauth2_scheme),db:Session= Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id ==token_data.id).first()
    return user


def verify_access_token(token: str,credential_exception)->bool:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[settings.algorithm])
        id:str = payload.get("user_id")
        if not id:
            raise credential_exception
        tokendata = schema.TokenData(id=id)
    except  JWTError as e:
        raise credential_exception
    return tokendata
    