from sqlalchemy.orm import Session
from . import models, serializer
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "elasticsearch", "port": 9200}])


def index_discussion(like: models.Like):
    es.index(
        index="likes",
        id=str(like.id),
        body={
            "discussion_id": str(like.discussion_id),
            "user_id": str(like.user_id),
            "created_at": like.created_at,
        },
    )


def get_like(db: Session, like_id: str):
    return db.query(models.Like).filter(models.Like.id == like_id).first()


def get_likes_by_discussion(
    db: Session, discussion_id: str, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Like)
        .filter(models.Like.discussion_id == discussion_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_like(db: Session, like: serializer.LikeCreate):
    db_like = models.Like(**like.dict(), created_at=int(datetime.now().timestamp()))
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    index_discussion(db_like)
    return db_like


def delete_like(db: Session, like_id: str):
    db_like = get_like(db, like_id)
    if db_like:
        db.delete(db_like)
        db.commit()
        es.delete(index="likes", id=str(like_id))
    return db_like
