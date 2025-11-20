#!/bin/bash
set -e

SKETCH_DIR="/tmp/sketch"

echo ">>> Using sketch directory: $SKETCH_DIR"
ls -l "$SKETCH_DIR"

cd "$SKETCH_DIR"

echo ">>> Compiling sketch..."
arduino-cli compile -b arduino:zephyr:unoq --output-dir . .

echo ">>> Searching generated .elf-zsk.bin file..."
BIN_FILE=$(ls *.elf-zsk.bin | head -n 1)

if [ -z "$BIN_FILE" ]; then
    echo "ERROR: No *.elf-zsk.bin file found!"
    exit 1
fi

echo ">>> Flashing using OpenOCD: $BIN_FILE"
/opt/openocd/bin/arduino-flash.sh "$BIN_FILE"

echo ">>> Done!"
