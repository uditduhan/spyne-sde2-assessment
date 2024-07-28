from pydantic import BaseModel
from typing import Optional
import uuid


class DiscussionCreate(BaseModel):
    user_id: uuid.UUID
    text: str
    image_url: Optional[str]
    hashtags: Optional[str]


class DiscussionUpdate(BaseModel):
    text: Optional[str]
    image_url: Optional[str]
    hashtags: Optional[str]


class Discussion(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    text: str
    image_url: Optional[str]
    created_at: int
    hashtags: Optional[str]

    class Config:
        orm_mode = True
