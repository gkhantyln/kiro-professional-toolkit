---
name: create-cpp-embedded-firmware
description: Production C++ embedded firmware with FreeRTOS, HAL abstraction layer, state machine, watchdog, OTA updates, and hardware-in-the-loop testing
---

# Create C++ Embedded Firmware

Production-ready gömülü sistem firmware'i oluşturur:
- FreeRTOS task yönetimi
- HAL abstraction layer (platform-agnostic)
- Hierarchical State Machine (HSM)
- Watchdog + fault handler
- OTA firmware update (dual-bank)
- Ring buffer + DMA
- Hardware-in-the-loop (HIL) test

## Usage
```
#create-cpp-embedded-firmware <target-mcu>
```

## include/hal/gpio.hpp (HAL Abstraction)
```cpp
#pragma once
#include <cstdint>

namespace hal {

enum class PinMode  : uint8_t { Input, Output, AlternateFunction, Analog };
enum class PinState : uint8_t { Low = 0, High = 1 };
enum class PullMode : uint8_t { None, PullUp, PullDown };

// Pure interface — platform-specific impl in src/hal/<target>/
class IGpio {
public:
    virtual ~IGpio() = default;
    virtual void     configure(PinMode mode, PullMode pull = PullMode::None) = 0;
    virtual void     write(PinState state) = 0;
    virtual void     toggle() = 0;
    [[nodiscard]]
    virtual PinState read() const = 0;
};

class IUart {
public:
    virtual ~IUart() = default;
    virtual void     init(uint32_t baud_rate) = 0;
    virtual bool     transmit(const uint8_t* data, uint16_t len, uint32_t timeout_ms) = 0;
    virtual uint16_t receive(uint8_t* buf, uint16_t max_len, uint32_t timeout_ms) = 0;
    virtual bool     data_available() const = 0;
};

class ISpi {
public:
    virtual ~ISpi() = default;
    virtual void init(uint32_t clock_hz) = 0;
    virtual bool transfer(const uint8_t* tx, uint8_t* rx, uint16_t len) = 0;
};

} // namespace hal
```

## include/rtos/task.hpp (FreeRTOS C++ wrapper)
```cpp
#pragma once
#include "FreeRTOS.h"
#include "task.h"
#include <cstddef>
#include <string_view>
#include <functional>

namespace rtos {

class Task {
public:
    Task(std::string_view name,
         std::size_t stack_words,
         UBaseType_t priority,
         std::function<void()> fn)
        : fn_(std::move(fn))
    {
        xTaskCreate(
            &Task::task_entry,
            name.data(),
            static_cast<configSTACK_DEPTH_TYPE>(stack_words),
            this,
            priority,
            &handle_
        );
    }

    ~Task() {
        if (handle_) vTaskDelete(handle_);
    }

    void suspend() noexcept { vTaskSuspend(handle_); }
    void resume()  noexcept { vTaskResume(handle_); }

    static void delay_ms(uint32_t ms) noexcept {
        vTaskDelay(pdMS_TO_TICKS(ms));
    }

    static void delay_until(TickType_t& last_wake, uint32_t period_ms) noexcept {
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(period_ms));
    }

private:
    static void task_entry(void* param) {
        static_cast<Task*>(param)->fn_();
        vTaskDelete(nullptr);
    }

    TaskHandle_t handle_ = nullptr;
    std::function<void()> fn_;
};

template<typename T, std::size_t Depth>
class Queue {
public:
    Queue() : handle_(xQueueCreate(Depth, sizeof(T))) {}
    ~Queue() { vQueueDelete(handle_); }

    bool send(const T& item, uint32_t timeout_ms = portMAX_DELAY) noexcept {
        return xQueueSend(handle_, &item, pdMS_TO_TICKS(timeout_ms)) == pdTRUE;
    }

    bool send_from_isr(const T& item) noexcept {
        BaseType_t higher_prio_woken = pdFALSE;
        bool ok = xQueueSendFromISR(handle_, &item, &higher_prio_woken) == pdTRUE;
        portYIELD_FROM_ISR(higher_prio_woken);
        return ok;
    }

    bool receive(T& item, uint32_t timeout_ms = portMAX_DELAY) noexcept {
        return xQueueReceive(handle_, &item, pdMS_TO_TICKS(timeout_ms)) == pdTRUE;
    }

private:
    QueueHandle_t handle_;
};

} // namespace rtos
```

## include/fsm/state_machine.hpp (Hierarchical State Machine)
```cpp
#pragma once
#include <cstdint>
#include <functional>
#include <array>
#include <optional>

namespace fsm {

template<typename StateEnum, typename EventEnum, std::size_t MaxTransitions>
class StateMachine {
public:
    using Action = std::function<void()>;
    using Guard  = std::function<bool()>;

    struct Transition {
        StateEnum from;
        EventEnum event;
        StateEnum to;
        Action    action;
        Guard     guard;
    };

    explicit StateMachine(StateEnum initial) : current_(initial) {}

    void add_transition(StateEnum from, EventEnum event, StateEnum to,
                        Action action = {}, Guard guard = {}) {
        transitions_[count_++] = {from, event, to, std::move(action), std::move(guard)};
    }

    bool process(EventEnum event) {
        for (std::size_t i = 0; i < count_; ++i) {
            auto& t = transitions_[i];
            if (t.from == current_ && t.event == event) {
                if (t.guard && !t.guard()) continue;
                if (on_exit_) on_exit_(current_);
                if (t.action) t.action();
                current_ = t.to;
                if (on_enter_) on_enter_(current_);
                return true;
            }
        }
        return false;  // no transition found
    }

    [[nodiscard]] StateEnum state() const noexcept { return current_; }

    void on_enter(std::function<void(StateEnum)> fn) { on_enter_ = std::move(fn); }
    void on_exit(std::function<void(StateEnum)> fn)  { on_exit_  = std::move(fn); }

private:
    StateEnum current_;
    std::array<Transition, MaxTransitions> transitions_{};
    std::size_t count_ = 0;
    std::function<void(StateEnum)> on_enter_, on_exit_;
};

} // namespace fsm
```

## src/firmware/watchdog.cpp
```cpp
#include "hal/watchdog.hpp"
#include "rtos/task.hpp"

// Watchdog task — must kick every WATCHDOG_PERIOD_MS or system resets
void watchdog_task() {
    hal::Watchdog wdt;
    wdt.init(5000);  // 5 second timeout
    wdt.start();

    TickType_t last_wake = xTaskGetTickCount();
    while (true) {
        wdt.kick();
        rtos::Task::delay_until(last_wake, 1000);  // kick every 1s
    }
}
```

## src/firmware/ota_update.cpp
```cpp
#include "hal/flash.hpp"
#include "hal/crc.hpp"
#include <cstdint>
#include <span>

// Dual-bank OTA: write to inactive bank, verify, then swap
class OtaUpdater {
    static constexpr uint32_t BANK_A_ADDR = 0x08000000;
    static constexpr uint32_t BANK_B_ADDR = 0x08080000;
    static constexpr uint32_t BANK_SIZE   = 0x80000;  // 512KB

public:
    enum class Status { Ok, CrcError, FlashError, InvalidSize };

    Status begin_update(uint32_t firmware_size, uint32_t expected_crc) {
        if (firmware_size > BANK_SIZE) return Status::InvalidSize;
        expected_crc_ = expected_crc;
        write_addr_ = inactive_bank_addr();
        bytes_written_ = 0;
        hal::Flash::erase(write_addr_, BANK_SIZE);
        return Status::Ok;
    }

    Status write_chunk(std::span<const uint8_t> chunk) {
        if (!hal::Flash::write(write_addr_ + bytes_written_, chunk.data(), chunk.size())) {
            return Status::FlashError;
        }
        bytes_written_ += chunk.size();
        return Status::Ok;
    }

    Status finalize() {
        uint32_t actual_crc = hal::Crc32::compute(
            reinterpret_cast<const uint8_t*>(inactive_bank_addr()), bytes_written_
        );
        if (actual_crc != expected_crc_) return Status::CrcError;

        // Write boot flag to swap banks on next reset
        hal::Flash::write_boot_flag(inactive_bank_addr());
        return Status::Ok;
    }

private:
    uint32_t inactive_bank_addr() const {
        // Determine active bank from boot flag
        return hal::Flash::active_bank() == BANK_A_ADDR ? BANK_B_ADDR : BANK_A_ADDR;
    }

    uint32_t expected_crc_  = 0;
    uint32_t write_addr_    = 0;
    uint32_t bytes_written_ = 0;
};
```

## CMakeLists.txt (ARM Cortex-M4 cross-compile)
```cmake
cmake_minimum_required(VERSION 3.25)
project(firmware LANGUAGES CXX ASM)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_CXX_COMPILER arm-none-eabi-g++)
set(CMAKE_ASM_COMPILER arm-none-eabi-gcc)
set(CMAKE_OBJCOPY arm-none-eabi-objcopy)
set(CMAKE_SIZE arm-none-eabi-size)

set(MCU_FLAGS "-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard")
set(CMAKE_CXX_FLAGS "${MCU_FLAGS} -fno-exceptions -fno-rtti -ffunction-sections -fdata-sections -Os")
set(CMAKE_EXE_LINKER_FLAGS "${MCU_FLAGS} -T${CMAKE_SOURCE_DIR}/linker/STM32F407.ld -Wl,--gc-sections -Wl,-Map=firmware.map")

add_executable(firmware.elf
    src/main.cpp
    src/firmware/watchdog.cpp
    src/firmware/ota_update.cpp
    src/hal/stm32/gpio.cpp
    src/hal/stm32/uart.cpp
    src/startup/startup_stm32f407.s
)

target_include_directories(firmware.elf PRIVATE include third_party/FreeRTOS/include)
target_compile_definitions(firmware.elf PRIVATE STM32F407xx USE_HAL_DRIVER)

# Generate .bin and .hex
add_custom_command(TARGET firmware.elf POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O binary firmware.elf firmware.bin
    COMMAND ${CMAKE_OBJCOPY} -O ihex   firmware.elf firmware.hex
    COMMAND ${CMAKE_SIZE} firmware.elf
)
```
