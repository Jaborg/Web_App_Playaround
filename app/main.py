from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session


from app import crud, models, schemas 
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    reviews = crud.read_reviews_crud()
    p_reviews = crud.pretty_reviews()
    return templates.TemplateResponse("index.html", {"request": request, "reviews" : reviews, 'p_reviews':p_reviews})

@app.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/reviews/", response_class=HTMLResponse)
async def read_reviews(request: Request):
    reviews_data = crud.read_reviews_crud
    return templates.TemplateResponse("reviews.html", {"request": request, "reviews": reviews_data})


@app.get("/reviews/{title}", response_class=HTMLResponse)
async def read_review_handler(request: Request, title: str):
    review = crud.read_review(title)
    return templates.TemplateResponse(review, {"request": request, "review": review})

@app.get("/reviews/{title}/edit", response_class=HTMLResponse)
async def edit_review_handler(request: Request, title: str):
    review = crud.read_review(title)
    return templates.TemplateResponse("edit_review.html", {"request": request, "review": review})

## New functions based on sqlalchemy models

# User functions

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users_test/", response_model=schemas.User)
def create_a_review(review: schemas.UserCreate, user_id : int, db: Session = Depends(get_db)):
    review = crud.get_reviews_by_title(db, title=review.title)
    if review:
        raise HTTPException(status_code=400, detail="Review already exists")
    return crud.create_review(db=db, user_id=user_id)



# Review functions

@app.get("/reviews_test/", response_model=list[schemas.Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = crud.get_reviews(db, skip=skip, limit=limit)
    return reviews

@app.get("/reviews_test/{title}", response_model=list[schemas.Review])
def read_review_by_title(title : str, db: Session = Depends(get_db)):
    review = crud.get_reviews_by_title(db, title=title)
    return review

@app.post("/reviews_test/", response_model=schemas.Review)
def create_a_review(review: schemas.ReviewCreate, user_id : int, db: Session = Depends(get_db)):
    mentioned_review = crud.get_reviews_by_title(db, title=review.title)
    if mentioned_review:
        raise HTTPException(status_code=400, detail="Review already exists")
    return crud.create_review(db=db, review = review, user_id=user_id)
