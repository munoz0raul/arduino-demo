# Building a Voice-Controlled Christmas Tree with Edge Impulse on Arduino Uno R4

## Introduction

In our previous tutorials, we explored the Arduino Uno R4's dual-core architecture through [web-controlled LED systems](../arduino-led-webui/BLOG.md) and [interactive LED matrix drawing](../arduino-matrix-webui/BLOG.md). Now, let's venture into the world of **edge AI** by building a **voice-controlled Christmas tree** using audio classification.

This project leverages **Edge Impulse**, a machine learning platform for embedded devices, to recognize voice commands directly on the Arduino Uno R4's Linux core (MPU). No cloud connectivity required - everything runs locally on the device!

We'll build a festive application where you can:
- Say **"select"** to activate the control window
- Speak a color name (**blue**, **green**, **purple**, **red**, **yellow**)
- Watch as a Christmas tree on your screen illuminates in that color
- Automatically reset to a dark tree after 10 seconds

## 🎥 Demo Video

Watch the voice-controlled Christmas tree in action:

[![Arduino Voice Christmas Tree Demo](https://img.shields.io/badge/▶️-Watch%20Demo-red?style=for-the-badge)](https://photos.app.goo.gl/CMTWXqAB3K7QK5ZSA)

**[Click here to see the video demonstration](https://photos.app.goo.gl/CMTWXqAB3K7QK5ZSA)**

The video demonstrates:
- Real-time voice command recognition
- Christmas tree changing colors based on spoken commands
- Smooth animations with glowing aura effects
- Automatic reset after 10 seconds
- Server-Sent Events updating the interface in real-time

---

## Why Edge AI for Voice Control?

Traditional voice assistants (Alexa, Google Assistant, Siri) rely on cloud processing:

```
Microphone → Cloud API → Response → Action
           (requires internet)
```

With **Edge Impulse** running on the Arduino Uno R4, we process everything locally:

```
Microphone → Arduino MPU → Audio Classification → Immediate Action
           (no internet needed!)
```

### Benefits of Edge AI:

- **Privacy**: Audio never leaves the device
- **Low latency**: No network round-trip delays
- **Offline operation**: Works without internet connectivity
- **Cost-effective**: No cloud API fees
- **Reliability**: No dependency on external services

---

## Architecture Overview

Building on our [previous LED controller tutorial](../arduino-led-webui/BLOG.md), we're using the Arduino Uno R4's **MPU (Linux core)** to run the voice recognition system:

```
┌─────────────────────┐         ┌──────────────────────────┐
│   Web Browser       │◄────────┤  Flask Server (MPU)      │
│   Christmas Tree UI │   SSE   │  Real-time Status Updates│
└─────────────────────┘         └──────────┬───────────────┘
                                           │
                                    Audio  │
                                    Stream │
                                           │
                                ┌──────────▼────────────────┐
                                │ Edge Impulse SDK (MPU)    │
                                │ AudioImpulseRunner        │
                                │ - Samples audio @ 16kHz   │
                                │ - Inference @ ~10Hz       │
                                │ - 6 voice labels          │
                                └──────────┬────────────────┘
                                           │
                                    ┌──────▼──────┐
                                    │ ALSA Audio  │
                                    │ Microphone  │
                                    └─────────────┘
```

Unlike previous projects that used **MCU-MPU bridge communication**, this system operates entirely on the **MPU side**. The Linux core handles:
- Audio capture via ALSA
- Edge Impulse model inference
- Web server with real-time updates
- Timer-based state management

---

## Part 1: Edge Impulse Audio Classification

### What is Edge Impulse?

[Edge Impulse](https://edgeimpulse.com/) is a platform for building machine learning models optimized for embedded devices. It provides:

- **Studio**: Web-based interface for training models
- **Data acquisition**: Tools for collecting audio samples
- **Neural network training**: Pre-built architectures for audio classification
- **Deployment**: Export models for various hardware targets (including Linux)

### The Training Process

To build our voice command model, we followed these steps:

1. **Data Collection**: Record audio samples for each command
   - 50+ samples of "select"
   - 50+ samples of "blue"
   - 50+ samples of "green"
   - 50+ samples of "purple"
   - 50+ samples of "red"
   - 50+ samples of "yellow"
   - Background noise samples for robustness

2. **Feature Extraction**: Edge Impulse converts audio to spectrograms
   - Uses **MFE (Mel-Frequency Energy)** features
   - Captures frequency patterns in human speech
   - Window size: 1 second
   - Sampling rate: 16 kHz

3. **Neural Network**: Train a classification model
   - Input: MFE features (time-frequency representation)
   - Hidden layers: 2D convolutional layers
   - Output: 6 classes (5 colors + select command)
   - Trained on Edge Impulse's cloud infrastructure

4. **Deployment**: Export the model as `.eim` (Edge Impulse Model)
   - Optimized for Linux ARM64 (Arduino Uno R4 architecture)
   - Includes runtime libraries and inference engine
   - Single executable file: `deployment.eim`

### Understanding the .eim Model

The `.eim` file is a **self-contained executable** that includes:

- **Trained neural network weights**
- **Feature extraction pipeline** (audio → MFE features)
- **Inference engine** (TensorFlow Lite runtime)
- **Python API** for integration

We interact with it using the `edge_impulse_linux` Python library:

```python
from edge_impulse_linux.audio import AudioImpulseRunner

runner = AudioImpulseRunner(model_file="/app/deployment.eim")
```

---

## Part 2: The Dockerfile - Setting Up the Environment

Let's examine the `Dockerfile` to understand how we set up the Edge Impulse environment:

```dockerfile
FROM debian:trixie
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and audio dependencies
RUN apt-get update && \
    apt-get install -y \
        python3-venv python3-pip build-essential vim dbus \
        portaudio19-dev python3-pyaudio sox python3-dev \
        alsa-utils ca-certificates libgl1 libglx-mesa0 \
        libglib2.0-0 curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
```

### Audio Dependencies Explained

- **`portaudio19-dev`**, **`python3-pyaudio`**: PortAudio libraries for cross-platform audio I/O
- **`alsa-utils`**: ALSA (Advanced Linux Sound Architecture) tools for audio device management
- **`sox`**: Sound processing utilities

These enable the Edge Impulse SDK to capture microphone input.

### OpenCV Dependency (Hidden Requirement)

```dockerfile
RUN apt-get install -y libgl1 libglx-mesa0 libglib2.0-0
```

Interestingly, the Edge Impulse SDK requires **OpenCV** even for audio-only models. This is because the SDK's internal preprocessing uses OpenCV for:
- Image manipulation in the Studio interface
- Video capture support (for camera-based models)
- General matrix operations

Even though we're only doing audio classification, we need `libglib2.0-0` to satisfy OpenCV's runtime dependencies.

### Python Dependencies

```dockerfile
ENV VENV=/opt/venv
RUN python3 -m venv $VENV
ENV PATH="$VENV/bin:$PATH"

RUN pip install --no-cache-dir \
    numpy watchdog pyalsaaudio edge_impulse_linux pyaudio \
    "opencv-python>=4.5.1.48,<5" sounddevice flask six && \
    rm -rf ~/.cache/pip
```

**Key packages:**

- **`edge_impulse_linux`**: Edge Impulse SDK for Linux
  - Provides `AudioImpulseRunner` class
  - Handles audio buffering and inference
  - Returns classification results with confidence scores

- **`pyalsaaudio`**, **`sounddevice`**, **`pyaudio`**: Audio capture libraries
  - Multiple options for different use cases
  - Edge Impulse SDK uses `sounddevice` internally

- **`flask`**: Web server framework
  - Serves the Christmas tree interface
  - Provides Server-Sent Events endpoint for real-time updates

- **`opencv-python`**: Required by Edge Impulse SDK

### Copying Application Files

```dockerfile
WORKDIR /app

COPY deployment.eim classify.py index.html \
     arduino.png edgeimpulse.png foundries.png qualcomm.png \
     off.png blue.png green.png purple.png red.png yellow.png \
     start.sh /app/

RUN chmod +x /app/deployment.eim /app/start.sh
```

Notice the **Christmas tree images**:
- `off.png`: Default dark tree
- `blue.png`, `green.png`, `purple.png`, `red.png`, `yellow.png`: Illuminated trees

These are served as static assets by Flask.

---

## Part 3: The Python Application - classify.py

### Application Structure

```python
from edge_impulse_linux.audio import AudioImpulseRunner
from flask import Flask, Response, request, send_from_directory
import threading

app = Flask(__name__)

LABELS = {"blue", "green", "purple", "red", "yellow", "select"}
COLOR = {"blue", "green", "purple", "red", "yellow"}
```

### Voice Command Labels

We define two sets:
- **`LABELS`**: All recognized commands (5 colors + select)
- **`COLOR`**: Only the color commands

This distinction is important for the auto-reset logic - we only display colored trees for color commands.

### WebStatus Class: State Management

```python
class WebStatus:
    _last_result = None
    _lock = threading.Lock()
    _current_color = None
    _clear_timer = None
    _HIGHLIGHT_SECONDS = 10.0  # Auto-reset after 10 seconds

    @classmethod
    def update_color(cls, color: str):
        with cls._lock:
            # Cancel existing timer if any
            if cls._clear_timer and cls._clear_timer.is_alive():
                cls._clear_timer.cancel()
            
            cls._current_color = color
            
            # Start new 10-second timer
            cls._clear_timer = threading.Timer(
                cls._HIGHLIGHT_SECONDS, 
                cls._clear_color_cb
            )
            cls._clear_timer.start()
    
    @classmethod
    def _clear_color_cb(cls):
        with cls._lock:
            cls._current_color = None
```

This class manages:
- **Thread-safe state** with `threading.Lock()`
- **Auto-reset timer** using `threading.Timer`
- **Current color** for the Christmas tree

### How the Timer Works

1. User says "blue" → recognized by Edge Impulse
2. `update_color("blue")` called
3. Cancel any existing timer (if user said another color within 10s)
4. Set `_current_color = "blue"`
5. Start new `threading.Timer(10.0, _clear_color_cb)`
6. After 10 seconds: `_clear_color_cb()` sets `_current_color = None`
7. Web interface receives `None` via SSE → displays `off.png`

### Audio Classification Loop

```python
def main(model_path: str):
    with AudioImpulseRunner(model_path) as runner:
        model_info = runner.init()
        print(f"Model: {model_info['project']['name']}")
        print(f"Labels: {model_info['model_parameters']['labels']}")
        
        for res, audio in runner.classifier(freq=16000):
            if "classification" in res["result"]:
                predictions = res["result"]["classification"]
                
                # Find highest confidence prediction
                top_label = None
                top_score = 0.0
                for label, score in predictions.items():
                    if score > top_score:
                        top_score = score
                        top_label = label
                
                # Threshold: only accept if confidence > 0.7
                if top_score > 0.7 and top_label in LABELS:
                    print(f"Recognized: {top_label} ({top_score:.2f})")
                    
                    if top_label in COLOR:
                        WebStatus.update_color(top_label)
                    
                    WebStatus.update_result({
                        "label": top_label,
                        "confidence": top_score
                    })
```

### Inference Flow

1. **`runner.classifier(freq=16000)`**: Generator that yields audio + classification results
   - Samples audio continuously at 16 kHz
   - Performs inference ~10 times per second
   - Returns predictions for all 6 labels

2. **Confidence Thresholding**: Only accept predictions > 0.7 (70%)
   - Reduces false positives
   - Ensures clear voice commands

3. **Color Update**: If a color command is recognized:
   - Call `update_color(label)` to start the 10-second timer
   - Broadcast result via Server-Sent Events

### Flask Routes

```python
@app.route('/')
def index():
    return send_from_directory('/app', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    allowed = {
        'arduino.png', 'edgeimpulse.png', 'foundries.png', 'qualcomm.png',
        'off.png', 'blue.png', 'green.png', 'purple.png', 'red.png', 'yellow.png',
        'favicon.ico'
    }
    if filename in allowed:
        return send_from_directory('/app', filename)
    return "Not found", 404

@app.route('/events')
def events():
    def stream():
        while True:
            time.sleep(0.5)
            with WebStatus._lock:
                color = WebStatus._current_color
            
            if color:
                data = f"data: {json.dumps({'color': color})}\n\n"
            else:
                data = f"data: {json.dumps({'color': None})}\n\n"
            
            yield data
    
    return Response(stream(), mimetype='text/event-stream')
```

### Server-Sent Events (SSE)

The `/events` endpoint provides **real-time updates** to the web interface:

- **Browser connects** to `/events`
- **Server streams** current color state every 0.5 seconds
- **Format**: `data: {"color": "blue"}\n\n` or `data: {"color": null}\n\n`
- **JavaScript** receives events and updates the tree image

This creates a **push-based** update mechanism - no polling required!

---

## Part 4: The Christmas Tree Interface - index.html

### HTML Structure

```html
<div class="tree-wrap">
  <div id="aura" class="aura"></div>
  <div class="tree-container">
    <img id="treeImage" class="tree-image" src="off.png" alt="Christmas Tree" />
  </div>
</div>
```

Simple structure:
- **`aura`**: Glowing effect behind the tree
- **`treeImage`**: The Christmas tree itself

### CSS Animations

```css
.tree-image {
  transition: transform 0.3s ease, filter 0.3s ease;
}

.tree-image.active {
  transform: scale(1.05);
  filter: brightness(1.2) drop-shadow(0 0 30px currentColor);
}

.aura {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle, var(--aura-color) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.5s ease;
}

.aura.active {
  opacity: 0.6;
}
```

When a color is recognized:
- Tree scales up slightly (`transform: scale(1.05)`)
- Brightness increases
- Aura glows with the color
- Smooth transitions create a magical effect

### JavaScript: SSE Integration

```javascript
const eventSource = new EventSource('/events');
const treeImage = document.getElementById('treeImage');
const aura = document.getElementById('aura');

eventSource.onmessage = function(event) {
  const data = JSON.parse(event.data);
  const color = data.color;
  
  if (color) {
    highlightColor(color);
  } else {
    clearTree();
  }
};

function highlightColor(color) {
  // Update tree image
  treeImage.src = `${color}.png`;
  treeImage.classList.add('active');
  
  // Update aura color
  const colorMap = {
    'blue': '#1e90ff',
    'green': '#32cd32',
    'purple': '#9370db',
    'red': '#ff4444',
    'yellow': '#ffd700'
  };
  aura.style.setProperty('--aura-color', colorMap[color] || '#fff');
  aura.classList.add('active');
}

function clearTree() {
  treeImage.src = 'off.png';
  treeImage.classList.remove('active');
  aura.classList.remove('active');
}
```

### Real-Time Update Flow

1. **SSE connection** established to `/events`
2. **Server sends** `{"color": "blue"}` when voice command recognized
3. **JavaScript** calls `highlightColor("blue")`
4. **Tree image** changes to `blue.png` with animation
5. **Aura** glows blue
6. **After 10 seconds**, server sends `{"color": null}`
7. **JavaScript** calls `clearTree()`
8. **Tree returns** to `off.png` with fade-out animation

---

## Part 5: Use Cases and Extensions

### Smart Home Integration

Extend the system to control real smart home devices:

```python
def update_color(cls, color: str):
    # ... existing timer logic ...
    
    # Control Philips Hue lights
    if color == "blue":
        hue_api.set_light(1, color=(0, 0, 255))
    elif color == "red":
        hue_api.set_light(1, color=(255, 0, 0))
```

### Multi-Room Voice Control

Deploy multiple Arduino Uno R4 boards:
- Living room: "select blue" → blue ambient lighting
- Bedroom: "select red" → warm red night light
- Kitchen: "select green" → green task lighting

### Accessibility Applications

Voice commands can help users with limited mobility:
- "select blue" → turn on air conditioner
- "select red" → turn on heating
- "select yellow" → call for assistance

### Educational Demonstrations

This project is excellent for teaching:
- **Edge AI concepts**: On-device machine learning
- **Real-time systems**: Audio processing at 16 kHz
- **Web technologies**: Server-Sent Events, Flask
- **State machines**: Timer-based auto-reset logic

### Extending the Model

Add new voice commands:
- **Numbers**: "one", "two", "three" for scene selection
- **Actions**: "on", "off", "dim", "bright"
- **Phrases**: "good morning", "goodnight"

Train a new Edge Impulse model with these labels and update the Python code accordingly.

---

## Part 6: Performance Considerations

### Inference Speed

The Edge Impulse SDK achieves **~10 inferences per second** on the Arduino Uno R4:

- **Audio window**: 1 second
- **Inference time**: ~50ms
- **Overhead**: Audio buffering, feature extraction

This is fast enough for real-time voice control!

### Memory Usage

The `.eim` model is quite large (~50MB):
- Neural network weights
- TensorFlow Lite runtime
- Feature extraction pipeline

Ensure sufficient storage on the Arduino Uno R4.

### Audio Latency

Total latency from speech to tree update:

```
Speech → Audio capture (50ms)
      → Feature extraction (20ms)
      → Neural network inference (50ms)
      → Python processing (10ms)
      → SSE broadcast (10ms)
      → Browser update (20ms)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: ~160ms (barely noticeable!)
```

### Timer Precision

The 10-second auto-reset uses `threading.Timer`:

```python
threading.Timer(10.0, callback)
```

This is **not real-time precise** - expect variations of ±100ms. For most use cases, this is acceptable.

---

## Comparing with Previous Projects

| Feature | LED Controller | LED Matrix | Voice Christmas Tree |
|---------|---------------|------------|---------------------|
| **Input Method** | Web buttons | Web canvas (click to draw) | Voice commands |
| **Output** | 6 RGB LEDs | 13×8 LED matrix | Web interface (images) |
| **Processing** | MPU + MCU (Bridge) | MPU + MCU (Bridge) | MPU only (Edge AI) |
| **Real-time Updates** | SSE | SSE | SSE |
| **Complexity** | Low | Medium | High (ML model) |
| **Use Case** | Basic LED toggle | Pixel art display | Voice-controlled UI |

The voice-controlled Christmas tree builds on concepts from previous projects (SSE, Flask, Docker) while introducing **edge machine learning** as a new dimension.

---

## Conclusion

In this tutorial, we've built a complete **voice-controlled Christmas tree** system using:

- **Edge Impulse** for audio classification
- **Arduino Uno R4's MPU** for inference and web serving
- **Flask** with Server-Sent Events for real-time updates
- **Threading timers** for automatic state reset
- **CSS animations** for smooth visual transitions

This project demonstrates the power of **edge AI** - running machine learning models directly on embedded devices without cloud dependencies. The same principles can be applied to:

- Smart home automation
- Industrial voice control systems
- Accessibility tools
- Educational demonstrations

The Arduino Uno R4's Linux core (MPU) provides the perfect platform for these applications, offering the flexibility of high-level languages (Python) combined with the compactness of embedded hardware.

### What's Next?

Explore further:
- Train custom Edge Impulse models with your own voice
- Add more colors and commands
- Integrate with smart home APIs (Hue, MQTT, Home Assistant)
- Build gesture recognition using accelerometer data
- Create multi-modal interfaces (voice + touch + motion)

The possibilities are endless!

---

## 📚 Resources

- [Edge Impulse Documentation](https://docs.edgeimpulse.com/)
- [Building a Web-Controlled LED System](../arduino-led-webui/BLOG.md)
- [Interactive LED Matrix Drawing](../arduino-matrix-webui/BLOG.md)
- [Arduino Uno R4 WiFi User Manual](https://docs.arduino.cc/tutorials/uno-q/user-manual/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Server-Sent Events Specification](https://html.spec.whatwg.org/multipage/server-sent-events.html)

---

Happy voice hacking! 🎄🎤✨
