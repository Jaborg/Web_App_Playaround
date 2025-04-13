import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.crud import UserCRUD, ReviewCRUD
from app.schemas import UserCreate, ReviewCreate

# Set up an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database schema
Base.metadata.create_all(bind=engine)

@pytest.fixture(autouse=True)
def setup_database():
    """Ensure a clean database state before each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    """Create a new database session for a test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_create_user(db_session):
    """Test creating a new user."""
    user_data = UserCreate(email="test@example.com", password="password123")
    user = UserCRUD.create_user(db_session, user_data)
    assert user.email == "test@example.com"
    assert user.hashed_password.endswith("notreallyhashed")

def test_get_user(db_session):
    """Test retrieving a user by ID."""
    user_data = UserCreate(email="test2@example.com", password="password123")
    user = UserCRUD.create_user(db_session, user_data)
    retrieved_user = UserCRUD.get_user(db_session, user.id)
    assert retrieved_user.email == "test2@example.com"

def test_create_review(db_session):
    """Test creating a new review."""
    user_data = UserCreate(email="reviewer@example.com", password="password123")
    user = UserCRUD.create_user(db_session, user_data)
    review_data = ReviewCreate(title="Test Review", author="Author", content="This is a test review.")
    review = ReviewCRUD.create_review(db_session, review_data, user.id)
    assert review.title == "Test Review"
    assert review.author == "Author"
    assert review.user_id == user.id

def test_get_reviews(db_session):
    """Test retrieving reviews with pagination."""
    user_data = UserCreate(email="reviewer2@example.com", password="password123")
    user = UserCRUD.create_user(db_session, user_data)
    review_data1 = ReviewCreate(title="Review 1", author="Author 1", content="Content 1")
    review_data2 = ReviewCreate(title="Review 2", author="Author 2", content="Content 2")
    ReviewCRUD.create_review(db_session, review_data1, user.id)
    ReviewCRUD.create_review(db_session, review_data2, user.id)

    # Retrieve reviews and assert the count matches the created reviews
    reviews = ReviewCRUD.get_reviews(db_session, skip=0, limit=10)
    assert len(reviews) == 2
    assert reviews[0].title == "Review 1"
    assert reviews[1].title == "Review 2"