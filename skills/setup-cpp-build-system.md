---
name: setup-cpp-build-system
description: Production C++ build system with CMake presets, Conan 2 + vcpkg, sanitizers, static analysis, fuzzing, and CI/CD pipeline
---

# Setup C++ Build System

Production-ready C++ build sistemi kurar:
- CMake 3.25+ presets (configure/build/test)
- Conan 2 + vcpkg paket yönetimi
- AddressSanitizer, UBSan, ThreadSanitizer
- clang-tidy + cppcheck statik analiz
- libFuzzer fuzz testing
- ccache + unity builds
- GitHub Actions CI

## Usage
```
#setup-cpp-build-system <project-name>
```

## CMakePresets.json
```json
{
  "version": 6,
  "cmakeMinimumRequired": { "major": 3, "minor": 25 },
  "configurePresets": [
    {
      "name": "base",
      "hidden": true,
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": {
        "CMAKE_EXPORT_COMPILE_COMMANDS": "ON",
        "CMAKE_CXX_STANDARD": "23"
      }
    },
    {
      "name": "debug",
      "inherits": "base",
      "displayName": "Debug",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "ENABLE_SANITIZERS": "ON",
        "ENABLE_COVERAGE": "ON"
      }
    },
    {
      "name": "release",
      "inherits": "base",
      "displayName": "Release",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_INTERPROCEDURAL_OPTIMIZATION": "ON"
      }
    },
    {
      "name": "asan",
      "inherits": "debug",
      "displayName": "AddressSanitizer",
      "cacheVariables": { "SANITIZER": "address" }
    },
    {
      "name": "tsan",
      "inherits": "debug",
      "displayName": "ThreadSanitizer",
      "cacheVariables": { "SANITIZER": "thread" }
    },
    {
      "name": "ubsan",
      "inherits": "debug",
      "displayName": "UndefinedBehaviorSanitizer",
      "cacheVariables": { "SANITIZER": "undefined" }
    },
    {
      "name": "fuzz",
      "inherits": "base",
      "displayName": "Fuzzing",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "RelWithDebInfo",
        "ENABLE_FUZZING": "ON",
        "CMAKE_CXX_COMPILER": "clang++"
      }
    }
  ],
  "buildPresets": [
    { "name": "debug",   "configurePreset": "debug" },
    { "name": "release", "configurePreset": "release" },
    { "name": "asan",    "configurePreset": "asan" },
    { "name": "fuzz",    "configurePreset": "fuzz" }
  ],
  "testPresets": [
    {
      "name": "debug",
      "configurePreset": "debug",
      "output": { "outputOnFailure": true },
      "execution": { "jobs": 4, "timeout": 120 }
    }
  ]
}
```

## cmake/sanitizers.cmake
```cmake
function(enable_sanitizers target)
    if(NOT ENABLE_SANITIZERS)
        return()
    endif()

    set(SANITIZER_FLAGS "")

    if(SANITIZER STREQUAL "address")
        list(APPEND SANITIZER_FLAGS -fsanitize=address,leak -fno-omit-frame-pointer)
    elseif(SANITIZER STREQUAL "thread")
        list(APPEND SANITIZER_FLAGS -fsanitize=thread)
    elseif(SANITIZER STREQUAL "undefined")
        list(APPEND SANITIZER_FLAGS -fsanitize=undefined -fno-sanitize-recover=all)
    elseif(SANITIZER STREQUAL "memory")
        list(APPEND SANITIZER_FLAGS -fsanitize=memory -fno-omit-frame-pointer)
    endif()

    if(SANITIZER_FLAGS)
        target_compile_options(${target} PRIVATE ${SANITIZER_FLAGS})
        target_link_options(${target} PRIVATE ${SANITIZER_FLAGS})
    endif()
endfunction()
```

## cmake/static_analysis.cmake
```cmake
function(enable_static_analysis target)
    # clang-tidy
    find_program(CLANG_TIDY clang-tidy)
    if(CLANG_TIDY)
        set_target_properties(${target} PROPERTIES
            CXX_CLANG_TIDY "${CLANG_TIDY};--config-file=${CMAKE_SOURCE_DIR}/.clang-tidy"
        )
    endif()

    # cppcheck
    find_program(CPPCHECK cppcheck)
    if(CPPCHECK)
        set_target_properties(${target} PROPERTIES
            CXX_CPPCHECK "${CPPCHECK};--enable=all;--suppress=missingInclude;--error-exitcode=1"
        )
    endif()
endfunction()
```

## .clang-tidy
```yaml
Checks: >
  clang-diagnostic-*,
  clang-analyzer-*,
  cppcoreguidelines-*,
  modernize-*,
  performance-*,
  readability-*,
  bugprone-*,
  -modernize-use-trailing-return-type,
  -cppcoreguidelines-avoid-magic-numbers,
  -readability-magic-numbers

WarningsAsErrors: "*"
HeaderFilterRegex: "include/.*"

CheckOptions:
  - key: readability-identifier-naming.ClassCase
    value: CamelCase
  - key: readability-identifier-naming.FunctionCase
    value: lower_case
  - key: readability-identifier-naming.VariableCase
    value: lower_case
  - key: readability-identifier-naming.MemberSuffix
    value: "_"
```

## tests/fuzz/fuzz_parser.cpp
```cpp
#include <cstdint>
#include <cstddef>
#include <string_view>
#include "parser/json_parser.hpp"

// libFuzzer entry point — compiled with -fsanitize=fuzzer,address
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, std::size_t size) {
    std::string_view input{reinterpret_cast<const char*>(data), size};
    try {
        auto result = JsonParser::parse(input);
        (void)result;
    } catch (const std::exception&) {
        // Expected — parser must not crash or UB
    }
    return 0;
}
```

## conanfile.py
```python
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps, cmake_layout

class CppServiceConan(ConanFile):
    name = "cpp-service"
    version = "1.0.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"

    def requirements(self):
        self.requires("boost/1.84.0")
        self.requires("spdlog/1.13.0")
        self.requires("nlohmann_json/3.11.3")
        self.requires("openssl/3.2.1")
        self.requires("gtest/1.14.0", test=True)
        self.requires("benchmark/1.8.3", test=True)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()
```

## .github/workflows/ci.yml
```yaml
name: CI

on: [push, pull_request]

jobs:
  build-test:
    runs-on: ubuntu-24.04
    strategy:
      matrix:
        preset: [debug, release, asan, ubsan]
    steps:
      - uses: actions/checkout@v4
      - uses: seanmiddleditch/gha-setup-ninja@master
      - uses: hendrikmuhs/ccache-action@v1.2
        with: { key: "${{ matrix.preset }}" }

      - name: Install Conan
        run: pip install conan && conan profile detect

      - name: Install dependencies
        run: conan install . --build=missing -pr:b=default -s build_type=Debug

      - name: Configure
        run: cmake --preset ${{ matrix.preset }}
          -DCMAKE_CXX_COMPILER_LAUNCHER=ccache

      - name: Build
        run: cmake --build --preset ${{ matrix.preset }} -j$(nproc)

      - name: Test
        run: ctest --preset ${{ matrix.preset }} --output-on-failure

  static-analysis:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get install -y clang-tidy cppcheck
      - run: cmake --preset debug
      - run: run-clang-tidy -p build/debug -j$(nproc)

  fuzz:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - run: cmake --preset fuzz && cmake --build --preset fuzz
      - run: ./build/fuzz/fuzz_parser -max_total_time=60 -jobs=4
```
