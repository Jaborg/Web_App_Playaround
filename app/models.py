from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , Date
from sqlalchemy.orm import relationship

from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True)
    author = Column(String)
    content = Column(String)
    date_created = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))


    user = relationship("User", back_populates="reviews", foreign_keys=[user_id])


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    hashed_password = Column(String, index=True)
    is_admin = Column(Boolean,default=False)
    user_id = Column(Integer, ForeignKey("reviews.user_id"))

    reviews = relationship("Review", back_populates="user", foreign_keys=[Review.user_id])