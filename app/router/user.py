
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .. import utils
from .. import oauth2
router = APIRouter(prefix="/user",tags=['USERS'])


@router.post("/login", status_code=status.HTTP_201_CREATED,response_model=schema.Token)
def login(user_req: schema.UserLogin, db: Session = Depends(get_db)):
    # hash password
    user = db.query(models.User).filter(
        models.User.email == user_req.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials")
    if not utils.verify(user_req.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials")
    token = oauth2.create_access_token(data={'user_id': user.id})
    return {
        "access_token":token,
        "token_type": "Bearer token",
    }


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # hash password
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    # hash password
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return user
