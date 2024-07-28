from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "elasticsearch", "port": 9200}])


def index_discussion(discussion: models.Discussion):
    es.index(
        index="discussions",
        id=str(discussion.id),
        body={
            "user_id": str(discussion.user_id),
            "text": discussion.text,
            "image_url": discussion.image_url,
            "created_at": discussion.created_at,
            "hashtags": discussion.hashtags,
        },
    )


def get_discussion(db: Session, discussion_id: str):
    return (
        db.query(models.Discussion)
        .filter(models.Discussion.id == discussion_id)
        .first()
    )


def get_discussions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Discussion).offset(skip).limit(limit).all()


def create_discussion(db: Session, discussion: schemas.DiscussionCreate):
    db_discussion = models.Discussion(
        **discussion.dict(), created_at=int(datetime.now().timestamp())
    )
    db.add(db_discussion)
    db.commit()
    db.refresh(db_discussion)
    index_discussion(db_discussion)
    return db_discussion


def update_discussion(
    db: Session, discussion_id: str, discussion: schemas.DiscussionUpdate
):
    db_discussion = get_discussion(db, discussion_id)
    if db_discussion:
        for key, value in discussion.dict(exclude_unset=True).items():
            setattr(db_discussion, key, value)
        db.commit()
        db.refresh(db_discussion)
        index_discussion(db_discussion)
    return db_discussion


def delete_discussion(db: Session, discussion_id: str):
    db_discussion = get_discussion(db, discussion_id)
    if db_discussion:
        db.delete(db_discussion)
        db.commit()
        es.delete(index="discussions", id=str(discussion_id))
    return db_discussion
