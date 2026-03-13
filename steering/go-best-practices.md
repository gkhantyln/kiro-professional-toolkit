---
inclusion: fileMatch
fileMatchPattern: "**/*.go"
---

# Go Best Practices

## Code Organization

### Project Structure
```
project/
├── cmd/
│   └── api/
│       └── main.go
├── internal/
│   ├── handlers/
│   ├── models/
│   ├── services/
│   └── repository/
├── pkg/
│   └── utils/
├── go.mod
└── go.sum
```

### Naming Conventions
```go
// Exported (public): PascalCase
type User struct {
    ID    int
    Email string
}

// Unexported (private): camelCase
type userRepository struct {
    db *sql.DB
}

// Constants: PascalCase or UPPER_SNAKE_CASE
const MaxConnections = 100
const API_VERSION = "v1"

// Interfaces: -er suffix
type Reader interface {
    Read(p []byte) (n int, err error)
}
```

## Error Handling

### Custom Errors
```go
import "errors"

var (
    ErrUserNotFound = errors.New("user not found")
    ErrInvalidEmail = errors.New("invalid email format")
)

// Error with context
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}
```

### Error Wrapping
```go
import "fmt"

func GetUser(id int) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, fmt.Errorf("failed to get user %d: %w", id, err)
    }
    return user, nil
}

// Check wrapped error
if errors.Is(err, ErrUserNotFound) {
    // Handle not found
}
```

## Structs and Methods

### Struct Definition
```go
type User struct {
    ID        int       `json:"id" db:"id"`
    Email     string    `json:"email" db:"email" validate:"required,email"`
    Name      string    `json:"name" db:"name"`
    CreatedAt time.Time `json:"created_at" db:"created_at"`
}

// Constructor
func NewUser(email, name string) *User {
    return &User{
        Email:     email,
        Name:      name,
        CreatedAt: time.Now(),
    }
}

// Method
func (u *User) Validate() error {
    if u.Email == "" {
        return ErrInvalidEmail
    }
    return nil
}
```

## Interfaces

### Small Interfaces
```go
// ✅ Good - small, focused
type UserGetter interface {
    GetUser(id int) (*User, error)
}

type UserCreator interface {
    CreateUser(user *User) error
}

// ❌ Bad - too large
type UserRepository interface {
    GetUser(id int) (*User, error)
    CreateUser(user *User) error
    UpdateUser(user *User) error
    DeleteUser(id int) error
    ListUsers() ([]*User, error)
}
```

## Concurrency

### Goroutines
```go
func processUsers(users []*User) {
    var wg sync.WaitGroup
    
    for _, user := range users {
        wg.Add(1)
        go func(u *User) {
            defer wg.Done()
            process(u)
        }(user)
    }
    
    wg.Wait()
}
```

### Channels
```go
func worker(jobs <-chan int, results chan<- int) {
    for job := range jobs {
        results <- job * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)
    
    // Start workers
    for w := 1; w <= 3; w++ {
        go worker(jobs, results)
    }
    
    // Send jobs
    for j := 1; j <= 5; j++ {
        jobs <- j
    }
    close(jobs)
    
    // Collect results
    for a := 1; a <= 5; a++ {
        <-results
    }
}
```

### Context
```go
func fetchUser(ctx context.Context, id int) (*User, error) {
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()
    
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    case user := <-getUserFromDB(id):
        return user, nil
    }
}
```

## Testing

### Table-Driven Tests
```go
func TestCalculate(t *testing.T) {
    tests := []struct {
        name     string
        input    int
        expected int
        wantErr  bool
    }{
        {"positive", 5, 10, false},
        {"zero", 0, 0, false},
        {"negative", -5, 0, true},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := Calculate(tt.input)
            
            if (err != nil) != tt.wantErr {
                t.Errorf("Calculate() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            
            if result != tt.expected {
                t.Errorf("Calculate() = %v, want %v", result, tt.expected)
            }
        })
    }
}
```
