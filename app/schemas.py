from pydantic import BaseModel
from datetime import date



class ReviewBase(BaseModel):
    title: str
    author: str
    content: str | None = None
   


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    date_created: date
    user_id : int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    id: int
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    is_admin: bool
    reviews: list[Review] = []

    class Config:
        from_attributes = True