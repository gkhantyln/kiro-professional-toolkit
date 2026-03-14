---
name: create-nextjs-app
description: Scaffold a production-ready Next.js 14+ app with App Router, TypeScript, Tailwind, auth, and testing
---

# Create Next.js App

Scaffolds a complete Next.js 14+ application with App Router including:
- TypeScript + ESLint + Prettier
- Tailwind CSS with design tokens
- NextAuth.js authentication
- Prisma ORM + PostgreSQL
- React Query for server state
- Zustand for client state
- Jest + Playwright testing
- Docker + CI/CD ready

## Usage
```
#create-nextjs-app <AppName>
```

## Project Structure
```
src/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (dashboard)/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── api/
│   │   └── auth/[...nextauth]/route.ts
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/          # shadcn/ui components
│   └── features/    # feature-specific components
├── lib/
│   ├── auth.ts
│   ├── db.ts
│   └── utils.ts
├── hooks/
├── stores/
└── types/
```

## Core Files

### app/layout.tsx
```typescript
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Providers } from '@/components/providers';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: { default: 'App', template: '%s | App' },
  description: 'Production-ready Next.js application',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### lib/auth.ts
```typescript
import NextAuth from 'next-auth';
import { PrismaAdapter } from '@auth/prisma-adapter';
import GitHub from 'next-auth/providers/github';
import Google from 'next-auth/providers/google';
import Credentials from 'next-auth/providers/credentials';
import { db } from '@/lib/db';
import bcrypt from 'bcryptjs';

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(db),
  session: { strategy: 'jwt' },
  providers: [
    GitHub,
    Google,
    Credentials({
      async authorize(credentials) {
        const { email, password } = credentials as { email: string; password: string };
        const user = await db.user.findUnique({ where: { email } });
        if (!user?.password) return null;
        const valid = await bcrypt.compare(password, user.password);
        return valid ? user : null;
      },
    }),
  ],
  callbacks: {
    jwt({ token, user }) {
      if (user) token.id = user.id;
      return token;
    },
    session({ session, token }) {
      if (token.id) session.user.id = token.id as string;
      return session;
    },
  },
  pages: { signIn: '/login' },
});
```

### lib/db.ts
```typescript
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const db = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
});

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db;
```

### middleware.ts
```typescript
import { auth } from '@/lib/auth';
import { NextResponse } from 'next/server';

const PUBLIC_ROUTES = ['/', '/login', '/register'];

export default auth((req) => {
  const isPublic = PUBLIC_ROUTES.includes(req.nextUrl.pathname);
  if (!req.auth && !isPublic) {
    return NextResponse.redirect(new URL('/login', req.url));
  }
});

export const config = { matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'] };
```

### next.config.ts
```typescript
import type { NextConfig } from 'next';

const config: NextConfig = {
  experimental: { typedRoutes: true },
  images: { remotePatterns: [{ protocol: 'https', hostname: '**' }] },
  logging: { fetches: { fullUrl: true } },
};

export default config;
```
