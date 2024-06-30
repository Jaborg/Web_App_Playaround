import os

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import date

from . import models, schemas
from app.models import Review, User
from app.schemas import ReviewCreate


# In-memory storage for book reviews
reviews = os.listdir('app/templates/reviews')

# Old operations based on review template dir


def pretty_reviews():
    new_reviews = [x[:-5].replace('-',' ') for x in reviews if x != 'images']
    return new_reviews

def read_reviews_crud():
    return [x for x in reviews if x != 'images']

def read_review(title: str):
    
    return f'reviews/{title}'


## New operations based on model

# User operations

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def delete_user(db: Session, user_id: int):
    try:
        user = db.query(User).filter(User.id == user_id).one()
        db.delete(user)
        db.commit()
    except NoResultFound:
        return None
    return user

# Review operations

def create_review(db: Session, review: ReviewCreate, user_id: int):
    # Create a new Review instance
    db_review = Review(
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


def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).offset(skip).limit(limit).all()

def get_reviews_by_title(db: Session, title: int):
    return db.query(Review).filter(Review.title == title).all()

def delete_review(db: Session, review_id: int):
    try:
        review = db.query(Review).filter(Review.id == review_id).one()
        db.delete(review)
        db.commit()
    except NoResultFound:
        return None
    return review