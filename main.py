from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from logging import log

from crud_operations import create_review, read_reviews, read_review, update_review, delete_review

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class ReviewInput(BaseModel):
    Title: str
    Content: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/reviews/", response_class=HTMLResponse)
async def read_reviews(request: Request):
    reviews_data = read_reviews()
    return templates.TemplateResponse("reviews.html", {"request": request, "reviews": reviews_data})

@app.post("/reviews/", response_class=HTMLResponse)
async def create_review_handler(request: Request, review: ReviewInput):
    create_review({'Title':review.Title,'Content':review.Content})
    return templates.TemplateResponse("review_created.html", {"request": request, "review": review})

@app.get("/reviews/{title}", response_class=HTMLResponse)
async def read_review_handler(request: Request, title: str):
    review = read_review(title)
    return templates.TemplateResponse("review_detail.html", {"request": request, "review": review})

@app.get("/reviews/{title}/edit", response_class=HTMLResponse)
async def edit_review_handler(request: Request, title: str):
    review = read_review(title)
    return templates.TemplateResponse("edit_review.html", {"request": request, "review": review})

@app.post("/reviews/{title}")
async def update_review_handler(request: Request, title: str, review: ReviewInput):
    update_review(title, review)
    return {"message": "Review updated successfully"}

@app.post("/reviews/{title}/delete")
async def delete_review_handler(request: Request, title: str):
    delete_review(title)
    return {"message": "Review deleted successfully"}
