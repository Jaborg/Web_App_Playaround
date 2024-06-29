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

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_admin: bool
    user_id : int
    reviews: list[Review] = []

    class Config:
        orm_mode = True