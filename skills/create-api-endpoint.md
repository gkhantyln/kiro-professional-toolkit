---
name: create-api-endpoint
description: Create a complete REST API endpoint with validation, error handling, and tests
---

# Create API Endpoint

Creates a production-ready REST API endpoint with:
- Request validation
- Error handling
- Database integration
- Unit tests
- API documentation

## Usage
```
#create-api-endpoint <resource> <method>
```

## Example
```
#create-api-endpoint users POST
```

## Generated Structure

### 1. Route Handler
```typescript
// routes/users.route.ts
import { Router } from 'express';
import { createUserSchema } from '../schemas/user.schema';
import { validate } from '../middleware/validate';
import { createUser } from '../controllers/user.controller';

const router = Router();

router.post('/users', validate(createUserSchema), createUser);

export default router;
```

### 2. Controller
```typescript
// controllers/user.controller.ts
import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/user.service';
import { AppError } from '../utils/errors';

export async function createUser(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const userData = req.body;
    const user = await UserService.create(userData);
    
    res.status(201).json({
      success: true,
      data: user,
    });
  } catch (error) {
    next(error);
  }
}
```

### 3. Service Layer
```typescript
// services/user.service.ts
import { db } from '../db';
import { AppError } from '../utils/errors';

export class UserService {
  static async create(data: CreateUserDto) {
    const existing = await db.user.findUnique({
      where: { email: data.email },
    });
    
    if (existing) {
      throw new AppError('User already exists', 'USER_EXISTS', 409);
    }
    
    const user = await db.user.create({
      data: {
        email: data.email,
        name: data.name,
      },
    });
    
    return user;
  }
}
```

### 4. Validation Schema
```typescript
// schemas/user.schema.ts
import { z } from 'zod';

export const createUserSchema = z.object({
  body: z.object({
    email: z.string().email('Invalid email format'),
    name: z.string().min(2, 'Name must be at least 2 characters'),
    password: z.string().min(8, 'Password must be at least 8 characters'),
  }),
});

export type CreateUserDto = z.infer<typeof createUserSchema.shape.body>;
```

### 5. Tests
```typescript
// tests/user.test.ts
import request from 'supertest';
import { app } from '../app';

describe('POST /users', () => {
  it('should create a new user', async () => {
    const response = await request(app)
      .post('/users')
      .send({
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123',
      });
    
    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data).toHaveProperty('id');
  });
  
  it('should return 400 for invalid email', async () => {
    const response = await request(app)
      .post('/users')
      .send({
        email: 'invalid-email',
        name: 'Test User',
        password: 'password123',
      });
    
    expect(response.status).toBe(400);
  });
});
```
