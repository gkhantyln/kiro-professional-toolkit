---
inclusion: fileMatch
fileMatchPattern: "**/*.{tsx,jsx,vue,svelte}"
---

# Frontend Development Standards

## Component Structure

### File Organization
```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.test.tsx
│   ├── Button.stories.tsx
│   ├── Button.module.css
│   └── index.ts
```

### Component Template (React)
```typescript
import React from 'react';
import styles from './Button.module.css';

interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  children,
}) => {
  return (
    <button
      className={`${styles.button} ${styles[variant]} ${styles[size]}`}
      disabled={disabled}
      onClick={onClick}
      aria-disabled={disabled}
    >
      {children}
    </button>
  );
};
```

## State Management

### Local State (useState)
- Use for component-specific state
- Form inputs, toggles, UI state

### Global State (Context/Redux/Zustand)
- User authentication
- Theme preferences
- Shopping cart
- Shared data across components

### Server State (React Query/SWR)
- API data fetching
- Caching and synchronization
- Background updates

## Performance Optimization

### Code Splitting
```typescript
// Lazy load routes
const Dashboard = lazy(() => import('./pages/Dashboard'));

// Lazy load heavy components
const Chart = lazy(() => import('./components/Chart'));
```

### Memoization
```typescript
// useMemo for expensive calculations
const sortedData = useMemo(() => {
  return data.sort((a, b) => a.value - b.value);
}, [data]);

// useCallback for function references
const handleClick = useCallback(() => {
  console.log('clicked');
}, []);

// React.memo for component memoization
export const ExpensiveComponent = React.memo(({ data }) => {
  return <div>{data}</div>;
});
```

### Image Optimization
- Use WebP format with fallback
- Lazy load images below fold
- Use responsive images (srcset)
- Compress images before upload
- Use CDN for static assets

## Accessibility (a11y)

### Semantic HTML
```tsx
// ✅ Good
<button onClick={handleClick}>Click me</button>
<nav><ul><li><a href="/">Home</a></li></ul></nav>

// ❌ Bad
<div onClick={handleClick}>Click me</div>
<div><div><div><span>Home</span></div></div></div>
```

### ARIA Attributes
```tsx
<button
  aria-label="Close dialog"
  aria-pressed={isPressed}
  aria-expanded={isExpanded}
>
  <CloseIcon aria-hidden="true" />
</button>
```

### Keyboard Navigation
- All interactive elements focusable
- Visible focus indicators
- Logical tab order
- Escape key closes modals
- Enter/Space activates buttons

### Color Contrast
- Text: 4.5:1 minimum (WCAG AA)
- Large text: 3:1 minimum
- UI components: 3:1 minimum
- Test with contrast checker tools

## Error Handling

### Error Boundaries (React)
```typescript
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

### API Error Handling
```typescript
try {
  const data = await fetchUser(id);
  setUser(data);
} catch (error) {
  if (error.status === 404) {
    setError('User not found');
  } else if (error.status === 500) {
    setError('Server error, please try again');
  } else {
    setError('Something went wrong');
  }
}
```

## Testing

### Unit Tests
- Test component rendering
- Test user interactions
- Test edge cases
- Mock external dependencies

### Integration Tests
- Test component combinations
- Test data flow
- Test routing
