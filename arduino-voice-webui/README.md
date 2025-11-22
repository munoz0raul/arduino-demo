# Arduino Voice-Controlled Christmas Tree

**📖 [Read the full blog post: Building a Voice-Controlled Christmas Tree with Edge Impulse](./BLOG.md)**

This project demonstrates **voice-controlled Christmas tree visualization** on the Arduino Uno Q. Using Edge Impulse's audio classification model, the system recognizes voice commands and displays a corresponding colored Christmas tree on a web interface. Say "select" to open the control window, then speak a color name to light up the tree!

This is a fully self-contained Docker environment for running **Edge Impulse audio classification** on the **Arduino Uno Q (MPU)**.

It includes:

- **Edge Impulse Linux SDK** for real-time audio classification
- **Pre-trained audio model** (`deployment.eim`) for voice command recognition
- **Flask web server** with real-time updates via Server-Sent Events
- **Interactive Christmas tree interface** with color animations
- **Auto-reset timer** (10 seconds) for automatic state cleanup
- **Python environment** with audio processing libraries

This allows you to run voice recognition **directly on the Arduino Uno Q's Linux core (MPU)** without external cloud services or internet connectivity.

---

## 🚀 Features

- **Voice command recognition** using Edge Impulse
- Recognized commands:
  - **select** - Opens the control window
  - **blue** - Displays blue Christmas tree
  - **green** - Displays green Christmas tree
  - **purple** - Displays purple Christmas tree
  - **red** - Displays red Christmas tree
  - **yellow** - Displays yellow Christmas tree
- **Real-time web interface** with animated Christmas tree
- **Automatic state reset** after 10 seconds of inactivity
- **Server-Sent Events (SSE)** for live status updates
- **Edge Impulse integration** for on-device audio classification
- Dockerized environment with:
  - Flask web server on port 5000
  - Audio input via ALSA
  - Real-time classification at ~10Hz
- Isolated environment with reproducible builds
- No internet required for inference (model runs locally)

---

## 📦 Requirements

- Docker
- Arduino Uno Q with audio input capability
- Microphone connected to ALSA audio device
- Linux host (recommended for audio device access)

---

## 🧱 Building the Docker Image

```sh
docker build -t arduino-voice-webui .
```

---

## ▶️ Running the Container

### Using Docker Run

Run the container with audio device access:

```sh
docker run -it --rm \
    --device /dev/snd \
    -p 5000:5000 \
    arduino-voice-webui
```

### Using Docker Compose

Alternatively, use docker-compose for easier management:

```sh
docker compose up
```

The container will:

1. Load the Edge Impulse model:

```sh
/opt/venv/bin/python3 /app/classify.py /app/deployment.eim
```

2. Start audio classification (continuous inference at ~10Hz)

3. Launch Flask web server on port 5000

4. Serve the Christmas tree interface at `http://<arduino-ip>:5000`

---

## 🎄 How It Works

### Voice Recognition Workflow

1. **Listening State**: The system continuously monitors audio input
2. **"Select" Command**: User says "select" to activate the interface
3. **Color Recognition**: User says a color name (blue, green, purple, red, yellow)
4. **Tree Display**: The corresponding colored Christmas tree appears on screen
5. **Auto-Reset**: After 10 seconds of inactivity, the tree returns to the "off" state

### Christmas Tree Interface

The web interface displays different Christmas tree images based on voice commands:

- **off.png** - Default state (dark tree)
- **blue.png** - Blue illuminated tree
- **green.png** - Green illuminated tree
- **purple.png** - Purple illuminated tree
- **red.png** - Red illuminated tree
- **yellow.png** - Yellow illuminated tree

Each color change includes a smooth animation with a glowing aura effect.

### Edge Impulse Audio Classification

The system uses Edge Impulse's `AudioImpulseRunner` to perform real-time audio classification:

- **Sampling Rate**: 16 kHz
- **Window Size**: ~1 second
- **Inference Frequency**: ~10 Hz (10 predictions per second)
- **Labels**: 6 voice commands (blue, green, purple, red, yellow, select)
- **Model Format**: `.eim` (Edge Impulse Model) compiled for Linux

When a voice command is recognized with sufficient confidence, the system:
1. Broadcasts the classification result via Server-Sent Events
2. Updates the web interface to display the corresponding tree image
3. Starts a 10-second timer to automatically reset to the "off" state

---

## 🌐 Web Interface

Access the interface by navigating to:

```
http://<arduino-ip>:5000
```

Replace `<arduino-ip>` with your Arduino Uno Q's IP address.

The interface includes:
- Real-time status display showing the last recognized command
- Animated Christmas tree that changes color based on voice input
- Glowing aura effect synchronized with tree state
- Automatic refresh via Server-Sent Events

---

## 🎨 Customization

### Changing the Auto-Reset Timer

Edit `classify.py` and modify the `_HIGHLIGHT_SECONDS` constant:

```python
class WebStatus:
    _HIGHLIGHT_SECONDS = 10.0  # Change to desired timeout in seconds
```

### Using a Custom Edge Impulse Model

1. Train your model on [Edge Impulse](https://edgeimpulse.com/)
2. Download the `.eim` Linux model file
3. Replace `deployment.eim` in the container:

```sh
docker run -it --rm \
    --device /dev/snd \
    -p 5000:5000 \
    -v /path/to/your-model.eim:/app/deployment.eim \
    arduino-voice-webui
```

Or mount via the assets directory:

```sh
docker run -it --rm \
    --device /dev/snd \
    -p 5000:5000 \
    -v /path/to/models:/var/local/assets \
    -e MODEL_NAME=your-model.eim \
    arduino-voice-webui
```

### Adding New Colors

To add new voice commands and tree colors:

1. Train the model with additional labels in Edge Impulse
2. Add new tree images (e.g., `orange.png`, `pink.png`)
3. Update `classify.py`:
   ```python
   LABELS = {"blue", "green", "purple", "red", "yellow", "select", "orange", "pink"}
   COLOR = {"blue", "green", "purple", "red", "yellow", "orange", "pink"}
   ```
4. Add images to `Dockerfile` COPY command and allowed static files list
5. Rebuild the container

---

## 🔧 Troubleshooting

### No audio input detected

Check that your microphone is connected and recognized by ALSA:

```sh
arecord -l
```

You should see your audio device listed.

### Model not found error

Ensure the `.eim` file is in the correct location:

```sh
ls -lh /app/deployment.eim
```

The file should be executable (`chmod +x deployment.eim` is applied automatically).

### Web interface not loading

Verify the Flask server is running:

```sh
docker logs <container-id>
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### Classification not working

Check the Edge Impulse runner output for errors:

```sh
docker logs -f <container-id>
```

Look for inference results like:
```
Predictions:
  blue: 0.95
  green: 0.02
  ...
```

---

## 📚 Learn More

- [Edge Impulse Documentation](https://docs.edgeimpulse.com/)
- [Arduino Uno R4 WiFi User Manual](https://docs.arduino.cc/tutorials/uno-q/user-manual/)
- [Building a Web-Controlled LED System](../arduino-led-webui/BLOG.md) - Introduction to MPU-MCU architecture
- [Interactive LED Matrix Drawing](../arduino-matrix-webui/BLOG.md) - Web-based LED matrix control

---

## 🎥 Demo

Watch the voice-controlled Christmas tree in action:

**[Video Demonstration](https://photos.app.goo.gl/CMTWXqAB3K7QK5ZSA)**

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 🤝 Credits

- **Edge Impulse** - Audio classification platform
- **Arduino** - Uno Q hardware
- **Flask** - Python web framework
- **Foundries.io** - Linux environment for Arduino Uno Q
