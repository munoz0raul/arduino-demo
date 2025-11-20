# Arduino Uno R4 Q – Dockerized Compiler & Flasher

This repository provides a fully self-contained Docker environment for **building and flashing Zephyr-based sketches** to the **Arduino Uno R4 (STM32U5)** board.

It includes:

- **arduino-cli**
- **Arduino Zephyr Core (`arduino:zephyr`)**
- **OpenOCD with Arduino-specific configuration** (`/opt/openocd`)
- A generic **build + flash script** (`build.sh`)
- Support for flashing via **linuxgpiod SWD** (Uno R4 uses SWD pins internally)

This allows you to compile and flash sketches **from any machine** without installing the Arduino IDE, Zephyr SDK, or OpenOCD locally.

---

## 🚀 Features

- Generic Docker container — works with **any sketch**
- Automatically:
  1. Compiles the sketch with `arduino-cli`
  2. Locates the generated `.elf-zsk.bin`
  3. Flashes to the STM32U5 using OpenOCD (`arduino-flash.sh`)
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
docker build -t arduino-flash .
```

---

## ▶️ Running the Container

Mount your sketch directory to `/tmp/sketch` and expose the necessary `gpiochip` devices:

```sh
docker run -it --privileged \
    --device /dev/gpiochip0 \
    --device /dev/gpiochip1 \
    --device /dev/gpiochip2 \
    -v /path/to/your/sketch:/tmp/sketch \
    arduino-flash
```

Example:

```sh
docker run -it --privileged \
    --device /dev/gpiochip0 \
    --device /dev/gpiochip1 \
    --device /dev/gpiochip2 \
    -v /root/arduino-fio/keyword-spotting/sketch:/tmp/sketch \
    arduino-flash
```

The container will:

1. Compile your sketch:

```sh
arduino-cli compile -b arduino:zephyr:unoq
```

2. Flash it to the board:

```sh
/opt/openocd/bin/arduino-flash.sh sketch.ino.elf-zsk.bin
```

---

## 🗂 Repository Structure

```
.
├── Dockerfile
├── build.sh
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

## ⚙️ build.sh (Automatic Compiler + Flasher)

The container runs this script by default:

```bash
#!/bin/bash
set -e
cd /tmp/sketch

arduino-cli compile -b arduino:zephyr:unoq --output-dir . .

BIN=$(ls *.elf-zsk.bin | head -n 1)
if [ -z "$BIN" ]; then
    echo "ERROR: No .elf-zsk.bin produced!"
    exit 1
fi

/opt/openocd/bin/arduino-flash.sh "$BIN"
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

