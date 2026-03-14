---
name: create-cpp-high-performance-lib
description: High-performance C++23 library with lock-free data structures, SIMD intrinsics, memory pools, cache-friendly layouts, and Google Benchmark
---

# Create C++ High Performance Library

İleri seviye C++ performans kütüphanesi oluşturur:
- Lock-free MPSC/SPSC queue (atomic)
- SIMD intrinsics (AVX2/AVX-512)
- Memory pool allocator
- Cache-friendly data layouts (SoA)
- False sharing prevention
- Google Benchmark entegrasyonu
- Perf profiling setup

## Usage
```
#create-cpp-high-performance-lib <lib-name>
```

## include/hplib/spsc_queue.hpp
```cpp
#pragma once
#include <atomic>
#include <array>
#include <optional>
#include <cstddef>
#include <new>  // std::hardware_destructive_interference_size

namespace hplib {

// Single-Producer Single-Consumer lock-free queue
// Bounded, wait-free, cache-line aligned
template<typename T, std::size_t Capacity>
    requires (Capacity > 0 && (Capacity & (Capacity - 1)) == 0)  // power of 2
class SpscQueue {
    static constexpr std::size_t MASK = Capacity - 1;
    static constexpr std::size_t CACHE_LINE = std::hardware_destructive_interference_size;

    struct alignas(CACHE_LINE) AlignedAtomic {
        std::atomic<std::size_t> value{0};
        std::byte padding[CACHE_LINE - sizeof(std::atomic<std::size_t>)]{};
    };

public:
    SpscQueue() = default;
    SpscQueue(const SpscQueue&) = delete;
    SpscQueue& operator=(const SpscQueue&) = delete;

    // Producer thread only
    [[nodiscard]] bool push(T item) noexcept {
        const std::size_t head = head_.value.load(std::memory_order_relaxed);
        const std::size_t next = (head + 1) & MASK;
        if (next == tail_.value.load(std::memory_order_acquire)) {
            return false;  // full
        }
        buffer_[head] = std::move(item);
        head_.value.store(next, std::memory_order_release);
        return true;
    }

    // Consumer thread only
    [[nodiscard]] std::optional<T> pop() noexcept {
        const std::size_t tail = tail_.value.load(std::memory_order_relaxed);
        if (tail == head_.value.load(std::memory_order_acquire)) {
            return std::nullopt;  // empty
        }
        T item = std::move(buffer_[tail]);
        tail_.value.store((tail + 1) & MASK, std::memory_order_release);
        return item;
    }

    [[nodiscard]] bool empty() const noexcept {
        return head_.value.load(std::memory_order_acquire) ==
               tail_.value.load(std::memory_order_acquire);
    }

    [[nodiscard]] std::size_t size() const noexcept {
        const auto h = head_.value.load(std::memory_order_acquire);
        const auto t = tail_.value.load(std::memory_order_acquire);
        return (h - t + Capacity) & MASK;
    }

private:
    AlignedAtomic head_{};
    AlignedAtomic tail_{};
    std::array<T, Capacity> buffer_{};
};

} // namespace hplib
```

## include/hplib/memory_pool.hpp
```cpp
#pragma once
#include <cstddef>
#include <cstdlib>
#include <cassert>
#include <new>
#include <memory>

namespace hplib {

// Fixed-size object pool — O(1) alloc/free, zero fragmentation
template<typename T, std::size_t BlockSize = 4096>
class MemoryPool {
    union Slot {
        alignas(T) std::byte storage[sizeof(T)];
        Slot* next;
    };

    struct Block {
        static constexpr std::size_t SLOTS_PER_BLOCK =
            (BlockSize - sizeof(Block*)) / sizeof(Slot);
        std::array<Slot, SLOTS_PER_BLOCK> slots;
        Block* next_block = nullptr;
    };

public:
    MemoryPool() { allocate_block(); }

    ~MemoryPool() {
        Block* b = current_block_;
        while (b) {
            Block* next = b->next_block;
            ::operator delete(b, std::align_val_t{alignof(Block)});
            b = next;
        }
    }

    MemoryPool(const MemoryPool&) = delete;
    MemoryPool& operator=(const MemoryPool&) = delete;

    template<typename... Args>
    [[nodiscard]] T* allocate(Args&&... args) {
        if (!free_list_) allocate_block();
        Slot* slot = free_list_;
        free_list_ = slot->next;
        return new (&slot->storage) T(std::forward<Args>(args)...);
    }

    void deallocate(T* ptr) noexcept {
        ptr->~T();
        auto* slot = reinterpret_cast<Slot*>(ptr);
        slot->next = free_list_;
        free_list_ = slot;
    }

private:
    void allocate_block() {
        auto* block = new (std::align_val_t{alignof(Block)}) Block{};
        block->next_block = current_block_;
        current_block_ = block;
        for (auto& slot : block->slots) {
            slot.next = free_list_;
            free_list_ = &slot;
        }
    }

    Block* current_block_ = nullptr;
    Slot*  free_list_     = nullptr;
};

} // namespace hplib
```

## include/hplib/simd_math.hpp
```cpp
#pragma once
#include <immintrin.h>  // AVX2
#include <cstddef>
#include <span>
#include <cassert>

namespace hplib::simd {

// Vectorized dot product using AVX2 (8 floats per cycle)
[[nodiscard]] float dot_product_avx2(std::span<const float> a, std::span<const float> b) noexcept {
    assert(a.size() == b.size());
    const std::size_t n = a.size();
    const std::size_t simd_end = n & ~7ULL;  // round down to multiple of 8

    __m256 sum = _mm256_setzero_ps();
    for (std::size_t i = 0; i < simd_end; i += 8) {
        __m256 va = _mm256_loadu_ps(a.data() + i);
        __m256 vb = _mm256_loadu_ps(b.data() + i);
        sum = _mm256_fmadd_ps(va, vb, sum);  // fused multiply-add
    }

    // Horizontal sum of 8 floats
    __m128 lo  = _mm256_castps256_ps128(sum);
    __m128 hi  = _mm256_extractf128_ps(sum, 1);
    __m128 s   = _mm_add_ps(lo, hi);
    s = _mm_hadd_ps(s, s);
    s = _mm_hadd_ps(s, s);
    float result = _mm_cvtss_f32(s);

    // Scalar tail
    for (std::size_t i = simd_end; i < n; ++i) {
        result += a[i] * b[i];
    }
    return result;
}

// Vectorized array addition in-place
void add_arrays_avx2(std::span<float> dst, std::span<const float> src) noexcept {
    assert(dst.size() == src.size());
    const std::size_t n = dst.size();
    const std::size_t simd_end = n & ~7ULL;

    for (std::size_t i = 0; i < simd_end; i += 8) {
        __m256 vd = _mm256_loadu_ps(dst.data() + i);
        __m256 vs = _mm256_loadu_ps(src.data() + i);
        _mm256_storeu_ps(dst.data() + i, _mm256_add_ps(vd, vs));
    }
    for (std::size_t i = simd_end; i < n; ++i) dst[i] += src[i];
}

} // namespace hplib::simd
```

## include/hplib/soa_particles.hpp (Structure of Arrays — cache-friendly)
```cpp
#pragma once
#include <vector>
#include <cstddef>
#include <span>

namespace hplib {

// SoA layout: cache-friendly for SIMD processing
// vs AoS (Array of Structs) which causes cache misses
struct ParticleSystem {
    std::vector<float> x, y, z;       // positions
    std::vector<float> vx, vy, vz;    // velocities
    std::vector<float> mass;
    std::vector<bool>  alive;

    explicit ParticleSystem(std::size_t capacity) {
        x.reserve(capacity);  y.reserve(capacity);  z.reserve(capacity);
        vx.reserve(capacity); vy.reserve(capacity); vz.reserve(capacity);
        mass.reserve(capacity);
        alive.reserve(capacity);
    }

    std::size_t add(float px, float py, float pz,
                    float pvx, float pvy, float pvz, float m) {
        x.push_back(px);   y.push_back(py);   z.push_back(pz);
        vx.push_back(pvx); vy.push_back(pvy); vz.push_back(pvz);
        mass.push_back(m);
        alive.push_back(true);
        return x.size() - 1;
    }

    // SIMD-friendly update — processes all x,y,z contiguously
    void integrate(float dt) noexcept {
        const std::size_t n = x.size();
        const std::size_t simd_end = n & ~7ULL;

        for (std::size_t i = 0; i < simd_end; i += 8) {
            __m256 vx8 = _mm256_loadu_ps(vx.data() + i);
            __m256 x8  = _mm256_loadu_ps(x.data()  + i);
            __m256 dt8 = _mm256_set1_ps(dt);
            _mm256_storeu_ps(x.data() + i, _mm256_fmadd_ps(vx8, dt8, x8));
        }
        for (std::size_t i = simd_end; i < n; ++i) {
            x[i] += vx[i] * dt;
            y[i] += vy[i] * dt;
            z[i] += vz[i] * dt;
        }
    }

    [[nodiscard]] std::size_t count() const noexcept { return x.size(); }
};

} // namespace hplib
```

## benchmarks/bench_queue.cpp
```cpp
#include <benchmark/benchmark.h>
#include "hplib/spsc_queue.hpp"
#include <queue>
#include <mutex>

// Lock-free SPSC vs mutex-protected std::queue
static void BM_SpscQueue(benchmark::State& state) {
    hplib::SpscQueue<int, 65536> q;
    for (auto _ : state) {
        q.push(42);
        auto v = q.pop();
        benchmark::DoNotOptimize(v);
    }
    state.SetItemsProcessed(state.iterations());
}

static void BM_MutexQueue(benchmark::State& state) {
    std::queue<int> q;
    std::mutex m;
    for (auto _ : state) {
        { std::lock_guard lk{m}; q.push(42); }
        { std::lock_guard lk{m}; auto v = q.front(); q.pop(); benchmark::DoNotOptimize(v); }
    }
    state.SetItemsProcessed(state.iterations());
}

BENCHMARK(BM_SpscQueue)->Threads(1)->UseRealTime();
BENCHMARK(BM_MutexQueue)->Threads(1)->UseRealTime();

static void BM_DotProductAVX2(benchmark::State& state) {
    const std::size_t N = state.range(0);
    std::vector<float> a(N, 1.0f), b(N, 2.0f);
    for (auto _ : state) {
        auto r = hplib::simd::dot_product_avx2(a, b);
        benchmark::DoNotOptimize(r);
    }
    state.SetBytesProcessed(state.iterations() * N * sizeof(float) * 2);
}
BENCHMARK(BM_DotProductAVX2)->RangeMultiplier(4)->Range(256, 1 << 20);

BENCHMARK_MAIN();
```
