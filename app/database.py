from pickle import TRUE
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
from .config import settings
import os


dotenv_path = Path(__file__).parent.parent
load_dotenv(dotenv_path=str(dotenv_path)+'/.env') 
host = os.getenv('DATABASE_HOSTNAME') 
user = os.getenv('DATABASE_USERNAME')
database =  os.getenv('DATABASE_NAME')
password = os.getenv('DATABASE_PASSWORD')

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
