from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True
    
class Vote(BaseModel):
    post_id: int
    dir : conint(le=1)

class PostCreate(PostBase):
    pass




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[int]= None

class UserCreate(BaseModel):
    password: str
    email: EmailStr




class UserLogin(BaseModel):
    password: str
    email: EmailStr

class UserOut(BaseModel):
    created_at: datetime
    email: EmailStr
    id: int

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner:UserOut
    user_id:int

    class Config:
        orm_mode = True
    
class PostOut(BaseModel):
    Post: Post
    votes :int

    class Config:
        orm_mode = True
    