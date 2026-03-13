---
inclusion: fileMatch
fileMatchPattern: "**/*.{ts,tsx}"
---

# TypeScript Guidelines

## Type Safety

### Strict Mode
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

### Avoid `any`
```typescript
// ❌ Bad
function process(data: any) {
  return data.value;
}

// ✅ Good
interface Data {
  value: string;
}
function process(data: Data) {
  return data.value;
}

// ✅ Good - when type is truly unknown
function process(data: unknown) {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    return (data as Data).value;
  }
}
```

## Type Definitions

### Interface vs Type
```typescript
// Use interface for objects (can be extended)
interface User {
  id: string;
  name: string;
}

interface Admin extends User {
  permissions: string[];
}

// Use type for unions, intersections, primitives
type Status = 'active' | 'inactive' | 'pending';
type ID = string | number;
type UserWithTimestamp = User & { createdAt: Date };
```

### Generics
```typescript
// Generic function
function getFirst<T>(arr: T[]): T | undefined {
  return arr[0];
}

// Generic interface
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

// Generic constraints
function merge<T extends object, U extends object>(obj1: T, obj2: U) {
  return { ...obj1, ...obj2 };
}
```

### Utility Types
```typescript
// Partial - all properties optional
type PartialUser = Partial<User>;

// Required - all properties required
type RequiredUser = Required<User>;

// Pick - select specific properties
type UserPreview = Pick<User, 'id' | 'name'>;

// Omit - exclude specific properties
type UserWithoutPassword = Omit<User, 'password'>;

// Record - object with specific key-value types
type UserRoles = Record<string, 'admin' | 'user'>;

// ReturnType - extract return type
type FunctionReturn = ReturnType<typeof myFunction>;
```

## Best Practices

### Discriminated Unions
```typescript
type Success = { status: 'success'; data: string };
type Error = { status: 'error'; error: string };
type Loading = { status: 'loading' };

type Result = Success | Error | Loading;

function handleResult(result: Result) {
  switch (result.status) {
    case 'success':
      return result.data; // TypeScript knows data exists
    case 'error':
      return result.error; // TypeScript knows error exists
    case 'loading':
      return 'Loading...';
  }
}
```

### Type Guards
```typescript
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj
  );
}

// Usage
if (isUser(data)) {
  console.log(data.name); // TypeScript knows it's User
}
```

### Const Assertions
```typescript
// Without const assertion
const colors = ['red', 'blue']; // string[]

// With const assertion
const colors = ['red', 'blue'] as const; // readonly ['red', 'blue']

// Object const assertion
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
} as const;
```

### Enum Alternatives
```typescript
// ❌ Avoid enums (they generate runtime code)
enum Status {
  Active,
  Inactive,
}

// ✅ Use const objects with as const
const Status = {
  Active: 'active',
  Inactive: 'inactive',
} as const;

type Status = typeof Status[keyof typeof Status];
```

## Error Handling

### Type-Safe Errors
```typescript
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// Usage
throw new AppError('User not found', 'USER_NOT_FOUND', 404);
```
