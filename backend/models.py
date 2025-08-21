from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    subscription_level: Literal["Free", "Basic", "Premium"]

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    is_locked: bool = False
    locked_until: Optional[datetime] = None
    
    class Config:
        orm_mode = True # For SQLAlchemy, but good practice for Pydantic models tied to data

class UserInDB(User):
    password_hash: str
    failed_login_attempts: int = 0

class Article(BaseModel):
    id: str
    title: str
    content: str
    article_type: Literal["Free", "Paid"]
    image_url: Optional[str] = None # For alt text
    image_alt_text: Optional[str] = None # For alt text
    url: str # To simulate direct navigation
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class TokenData(BaseModel):
    username: Optional[str] = None
    scope: Optional[str] = None # To store subscription level
