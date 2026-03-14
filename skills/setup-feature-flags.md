---
name: setup-feature-flags
description: Feature flag system with OpenFeature SDK, LaunchDarkly/Unleash integration, gradual rollouts, and A/B testing
---

# Setup Feature Flags

Production-ready feature flag sistemi kurar:
- OpenFeature SDK (vendor-agnostic)
- LaunchDarkly veya Unleash entegrasyonu
- Gradual rollout (percentage-based)
- User targeting & segmentation
- A/B testing framework
- Flag evaluation analytics

## Usage
```
#setup-feature-flags <launchdarkly|unleash|self-hosted>
```

## lib/feature-flags/client.ts
```typescript
import { OpenFeature, Client } from '@openfeature/server-sdk';
import { LaunchDarklyProvider } from '@openfeature/launchdarkly-provider';

let featureClient: Client;

export async function initFeatureFlags(): Promise<void> {
  const provider = new LaunchDarklyProvider(process.env.LAUNCHDARKLY_SDK_KEY!);
  await OpenFeature.setProviderAndWait(provider);
  featureClient = OpenFeature.getClient('app');
}

export function getFeatureClient(): Client {
  if (!featureClient) throw new Error('Feature flags not initialized');
  return featureClient;
}
```

## lib/feature-flags/flags.ts
```typescript
// Centralized flag definitions — single source of truth
export const FLAGS = {
  NEW_DASHBOARD: 'new-dashboard',
  AI_SUGGESTIONS: 'ai-suggestions',
  BETA_CHECKOUT: 'beta-checkout',
  DARK_MODE: 'dark-mode',
  RATE_LIMIT_V2: 'rate-limit-v2',
} as const;

export type FlagKey = typeof FLAGS[keyof typeof FLAGS];
```

## lib/feature-flags/evaluate.ts
```typescript
import { getFeatureClient } from './client';
import { type FlagKey } from './flags';
import { logger } from '../logger';

export type EvaluationContext = {
  userId?: string;
  email?: string;
  plan?: string;
  country?: string;
  [key: string]: string | boolean | number | undefined;
};

export async function isEnabled(flag: FlagKey, ctx: EvaluationContext = {}): Promise<boolean> {
  try {
    const client = getFeatureClient();
    return await client.getBooleanValue(flag, false, ctx);
  } catch (err) {
    logger.error({ err, flag }, 'Feature flag evaluation failed, using default');
    return false;
  }
}

export async function getVariant<T>(
  flag: FlagKey,
  defaultValue: T,
  ctx: EvaluationContext = {},
): Promise<T> {
  try {
    const client = getFeatureClient();
    if (typeof defaultValue === 'string') {
      return await client.getStringValue(flag, defaultValue as string, ctx) as T;
    }
    if (typeof defaultValue === 'number') {
      return await client.getNumberValue(flag, defaultValue as number, ctx) as T;
    }
    return await client.getObjectValue(flag, defaultValue as object, ctx) as T;
  } catch (err) {
    logger.error({ err, flag }, 'Feature flag variant evaluation failed');
    return defaultValue;
  }
}
```

## middleware/feature-gate.ts (Next.js)
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { isEnabled } from '@/lib/feature-flags/evaluate';
import { FLAGS } from '@/lib/feature-flags/flags';

export async function featureGateMiddleware(req: NextRequest) {
  const userId = req.cookies.get('userId')?.value;
  const ctx = { userId };

  if (req.nextUrl.pathname.startsWith('/dashboard')) {
    const newDashboard = await isEnabled(FLAGS.NEW_DASHBOARD, ctx);
    if (newDashboard) {
      return NextResponse.rewrite(new URL('/dashboard-v2', req.url));
    }
  }

  return NextResponse.next();
}
```

## hooks/useFeatureFlag.ts (React)
```typescript
import { useEffect, useState } from 'react';
import { OpenFeature } from '@openfeature/web-sdk';
import type { FlagKey } from '@/lib/feature-flags/flags';

export function useFeatureFlag(flag: FlagKey, defaultValue = false): boolean {
  const [enabled, setEnabled] = useState(defaultValue);

  useEffect(() => {
    const client = OpenFeature.getClient();
    client.getBooleanValue(flag, defaultValue).then(setEnabled);

    const handler = () => client.getBooleanValue(flag, defaultValue).then(setEnabled);
    client.addHandler('PROVIDER_CONFIGURATION_CHANGED', handler);
    return () => client.removeHandler('PROVIDER_CONFIGURATION_CHANGED', handler);
  }, [flag, defaultValue]);

  return enabled;
}

// Usage: const showNewUI = useFeatureFlag(FLAGS.NEW_DASHBOARD);
```
