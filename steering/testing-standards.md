---
inclusion: fileMatch
fileMatchPattern: "**/*.{test,spec}.{ts,tsx,js,jsx,py,go}"
---

# Testing Standards — İleri Seviye

## Test Piramidi

```
        /\
       /E2E\        az sayıda, yavaş, pahalı
      /------\
     /Integr. \     orta sayıda
    /----------\
   /  Unit Tests \  çok sayıda, hızlı, ucuz
  /--------------\
```

## TypeScript — Vitest + Testing Library

```typescript
// ✅ AAA pattern: Arrange, Act, Assert
describe("OrderService", () => {
  let service: OrderService;
  let mockRepo: MockedObject<OrderRepository>;

  beforeEach(() => {
    mockRepo = createMock<OrderRepository>();
    service = new OrderService(mockRepo);
  });

  it("should create order and emit event", async () => {
    // Arrange
    const userId = "user-123";
    const items = [{ productId: "p-1", quantity: 2, price: 50 }];
    mockRepo.save.mockResolvedValue({ id: "order-1", userId, items, total: 100 });

    // Act
    const result = await service.createOrder(userId, items);

    // Assert
    expect(result.id).toBe("order-1");
    expect(result.total).toBe(100);
    expect(mockRepo.save).toHaveBeenCalledOnce();
    expect(mockRepo.save).toHaveBeenCalledWith(expect.objectContaining({ userId }));
  });

  it("should throw when items is empty", async () => {
    await expect(service.createOrder("user-1", [])).rejects.toThrow("Items cannot be empty");
  });
});

// ✅ React Testing Library — kullanıcı davranışı test et
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

describe("LoginForm", () => {
  it("should show error on invalid email", async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={vi.fn()} />);

    await user.type(screen.getByLabelText(/email/i), "invalid-email");
    await user.click(screen.getByRole("button", { name: /giriş/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent("Geçerli email girin");
  });

  it("should call onSubmit with credentials", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    render(<LoginForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/email/i), "test@example.com");
    await user.type(screen.getByLabelText(/şifre/i), "password123");
    await user.click(screen.getByRole("button", { name: /giriş/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: "test@example.com",
        password: "password123",
      });
    });
  });
});
```

## Python — pytest İleri Seviye

```python
# conftest.py
import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def db_engine():
    engine = create_async_engine("postgresql+asyncpg://test:test@localhost/test_db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    async with AsyncSession(db_engine) as session:
        async with session.begin():
            yield session
            await session.rollback()  # Her test sonrası rollback

@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# test_orders.py
import pytest
from unittest.mock import AsyncMock, patch

class TestOrderService:
    async def test_create_order_success(self, db_session):
        service = OrderService(db_session)
        order = await service.create_order(
            user_id="user-1",
            items=[{"product_id": "p-1", "quantity": 2}]
        )
        assert order.id is not None
        assert order.status == "pending"

    async def test_create_order_insufficient_stock(self, db_session):
        with pytest.raises(InsufficientStockError) as exc_info:
            await service.create_order("user-1", [{"product_id": "p-out", "quantity": 999}])
        assert "insufficient stock" in str(exc_info.value).lower()

    @pytest.mark.parametrize("quantity,expected_total", [
        (1, 50.0),
        (2, 100.0),
        (10, 500.0),
    ])
    async def test_order_total_calculation(self, quantity, expected_total, db_session):
        service = OrderService(db_session)
        order = await service.create_order("user-1", [{"product_id": "p-1", "quantity": quantity}])
        assert order.total == expected_total

# ✅ Integration test — gerçek HTTP
class TestOrderAPI:
    async def test_create_order_endpoint(self, client, auth_headers):
        response = await client.post(
            "/api/v1/orders",
            json={"items": [{"product_id": "p-1", "quantity": 1}]},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "pending"
        assert "id" in data
```

## Go — Table-Driven Tests

```go
func TestOrderService_CreateOrder(t *testing.T) {
    tests := []struct {
        name      string
        userID    string
        items     []OrderItem
        wantErr   bool
        errType   error
        wantTotal float64
    }{
        {
            name:      "valid order",
            userID:    "user-1",
            items:     []OrderItem{{ProductID: "p-1", Quantity: 2, Price: 50}},
            wantTotal: 100,
        },
        {
            name:    "empty items",
            userID:  "user-1",
            items:   []OrderItem{},
            wantErr: true,
            errType: ErrEmptyItems,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            repo := &mockOrderRepo{}
            svc := NewOrderService(repo)

            order, err := svc.CreateOrder(context.Background(), tt.userID, tt.items)

            if tt.wantErr {
                require.Error(t, err)
                assert.ErrorIs(t, err, tt.errType)
                return
            }
            require.NoError(t, err)
            assert.Equal(t, tt.wantTotal, order.Total)
        })
    }
}
```

## Coverage Hedefleri

```yaml
# vitest.config.ts
coverage:
  thresholds:
    lines: 80
    functions: 80
    branches: 75
    statements: 80

# pytest — pyproject.toml
[tool.coverage.report]
fail_under = 80
exclude_lines = ["pragma: no cover", "if TYPE_CHECKING:"]

# go test
go test ./... -coverprofile=coverage.out
go tool cover -func=coverage.out | grep total  # hedef: 80%+
```

## Kurallar

- Test isimleri: `should [beklenen davranış] when [koşul]`
- Her test bağımsız olmalı — test sırası önemli olmamalı
- Mock'ları sadece dış bağımlılıklar için kullan (DB, HTTP, queue)
- `beforeEach` ile state'i sıfırla
- Snapshot test'leri UI bileşenleri için kullan, logic için değil
- Flaky test'leri hemen düzelt — CI'ı kirletir
- Integration test'lerde gerçek DB kullan (test container)
- Coverage'ı metrik olarak değil, kılavuz olarak kullan
