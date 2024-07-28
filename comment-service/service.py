from sqlalchemy.orm import Session
from . import models, serializer
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "elasticsearch", "port": 9200}])


def index_discussion(comment: models.Comment):
    es.index(
        index="comments",
        id=str(comment.id),
        body={
            "discussion_id": str(comment.discussion_id),
            "user_id": str(comment.user_id),
            "text": comment.text,
            "created_at": comment.created_at,
        },
    )


def get_comment(db: Session, comment_id: str):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def get_comments_by_discussion(
    db: Session, discussion_id: str, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Comment)
        .filter(models.Comment.discussion_id == discussion_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_comment(db: Session, comment: serializer.CommentCreate):
    db_comment = models.Comment(
        **comment.dict(), created_at=int(datetime.now().timestamp())
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    index_discussion(db_comment)
    return db_comment


def update_comment(db: Session, comment_id: str, comment: serializer.CommentUpdate):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        for key, value in comment.dict(exclude_unset=True).items():
            setattr(db_comment, key, value)
        db.commit()
        db.refresh(db_comment)
        index_discussion(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: str):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()
        es.delete(index="comments", id=str(comment_id))
    return db_comment
