---
inclusion: fileMatch
fileMatchPattern: "**/*.{api,route,controller,endpoint}.*"
---

# API Design Guidelines

## RESTful API Standards

### Resource Naming
- Use plural nouns: `/users`, `/products`, `/orders`
- Use kebab-case: `/user-profiles`, `/order-items`
- Avoid verbs in URLs: ❌ `/getUsers`, ✅ `/users`
- Use nested resources: `/users/:id/orders`

### HTTP Methods
```
GET     /users          # List all users
GET     /users/:id      # Get specific user
POST    /users          # Create new user
PUT     /users/:id      # Full update
PATCH   /users/:id      # Partial update
DELETE  /users/:id      # Delete user
```

### Status Codes
```
200 OK                  # Successful GET, PUT, PATCH
201 Created             # Successful POST
204 No Content          # Successful DELETE
400 Bad Request         # Invalid input
401 Unauthorized        # Missing/invalid authentication
403 Forbidden           # Authenticated but not authorized
404 Not Found           # Resource doesn't exist
409 Conflict            # Duplicate resource
422 Unprocessable       # Validation error
429 Too Many Requests   # Rate limit exceeded
500 Internal Error      # Server error
503 Service Unavailable # Temporary unavailable
```

## Request/Response Format

### Request Body (POST/PUT/PATCH)
```json
{
  "data": {
    "type": "users",
    "attributes": {
      "email": "user@example.com",
      "name": "John Doe"
    }
  }
}
```

### Success Response
```json
{
  "success": true,
  "data": {
    "id": "123",
    "type": "users",
    "attributes": {
      "email": "user@example.com",
      "name": "John Doe",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  },
  "meta": {
    "timestamp": "2024-01-01T00:00:00Z",
    "version": "1.0"
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Email format is invalid"
      }
    ]
  },
  "meta": {
    "timestamp": "2024-01-01T00:00:00Z",
    "requestId": "req_123abc"
  }
}
```

## Pagination

### Cursor-Based (Recommended)
```
GET /users?cursor=eyJpZCI6MTIzfQ&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTQzfQ",
    "prevCursor": "eyJpZCI6MTAzfQ",
    "hasNext": true,
    "hasPrev": true
  }
}
```

### Offset-Based
```
GET /users?page=2&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

## Filtering, Sorting, Searching

### Filtering
```
GET /users?status=active&role=admin
GET /products?price[gte]=100&price[lte]=500
GET /orders?createdAt[after]=2024-01-01
```

### Sorting
```
GET /users?sort=createdAt          # Ascending
GET /users?sort=-createdAt         # Descending
GET /users?sort=name,-createdAt    # Multiple fields
```

### Searching
```
GET /users?search=john
GET /products?q=laptop&fields=name,description
```

### Field Selection
```
GET /users?fields=id,name,email
GET /users/:id?include=orders,profile
```

## Versioning

### URL Versioning (Recommended)
```
/api/v1/users
/api/v2/users
```

### Header Versioning
```
Accept: application/vnd.api+json;version=1
```

## Authentication & Authorization

### JWT Bearer Token
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### API Key
```
X-API-Key: your-api-key-here
```

### OAuth 2.0 Flow
```
1. GET /oauth/authorize
2. POST /oauth/token
3. Use access_token in requests
4. Refresh with refresh_token
```

## Rate Limiting

### Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
Retry-After: 3600
```

### Rate Limit Response (429)
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retryAfter": 3600
  }
}
```

## Caching

### Cache Headers
```
Cache-Control: public, max-age=3600
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Last-Modified: Wed, 21 Oct 2024 07:28:00 GMT
```

### Conditional Requests
```
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"
If-Modified-Since: Wed, 21 Oct 2024 07:28:00 GMT
```

## CORS Configuration

```typescript
{
  origin: process.env.ALLOWED_ORIGINS.split(','),
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  exposedHeaders: ['X-RateLimit-Limit', 'X-RateLimit-Remaining'],
  credentials: true,
  maxAge: 86400
}
```

## Webhooks

### Webhook Payload
```json
{
  "event": "user.created",
  "timestamp": "2024-01-01T00:00:00Z",
  "data": {
    "id": "123",
    "email": "user@example.com"
  },
  "signature": "sha256=..."
}
```

### Webhook Security
- Use HMAC signature verification
- Implement retry mechanism (exponential backoff)
- Provide webhook logs and debugging
- Support webhook URL validation

## API Documentation

### OpenAPI/Swagger Required Fields
```yaml
openapi: 3.0.0
info:
  title: API Name
  version: 1.0.0
  description: API description
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
```

## Health Check Endpoint

```typescript
GET /health

Response:
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "queue": "healthy"
  },
  "uptime": 86400
}
```

## Idempotency

### Idempotency Key
```
POST /payments
Idempotency-Key: unique-key-123

# Same request with same key returns cached response
```

## Bulk Operations

```
POST /users/bulk
{
  "operations": [
    { "method": "create", "data": {...} },
    { "method": "update", "id": "123", "data": {...} },
    { "method": "delete", "id": "456" }
  ]
}

Response:
{
  "results": [
    { "status": "success", "id": "789" },
    { "status": "success", "id": "123" },
    { "status": "error", "error": "Not found" }
  ]
}
```

## Deprecation Strategy

### Deprecation Header
```
Deprecation: true
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
Link: <https://api.example.com/v2/users>; rel="successor-version"
```

### Deprecation Notice Period
- Announce 6 months before deprecation
- Provide migration guide
- Support old version for 12 months minimum
- Log usage of deprecated endpoints
