# Arduino Heart Animation – LED Matrix Demo

This project demonstrates a **heart animation on the Arduino Uno R4's LED matrix display**. The sketch displays a static heart that comes to life with an animated beating effect when triggered by a `keyword_detected` event.

This is a fully self-contained Docker environment for **building and flashing Zephyr-based sketches** to the **Arduino Uno R4 (STM32U5)** board.

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

- **Heart animation on LED matrix display**
- Displays a static heart pattern on startup
- Animates with beating effect when triggered
- Python application automatically sends `keyword_detected` events every 10 seconds
- Dockerized environment with:
  - Automatic compilation with `arduino-cli`
  - Flashing to STM32U5 using OpenOCD
  - Python-Arduino bridge communication
- Isolated environment with reproducible builds
- Compatible with Uno R4 Minima and Uno R4 WiFi (same MCU)

---

## 📦 Requirements

- Docker
- Access to the board's GPIO chip devices (required for SWD)
- Linux host (Windows/macOS not compatible with gpiod flashing)

---

## 🧱 Building the Docker Image

```sh
docker build -t arduino-heart .
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
    arduino-heart
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

The Python app sends a `keyword_detected` event automatically every 10 seconds via the Arduino Bridge, triggering the heart animation on the LED matrix.

---

## 🎯 How It Works

The Arduino sketch (`sketch.ino`):
- Initializes the LED matrix display
- Shows a static heart pattern on startup
- Listens for `keyword_detected` events via the Arduino Bridge
- When triggered, plays an 8-frame beating heart animation
- Returns to the static heart pattern after animation completes

The Python application (`main.py`):
- Automatically sends `keyword_detected` events every 10 seconds
- Uses the Arduino Bridge to communicate with the sketch
- Can be modified to trigger on actual keyword detection from audio input

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
