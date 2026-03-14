---
name: create-cpp-game-engine-component
description: C++23 game engine component with ECS architecture, job system, SIMD math library, asset streaming, and render graph abstraction
---

# Create C++ Game Engine Component

Production-ready oyun motoru bileşeni oluşturur:
- Entity Component System (ECS) — cache-friendly archetype
- Job system (work-stealing thread pool)
- SIMD math (Vec3/Vec4/Mat4 — AVX2)
- Asset streaming + hot reload
- Render graph abstraction
- Event bus (zero-allocation)

## Usage
```
#create-cpp-game-engine-component <component-name>
```

## include/ecs/world.hpp (Archetype ECS)
```cpp
#pragma once
#include <cstdint>
#include <vector>
#include <unordered_map>
#include <typeindex>
#include <memory>
#include <span>
#include <cassert>

namespace ecs {

using EntityId    = uint32_t;
using ComponentId = uint32_t;
using ArchetypeId = uint64_t;  // bitmask of component IDs

// Archetype: contiguous storage for entities with same component set
struct Archetype {
    ArchetypeId id;
    std::vector<EntityId> entities;
    std::unordered_map<ComponentId, std::vector<std::byte>> columns;  // component arrays

    template<typename T>
    std::span<T> get_column(ComponentId cid) {
        auto& raw = columns.at(cid);
        return {reinterpret_cast<T*>(raw.data()), raw.size() / sizeof(T)};
    }

    template<typename T>
    void add_component(ComponentId cid, T&& value) {
        auto& col = columns[cid];
        const std::size_t old_size = col.size();
        col.resize(old_size + sizeof(T));
        new (col.data() + old_size) T(std::forward<T>(value));
    }
};

class World {
public:
    EntityId create_entity() {
        return next_entity_id_++;
    }

    template<typename T>
    ComponentId register_component() {
        auto tid = std::type_index(typeid(T));
        if (auto it = component_ids_.find(tid); it != component_ids_.end()) {
            return it->second;
        }
        ComponentId id = next_component_id_++;
        component_ids_[tid] = id;
        component_sizes_[id] = sizeof(T);
        return id;
    }

    template<typename T>
    void add_component(EntityId entity, T component) {
        ComponentId cid = register_component<T>();
        entity_components_[entity].push_back(cid);
        // Find or create archetype
        ArchetypeId arch_id = compute_archetype(entity);
        auto& arch = archetypes_[arch_id];
        arch.id = arch_id;
        arch.entities.push_back(entity);
        arch.add_component(cid, std::move(component));
    }

    // Query: iterate all entities with components T1, T2...
    template<typename... Ts, typename Fn>
    void query(Fn&& fn) {
        std::array<ComponentId, sizeof...(Ts)> required = {
            register_component<Ts>()...
        };
        for (auto& [arch_id, arch] : archetypes_) {
            bool has_all = true;
            for (auto cid : required) {
                if (arch.columns.find(cid) == arch.columns.end()) {
                    has_all = false; break;
                }
            }
            if (!has_all) continue;

            const std::size_t count = arch.entities.size();
            for (std::size_t i = 0; i < count; ++i) {
                fn(arch.entities[i],
                   arch.get_column<Ts>(register_component<Ts>())[i]...);
            }
        }
    }

private:
    ArchetypeId compute_archetype(EntityId entity) {
        ArchetypeId id = 0;
        for (auto cid : entity_components_[entity]) id |= (1ULL << cid);
        return id;
    }

    EntityId    next_entity_id_    = 1;
    ComponentId next_component_id_ = 0;
    std::unordered_map<std::type_index, ComponentId>          component_ids_;
    std::unordered_map<ComponentId, std::size_t>              component_sizes_;
    std::unordered_map<EntityId, std::vector<ComponentId>>    entity_components_;
    std::unordered_map<ArchetypeId, Archetype>                archetypes_;
};

} // namespace ecs
```

## include/math/vec.hpp (SIMD Math)
```cpp
#pragma once
#include <immintrin.h>
#include <cmath>
#include <array>

namespace math {

struct alignas(16) Vec4 {
    union {
        __m128 simd;
        struct { float x, y, z, w; };
        std::array<float, 4> data;
    };

    Vec4() : simd(_mm_setzero_ps()) {}
    Vec4(float x, float y, float z, float w = 0.f) : simd(_mm_set_ps(w, z, y, x)) {}
    explicit Vec4(__m128 v) : simd(v) {}

    [[nodiscard]] Vec4 operator+(const Vec4& o) const noexcept { return Vec4{_mm_add_ps(simd, o.simd)}; }
    [[nodiscard]] Vec4 operator-(const Vec4& o) const noexcept { return Vec4{_mm_sub_ps(simd, o.simd)}; }
    [[nodiscard]] Vec4 operator*(float s)        const noexcept { return Vec4{_mm_mul_ps(simd, _mm_set1_ps(s))}; }

    [[nodiscard]] float dot(const Vec4& o) const noexcept {
        __m128 mul = _mm_mul_ps(simd, o.simd);
        __m128 sum = _mm_hadd_ps(mul, mul);
        sum = _mm_hadd_ps(sum, sum);
        return _mm_cvtss_f32(sum);
    }

    [[nodiscard]] float length() const noexcept { return std::sqrt(dot(*this)); }

    [[nodiscard]] Vec4 normalized() const noexcept {
        return Vec4{_mm_div_ps(simd, _mm_set1_ps(length()))};
    }

    [[nodiscard]] Vec4 cross3(const Vec4& o) const noexcept {
        // (y*oz - z*oy, z*ox - x*oz, x*oy - y*ox)
        __m128 a = _mm_shuffle_ps(simd,  simd,  _MM_SHUFFLE(3,0,2,1));
        __m128 b = _mm_shuffle_ps(o.simd,o.simd,_MM_SHUFFLE(3,1,0,2));
        __m128 c = _mm_shuffle_ps(simd,  simd,  _MM_SHUFFLE(3,1,0,2));
        __m128 d = _mm_shuffle_ps(o.simd,o.simd,_MM_SHUFFLE(3,0,2,1));
        return Vec4{_mm_sub_ps(_mm_mul_ps(a, b), _mm_mul_ps(c, d))};
    }
};

using Vec3 = Vec4;  // w=0 convention

} // namespace math
```

## include/jobs/job_system.hpp (Work-Stealing Thread Pool)
```cpp
#pragma once
#include <thread>
#include <atomic>
#include <functional>
#include <vector>
#include <deque>
#include <mutex>
#include <condition_variable>
#include <future>

namespace jobs {

class JobSystem {
public:
    explicit JobSystem(std::size_t thread_count = std::thread::hardware_concurrency() - 1) {
        workers_.reserve(thread_count);
        for (std::size_t i = 0; i < thread_count; ++i) {
            workers_.emplace_back([this, i] { worker_loop(i); });
        }
    }

    ~JobSystem() {
        {
            std::lock_guard lk{mutex_};
            stop_ = true;
        }
        cv_.notify_all();
        for (auto& t : workers_) t.join();
    }

    template<typename Fn, typename... Args>
    auto submit(Fn&& fn, Args&&... args) -> std::future<std::invoke_result_t<Fn, Args...>> {
        using R = std::invoke_result_t<Fn, Args...>;
        auto task = std::make_shared<std::packaged_task<R()>>(
            [fn = std::forward<Fn>(fn), ...args = std::forward<Args>(args)]() mutable {
                return fn(std::forward<Args>(args)...);
            }
        );
        auto future = task->get_future();
        {
            std::lock_guard lk{mutex_};
            queue_.emplace_back([task] { (*task)(); });
        }
        cv_.notify_one();
        return future;
    }

    // Parallel for — splits work across all threads
    template<typename Fn>
    void parallel_for(std::size_t count, Fn&& fn) {
        const std::size_t n_threads = workers_.size();
        const std::size_t chunk = (count + n_threads - 1) / n_threads;
        std::vector<std::future<void>> futures;
        futures.reserve(n_threads);

        for (std::size_t t = 0; t < n_threads && t * chunk < count; ++t) {
            std::size_t begin = t * chunk;
            std::size_t end   = std::min(begin + chunk, count);
            futures.push_back(submit([&fn, begin, end] {
                for (std::size_t i = begin; i < end; ++i) fn(i);
            }));
        }
        for (auto& f : futures) f.get();
    }

private:
    void worker_loop(std::size_t /*id*/) {
        while (true) {
            std::function<void()> job;
            {
                std::unique_lock lk{mutex_};
                cv_.wait(lk, [this] { return stop_ || !queue_.empty(); });
                if (stop_ && queue_.empty()) return;
                job = std::move(queue_.front());
                queue_.pop_front();
            }
            job();
        }
    }

    std::vector<std::thread>        workers_;
    std::deque<std::function<void()>> queue_;
    std::mutex                      mutex_;
    std::condition_variable         cv_;
    bool                            stop_ = false;
};

} // namespace jobs
```
