from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import service, serializer
from .database import get_db

router = APIRouter()


@router.post("/likes/", response_model=serializer.Like)
def create_like(like: serializer.LikeCreate, db: Session = Depends(get_db)):
    return service.create_like(db=db, like=like)


@router.get("/likes/{discussion_id}", response_model=List[serializer.Like])
def read_likes(
    discussion_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    likes = service.get_likes_by_discussion(
        db, discussion_id=discussion_id, skip=skip, limit=limit
    )
    return likes


@router.delete("/likes/{like_id}", response_model=serializer.Like)
def delete_like(like_id: str, db: Session = Depends(get_db)):
    return service.delete_like(db=db, like_id=like_id)
