from sqlalchemy.orm.session import Session
from routers.schemas import PostBase
from db.models import DbPost
from datetime import datetime
from fastapi import HTTPException, status

def create_post(db:Session, request: PostBase):
    new_post =DbPost(
        image_url = request.image_url,
        image_url_type= request.image_url_type,
        caption=request.caption,
        timestamp=datetime.now(),
        user_id= request.creator_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_all(db:Session):
    return db.query(DbPost).all()

def delete(db: Session, id:int, user_id:int):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Post with the id {id}")
    
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Only post creator can delete post {user_id}")
    
    db.delete(post)
    db.commit()
    return{
        "id" :user_id,
        "message": "Deleted Succesfully" 
    }