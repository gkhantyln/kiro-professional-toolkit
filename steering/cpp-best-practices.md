---
inclusion: fileMatch
fileMatchPattern: "**/*.{cpp,cxx,cc,hpp,hxx,h}"
---

# C++ Best Practices (C++23)

## Modern C++ Core Rules

### Resource Management (RAII)
```cpp
// ❌ Bad — manual memory management
void bad() {
    int* data = new int[100];
    process(data);  // leak if throws
    delete[] data;
}

// ✅ Good — RAII, automatic cleanup
void good() {
    std::vector<int> data(100);
    process(data);  // always cleaned up
}

// ✅ Smart pointers for ownership
auto obj = std::make_unique<MyClass>(args);
auto shared = std::make_shared<Resource>();
```

### Type Safety
```cpp
// ❌ Bad — C-style casts
double x = 3.14;
int n = (int)x;

// ✅ Good — named casts
int n = static_cast<int>(x);
auto* derived = dynamic_cast<Derived*>(base_ptr);

// ✅ Use std::bit_cast for type-punning (C++20)
float f = 1.0f;
uint32_t bits = std::bit_cast<uint32_t>(f);
```

### Const Correctness
```cpp
// ✅ Always const where possible
const std::string& getName() const noexcept { return name_; }
void process(const std::vector<int>& data);

// ✅ constexpr for compile-time computation
constexpr std::size_t BUFFER_SIZE = 4096;
constexpr double PI = std::numbers::pi;

// ✅ consteval for guaranteed compile-time (C++20)
consteval int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}
```

## Error Handling

### Use std::expected (C++23) over exceptions for expected failures
```cpp
#include <expected>

std::expected<User, std::string> find_user(int id) {
    if (id <= 0) return std::unexpected("Invalid ID");
    auto user = db.query(id);
    if (!user) return std::unexpected("User not found");
    return *user;
}

// Usage
auto result = find_user(42);
if (result) {
    process(*result);
} else {
    log_error(result.error());
}
```

### Exception safety levels
```cpp
// ✅ Strong exception safety — commit-or-rollback
void transfer(Account& from, Account& to, double amount) {
    // Use copy-and-swap or transactional approach
    auto from_copy = from;
    auto to_copy = to;
    from_copy.debit(amount);   // may throw
    to_copy.credit(amount);    // may throw
    std::swap(from, from_copy);
    std::swap(to, to_copy);    // noexcept swap
}
```

## Performance

### Avoid unnecessary copies
```cpp
// ❌ Bad — copies string
std::string process(std::string s) { return s + "!"; }

// ✅ Good — pass by value when you need a copy anyway (move semantics)
std::string process(std::string s) {
    s += "!";
    return s;  // NRVO or move
}

// ✅ string_view for read-only string params
void log(std::string_view message) noexcept;
void parse(std::span<const uint8_t> data);
```

### Move semantics
```cpp
// ✅ Move expensive resources
class Buffer {
    std::vector<uint8_t> data_;
public:
    Buffer(Buffer&&) noexcept = default;
    Buffer& operator=(Buffer&&) noexcept = default;
    Buffer(const Buffer&) = default;
    Buffer& operator=(const Buffer&) = default;
};

// ✅ Perfect forwarding
template<typename T>
void emplace(std::vector<T>& vec, auto&&... args) {
    vec.emplace_back(std::forward<decltype(args)>(args)...);
}
```

### Cache-friendly data structures
```cpp
// ❌ Bad — AoS (Array of Structs) — poor cache locality for SIMD
struct Particle { float x, y, z, vx, vy, vz; };
std::vector<Particle> particles;

// ✅ Good — SoA (Struct of Arrays) — SIMD-friendly
struct ParticleSystem {
    std::vector<float> x, y, z;
    std::vector<float> vx, vy, vz;
};
```

## Concurrency

### Prefer high-level primitives
```cpp
// ✅ std::jthread (C++20) — auto-joins on destruction
std::jthread worker([](std::stop_token st) {
    while (!st.stop_requested()) {
        do_work();
    }
});

// ✅ std::atomic for lock-free simple state
std::atomic<bool> running{true};
std::atomic<int64_t> counter{0};
counter.fetch_add(1, std::memory_order_relaxed);

// ✅ Coroutines for async I/O (C++20)
asio::awaitable<std::string> fetch_data(std::string url) {
    auto response = co_await http_client.get(url);
    co_return response.body();
}
```

### Avoid data races
```cpp
// ✅ Protect shared state with mutex + lock_guard
class ThreadSafeCache {
    mutable std::shared_mutex mutex_;
    std::unordered_map<std::string, std::string> cache_;
public:
    std::optional<std::string> get(const std::string& key) const {
        std::shared_lock lock{mutex_};  // multiple readers
        auto it = cache_.find(key);
        return it != cache_.end() ? std::optional{it->second} : std::nullopt;
    }
    void set(const std::string& key, std::string value) {
        std::unique_lock lock{mutex_};  // exclusive writer
        cache_.emplace(key, std::move(value));
    }
};
```

## Code Organization

### Header hygiene
```cpp
// ✅ Use #pragma once (or include guards)
#pragma once

// ✅ Forward declare instead of including
class MyClass;  // forward decl in header
// #include "my_class.hpp"  // only in .cpp

// ✅ Prefer modules (C++20) for new code
export module mylib.utils;
export class StringUtils { ... };
```

### Naming conventions
```cpp
// Classes/Structs: PascalCase
class HttpServer {};
struct ConnectionConfig {};

// Functions/methods: snake_case
void process_request();
int calculate_checksum();

// Member variables: trailing underscore
class Foo {
    int value_;
    std::string name_;
};

// Constants: kPascalCase or UPPER_SNAKE_CASE
constexpr int kMaxRetries = 3;
constexpr std::size_t BUFFER_SIZE = 4096;

// Template params: single uppercase or PascalCase
template<typename T, typename Allocator = std::allocator<T>>
```

## Build & Tooling

### Compiler flags (production)
```cmake
target_compile_options(mylib PRIVATE
    -Wall -Wextra -Wpedantic -Werror
    -Wno-unused-parameter
    $<$<CONFIG:Release>:-O3 -march=native -flto -DNDEBUG>
    $<$<CONFIG:Debug>:-O0 -g3 -fsanitize=address,undefined>
)
```

### Static analysis checklist
- [ ] clang-tidy with cppcoreguidelines-* rules
- [ ] cppcheck for undefined behavior
- [ ] Valgrind / AddressSanitizer for memory errors
- [ ] ThreadSanitizer for data races
- [ ] UBSan for undefined behavior
