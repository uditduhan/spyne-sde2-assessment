from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import service, serializer
from .database import get_db

router = APIRouter()


@router.post("/comments/", response_model=serializer.Comment)
def create_comment(comment: serializer.CommentCreate, db: Session = Depends(get_db)):
    return service.create_comment(db=db, comment=comment)


@router.get("/comments/{discussion_id}", response_model=List[serializer.Comment])
def read_comments(
    discussion_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    comments = service.get_comments_by_discussion(
        db, discussion_id=discussion_id, skip=skip, limit=limit
    )
    return comments


@router.put("/comments/{comment_id}", response_model=serializer.Comment)
def update_comment(
    comment_id: str, comment: serializer.CommentUpdate, db: Session = Depends(get_db)
):
    return service.update_comment(db=db, comment_id=comment_id, comment=comment)


@router.delete("/comments/{comment_id}", response_model=serializer.Comment)
def delete_comment(comment_id: str, db: Session = Depends(get_db)):
    return service.delete_comment(db=db, comment_id=comment_id)
