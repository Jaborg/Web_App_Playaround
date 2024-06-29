import os

from sqlalchemy.orm import Session

from . import models, schemas


# In-memory storage for book reviews
reviews = os.listdir('app/templates/reviews')


def pretty_reviews():
    new_reviews = [x[:-5].replace('-',' ') for x in reviews if x != 'images']
    return new_reviews

def read_reviews_crud():
    return [x for x in reviews if x != 'images']

def read_review(title: str):
    
    return f'reviews/{title}'


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_review(db: Session, user: schemas.ReviewCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).offset(skip).limit(limit).all()


def create_user_review(db: Session, review: schemas.ReviewCreate, user_id: int):
    db_review = models.Item(**review.dict(), review_id=user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review