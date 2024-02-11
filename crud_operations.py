from pydantic import BaseModel

# In-memory storage for book reviews
reviews = {}

class Review(BaseModel):
    title: str
    content: str

def create_review(review: Review):
    if review.title in reviews:
        raise ValueError("Review already exists")
    else:
        reviews[review.title] = review

def read_reviews():
    return reviews

def read_review(title: str):
    if title in reviews:
        return reviews[title]
    else:
        raise ValueError("Review not found")

def update_review(title: str, review: Review):
    if title in reviews:
        reviews[title] = review
    else:
        raise ValueError("Review not found")

def delete_review(title: str):
    if title in reviews:
        del reviews[title]
    else:
        raise ValueError("Review not found")
