---
inclusion: fileMatch
fileMatchPattern: "**/*.py"
---

# Python Best Practices

## Code Style (PEP 8)

### Naming Conventions
```python
# Variables and functions: snake_case
user_name = "John"
def calculate_total(items):
    pass

# Classes: PascalCase
class UserProfile:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_CONNECTIONS = 100
API_KEY = "secret"

# Private: _leading_underscore
def _internal_method():
    pass

# Protected: __double_underscore
class MyClass:
    def __init__(self):
        self.__private_var = 42
```

### Imports
```python
# Standard library first
import os
import sys
from datetime import datetime

# Third-party packages
import requests
import numpy as np
from flask import Flask, request

# Local imports
from .models import User
from .utils import validate_email
```

## Type Hints (Python 3.9+)

### Basic Types
```python
from typing import List, Dict, Optional, Union, Tuple

def greet(name: str) -> str:
    return f"Hello, {name}"

def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

def find_user(user_id: int) -> Optional[User]:
    # Returns User or None
    return db.get_user(user_id)
```

### Advanced Types
```python
from typing import Protocol, TypeVar, Generic

# Protocol (structural typing)
class Drawable(Protocol):
    def draw(self) -> None: ...

# Generic types
T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        return self._items.pop()
```

## Error Handling

### Custom Exceptions
```python
class ValidationError(Exception):
    """Raised when validation fails"""
    def __init__(self, message: str, field: str):
        self.message = message
        self.field = field
        super().__init__(self.message)

# Usage
if not email:
    raise ValidationError("Email is required", "email")
```

### Context Managers
```python
# File handling
with open('file.txt', 'r') as f:
    content = f.read()

# Database connection
with db.connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    start = time.time()
    try:
        yield
    finally:
        print(f"{name} took {time.time() - start:.2f}s")

# Usage
with timer("Database query"):
    results = db.query("SELECT * FROM users")
```

## Data Classes

### Using dataclasses
```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    id: int
    email: str
    name: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    
    def __post_init__(self):
        if not self.email:
            raise ValueError("Email is required")
```

### Using Pydantic (Recommended for APIs)
```python
from pydantic import BaseModel, EmailStr, validator

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "password": "securepass123"
            }
        }
```

## Async/Await

### Async Functions
```python
import asyncio
import aiohttp

async def fetch_user(user_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'/users/{user_id}') as response:
            return await response.json()

async def main():
    # Run multiple requests concurrently
    users = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3)
    )
    return users

# Run
asyncio.run(main())
```

## List Comprehensions & Generators

### List Comprehensions
```python
# Basic
squares = [x**2 for x in range(10)]

# With condition
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Nested
matrix = [[i*j for j in range(3)] for i in range(3)]

# Dict comprehension
user_dict = {user.id: user.name for user in users}
```

### Generators (Memory Efficient)
```python
# Generator expression
squares_gen = (x**2 for x in range(1000000))  # Doesn't create list

# Generator function
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Usage
for num in fibonacci():
    if num > 100:
        break
    print(num)
```

## Decorators

### Function Decorators
```python
from functools import wraps
import time

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done"
```

### Class Decorators
```python
def singleton(cls):
    instances = {}
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        self.connection = None
```

## Testing (pytest)

### Test Structure
```python
import pytest
from myapp import calculate_total

def test_calculate_total_with_items():
    # Arrange
    items = [10, 20, 30]
    
    # Act
    result = calculate_total(items)
    
    # Assert
    assert result == 60

def test_calculate_total_empty_list():
    assert calculate_total([]) == 0

def test_calculate_total_raises_error():
    with pytest.raises(TypeError):
        calculate_total(None)
```

### Fixtures
```python
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()

def test_user_creation(db_connection):
    user = User.create(db_connection, email="test@example.com")
    assert user.id is not None
```

## Virtual Environments

### Setup
```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Unix/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Freeze dependencies
pip freeze > requirements.txt
```

## Project Structure
```
project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── utils/
│       ├── __init__.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_services.py
├── requirements.txt
├── setup.py
└── README.md
```

## Performance Tips

### Use Built-in Functions
```python
# ✅ Fast
sum(numbers)
max(numbers)
any(conditions)
all(conditions)

# ❌ Slow
total = 0
for num in numbers:
    total += num
```

### Use Sets for Membership
```python
# ✅ Fast - O(1)
allowed_users = {'user1', 'user2', 'user3'}
if user in allowed_users:
    pass

# ❌ Slow - O(n)
allowed_users = ['user1', 'user2', 'user3']
if user in allowed_users:
    pass
```
