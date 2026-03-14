---
inclusion: fileMatch
fileMatchPattern: "**/*.{tsx,jsx}"
---

# React Best Practices — İleri Seviye

## Hooks Kuralları

```tsx
// ❌ Koşullu hook çağrısı — yasak
if (isLoggedIn) {
  const [data] = useState(null); // HATA
}

// ✅ Hook'u her zaman en üstte çağır
const [data, setData] = useState<User | null>(null);
if (!isLoggedIn) return null;
```

## useMemo / useCallback — Doğru Kullanım

```tsx
// ❌ Her render'da yeni referans — gereksiz re-render
const handleClick = () => setCount(c => c + 1);

// ✅ useCallback — referans stabilitesi
const handleClick = useCallback(() => setCount(c => c + 1), []);

// ✅ useMemo — pahalı hesaplama
const sortedItems = useMemo(
  () => items.slice().sort((a, b) => a.price - b.price),
  [items]
);

// ✅ React.memo — prop değişmezse re-render yok
const ProductCard = React.memo(({ product, onAdd }: Props) => {
  return <div onClick={() => onAdd(product.id)}>{product.name}</div>;
});
```

## Custom Hooks — Mantığı Ayır

```tsx
// hooks/useAsync.ts
function useAsync<T>(asyncFn: () => Promise<T>, deps: DependencyList) {
  const [state, setState] = useState<{
    data: T | null;
    loading: boolean;
    error: Error | null;
  }>({ data: null, loading: true, error: null });

  useEffect(() => {
    let cancelled = false;
    setState(s => ({ ...s, loading: true, error: null }));

    asyncFn()
      .then(data => { if (!cancelled) setState({ data, loading: false, error: null }); })
      .catch(error => { if (!cancelled) setState({ data: null, loading: false, error }); });

    return () => { cancelled = true; };
  }, deps);

  return state;
}

// hooks/useDebounce.ts
function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debounced;
}
```

## Suspense + Error Boundary

```tsx
// ErrorBoundary.tsx
class ErrorBoundary extends React.Component<
  { fallback: ReactNode; children: ReactNode },
  { hasError: boolean; error: Error | null }
> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) return this.props.fallback;
    return this.props.children;
  }
}

// App.tsx
<ErrorBoundary fallback={<ErrorPage />}>
  <Suspense fallback={<Skeleton />}>
    <LazyDashboard />
  </Suspense>
</ErrorBoundary>
```

## React Server Components (Next.js App Router)

```tsx
// app/products/page.tsx — Server Component (default)
// ✅ Doğrudan DB/API çağrısı — client'a bundle edilmez
async function ProductsPage() {
  const products = await db.product.findMany({ take: 20 });
  return (
    <div>
      {products.map(p => <ProductCard key={p.id} product={p} />)}
    </div>
  );
}

// components/AddToCart.tsx — Client Component
"use client";
function AddToCart({ productId }: { productId: string }) {
  const [loading, setLoading] = useState(false);
  // interaktif mantık burada
}
```

## State Management — Zustand

```tsx
// store/cart.ts
import { create } from "zustand";
import { immer } from "zustand/middleware/immer";
import { persist } from "zustand/middleware";

interface CartStore {
  items: CartItem[];
  addItem: (product: Product) => void;
  removeItem: (id: string) => void;
  total: () => number;
}

export const useCartStore = create<CartStore>()(
  persist(
    immer((set, get) => ({
      items: [],
      addItem: (product) => set(state => {
        const existing = state.items.find(i => i.id === product.id);
        if (existing) existing.quantity += 1;
        else state.items.push({ ...product, quantity: 1 });
      }),
      removeItem: (id) => set(state => {
        state.items = state.items.filter(i => i.id !== id);
      }),
      total: () => get().items.reduce((sum, i) => sum + i.price * i.quantity, 0),
    })),
    { name: "cart-storage" }
  )
);
```

## Form — React Hook Form + Zod

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
  email: z.string().email("Geçerli email girin"),
  password: z.string().min(8, "En az 8 karakter"),
});

type FormData = z.infer<typeof schema>;

function LoginForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    await login(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email")} aria-invalid={!!errors.email} />
      {errors.email && <span role="alert">{errors.email.message}</span>}
      <button type="submit" disabled={isSubmitting}>Giriş</button>
    </form>
  );
}
```

## Kurallar

- `"use client"` direktifini sadece gerektiğinde ekle — RSC'yi tercih et
- `useEffect` dependency array'ini eksiksiz doldur
- `key` prop olarak index kullanma — stabil ID kullan
- Component'leri küçük tut, tek sorumluluk prensibi
- `React.memo` + `useCallback` kombinasyonunu liste render'larında kullan
- Global state için Zustand, server state için TanStack Query
- Form validasyonu için Zod + React Hook Form
- Lazy loading: `React.lazy` + `Suspense` ile code splitting
