import os
from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from . import models, schemas

# In-memory operations for reviews

def pretty_reviews() -> List[str]:
    """Generate a list of prettified review titles."""
    reviews = os.listdir('app/templates/reviews')
    return [x[:-5].replace('-', ' ') for x in reviews if x != 'images']

def read_reviews_crud() -> List[str]:
    """Read all review filenames from the templates directory."""
    reviews = os.listdir('app/templates/reviews')
    return [x for x in reviews if x != 'images']

def read_review(title: str) -> str:
    """Get the path to a specific review template."""
    return f'reviews/{title}'

class ReviewCRUD:
    """CRUD operations for reviews."""

    @staticmethod
    def create_review(db: Session, review: schemas.ReviewCreate, user_id: int) -> models.Review:
        db_review = models.Review(
            title=review.title,
            author=review.author,
            content=review.content,
            date_created=date.today(),
            user_id=user_id
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review

    @staticmethod
    def get_reviews(db: Session, skip: int = 0, limit: int = 100) -> List[models.Review]:
        return db.query(models.Review).offset(skip).limit(limit).all()

    @staticmethod
    def get_reviews_by_title(db: Session, title: str) -> List[models.Review]:
        return db.query(models.Review).filter(models.Review.title == title).all()

    @staticmethod
    def delete_review(db: Session, review_id: int) -> Optional[models.Review]:
        try:
            review = db.query(models.Review).filter(models.Review.id == review_id).one()
            db.delete(review)
            db.commit()
        except NoResultFound:
            return None
        return review

class UserCRUD:
    """CRUD operations for users."""

    @staticmethod
    def create_user(db: Session, user: schemas.UserCreate) -> models.User:
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
        return db.query(models.User).offset(skip).limit(limit).all()

    @staticmethod
    def delete_user(db: Session, user_id: int) -> Optional[models.User]:
        try:
            user = db.query(models.User).filter(models.User.id == user_id).one()
            db.delete(user)
            db.commit()
        except NoResultFound:
            return None
        return user