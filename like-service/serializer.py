from pydantic import BaseModel
import uuid


class LikeCreate(BaseModel):
    discussion_id: uuid.UUID
    user_id: uuid.UUID


class Like(BaseModel):
    id: uuid.UUID
    discussion_id: uuid.UUID
    user_id: uuid.UUID
    created_at: int

    class Config:
        orm_mode = True
