# Interactive LED Matrix Drawing with Arduino Uno R4: Building a Web-Based Pixel Art Controller

## Introduction

In our [previous tutorial](../arduino-led-webui/BLOG.md), we explored the Arduino Uno R4's dual-core architecture by building a web-controlled LED system. Now, let's take it to the next level by creating an **interactive drawing interface** for the board's built-in **13×8 LED matrix display**.

The [Arduino Uno R4 WiFi](https://docs.arduino.cc/tutorials/uno-q/user-manual/) features a **red LED matrix** with 104 individually controllable LEDs arranged in a 13-column by 8-row grid. This opens up exciting possibilities for:

- **Pixel art drawing**
- **Custom patterns and animations**
- **Real-time data visualization**
- **Interactive displays and games**

In this project, we'll build a web interface where you can **click on squares to draw pixel art** that appears instantly on the physical LED matrix. Think of it as a **miniature LED canvas** controlled from your browser!

## 🎥 Demo Video

Watch the interactive LED matrix in action:

[![Arduino LED Matrix Controller Demo](https://img.shields.io/badge/▶️-Watch%20Demo-red?style=for-the-badge)](https://photos.app.goo.gl/NdSUbqcuH2HFy39w6)

**[Click here to see the video demonstration](https://photos.app.goo.gl/NdSUbqcuH2HFy39w6)**

The video demonstrates:
- Web interface with 13×8 clickable grid
- Real-time pixel drawing on the physical LED matrix
- Click-to-toggle individual LEDs
- Clear all functionality
- Perfect synchronization between browser and hardware

---

## The LED Matrix: Hardware Overview

### Physical Layout

The LED matrix on the Arduino Uno R4 is a **13×8 monochrome display**:

```
Columns:  0  1  2  3  4  5  6  7  8  9 10 11 12
       ┌─────────────────────────────────────┐
Row 0  │ ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■ │
Row 1  │ ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■ │
Row 2  │ ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■ │
Row 3  │ ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■ │
Row 4  │ ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■ │
Row 5  │ ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■ │
Row 6  │ ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■ │
Row 7  │ ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■  ■ │
       └─────────────────────────────────────┘
       Total: 104 LEDs (13 × 8)
```

### Accessing the Matrix Hardware

Unlike individual GPIO pins, the LED matrix is controlled through a **dedicated hardware interface** provided by the MCU firmware. The Arduino Uno R4 exposes two key functions:

```cpp
extern "C" void matrixBegin();              // Initialize the matrix
extern "C" void matrixWrite(const uint32_t* buf);  // Update all LEDs
```

These are **low-level Zephyr RTOS functions** that communicate directly with the matrix controller hardware.

### The Data Format Challenge

Here's the interesting part: the matrix uses a **packed binary format** where all 104 LED states are stored in just **4 × 32-bit integers (128 bits total)**:

- **First 32 LEDs** → `buffer[0]` (bits 0-31)
- **Next 32 LEDs** → `buffer[1]` (bits 0-31)
- **Next 32 LEDs** → `buffer[2]` (bits 0-31)
- **Last 8 LEDs** → `buffer[3]` (bits 0-7)

Each bit represents one LED: `1` = ON, `0` = OFF.

This compact format is efficient but requires conversion from our more intuitive (x, y) coordinate system.

---

## Project Architecture: From Click to LED

Let's see how a mouse click translates to a lit LED:

```
┌──────────────┐
│ Web Browser  │ User clicks grid square (x=5, y=3)
└──────┬───────┘
       │ POST /matrix/toggle {x:5, y:3}
       │
┌──────▼────────┐
│ Flask (MPU)   │ Receives request
│               │ Toggles matrix_state[3][5]
│               │ Calls Bridge.call("set_led", 5, 3, 1)
└──────┬────────┘
       │ IPC via Bridge
       │
┌──────▼────────┐
│ MCU Firmware  │ set_led(x=5, y=3, state=1) executed
│               │ Calculates index = 3*13 + 5 = 44
│               │ Sets matrixState[44] = 1
│               │ Calls updateDisplay()
└──────┬────────┘
       │
┌──────▼────────┐
│ updateDisplay │ Converts 104 bytes → 4 uint32_t
│               │ Sets bit 44 in buffer[1]
│               │ Calls matrixWrite(buffer)
└──────┬────────┘
       │
┌──────▼────────┐
│ LED Matrix    │ LED at position (5,3) lights up! 🔴
└───────────────┘
```

---

## The MCU Firmware: Matrix Control Logic

### State Management

The firmware maintains the matrix state as a simple array:

```cpp
#define MATRIX_COLS 13
#define MATRIX_ROWS 8
#define MATRIX_SIZE 104  // 13 × 8

uint8_t matrixState[MATRIX_SIZE] = {0};
```

This is a **linearized representation** where position (x, y) maps to index `y × 13 + x`.

### Setting Individual LEDs

The `set_led()` function handles individual pixel control:

```cpp
void set_led(int x, int y, int state) {
  if (x < 0 || x >= MATRIX_COLS || y < 0 || y >= MATRIX_ROWS) {
    return;  // Bounds checking
  }
  
  // Calculate linear index (row-major order)
  int index = y * MATRIX_COLS + x;
  
  // Update state
  matrixState[index] = (state != 0) ? 1 : 0;
  
  // Refresh the display
  updateDisplay();
}
```

**Key points:**

1. **Coordinate validation** - Ensures x ∈ [0, 12] and y ∈ [0, 7]
2. **Index calculation** - Converts 2D (x, y) to 1D array index
3. **State update** - Sets the LED to ON (1) or OFF (0)
4. **Display refresh** - Immediately updates the physical matrix

### The Bit-Packing Magic: updateDisplay()

This is where the conversion happens:

```cpp
void updateDisplay() {
  uint32_t buffer[4] = {0, 0, 0, 0};
  
  for (int i = 0; i < MATRIX_SIZE; i++) {
    if (matrixState[i]) {
      int uint32_index = i / 32;        // Which uint32_t (0-3)
      int bit_position = i % 32;        // Bit position (0-31)
      buffer[uint32_index] |= (1UL << bit_position);
    }
  }
  
  matrixWrite(buffer);
}
```

**Understanding the conversion:**

Let's say LED 44 (position x=5, y=3) is ON:
- `i = 44`
- `uint32_index = 44 / 32 = 1` → Goes into `buffer[1]`
- `bit_position = 44 % 32 = 12` → Bit 12 of that uint32_t
- `buffer[1] |= (1UL << 12)` → Sets bit 12 to 1

The result: all 104 LED states packed into just 16 bytes!

### Bridge Registration

The firmware exposes three functions to the MPU:

```cpp
void setup() {
  matrixBegin();  // Initialize hardware
  clearMatrix();  // Clear all LEDs
  
  Bridge.begin();
  Bridge.provide("set_led", set_led);              // Control individual LED
  Bridge.provide("clear_matrix", clear_matrix_bridge);  // Clear all
  Bridge.provide("get_matrix", get_matrix);        // Query state
}
```

---

## The Web Interface: Interactive Drawing Canvas

### Grid Layout with CSS Grid

The HTML creates a perfect 13×8 grid of clickable squares:

```css
.led-grid{
    display: grid;
    grid-template-columns: repeat(13, 1fr);  /* 13 equal columns */
    gap: 4px;
}

.led{
    width: 32px;
    height: 32px;
    background: var(--led-off);
    cursor: pointer;
}

.led.active{
    background: var(--led-on);
    box-shadow: 0 0 12px var(--led-on);  /* Glow effect */
}
```

### JavaScript Grid Generation

The grid is dynamically created to match the matrix dimensions:

```javascript
const MATRIX_COLS = 13;
const MATRIX_ROWS = 8;

function initGrid() {
    const grid = document.getElementById('ledGrid');
    
    for (let y = 0; y < MATRIX_ROWS; y++) {
        for (let x = 0; x < MATRIX_COLS; x++) {
            const led = document.createElement('div');
            led.className = 'led';
            led.dataset.x = x;
            led.dataset.y = y;
            led.dataset.coords = `(${x},${y})`;  // Tooltip
            led.onclick = () => toggleLED(x, y);
            grid.appendChild(led);
        }
    }
}
```

This creates **104 clickable divs** in perfect alignment with the physical matrix.

### Toggle Logic with Visual Feedback

When you click a square:

```javascript
async function toggleLED(x, y) {
    // Send request to Flask server
    const response = await fetch('/matrix/toggle', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({x: x, y: y})
    });
    
    const data = await response.json();
    
    if (data.success) {
        // Update local state
        matrixState[y][x] = data.state;
        
        // Update UI with smooth animation
        updateLED(x, y, data.state);
    }
}

function updateLED(x, y, state) {
    const led = document.querySelector(`[data-x="${x}"][data-y="${y}"]`);
    if (state) {
        led.classList.add('active');  // Light up with glow
    } else {
        led.classList.remove('active');  // Turn off
    }
}
```

### Coordinate Tooltips

Hover over any square to see its coordinates:

```css
.led::after{
    content: attr(data-coords);  /* Shows "(x,y)" */
    position: absolute;
    bottom: 100%;
    background: rgba(0,0,0,0.9);
    padding: 4px 8px;
    opacity: 0;
}

.led:hover::after{
    opacity: 1;  /* Fade in on hover */
}
```

---

## The Python Backend: Matrix State Management

### 2D State Tracking

The MPU maintains a 2D representation for easier manipulation:

```python
MATRIX_COLS = 13
MATRIX_ROWS = 8

# Initialize as 2D array (more intuitive than linear)
matrix_state = [[0 for _ in range(MATRIX_COLS)] for _ in range(MATRIX_ROWS)]
```

This allows natural access like `matrix_state[y][x]` instead of calculating indices.

### Toggle Endpoint with Bridge Call

```python
@app.route('/matrix/toggle', methods=['POST'])
def toggle_led():
    data = request.get_json()
    x = int(data.get('x'))
    y = int(data.get('y'))
    
    # Validate coordinates
    if x < 0 or x >= MATRIX_COLS or y < 0 or y >= MATRIX_ROWS:
        return jsonify({'success': False, 'error': 'Invalid coordinates'}), 400
    
    # Toggle state
    matrix_state[y][x] = 1 if matrix_state[y][x] == 0 else 0
    new_state = matrix_state[y][x]
    
    # Update MCU firmware via Bridge
    Bridge.call("set_led", x, y, new_state)
    
    # Broadcast status update via SSE
    WebStatus.update_status(f"LED ({x},{y}): {'ON' if new_state else 'OFF'}")
    
    return jsonify({'success': True, 'x': x, 'y': y, 'state': new_state})
```

### Clear Matrix Function

One-click to reset the entire display:

```python
@app.route('/matrix/clear', methods=['POST'])
def clear_matrix():
    # Reset Python state
    for y in range(MATRIX_ROWS):
        for x in range(MATRIX_COLS):
            matrix_state[y][x] = 0
    
    # Clear MCU hardware
    Bridge.call("clear_matrix")
    
    WebStatus.update_status("Matrix cleared")
    return jsonify({'success': True})
```

---

## Use Cases and Applications

### 1. Pixel Art Drawing

Create custom icons and patterns:
- Draw hearts, smiley faces, logos
- Design 8-bit style graphics
- Create frame-by-frame animations

### 2. Data Visualization

Display real-time information:
- **Bar graphs** - Show sensor readings
- **Heatmaps** - Visualize data distributions
- **Status indicators** - System health monitoring

### 3. Interactive Games

Build simple LED games:
- **Snake** - Classic game on LED matrix
- **Pong** - Two-player LED tennis
- **Conway's Game of Life** - Cellular automaton

### 4. Message Display

Show text and notifications:
- Scrolling text messages
- Alert symbols
- QR codes (limited by resolution)

---

## Extending the Project

### Add Drawing Tools

Implement additional features:

```javascript
// Brush tool - drag to draw
let isDrawing = false;

led.onmousedown = () => { isDrawing = true; toggleLED(x, y); }
led.onmouseup = () => { isDrawing = false; }
led.onmouseenter = () => { if (isDrawing) toggleLED(x, y); }
```

### Save and Load Patterns

Store designs as JSON:

```python
@app.route('/matrix/save', methods=['POST'])
def save_pattern():
    pattern = {
        'name': request.json.get('name'),
        'data': matrix_state
    }
    # Save to file or database
    return jsonify({'success': True})
```

### Animation Playback

Display pre-defined animations:

```cpp
// In MCU firmware
void playAnimation(const uint8_t frames[][104], int frameCount, int delay_ms) {
    for (int i = 0; i < frameCount; i++) {
        memcpy(matrixState, frames[i], 104);
        updateDisplay();
        delay(delay_ms);
    }
}
```

### Brightness Control

Some matrices support PWM brightness:

```cpp
// If supported by hardware
extern "C" void matrixSetBrightness(uint8_t level);  // 0-255
```

---

## Performance Considerations

### Update Frequency

The matrix can update very quickly:
- **Typical latency**: 20-50ms per LED toggle
- **Maximum update rate**: ~50 FPS for full frame updates
- **Network overhead**: Main bottleneck is HTTP request time

### Optimization Strategies

1. **Batch updates** - Send multiple LEDs at once:
```python
@app.route('/matrix/set_multiple', methods=['POST'])
def set_multiple_leds():
    leds = request.json.get('leds')  # [{x, y, state}, ...]
    for led in leds:
        Bridge.call("set_led", led['x'], led['y'], led['state'])
```

2. **Debouncing** - Prevent rapid-fire toggles:
```javascript
let lastToggle = 0;
const DEBOUNCE_MS = 50;

if (Date.now() - lastToggle > DEBOUNCE_MS) {
    toggleLED(x, y);
    lastToggle = Date.now();
}
```

3. **WebSocket alternative** - For real-time drawing:
```python
# Replace HTTP POST with WebSocket for lower latency
from flask_socketio import SocketIO
```

---

## Comparison with Individual LED Control

| Feature | Individual LEDs (arduino-led-webui) | LED Matrix (arduino-matrix-webui) |
|---------|-------------------------------------|-----------------------------------|
| **LED Count** | 6 RGB (18 total) | 104 monochrome |
| **Control Method** | Direct GPIO (`digitalWrite`) | Hardware matrix interface |
| **Data Format** | One pin per LED | Packed binary (4 × uint32_t) |
| **Use Case** | Status indicators, simple patterns | Graphics, text, visualization |
| **Update Speed** | Instant (microseconds) | Fast (milliseconds) |
| **Complexity** | Simple | Moderate (bit manipulation) |

---

## Running the Project

### Prerequisites

Same as [arduino-led-webui](../arduino-led-webui/BLOG.md#running-the-project) - Docker environment already configured.

### Build and Run

```bash
cd arduino-matrix-webui
docker build -t arduino-matrix-webui .
docker compose up
```

### Access the Interface

Open **http://localhost:8000** and start drawing!

**Try drawing:**
- A heart shape
- Your initials
- Simple patterns
- Animated sequences

---

## Key Takeaways

### What Makes This Different

1. **Coordinate-based control** - (x, y) addressing vs. pin numbers
2. **Bit-packing format** - Efficient binary representation
3. **Hardware abstraction** - `matrixWrite()` handles complexity
4. **Interactive canvas** - Real-time pixel art creation

### Skills Demonstrated

- **Binary data manipulation** - Bit shifting and masking
- **2D array management** - Coordinate transformations
- **Hardware interfaces** - Working with dedicated controllers
- **Interactive web UI** - Grid layouts and mouse events

### Learning Path

This project bridges the gap between:
- **Simple GPIO** (arduino-led-webui) → Individual pin control
- **LED Matrix** (this project) → Coordinate-based graphics
- **Advanced displays** (future) → Full-color TFT screens

---

## Next Steps

After mastering the LED matrix, explore:

1. **Animation engine** - Create smooth transitions
2. **Game development** - Build interactive LED games
3. **Sensor integration** - Display real-time data
4. **Multi-user drawing** - Collaborative pixel art

---

## Resources

- [Arduino Uno R4 User Manual (LED Matrix)](https://docs.arduino.cc/tutorials/uno-q/user-manual/)
- [Previous Tutorial: Individual LED Control](../arduino-led-webui/BLOG.md)
- [Arduino App Bricks Documentation](https://docs.arduino.cc/software/app-lab/tutorials/bricks/)

---

**Happy Drawing! 🎨**
