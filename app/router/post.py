
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema
from typing import Optional, List
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user


router = APIRouter(prefix="/posts", tags=['Posts'])




@router.get("/", response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), current_user=Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    # posts = cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    print(limit)
    # %20 is space in query url
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id ==
                                                                                        models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(result)
    return result


@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model=schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id=(%s)""", str(id))
    # post = cursor.fetchone()
    # print(id)
    # post = find_post(int(id))
    # post = db.query(models.Post).filter(models.Post.id == id,
    #                                     models.Post.user_id == current_user.id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id ==
                                                                               models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id,
                                                                                                                                             models.Post.user_id == current_user.id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"post with id {id} not found"}

    return post


@router.delete("/{id}", status_code=200, response_model=schema.Post)
def delete_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=(%s) RETURNING *""", str(id))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    if post.first().user_id != current_user.id:
        print(post.first().user_id, current_user.id)
        raise HTTPException(status_code=403,
                            detail=f"cant complete operation on post with id")

    post.delete(synchronize_session=False)
    db.commit()
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"post with id {id} not found"}

    return post.first()


@router.post("/", response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # m_post = new_post.dict()
    # cursor.execute("""INSERT INTO posts (title, content,published) VALUES (%s,%s,%s) RETURNING * """,
    #                (new_post.title, new_post.content, new_post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    print(current_user.email)
    new_post = models.Post(**post.dict(), user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, new_post: schema.PostCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # indx = find_index_post(int(id))
    # cursor.execute("""UPDATE posts SET title =%s,content= %s,published= %s WHERE id=%s RETURNING *""",
    #                (new_post.title, new_post.content, new_post.published, str(id)))
    # post = cursor.fetchmany()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    if post.user_id != current_user.id:
        print(post.user_id, current_user.id)
        raise HTTPException(status_code=403,
                            detail=f"cant complete operation on post with id")
    post_query.update(new_post.dict(), synchronize_session=False)
    db.commit()
    # post_dict = new_post.dict()
    # post_dict['id'] = id
    # my_posts[indx] = post_dict
    # print(new_post.dict())
    return post_query.first()
