import os

from pydantic import BaseModel

# In-memory storage for book reviews
reviews = os.listdir('app/templates/reviews')

class Review(BaseModel):
    title: str
    content: str


def pretty_reviews():
    new_reviews = [x[:-5].replace('-',' ') for x in reviews if x != 'images']
    return new_reviews

def read_reviews_crud():
    return [x for x in reviews if x != 'images']

def read_review(title: str):
    
    return f'reviews/{title}'

    