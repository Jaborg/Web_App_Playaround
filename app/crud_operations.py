import os

from pydantic import BaseModel

# In-memory storage for book reviews
reviews = os.listdir('app/templates/reviews')

class Review(BaseModel):
    title: str
    content: str

def read_reviews_crud():
    return reviews

def read_review(title: str):
    
    return f'reviews/{title}'

    