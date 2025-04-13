from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date
from typing import List, Optional

class ReviewBase(BaseModel):
    title: str = Field(..., max_length=100, description="Title of the review")
    author: str = Field(..., max_length=50, description="Author of the review")
    content: Optional[str] = Field(None, description="Content of the review")

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    date_created: date
    user_id: int

    class Config(ConfigDict):
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email address of the user")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password for the user")

class User(UserBase):
    id: int
    is_admin: bool = Field(False, description="Indicates if the user is an admin")
    reviews: List[Review] = []

    class Config(ConfigDict):
        from_attributes = True