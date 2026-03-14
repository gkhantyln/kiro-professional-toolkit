---
name: setup-python-testing-advanced
description: Advanced Python testing with pytest fixtures, property-based testing (Hypothesis), mutation testing (mutmut), contract testing (Pact), and async test patterns
---

# Setup Python Testing Advanced

İleri seviye Python test altyapısı kurar:
- pytest advanced fixtures + factories
- Property-based testing (Hypothesis)
- Mutation testing (mutmut)
- Contract testing (Pact)
- Async test patterns (pytest-asyncio)
- Snapshot testing
- Performance regression tests

## Usage
```
#setup-python-testing-advanced <project-name>
```

## conftest.py
```python
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from unittest.mock import AsyncMock
import factory
from factory.alchemy import SQLAlchemyModelFactory
from app.main import app
from app.database import Base, get_session
from app.models import User, Order

# ── Database fixtures ──────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def event_loop_policy():
    import asyncio
    return asyncio.DefaultEventLoopPolicy()

@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture
async def session(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as s:
        async with s.begin():
            yield s
            await s.rollback()

@pytest_asyncio.fixture
async def client(session):
    async def override_session():
        yield session

    app.dependency_overrides[get_session] = override_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

# ── Factory fixtures ───────────────────────────────────────────────────────────

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    id = factory.LazyFunction(lambda: str(__import__("uuid").uuid4()))
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    role = "user"
    is_active = True

class OrderFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Order
        sqlalchemy_session_persistence = "commit"

    id = factory.LazyFunction(lambda: str(__import__("uuid").uuid4()))
    user = factory.SubFactory(UserFactory)
    total = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    status = "pending"

@pytest.fixture
def make_user(session):
    UserFactory._meta.sqlalchemy_session = session
    return UserFactory

@pytest.fixture
def make_order(session):
    OrderFactory._meta.sqlalchemy_session = session
    OrderFactory._meta.sqlalchemy_session = session
    return OrderFactory
```

## tests/test_property_based.py (Hypothesis)
```python
from hypothesis import given, settings, assume, HealthCheck
from hypothesis import strategies as st
from hypothesis.extra.pandas import data_frames, column
import pytest
from app.services.pricing import calculate_discount, validate_email, parse_amount

# ── Property-based tests ───────────────────────────────────────────────────────

@given(
    price=st.floats(min_value=0.01, max_value=1_000_000, allow_nan=False, allow_infinity=False),
    discount_pct=st.integers(min_value=0, max_value=100),
)
@settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
def test_discount_never_exceeds_price(price: float, discount_pct: int):
    """Discount must never make price negative."""
    result = calculate_discount(price, discount_pct)
    assert result >= 0
    assert result <= price

@given(st.emails())
def test_valid_emails_always_accepted(email: str):
    assert validate_email(email) is True

@given(
    amount_str=st.from_regex(r"\d{1,8}\.\d{2}", fullmatch=True),
)
def test_parse_amount_roundtrip(amount_str: str):
    """Parsing and re-serializing amount must be idempotent."""
    parsed = parse_amount(amount_str)
    assert str(parsed) == amount_str

@given(
    items=st.lists(
        st.fixed_dictionaries({"price": st.floats(min_value=0, max_value=9999), "qty": st.integers(min_value=1, max_value=100)}),
        min_size=1, max_size=50,
    )
)
def test_order_total_equals_sum_of_items(items):
    from app.services.order import compute_total
    total = compute_total(items)
    expected = sum(i["price"] * i["qty"] for i in items)
    assert abs(total - expected) < 0.001  # float tolerance
```

## tests/test_contracts.py (Pact consumer)
```python
import pytest
from pact import Consumer, Provider
import requests

PACT_MOCK_HOST = "localhost"
PACT_MOCK_PORT = 1234

@pytest.fixture(scope="module")
def pact():
    pact = Consumer("OrderService").has_pact_with(
        Provider("UserService"),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT,
        pact_dir="./pacts",
    )
    pact.start_service()
    yield pact
    pact.stop_service()

def test_get_user_contract(pact):
    expected_user = {"id": "abc-123", "email": "user@example.com", "name": "Test User"}

    (pact
     .given("User abc-123 exists")
     .upon_receiving("a request for user abc-123")
     .with_request("GET", "/api/v1/users/abc-123")
     .will_respond_with(200, body=expected_user))

    with pact:
        result = requests.get(f"http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}/api/v1/users/abc-123")
        assert result.json() == expected_user
```

## tests/test_performance.py (pytest-benchmark)
```python
import pytest
from app.services.search import search_users

@pytest.mark.benchmark(group="search", min_rounds=100)
def test_search_performance(benchmark, make_user):
    """Search must complete in < 50ms at p99."""
    users = [make_user(name=f"User {i}") for i in range(1000)]

    result = benchmark.pedantic(
        search_users,
        args=("User 500",),
        iterations=10,
        rounds=100,
    )
    assert benchmark.stats["mean"] < 0.05  # 50ms
    assert len(result) > 0
```

## pyproject.toml (test config)
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = [
    "--strict-markers",
    "--tb=short",
    "-p no:warnings",
    "--cov=app",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=85",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
    "contract: marks contract tests",
]

[tool.mutmut]
paths_to_mutate = "app/"
tests_dir = "tests/"
runner = "python -m pytest tests/unit -x -q"
```
