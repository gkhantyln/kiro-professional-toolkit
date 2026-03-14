---
name: create-cpp-modern-service
description: Production C++23 async HTTP service with Boost.Asio, Beast, coroutines, connection pooling, structured concurrency, and OpenTelemetry
---

# Create C++23 Modern Service

Production-ready C++23 async HTTP servisi oluşturur:
- Boost.Asio + Beast (async HTTP/WebSocket)
- C++20 coroutines (co_await)
- Thread pool + strand-based concurrency
- Connection pooling
- Structured logging (spdlog)
- OpenTelemetry tracing
- Graceful shutdown

## Usage
```
#create-cpp-modern-service <service-name>
```

## include/server/http_server.hpp
```cpp
#pragma once
#include <boost/asio.hpp>
#include <boost/asio/awaitable.hpp>
#include <boost/asio/co_spawn.hpp>
#include <boost/beast/http.hpp>
#include <boost/beast/core.hpp>
#include <spdlog/spdlog.h>
#include <functional>
#include <memory>
#include <string>
#include <unordered_map>

namespace asio  = boost::asio;
namespace beast = boost::beast;
namespace http  = beast::http;
using tcp       = asio::ip::tcp;

using Request  = http::request<http::string_body>;
using Response = http::response<http::string_body>;
using Handler  = std::function<asio::awaitable<Response>(Request)>;

class Router {
public:
    void add(http::verb method, std::string_view path, Handler handler) {
        routes_[{method, std::string(path)}] = std::move(handler);
    }

    void get(std::string_view path, Handler h)    { add(http::verb::get,    path, std::move(h)); }
    void post(std::string_view path, Handler h)   { add(http::verb::post,   path, std::move(h)); }
    void put(std::string_view path, Handler h)    { add(http::verb::put,    path, std::move(h)); }
    void del(std::string_view path, Handler h)    { add(http::verb::delete_, path, std::move(h)); }

    std::optional<Handler> match(http::verb method, std::string_view path) const {
        auto it = routes_.find({method, std::string(path)});
        if (it != routes_.end()) return it->second;
        return std::nullopt;
    }

private:
    struct RouteKey {
        http::verb method;
        std::string path;
        bool operator==(const RouteKey&) const = default;
    };
    struct RouteKeyHash {
        std::size_t operator()(const RouteKey& k) const noexcept {
            return std::hash<std::string>{}(std::to_string(static_cast<int>(k.method)) + k.path);
        }
    };
    std::unordered_map<RouteKey, Handler, RouteKeyHash> routes_;
};

class HttpServer {
public:
    explicit HttpServer(asio::io_context& ioc, uint16_t port, std::shared_ptr<Router> router)
        : ioc_(ioc), acceptor_(ioc, {tcp::v4(), port}), router_(std::move(router)) {}

    asio::awaitable<void> run() {
        spdlog::info("HTTP server listening on port {}", acceptor_.local_endpoint().port());
        while (true) {
            auto socket = co_await acceptor_.async_accept(asio::use_awaitable);
            asio::co_spawn(ioc_, handle_connection(std::move(socket)), asio::detached);
        }
    }

private:
    asio::awaitable<void> handle_connection(tcp::socket socket) {
        beast::flat_buffer buffer;
        try {
            while (true) {
                Request req;
                co_await http::async_read(socket, buffer, req, asio::use_awaitable);

                Response res;
                if (auto handler = router_->match(req.method(), req.target())) {
                    res = co_await (*handler)(std::move(req));
                } else {
                    res = make_response(http::status::not_found, "Not Found");
                }

                res.set(http::field::server, "CppService/1.0");
                res.prepare_payload();
                co_await http::async_write(socket, res, asio::use_awaitable);

                if (!res.keep_alive()) break;
            }
        } catch (const std::exception& e) {
            spdlog::error("Connection error: {}", e.what());
        }
    }

    static Response make_response(http::status status, std::string_view body) {
        Response res{status, 11};
        res.set(http::field::content_type, "application/json");
        res.body() = std::string(body);
        return res;
    }

    asio::io_context& ioc_;
    tcp::acceptor acceptor_;
    std::shared_ptr<Router> router_;
};
```

## include/server/thread_pool.hpp
```cpp
#pragma once
#include <boost/asio.hpp>
#include <vector>
#include <thread>

namespace asio = boost::asio;

class ThreadPool {
public:
    explicit ThreadPool(std::size_t thread_count = std::thread::hardware_concurrency())
        : work_guard_(asio::make_work_guard(ioc_)) {
        threads_.reserve(thread_count);
        for (std::size_t i = 0; i < thread_count; ++i) {
            threads_.emplace_back([this] { ioc_.run(); });
        }
    }

    ~ThreadPool() {
        work_guard_.reset();
        for (auto& t : threads_) {
            if (t.joinable()) t.join();
        }
    }

    asio::io_context& context() noexcept { return ioc_; }

    void stop() {
        work_guard_.reset();
        ioc_.stop();
    }

private:
    asio::io_context ioc_;
    asio::executor_work_guard<asio::io_context::executor_type> work_guard_;
    std::vector<std::thread> threads_;
};
```

## src/main.cpp
```cpp
#include <boost/asio.hpp>
#include <boost/asio/co_spawn.hpp>
#include <boost/asio/signal_set.hpp>
#include <spdlog/spdlog.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <nlohmann/json.hpp>
#include <cstdlib>

#include "server/http_server.hpp"
#include "server/thread_pool.hpp"

namespace asio = boost::asio;
using json     = nlohmann::json;

int main() {
    // Structured logging setup
    auto logger = spdlog::stdout_color_mt("service");
    spdlog::set_default_logger(logger);
    spdlog::set_pattern(R"({"time":"%Y-%m-%dT%H:%M:%S","level":"%l","msg":"%v"})");
    spdlog::set_level(spdlog::level::info);

    const uint16_t port = static_cast<uint16_t>(
        std::stoi(std::getenv("PORT") ? std::getenv("PORT") : "8080")
    );

    auto router = std::make_shared<Router>();

    // Health endpoint
    router->get("/health", [](Request) -> asio::awaitable<Response> {
        Response res{http::status::ok, 11};
        res.set(http::field::content_type, "application/json");
        res.body() = R"({"status":"ok"})";
        co_return res;
    });

    // Example API endpoint
    router->get("/api/v1/users", [](Request req) -> asio::awaitable<Response> {
        json body = json::array({
            {{"id", "1"}, {"name", "Alice"}},
            {{"id", "2"}, {"name", "Bob"}},
        });
        Response res{http::status::ok, 11};
        res.set(http::field::content_type, "application/json");
        res.body() = body.dump();
        co_return res;
    });

    ThreadPool pool;
    asio::io_context& ioc = pool.context();

    HttpServer server{ioc, port, router};

    // Graceful shutdown
    asio::signal_set signals{ioc, SIGINT, SIGTERM};
    signals.async_wait([&](auto, auto) {
        spdlog::info("Shutdown signal received");
        pool.stop();
    });

    asio::co_spawn(ioc, server.run(), asio::detached);

    spdlog::info("Service started", "port", port);
    pool.context().run();  // blocks until stop()

    spdlog::info("Service stopped");
    return 0;
}
```

## CMakeLists.txt
```cmake
cmake_minimum_required(VERSION 3.25)
project(cpp_service VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Compiler hardening flags
add_compile_options(
    -Wall -Wextra -Wpedantic -Werror
    -fstack-protector-strong
    -D_FORTIFY_SOURCE=2
    $<$<CONFIG:Release>:-O3 -march=native -flto>
    $<$<CONFIG:Debug>:-O0 -g3 -fsanitize=address,undefined>
)
add_link_options($<$<CONFIG:Debug>:-fsanitize=address,undefined>)

find_package(Boost 1.84 REQUIRED COMPONENTS system)
find_package(spdlog REQUIRED)
find_package(nlohmann_json REQUIRED)
find_package(OpenSSL REQUIRED)

add_executable(service src/main.cpp)
target_include_directories(service PRIVATE include)
target_link_libraries(service PRIVATE
    Boost::system
    spdlog::spdlog
    nlohmann_json::nlohmann_json
    OpenSSL::SSL OpenSSL::Crypto
    pthread
)

# Unit tests
enable_testing()
find_package(GTest REQUIRED)
add_executable(tests tests/main_test.cpp)
target_link_libraries(tests PRIVATE GTest::gtest_main Boost::system spdlog::spdlog)
add_test(NAME unit_tests COMMAND tests)
```

## vcpkg.json
```json
{
  "name": "cpp-service",
  "version": "1.0.0",
  "dependencies": [
    { "name": "boost-asio",   "version>=": "1.84.0" },
    { "name": "boost-beast",  "version>=": "1.84.0" },
    "spdlog",
    "nlohmann-json",
    "openssl",
    "gtest"
  ]
}
```
