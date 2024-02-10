from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# In-memory storage for book reviews
reviews = {}

class Review(BaseModel):
    title: str
    content: str

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("templates/index.html", {"request": request, "message": "Welcome to the Book Review API!"})

@app.get("/reviews/", response_class=HTMLResponse)
def read_reviews(request: Request):
    return templates.TemplateResponse("templates/reviews.html", {"request": request, "reviews": reviews})

@app.post("/reviews/", response_class=HTMLResponse)
def create_review(request: Request, review: Review):
    if review.title in reviews:
        raise HTTPException(status_code=400, detail="Review already exists")
    else:
        reviews[review.title] = review
        return templates.TemplateResponse("templates/review_created.html", {"request": request, "review": review})

@app.get("/reviews/{title}", response_class=HTMLResponse)
def read_review(request: Request, title: str):
    if title in reviews:
        review = reviews[title]
        return templates.TemplateResponse("templates/review_detail.html", {"request": request, "review": review})
    else:
        raise HTTPException(status_code=404, detail="Review not found")

@app.put("/reviews/{title}", response_class=HTMLResponse)
def update_review(request: Request, title: str, review: Review):
    if title in reviews:
        reviews[title] = review
        return templates.TemplateResponse("templates/review_updated.html", {"request": request, "review": review})
    else:
        raise HTTPException(status_code=404, detail="Review not found")

@app.delete("/reviews/{title}", response_class=HTMLResponse)
def delete_review(request: Request, title: str):
    if title in reviews:
        del reviews[title]
        return templates.TemplateResponse("templates/review_deleted.html", {"request": request, "title": title})
    else:
        raise HTTPException(status_code=404, detail="Review not found")
