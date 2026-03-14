---
name: create-openapi-spec
description: Generate production-grade OpenAPI 3.1 spec with Zod schemas, type generation, mock server, and contract testing
---

# Create OpenAPI Spec

Production-ready OpenAPI 3.1 spec oluşturur:
- Zod → OpenAPI schema generation
- TypeScript client auto-generation
- Mock server (Prism)
- Contract testing (Dredd)
- Redoc/Swagger UI hosting

## Usage
```
#create-openapi-spec <api-name>
```

## openapi/schema.ts (Zod → OpenAPI)
```typescript
import { z } from 'zod';
import { extendZodWithOpenApi } from '@asteasolutions/zod-to-openapi';

extendZodWithOpenApi(z);

export const UserSchema = z.object({
  id: z.string().uuid().openapi({ example: '550e8400-e29b-41d4-a716-446655440000' }),
  email: z.string().email().openapi({ example: 'user@example.com' }),
  name: z.string().min(1).max(100).openapi({ example: 'John Doe' }),
  role: z.enum(['admin', 'user', 'viewer']).openapi({ example: 'user' }),
  createdAt: z.string().datetime().openapi({ example: '2024-01-01T00:00:00Z' }),
}).openapi('User');

export const CreateUserSchema = UserSchema.omit({ id: true, createdAt: true });

export const PaginatedUsersSchema = z.object({
  data: z.array(UserSchema),
  meta: z.object({
    total: z.number().int().openapi({ example: 100 }),
    page: z.number().int().openapi({ example: 1 }),
    perPage: z.number().int().openapi({ example: 20 }),
    totalPages: z.number().int().openapi({ example: 5 }),
  }),
}).openapi('PaginatedUsers');

export const ErrorSchema = z.object({
  code: z.string().openapi({ example: 'VALIDATION_ERROR' }),
  message: z.string().openapi({ example: 'Invalid input' }),
  details: z.array(z.object({
    field: z.string(),
    message: z.string(),
  })).optional(),
}).openapi('Error');
```

## openapi/registry.ts
```typescript
import { OpenAPIRegistry, OpenApiGeneratorV31 } from '@asteasolutions/zod-to-openapi';
import { UserSchema, CreateUserSchema, PaginatedUsersSchema, ErrorSchema } from './schema';

const registry = new OpenAPIRegistry();

const bearerAuth = registry.registerComponent('securitySchemes', 'bearerAuth', {
  type: 'http',
  scheme: 'bearer',
  bearerFormat: 'JWT',
});

registry.registerPath({
  method: 'get',
  path: '/api/v1/users',
  summary: 'List users',
  tags: ['Users'],
  security: [{ [bearerAuth.name]: [] }],
  request: {
    query: z.object({
      page: z.coerce.number().int().min(1).default(1).optional(),
      perPage: z.coerce.number().int().min(1).max(100).default(20).optional(),
      search: z.string().optional(),
    }),
  },
  responses: {
    200: { description: 'Users list', content: { 'application/json': { schema: PaginatedUsersSchema } } },
    401: { description: 'Unauthorized', content: { 'application/json': { schema: ErrorSchema } } },
  },
});

registry.registerPath({
  method: 'post',
  path: '/api/v1/users',
  summary: 'Create user',
  tags: ['Users'],
  security: [{ [bearerAuth.name]: [] }],
  request: { body: { content: { 'application/json': { schema: CreateUserSchema } } } },
  responses: {
    201: { description: 'User created', content: { 'application/json': { schema: UserSchema } } },
    409: { description: 'Email already exists', content: { 'application/json': { schema: ErrorSchema } } },
  },
});

export function generateOpenAPIDocument() {
  const generator = new OpenApiGeneratorV31(registry.definitions);
  return generator.generateDocument({
    openapi: '3.1.0',
    info: { title: 'My API', version: '1.0.0', description: 'Production API documentation' },
    servers: [
      { url: 'https://api.example.com', description: 'Production' },
      { url: 'https://staging-api.example.com', description: 'Staging' },
      { url: 'http://localhost:3000', description: 'Local' },
    ],
  });
}
```

## scripts/generate-spec.ts
```typescript
import { writeFileSync } from 'fs';
import yaml from 'js-yaml';
import { generateOpenAPIDocument } from '../openapi/registry';

const doc = generateOpenAPIDocument();

// Generate YAML spec
writeFileSync('openapi.yaml', yaml.dump(doc, { indent: 2 }));

// Generate JSON spec
writeFileSync('openapi.json', JSON.stringify(doc, null, 2));

console.log('OpenAPI spec generated: openapi.yaml, openapi.json');
```

## package.json scripts
```json
{
  "scripts": {
    "spec:generate": "tsx scripts/generate-spec.ts",
    "spec:mock": "npx @stoplight/prism-cli mock openapi.yaml --port 4010",
    "spec:validate": "npx @redocly/cli lint openapi.yaml",
    "spec:docs": "npx @redocly/cli preview-docs openapi.yaml",
    "client:generate": "npx openapi-typescript openapi.yaml -o src/types/api.d.ts"
  }
}
```
