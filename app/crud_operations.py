import os

from pydantic import BaseModel

# In-memory storage for book reviews
reviews = os.listdir('app/templates/reviews')

class Review(BaseModel):
    title: str
    content: str


def pretty_reviews():
    new_reviews = [x[:-5].replace('-',' ') for x in reviews]
    return new_reviews

def read_reviews_crud():
    return reviews

def read_review(title: str):
    
    return f'reviews/{title}'

    