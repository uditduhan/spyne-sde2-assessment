from pydantic import BaseModel, EmailStr
import uuid
from typing import Optional

class UserCreate(BaseModel):
    name: str
    mobile_no: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    mobile_no: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

class User(BaseModel):
    id: uuid.UUID
    name: str
    mobile_no: str
    email: EmailStr
    created_at: int

    class Config:
        orm_mode = True
