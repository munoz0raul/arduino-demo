# Arduino LED Matrix Display Controller

**📖 [Read the full blog post: Interactive LED Matrix Drawing with Arduino Uno Q](./BLOG.md)**

This project provides an **interactive LED matrix display controller** for the Arduino Uno Q. Through a Python-based menu interface, you can display various images and animations on the board's built-in LED matrix, including hearts, microphones, signal indicators, and logos.

This is a fully self-contained Docker environment for **building and flashing Zephyr-based sketches** to the **Arduino Uno Q (STM32U5)** board.

It includes:

- **arduino-cli**
- **Arduino Zephyr Core (`arduino:zephyr`)**
- **OpenOCD with Arduino-specific configuration** (`/opt/openocd`)
- A generic **build + flash script** (`start.sh`)
- **Python environment** with Arduino app utilities
- Support for flashing via **linuxgpiod SWD** (Uno R4 uses SWD pins internally)

This allows you to compile, flash sketches, and run Python applications **from any machine** without installing the Arduino IDE, Zephyr SDK, or OpenOCD locally.

---

## 🚀 Features

- **Interactive menu-driven LED matrix control**
- Multiple image categories:
  - 🫀 **Hearts** (9 variations: LittleHeart, Heart1-8)
  - 🎤 **Microphones** (4 variations: Mic1-4)
  - 📡 **Signals** (10 variations: Sig1-10)
  - 🎨 **Logos** (Foundries & Arduino)
- **Built-in animations**:
  - Signal animation (Sig1-10 sequence)
  - Microphone animation (Mic1-4 sequence)
- **Display control** (clear display, stop animations)
- Dockerized environment with:
  - Automatic compilation with `arduino-cli`
  - Flashing to STM32U5 using OpenOCD
  - Python-Arduino bridge communication
- Isolated environment with reproducible builds
- Compatible with Uno Q Minima and Uno Q WiFi (same MCU)

---

## 📦 Requirements

- Docker
- Access to the board's GPIO chip devices (required for SWD)
- Linux host (Windows/macOS not compatible with gpiod flashing)

---

## 🧱 Building the Docker Image

```sh
docker build -t arduino-matrix .
```

---

## ▶️ Running the Container

### Using Docker Run

Run the container with the necessary GPIO devices and socket mount:

```sh
docker run -it --privileged \
    --device /dev/gpiochip0 \
    --device /dev/gpiochip1 \
    --device /dev/gpiochip2 \
    -v /var/run/arduino-router.sock:/var/run/arduino-router.sock \
    arduino-matrix
```

### Using Docker Compose

Alternatively, use docker-compose for easier management:

```sh
docker compose up
```

The container will:

1. Compile the sketch in `/app/sketch`:

```sh
arduino-cli compile -b arduino:zephyr:unoq --output-dir /app/sketch /app/sketch
```

2. Flash it to the board:

```sh
/opt/openocd/bin/arduino-flash.sh sketch.ino.elf-zsk.bin
```

3. Run the Python application:

```sh
python /app/main.py
```

The Python app presents an interactive menu where you can select images and control animations on the LED matrix display.

---

## 🎮 Interactive Menu

Once running, the Python application displays a menu with the following options:

### 🫀 Hearts
- `0` - LittleHeart
- `1-8` - Heart1 through Heart8

### 🎤 Microphones
- `m1-m4` - Mic1 through Mic4

### 📡 Signals
- `s1-s10` - Sig1 through Sig10

### 🎨 Logos
- `f` - Foundries Logo
- `a` - Arduino Logo

### 🎬 Animations
- `i` - Start Signal animation (Sig1-10 sequence)
- `s` - Stop animation
- `mi` - Start Microphone animation (Mic1-4 sequence)
- `ms` - Stop Microphone animation

### ⚙️ Utilities
- `z` - Zero (clear display)
- `q` - Quit

---

## 🎯 How It Works

The Arduino sketch (`sketch.ino`):
- Initializes the LED matrix display
- Registers multiple Bridge functions for each image and animation
- Converts 8-bit frame data to 32-bit format for the LED matrix
- Handles static image display and continuous animations
- Responds to commands from the Python application via Arduino Bridge

The Python application (`main.py`):
- Provides an interactive command-line menu
- Sends commands to the Arduino via the Bridge interface
- Allows real-time control of the LED matrix display
- Supports both static images and continuous animations

---

## 🗂 Repository Structure

```
.
├── Dockerfile
├── start.sh
├── main.py
├── sketch.ino
├── sketch.yaml
├── frames.h
├── openocd/
│   ├── bin/openocd
│   ├── bin/arduino-flash.sh
│   ├── openocd_gpiod.cfg
│   └── additional stm32 configs...
├── arduino.asc
├── arduino.conf
└── arduino.list
```

### `/opt/openocd`

The container includes Arduino’s custom OpenOCD bundle that supports:

- linuxgpiod SWD backend
- STM32U5 flashing
- arduino-flash.sh wrapper script
- Arduino’s board-specific config files

This is the same mechanism used by the **Arduino IDE** and **arduino-cli**.

---

## ⚙️ start.sh (Automatic Compiler + Flasher + Python App)

The container runs this script by default:

```bash
#!/bin/bash
set -e

SKETCH_DIR="/app/sketch"

echo ">>> Compiling sketch..."
arduino-cli compile -b arduino:zephyr:unoq --output-dir "$SKETCH_DIR" "$SKETCH_DIR"

echo ">>> Flashing..."
BIN_FILE=$(ls "$SKETCH_DIR"/*.elf-zsk.bin | head -n 1)
if [ -z "$BIN_FILE" ]; then
    echo "ERROR: No .elf-zsk.bin found"
    exit 1
fi

/opt/openocd/bin/arduino-flash.sh "$BIN_FILE"

echo ">>> Activating virtualenv"
source /opt/venv/bin/activate

echo ">>> Running Python App..."
python /app/main.py
```

---

## 🛠 Troubleshooting

### OpenOCD cannot access GPIO
Make sure you passed the `--device /dev/gpiochip*` arguments.

### Permission denied on gpiochip
Run as root or adjust udev rules.

### Sketch fails to compile
Make sure your sketch contains:

- A valid Zephyr-based Arduino project
- Board set to `arduino:zephyr:unoq`
