from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.crud_operations import  read_review, read_reviews_crud

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


class ReviewInput(BaseModel):
    title: str
    content: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    reviews = read_reviews_crud()
    return templates.TemplateResponse("index.html", {"request": request, "reviews" : reviews})

@app.get("/reviews/", response_class=HTMLResponse)
async def read_reviews(request: Request):
    reviews_data = read_reviews_crud
    return templates.TemplateResponse("reviews.html", {"request": request, "reviews": reviews_data})


@app.get("/reviews/{title}", response_class=HTMLResponse)
async def read_review_handler(request: Request, title: str):
    review = read_review(title)
    return templates.TemplateResponse(review, {"request": request, "review": review})

@app.get("/reviews/{title}/edit", response_class=HTMLResponse)
async def edit_review_handler(request: Request, title: str):
    review = read_review(title)
    return templates.TemplateResponse("edit_review.html", {"request": request, "review": review})

