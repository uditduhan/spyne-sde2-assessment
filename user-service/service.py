from sqlalchemy.orm import Session
from . import models, serializer
from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "elasticsearch", "port": 9200}])


def index_users(user: models.User):
    es.index(
        index="users",
        id=str(user.id),
        body={
            "name": str(user.name),
            "mobile_no": user.mobile_no,
            "email": user.email,
            "created_at": user.created_at,
        },
    )


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: serializer.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    index_users(db_user)
    return db_user


def update_user(db: Session, user_id: str, user: serializer.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        index_users(db_user)
    return db_user


def delete_user(db: Session, user_id: str):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        es.delete(index="users", id=str(user_id))
    return db_user
