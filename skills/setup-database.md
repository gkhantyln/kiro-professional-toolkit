---
name: setup-database
description: Setup database with ORM, migrations, seeders, and connection pooling
---

# Setup Database

Creates complete database setup with:
- ORM configuration (Prisma/TypeORM/Sequelize)
- Connection pooling
- Migrations
- Seeders
- Backup strategy

## Usage
```
#setup-database <orm> <database>
```

## Example
```
#setup-database prisma postgresql
```

## Prisma Setup

### 1. Installation
```bash
npm install prisma @prisma/client
npx prisma init
```

### 2. Schema Definition
```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String
  password  String
  role      Role     @default(USER)
  isActive  Boolean  @default(true)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  posts     Post[]
  profile   Profile?
  
  @@index([email])
  @@map("users")
}

model Profile {
  id        Int     @id @default(autoincrement())
  bio       String?
  avatar    String?
  userId    Int     @unique
  user      User    @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  @@map("profiles")
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String
  published Boolean  @default(false)
  authorId  Int
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  @@index([authorId])
  @@index([published])
  @@map("posts")
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

### 3. Database Client
```javascript
// src/config/database.js
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient({
  log: process.env.NODE_ENV === 'development' 
    ? ['query', 'info', 'warn', 'error']
    : ['error'],
  errorFormat: 'pretty',
});

// Connection test
async function connectDB() {
  try {
    await prisma.$connect();
    console.log('Database connected successfully');
  } catch (error) {
    console.error('Database connection failed:', error);
    process.exit(1);
  }
}

// Graceful shutdown
async function disconnectDB() {
  await prisma.$disconnect();
}

process.on('beforeExit', disconnectDB);

module.exports = { prisma, connectDB, disconnectDB };
```

### 4. Migration Commands
```bash
# Create migration
npx prisma migrate dev --name add_user_table

# Run migrations
npx prisma migrate deploy

# Reset database
npx prisma migrate reset

# Generate Prisma Client
npx prisma generate
```

### 5. Seeder
```javascript
// prisma/seed.js
const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcrypt');

const prisma = new PrismaClient();

async function main() {
  // Create admin user
  const adminPassword = await bcrypt.hash('admin123', 12);
  const admin = await prisma.user.upsert({
    where: { email: 'admin@example.com' },
    update: {},
    create: {
      email: 'admin@example.com',
      name: 'Admin User',
      password: adminPassword,
      role: 'ADMIN',
      profile: {
        create: {
          bio: 'System administrator',
        },
      },
    },
  });

  console.log('Seeded admin user:', admin);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

Run seeder:
```bash
npx prisma db seed
```

Add to package.json:
```json
{
  "prisma": {
    "seed": "node prisma/seed.js"
  }
}
```
