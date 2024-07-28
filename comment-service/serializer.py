from pydantic import BaseModel
from typing import Optional
import uuid


class CommentCreate(BaseModel):
    discussion_id: uuid.UUID
    user_id: uuid.UUID
    text: str


class CommentUpdate(BaseModel):
    text: Optional[str]


class Comment(BaseModel):
    id: uuid.UUID
    discussion_id: uuid.UUID
    user_id: uuid.UUID
    text: str
    created_at: int

    class Config:
        orm_mode = True
