from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import service, serializer, models
from .database import get_db

router = APIRouter()


@router.post("/discussions/", response_model=serializer.Discussion)
def create_discussion(
    discussion: serializer.DiscussionCreate, db: Session = Depends(get_db)
):
    return service.create_discussion(db=db, discussion=discussion)


@router.get("/discussions/", response_model=List[serializer.Discussion])
def read_discussions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    discussions = service.get_discussions(db, skip=skip, limit=limit)
    return discussions


@router.get("/discussions/{discussion_id}", response_model=serializer.Discussion)
def read_discussion(discussion_id: str, db: Session = Depends(get_db)):
    discussion = service.get_discussion(db, discussion_id=discussion_id)
    if discussion is None:
        raise HTTPException(status_code=404, detail="Discussion not found")
    return discussion


@router.put("/discussions/{discussion_id}", response_model=serializer.Discussion)
def update_discussion(
    discussion_id: str,
    discussion: serializer.DiscussionUpdate,
    db: Session = Depends(get_db),
):
    return service.update_discussion(
        db=db, discussion_id=discussion_id, discussion=discussion
    )


@router.delete("/discussions/{discussion_id}", response_model=serializer.Discussion)
def delete_discussion(discussion_id: str, db: Session = Depends(get_db)):
    return service.delete_discussion(db=db, discussion_id=discussion_id)
