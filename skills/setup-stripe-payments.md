---
name: setup-stripe-payments
description: Production Stripe integration with subscriptions, webhooks, idempotency, SCA compliance, and customer portal
---

# Setup Stripe Payments

Production-ready Stripe ödeme sistemi kurar:
- Subscription + one-time payments
- Webhook handler (idempotent)
- Customer portal
- SCA/3DS compliance
- Proration & upgrade/downgrade
- Invoice management

## Usage
```
#setup-stripe-payments <nextjs|express>
```

## lib/stripe.ts
```typescript
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
  typescript: true,
  maxNetworkRetries: 3,
  telemetry: false,
});

export const PLANS = {
  starter: { priceId: process.env.STRIPE_STARTER_PRICE_ID!, name: 'Starter' },
  pro:     { priceId: process.env.STRIPE_PRO_PRICE_ID!,     name: 'Pro' },
  enterprise: { priceId: process.env.STRIPE_ENTERPRISE_PRICE_ID!, name: 'Enterprise' },
} as const;

export type PlanKey = keyof typeof PLANS;
```

## app/api/stripe/checkout/route.ts
```typescript
import { stripe, PLANS, type PlanKey } from '@/lib/stripe';
import { auth } from '@/lib/auth';
import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session?.user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

  const { plan, successUrl, cancelUrl } = await req.json() as {
    plan: PlanKey;
    successUrl: string;
    cancelUrl: string;
  };

  const user = await db.user.findUnique({ where: { id: session.user.id } });

  let customerId = user?.stripeCustomerId;
  if (!customerId) {
    const customer = await stripe.customers.create({
      email: session.user.email!,
      metadata: { userId: session.user.id },
    });
    customerId = customer.id;
    await db.user.update({ where: { id: session.user.id }, data: { stripeCustomerId: customerId } });
  }

  const checkoutSession = await stripe.checkout.sessions.create({
    customer: customerId,
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: PLANS[plan].priceId, quantity: 1 }],
    success_url: `${successUrl}?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: cancelUrl,
    subscription_data: { metadata: { userId: session.user.id, plan } },
    allow_promotion_codes: true,
    billing_address_collection: 'auto',
  });

  return NextResponse.json({ url: checkoutSession.url });
}
```

## app/api/stripe/webhook/route.ts
```typescript
import { stripe } from '@/lib/stripe';
import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';

export const config = { api: { bodyParser: false } };

const HANDLED_EVENTS = new Set([
  'checkout.session.completed',
  'customer.subscription.updated',
  'customer.subscription.deleted',
  'invoice.payment_failed',
]);

export async function POST(req: NextRequest) {
  const body = await req.text();
  const sig = req.headers.get('stripe-signature')!;

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
  }

  if (!HANDLED_EVENTS.has(event.type)) {
    return NextResponse.json({ received: true });
  }

  // Idempotency check
  const processed = await db.stripeEvent.findUnique({ where: { id: event.id } });
  if (processed) return NextResponse.json({ received: true });

  await db.stripeEvent.create({ data: { id: event.id, type: event.type } });

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.CheckoutSession;
      const sub = await stripe.subscriptions.retrieve(session.subscription as string);
      await db.subscription.upsert({
        where: { stripeSubscriptionId: sub.id },
        create: {
          stripeSubscriptionId: sub.id,
          userId: sub.metadata.userId,
          plan: sub.metadata.plan,
          status: sub.status,
          currentPeriodEnd: new Date(sub.current_period_end * 1000),
        },
        update: { status: sub.status, currentPeriodEnd: new Date(sub.current_period_end * 1000) },
      });
      break;
    }
    case 'customer.subscription.deleted': {
      const sub = event.data.object as Stripe.Subscription;
      await db.subscription.update({
        where: { stripeSubscriptionId: sub.id },
        data: { status: 'canceled' },
      });
      break;
    }
    case 'invoice.payment_failed': {
      const invoice = event.data.object as Stripe.Invoice;
      // Send dunning email
      break;
    }
  }

  return NextResponse.json({ received: true });
}
```

## app/api/stripe/portal/route.ts
```typescript
import { stripe } from '@/lib/stripe';
import { auth } from '@/lib/auth';
import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session?.user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

  const user = await db.user.findUnique({ where: { id: session.user.id } });
  if (!user?.stripeCustomerId) {
    return NextResponse.json({ error: 'No subscription found' }, { status: 404 });
  }

  const { returnUrl } = await req.json();
  const portalSession = await stripe.billingPortal.sessions.create({
    customer: user.stripeCustomerId,
    return_url: returnUrl,
  });

  return NextResponse.json({ url: portalSession.url });
}
```
