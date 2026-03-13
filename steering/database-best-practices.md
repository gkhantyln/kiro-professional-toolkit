---
inclusion: fileMatch
fileMatchPattern: "**/*.{sql,prisma,migration,model,entity,repository}.*"
---

# Database Best Practices

## Schema Design

### Naming Conventions
- Tables: plural, snake_case: `users`, `order_items`
- Columns: singular, snake_case: `user_id`, `created_at`
- Primary keys: `id` or `{table}_id`
- Foreign keys: `{referenced_table}_id`
- Indexes: `idx_{table}_{columns}`
- Constraints: `{type}_{table}_{columns}`

### Data Types
- Use appropriate types: INT for IDs, VARCHAR for strings, TIMESTAMP for dates
- Avoid TEXT for short strings, use VARCHAR with limit
- Use DECIMAL for money, never FLOAT
- Use BOOLEAN for true/false, not TINYINT
- Use ENUM sparingly, prefer lookup tables

### Normalization
- Apply 3NF (Third Normal Form) minimum
- Avoid data duplication
- Use junction tables for many-to-many
- Denormalize only for performance with justification

## Indexing Strategy

### When to Index
```sql
-- Primary keys (automatic)
-- Foreign keys (always)
-- Columns in WHERE clauses
-- Columns in JOIN conditions
-- Columns in ORDER BY
-- Columns in GROUP BY
```

### Index Types
- B-tree: Default, good for equality and range
- Hash: Only equality, faster than B-tree
- GiST/GIN: Full-text search, arrays
- Partial: Index subset of rows

### Composite Indexes
```sql
-- Order matters! Most selective column first
CREATE INDEX idx_users_email_status ON users(email, status);
-- Good for: WHERE email = ? AND status = ?
-- Good for: WHERE email = ?
-- Bad for: WHERE status = ?
```

## Query Optimization

### Avoid N+1 Queries
```typescript
// ❌ Bad - N+1 problem
const users = await User.findAll();
for (const user of users) {
  user.orders = await Order.findAll({ where: { userId: user.id } });
}

// ✅ Good - Single query with join
const users = await User.findAll({
  include: [{ model: Order }]
});
```

### Use Pagination
```sql
-- Offset-based (simple but slow for large offsets)
SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 100;

-- Cursor-based (faster, recommended)
SELECT * FROM users WHERE id > 100 ORDER BY id LIMIT 20;
```

### Avoid SELECT *
```sql
-- ❌ Bad
SELECT * FROM users;

-- ✅ Good
SELECT id, email, name FROM users;
```

## Transactions

### ACID Properties
- Atomicity: All or nothing
- Consistency: Valid state always
- Isolation: Concurrent transactions don't interfere
- Durability: Committed data persists

### Transaction Usage
```typescript
await db.transaction(async (trx) => {
  const user = await trx('users').insert({ email });
  await trx('profiles').insert({ userId: user.id });
  // Both succeed or both rollback
});
```

## Migrations

### Migration Rules
- Never modify existing migrations in production
- Always reversible (up and down)
- Test migrations on staging first
- Backup before running migrations
- Use transactions for DDL when possible

### Migration Example
```sql
-- Up
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Down
DROP INDEX idx_users_email;
DROP TABLE users;
```

## Security

### SQL Injection Prevention
```typescript
// ❌ Bad - SQL injection vulnerable
db.query(`SELECT * FROM users WHERE email = '${email}'`);

// ✅ Good - Parameterized query
db.query('SELECT * FROM users WHERE email = ?', [email]);
```

### Access Control
- Use least privilege principle
- Separate read/write users
- Never use root in application
- Encrypt sensitive data at rest
