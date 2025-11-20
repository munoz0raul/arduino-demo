# Arduino Uno R4 Demo Projects

This repository contains demonstration projects for the **Arduino Uno R4** board, showcasing LED matrix display capabilities using Dockerized development environments.

## 📁 Projects

### 🫀 [arduino-heart](./arduino-heart)
A heart animation demo that displays a static heart on the LED matrix and triggers a beating animation when receiving `keyword_detected` events. This project demonstrates event-driven animations and Python-Arduino bridge communication.

**Features:**
- Static heart display on startup
- 8-frame beating heart animation
- Automatic triggering via Python application (every 10 seconds)
- Can be adapted for real keyword detection from audio input

### 🎨 [arduino-matrix](./arduino-matrix)
An interactive LED matrix display controller with a menu-driven interface for displaying various images and animations.

**Features:**
- 30+ different images across multiple categories:
  - Hearts (9 variations)
  - Microphones (4 variations)
  - Signals (10 variations)
  - Logos (Foundries & Arduino)
- Built-in animations (Signal and Microphone sequences)
- Interactive Python menu for real-time control
- Display management (clear, start/stop animations)

## 🚀 Technology Stack

Both projects use:
- **Arduino Uno R4** (STM32U5 MCU)
- **Zephyr RTOS** via Arduino Zephyr Core
- **Docker** for isolated build environments
- **OpenOCD** for flashing via SWD
- **Python** for host-side applications
- **Arduino Bridge** for Python-Arduino communication

## 🧱 Getting Started

Each project is self-contained with its own:
- `Dockerfile` - Complete development environment
- `docker-compose.yml` - Easy container management
- `sketch.ino` - Arduino sketch for the board
- `main.py` - Python application for interaction
- `README.md` - Detailed setup and usage instructions

### Prerequisites
- Docker installed
- Linux host (required for GPIO-based SWD flashing)
- Access to GPIO chip devices (`/dev/gpiochip0`, `/dev/gpiochip1`, `/dev/gpiochip2`)

### Quick Start
Navigate to any project directory and run:

```bash
# Build the Docker image
docker build -t <project-name> .

# Run with Docker Compose
docker compose up
```

Or use Docker directly:

```bash
docker run -it --privileged \
    --device /dev/gpiochip0 \
    --device /dev/gpiochip1 \
    --device /dev/gpiochip2 \
    -v /var/run/arduino-router.sock:/var/run/arduino-router.sock \
    <project-name>
```

## 📖 Documentation

For detailed information about each project, including:
- Build instructions
- Configuration options
- Code explanations
- Usage examples

Please refer to the individual README.md files in each project directory.

## 🎯 Purpose

These projects serve as:
- **Learning resources** for Arduino Uno R4 LED matrix programming
- **Templates** for Dockerized Arduino development
- **Examples** of Python-Arduino bridge communication
- **Test cases** for Arduino Uno R4 capabilities

## 📝 License

Check individual project directories for license information.
