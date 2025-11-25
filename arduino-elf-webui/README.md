# Arduino Elf Detector – Real-time Object Detection with Edge Impulse

This project demonstrates **real-time object detection on the Arduino Uno Q** using Edge Impulse AI. It runs a live camera feed with object detection inference directly on the device.

This is a fully self-contained Docker environment for running Edge Impulse object detection models on the Arduino Uno Q.

It includes:

- **Edge Impulse SDK** for running `.eim` models
- **OpenCV** for camera capture and video streaming
- **Flask web server** with real-time video feed
- **Python environment** with all necessary dependencies
- Support for USB cameras via `/dev/video0`

This allows you to run AI-powered object detection **from any machine** without installing dependencies locally.

---

## 🚀 Features

- **Real-time object detection** with Edge Impulse
- Live camera streaming with bounding boxes
- Color-coded confidence levels (pink → orange → yellow → blue → green)
- Automatic model detection (searches for `.eim` files)
- Dockerized environment with:
  - Automatic camera initialization
  - Flask web server on port 8000
  - Server-Sent Events for status updates
- Isolated environment with reproducible builds
- Compatible with Arduino Uno Q

---

## 📦 Requirements

- Docker
- USB camera connected to `/dev/video0`
- Access to GPIO chip devices (for board integration)
- Linux host (recommended)
- **Edge Impulse Model**: You must provide your own `model.eim` file (see below)

---

## � Edge Impulse Model Setup

This project requires an Edge Impulse object detection model. The model file is **not included** in this repository.

### Creating Your Own Model

1. **Create an Edge Impulse Account**: https://edgeimpulse.com/
2. **Create a New Project** for object detection (Image data, 224x224)
3. **Collect Image Samples**: Upload or capture images with objects to detect (e.g., "elf", "person")
4. **Configure Processing**: Use Image block with RGB color depth
5. **Train Your Model**: Use YOLOv5 (Pico model) - see `model.eim.example` for detailed settings
6. **Download the Model**:
   - Go to "Deployment" tab
   - Select **"Linux AARCH64"** (ARM64 architecture)
   - Download the `.eim` file
7. **Place the Model**: 
   - Rename it to `model.eim`
   - Place it in the `arduino-elf-webui/` directory

See `model.eim.example` for complete YOLOv5 configuration details.

---

## �🧱 Building the Docker Image

**Important**: Place your `model.eim` file in this directory before building!

```sh
export FACTORY=<My-Factory-Name>
docker build -t hub.foundries.io/${FACTORY}/arduino-elf-webui:latest .
```

---

## ▶️ Running the Container

### Using Docker Run

Run the container with the necessary devices:

```sh
docker run -it --privileged \
    --device /dev/video0 \
    --device /dev/gpiochip0 \
    --device /dev/gpiochip1 \
    --device /dev/gpiochip2 \
    --network host \
    -v /var/run/arduino-router.sock:/var/run/arduino-router.sock \
    hub.foundries.io/${FACTORY}/arduino-elf-webui:latest
```

### Using Docker Compose

Alternatively, use docker-compose for easier management:

```sh
docker compose up
```

**Note:** Docker Compose will automatically use `hub.foundries.io/${FACTORY}/arduino-elf-webui:latest` as defined in `docker-compose.yml`.

The container will:

1. **Detect the Edge Impulse model** (`.eim` file)
2. **Start the camera** on `/dev/video0`
3. **Launch Flask server** on port 8000
4. **Begin object detection** with bounding boxes

---

## 🌐 Accessing the Web Interface

Once the container is running, open your browser and navigate to:

```
http://<arduino-ip>:8000
```

You'll see:
- **Live camera feed** with real-time object detection
- **Bounding boxes** around detected objects
- **Color-coded confidence** levels
- **Automatic detection** running at ~10 FPS

---

## 🎯 How It Works

### Edge Impulse Model

The application uses an Edge Impulse model (`elf-on-the-shelf-linux-aarch64-v10.eim`) trained for object detection. The model:

- Processes camera frames at 16 kHz sampling
- Runs inference every 10th frame (optimized for performance)
- Outputs bounding boxes with confidence scores
- Color-codes results based on confidence:
  - 🟣 Pink: 0-20%
  - 🟠 Orange: 21-40%
  - 🟡 Yellow: 41-60%
  - 🔵 Light Blue: 61-80%
  - 🟢 Green: 81-100%

### Architecture

```
┌─────────────────────┐
│   Web Browser       │
│   Live Video Feed   │
└──────────┬──────────┘
           │ HTTP
           │
┌──────────▼──────────┐
│  Flask Server       │
│  - Video streaming  │
│  - SSE status       │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ Edge Impulse SDK    │
│ - Object detection  │
│ - Bounding boxes    │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  OpenCV Camera      │
│  /dev/video0        │
└─────────────────────┘
```

---

## 🔧 Configuration

### Environment Variables

You can customize the application behavior using environment variables in `docker-compose.yml`:

- `DEBUG`: Enable debug output (`0` or `1`)
- `MODEL_NAME`: Override default model filename
- `ASSETS_DIR`: Custom path for model files

### Custom Model

To use a different Edge Impulse model:

1. Export your model as **Linux (AARCH64)** from Edge Impulse Studio
2. Download the `.eim` file
3. Replace `elf-on-the-shelf-linux-aarch64-v10.eim` in the project directory
4. Rebuild the Docker image

Or mount it at runtime:

```sh
docker run ... \
    -v /path/to/your/model.eim:/var/local/assets/deployment.eim \
    hub.foundries.io/${FACTORY}/arduino-elf-webui:latest
```

---

## 🐛 Troubleshooting

### Camera Not Found

**Issue**: `Camera not available` or black screen

**Solutions**:
- Check camera connection: `ls -l /dev/video*`
- Verify camera works: `v4l2-ctl --list-devices`
- Ensure device is mapped in docker-compose.yml
- Try a different USB port

### Model Not Loading

**Issue**: `No .eim model found` or detection doesn't work

**Solutions**:
- Verify `.eim` file exists in the container
- Check file permissions: `ls -l /app/*.eim`
- Enable debug mode: `DEBUG=1` in docker-compose.yml
- Check logs: `docker logs <container-id>`

### Slow Detection

**Issue**: Low FPS or laggy video

**Solutions**:
- Detection runs every 10th frame by default (optimized)
- Check CPU usage on the board
- Reduce video resolution if needed
- Ensure no other heavy processes are running

### Port 8000 Already in Use

**Issue**: `Address already in use`

**Solutions**:
- Stop other applications using port 8000
- Change port in `main.py` or via command line argument
- Check running containers: `docker ps`

---

## 📚 Files

- **main.py** - Flask application with Edge Impulse integration
- **camera_server.py** - OpenCV camera capture module
- **index.html** - Web interface with live video stream
- **start.sh** - Container startup script
- **Dockerfile** - Container image definition
- **docker-compose.yml** - Docker Compose configuration
- **elf-on-the-shelf-linux-aarch64-v10.eim** - Edge Impulse model

---

## 🎓 Learn More

- [Edge Impulse Documentation](https://docs.edgeimpulse.com/)
- [Arduino Uno Q User Manual](https://docs.arduino.cc/tutorials/uno-q/user-manual/)
- [OpenCV Camera Capture](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 📝 License

This project is licensed under MPL-2.0.
