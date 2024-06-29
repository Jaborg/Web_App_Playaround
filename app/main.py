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


@app.post("/reviews_test/", response_model=schemas.Review)
def create_review(user: schemas.ReviewCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


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


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_review_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items