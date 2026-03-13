---
inclusion: fileMatch
fileMatchPattern: "**/*.{server,app,middleware,config}.*"
---

# Security Headers Configuration

## Required Security Headers

### 1. Content Security Policy (CSP)
```javascript
// Express.js with Helmet
const helmet = require('helmet');

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'unsafe-inline'", "https://trusted-cdn.com"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", "data:", "https:"],
    connectSrc: ["'self'", "https://api.example.com"],
    fontSrc: ["'self'", "https://fonts.gstatic.com"],
    objectSrc: ["'none'"],
    mediaSrc: ["'self'"],
    frameSrc: ["'none'"],
    upgradeInsecureRequests: [],
  },
}));
```

### 2. HTTP Strict Transport Security (HSTS)
```javascript
app.use(helmet.hsts({
  maxAge: 31536000, // 1 year
  includeSubDomains: true,
  preload: true
}));
```

### 3. X-Frame-Options
```javascript
// Prevent clickjacking
app.use(helmet.frameguard({ action: 'deny' }));

// Or allow same origin
app.use(helmet.frameguard({ action: 'sameorigin' }));
```

### 4. X-Content-Type-Options
```javascript
// Prevent MIME sniffing
app.use(helmet.noSniff());
```

### 5. X-XSS-Protection
```javascript
// Enable XSS filter
app.use(helmet.xssFilter());
```

### 6. Referrer-Policy
```javascript
app.use(helmet.referrerPolicy({ policy: 'strict-origin-when-cross-origin' }));
```

### 7. Permissions-Policy
```javascript
app.use((req, res, next) => {
  res.setHeader('Permissions-Policy', 
    'geolocation=(), microphone=(), camera=()'
  );
  next();
});
```

## Complete Security Setup

### Node.js/Express
```javascript
const express = require('express');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const mongoSanitize = require('express-mongo-sanitize');
const xss = require('xss-clean');
const hpp = require('hpp');
const cors = require('cors');

const app = express();

// Security headers
app.use(helmet());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP'
});
app.use('/api/', limiter);

// Body parser
app.use(express.json({ limit: '10kb' }));

// Data sanitization against NoSQL injection
app.use(mongoSanitize());

// Data sanitization against XSS
app.use(xss());

// Prevent parameter pollution
app.use(hpp({
  whitelist: ['duration', 'price', 'difficulty']
}));

// CORS
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS.split(','),
  credentials: true
}));

// Disable X-Powered-By
app.disable('x-powered-by');
```

### Python/FastAPI
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

### Go/Gin
```go
package main

import (
    "github.com/gin-gonic/gin"
    "github.com/gin-contrib/cors"
    "github.com/ulule/limiter/v3"
    "github.com/ulule/limiter/v3/drivers/middleware/gin"
)

func SecurityHeaders() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Header("X-Content-Type-Options", "nosniff")
        c.Header("X-Frame-Options", "DENY")
        c.Header("X-XSS-Protection", "1; mode=block")
        c.Header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        c.Header("Content-Security-Policy", "default-src 'self'")
        c.Header("Referrer-Policy", "strict-origin-when-cross-origin")
        c.Next()
    }
}

func main() {
    r := gin.Default()
    
    // Security headers
    r.Use(SecurityHeaders())
    
    // CORS
    r.Use(cors.New(cors.Config{
        AllowOrigins:     []string{"https://example.com"},
        AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},
        AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
        AllowCredentials: true,
    }))
    
    // Rate limiting
    rate := limiter.Rate{
        Period: 1 * time.Minute,
        Limit:  100,
    }
    store := memory.NewStore()
    middleware := gin.NewMiddleware(limiter.New(store, rate))
    r.Use(middleware)
    
    r.Run(":8080")
}
```

## Security Testing

### Test Security Headers
```bash
# Using curl
curl -I https://example.com

# Using securityheaders.com
curl https://securityheaders.com/?q=https://example.com

# Using Mozilla Observatory
curl https://http-observatory.security.mozilla.org/api/v1/analyze?host=example.com
```

### Expected Headers
```
HTTP/2 200
strict-transport-security: max-age=31536000; includeSubDomains
x-content-type-options: nosniff
x-frame-options: DENY
x-xss-protection: 1; mode=block
content-security-policy: default-src 'self'
referrer-policy: strict-origin-when-cross-origin
permissions-policy: geolocation=(), microphone=(), camera=()
```

## Common Mistakes

### ❌ Bad
```javascript
// No security headers
app.get('/api/users', (req, res) => {
  res.json(users);
});

// Allowing all origins
app.use(cors({ origin: '*' }));

// No rate limiting
// Vulnerable to brute force
```

### ✅ Good
```javascript
// With security headers
app.use(helmet());

// Specific origins
app.use(cors({
  origin: ['https://example.com'],
  credentials: true
}));

// Rate limiting
app.use('/api/', limiter);
```
