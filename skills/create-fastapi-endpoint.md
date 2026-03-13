---
name: create-fastapi-endpoint
description: Create FastAPI endpoint with validation, error handling, and async support
---

# Create FastAPI Endpoint

Creates a production-ready FastAPI endpoint with:
- Pydantic validation
- Async/await support
- Error handling
- OpenAPI documentation
- Dependency injection

## Usage
```
#create-fastapi-endpoint <resource> <method>
```

## Example
```
#create-fastapi-endpoint users POST
```

## Implementation

### 1. Router
```python
# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..schemas.user import UserCreate, UserResponse
from ..services.user_service import UserService
from ..dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with email and password"
)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user with the following information:
    
    - **email**: Valid email address
    - **name**: User's full name
    - **password**: Strong password (min 8 characters)
    """
    try:
        user = await UserService.create(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID"
)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = await UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
```

### 2. Schemas (Pydantic)
```python
# schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True
```

### 3. Service Layer
```python
# services/user_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from typing import Optional

from ..models.user import User
from ..schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    async def create(db: Session, user_data: UserCreate) -> User:
        # Check if user exists
        existing = db.query(User).filter(
            User.email == user_data.email
        ).first()
        
        if existing:
            raise ValueError("User with this email already exists")
        
        # Hash password
        hashed_password = pwd_context.hash(user_data.password)
        
        # Create user
        user = User(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password
        )
        
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            raise ValueError("Failed to create user")
    
    @staticmethod
    async def get_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()
```

### 4. Model
```python
# models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### 5. Tests
```python
# tests/test_users.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app
from ..database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)

def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "SecurePass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_user_duplicate_email(client):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "SecurePass123"
    }
    client.post("/users/", json=user_data)
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
```
