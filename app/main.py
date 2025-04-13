from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal, engine

# Initialize database and app
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

class InMemoryRoutes:
    """Routes for in-memory operations."""

    @staticmethod
    @app.get("/", response_class=HTMLResponse)
    async def read_root(request: Request):
        reviews = crud.read_reviews_crud()
        p_reviews = crud.pretty_reviews()
        return templates.TemplateResponse("index.html", {"request": request, "reviews": reviews, "p_reviews": p_reviews})

    @staticmethod
    @app.get("/about", response_class=HTMLResponse)
    async def read_about(request: Request):
        return templates.TemplateResponse("about.html", {"request": request})

    @staticmethod
    @app.get("/reviews/{title}", response_class=HTMLResponse)
    async def read_review_handler(request: Request, title: str):
        review = crud.read_review(title)
        return templates.TemplateResponse(review, {"request": request, "review": review})

class DatabaseRoutes:
    """Routes for database operations."""

    @staticmethod
    @app.get("/users/", response_model=list[schemas.User])
    def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return crud.UserCRUD.get_users(db, skip=skip, limit=limit)

    @staticmethod
    @app.get("/users/{user_id}", response_model=schemas.User)
    def read_user(user_id: int, db: Session = Depends(get_db)):
        db_user = crud.UserCRUD.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    @staticmethod
    @app.post("/users/", response_model=schemas.User)
    def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
        existing_user = crud.UserCRUD.get_user_by_email(db, email=user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        return crud.UserCRUD.create_user(db=db, user=user)

    @staticmethod
    @app.get("/reviews/", response_model=list[schemas.Review])
    def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return crud.ReviewCRUD.get_reviews(db, skip=skip, limit=limit)

    @staticmethod
    @app.get("/reviews/{title}", response_model=list[schemas.Review])
    def read_review_by_title(title: str, db: Session = Depends(get_db)):
        return crud.ReviewCRUD.get_reviews_by_title(db, title=title)

    @staticmethod
    @app.post("/reviews/", response_model=schemas.Review)
    def create_review(review: schemas.ReviewCreate, user_id: int, db: Session = Depends(get_db)):
        existing_review = crud.ReviewCRUD.get_reviews_by_title(db, title=review.title)
        if existing_review:
            raise HTTPException(status_code=400, detail="Review already exists")
        return crud.ReviewCRUD.create_review(db=db, review=review, user_id=user_id)
