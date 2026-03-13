---
inclusion: auto
---

# Enterprise Coding Standards

## Code Quality Principles

### SOLID Principles
- **S**ingle Responsibility: Her class/function tek bir sorumluluğa sahip olmalı
- **O**pen/Closed: Extension'a açık, modification'a kapalı
- **L**iskov Substitution: Alt sınıflar üst sınıfların yerine kullanılabilmeli
- **I**nterface Segregation: Büyük interface'ler yerine küçük, spesifik interface'ler
- **D**ependency Inversion: Somut sınıflara değil, abstraction'lara bağımlı ol

### Clean Code Rules
- Fonksiyon isimleri açıklayıcı ve verb olmalı: `getUserById()`, `calculateTotal()`
- Değişken isimleri anlamlı ve noun olmalı: `userData`, `totalPrice`
- Magic number kullanma, constant tanımla
- Nested if'lerden kaçın, early return kullan
- Fonksiyon maksimum 20-30 satır olmalı
- Class maksimum 200-300 satır olmalı
- Parametre sayısı 3'ü geçmemeli, gerekirse object kullan

### Code Organization
```
src/
├── components/     # UI components
├── services/       # Business logic
├── utils/          # Helper functions
├── types/          # Type definitions
├── constants/      # Constants and enums
├── hooks/          # Custom hooks (React)
└── tests/          # Test files
```

## Documentation Standards

### Function Documentation
```typescript
/**
 * Retrieves user data from the database by ID
 * 
 * @param userId - The unique identifier of the user
 * @param includeDeleted - Whether to include soft-deleted users
 * @returns Promise resolving to user object or null if not found
 * @throws {DatabaseError} If database connection fails
 * @throws {ValidationError} If userId is invalid
 * 
 * @example
 * const user = await getUserById('123', false);
 */
```

### File Headers
```typescript
/**
 * @fileoverview User authentication service
 * @module services/auth
 * @requires jsonwebtoken
 * @requires bcrypt
 */
```

## Error Handling

### Always Use Proper Error Types
```typescript
// ❌ Bad
throw new Error('Something went wrong');

// ✅ Good
throw new ValidationError('Email format is invalid', { field: 'email' });
```

### Error Handling Pattern
```typescript
try {
  const result = await riskyOperation();
  return { success: true, data: result };
} catch (error) {
  logger.error('Operation failed', { error, context });
  throw new OperationError('Failed to complete operation', { cause: error });
}
```

## Security Standards

### Input Validation
- Her external input validate edilmeli (API, form, query params)
- Zod, Joi, Yup gibi validation library kullan
- SQL injection, XSS, CSRF koruması şart

### Authentication & Authorization
- JWT token'lar için short expiry (15-30 min)
- Refresh token kullan
- Rate limiting implement et
- Sensitive data'yı log'lama

### Secrets Management
- Environment variables kullan
- `.env` dosyası `.gitignore`'da olmalı
- Production'da secret manager kullan (AWS Secrets Manager, Vault)

## Performance Standards

### Database Queries
- N+1 query probleminden kaçın
- Index'leri doğru kullan
- Pagination implement et
- Connection pooling kullan

### Caching Strategy
- Redis/Memcached kullan
- Cache invalidation stratejisi belirle
- TTL değerlerini optimize et

### API Response Times
- GET endpoints: < 200ms
- POST/PUT endpoints: < 500ms
- Complex operations: < 2s
- Timeout değerleri belirle

## Testing Standards

### Test Coverage
- Minimum %80 code coverage
- Unit tests: Her fonksiyon için
- Integration tests: API endpoints için
- E2E tests: Critical user flows için

### Test Naming Convention
```typescript
describe('UserService', () => {
  describe('getUserById', () => {
    it('should return user when valid ID is provided', async () => {
      // Arrange, Act, Assert
    });
    
    it('should throw ValidationError when ID is invalid', async () => {
      // Test
    });
    
    it('should return null when user not found', async () => {
      // Test
    });
  });
});
```

## Git Standards

### Commit Message Format
```
type(scope): subject

body

footer
```

**Types**: feat, fix, docs, style, refactor, test, chore, perf

**Example**:
```
feat(auth): add JWT refresh token mechanism

- Implement refresh token generation
- Add token rotation on refresh
- Update authentication middleware

Closes #123
```

### Branch Naming
- `feature/user-authentication`
- `bugfix/login-validation`
- `hotfix/security-patch`
- `refactor/database-layer`

## Code Review Checklist

- [ ] Code follows SOLID principles
- [ ] All functions have proper documentation
- [ ] Error handling is comprehensive
- [ ] Security best practices applied
- [ ] Tests are written and passing
- [ ] No console.log or debug code
- [ ] Performance considerations addressed
- [ ] Accessibility requirements met
- [ ] No hardcoded values or secrets
- [ ] Code is DRY (Don't Repeat Yourself)
