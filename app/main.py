
# import time
# from typing import Optional,List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
# from .utils import hash
from .router import user,post,vote
# import psycopg2
# from psycopg2.extras ximport RealDictCursor
from . import models
# from sqlalchemy.orm import Session
from .database import engine, get_db

# class Settings(BaseSettings):
#     database_hostname:str 
#     database_password:str  
#     database_username: str 
#     database_port :str
#     database_name:str
#     secret_key:str
#     algorithm:str
#     access_expire:int

# settings = Settings()


models.Base.metadata.create_all(bind=engine)
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,ppro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
# router
# yea



# while True:
#     try:
#         conn = psycopg2.connect(host=host, database=database, user=username,
#                                 password=password, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('db connection established!')
#         break
#     except Exception as error:
#         print(f'connecting to db failed ${error}')
#         time.sleep(2)




