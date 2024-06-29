from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , Date
from sqlalchemy.orm import relationship

from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True)
    author = Column(String)
    content = Column(Boolean)
    date_created = Column(Date)

    user = relationship("User", back_populates="reviews")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    hashed_password = Column(String, index=True)
    is_admin = Column(Boolean,)
    user_id = Column(Integer, ForeignKey("reviews.id"))

    reviews = relationship("Review", back_populates="user")