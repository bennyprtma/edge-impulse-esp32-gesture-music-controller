# ESP32 Hand Gesture Music Controller

A hand gesture-based music control system using ESP32-CAM, Edge Impulse, Python, Flask, and Pygame.

This project uses a camera-equipped ESP32 to recognize hand gestures using a machine learning model trained with Edge Impulse. The detected gesture is sent through an HTTP request to a Python Flask server, which controls music playback on a computer.

## Features

- Real-time hand gesture recognition
- Edge Impulse machine learning inference on ESP32
- Touchless music control
- Next track control
- Previous track control
- HTTP communication between ESP32 and computer
- Local Flask REST API
- MP3 playback using Pygame
- Configurable gesture confidence threshold
- Local Wi-Fi communication

## System Architecture

```text
Hand Gesture
     ↓
ESP32 Camera
     ↓
Edge Impulse Model
     ↓
Gesture Detection
     ↓
NEXT / PREVIOUS
     ↓
HTTP POST Request
     ↓
Python Flask Server
     ↓
Pygame
     ↓
Music Folder
```

The ESP32 captures an image from the camera and performs inference using the Edge Impulse model.

If the detected gesture exceeds the confidence threshold, the ESP32 sends a command to the Flask server.

The server then changes the currently playing music track.

## Supported Gestures

| Gesture | HTTP Command | Action |
|---|---|---|
| `NEXT` | `next` | Play next track |
| `PREVIOUS` | `previous` | Play previous track |
| `PREV` | `previous` | Play previous track |

The default confidence threshold is:

```text
0.50
```

## Technologies

- ESP32
- ESP32-CAM
- Arduino
- Edge Impulse
- TinyML
- Computer Vision
- Object Detection
- Python
- Flask
- Pygame
- Mutagen
- ArduinoJson
- HTTP REST API

## Hardware Requirements

- ESP32-CAM AI Thinker or compatible ESP32 camera board
- Camera module
- USB programmer or USB connection
- Computer or laptop
- Wi-Fi network

> The current firmware configuration uses `CAMERA_MODEL_AI_THINKER`. If another ESP32 camera board is used, the camera GPIO configuration must be adjusted.

## Software Requirements

Before running the project, install:

- Python 3
- Git
- Arduino IDE
- ESP32 Board Package
- ArduinoJson
- Edge Impulse Arduino Library

## Repository Structure

```text
esp32-hand-gesture-music-controller/
│
├── firmware/
│   └── gesture_controller.ino
│
├── server/
│   └── music_controller.py
│
├── edge-impulse/
│
├── music/
│
├── docs/
│
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

# Installation

## 1. Clone the Repository

Clone this repository:

```bash
git clone https://github.com/YOUR_USERNAME/esp32-hand-gesture-music-controller.git
```

Open the project directory:

```bash
cd esp32-hand-gesture-music-controller
```

Replace:

```text
YOUR_USERNAME
```

with your GitHub username.

## 2. Setup Python Environment

Check whether Python is installed:

```bash
python --version
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## 3. Install Python Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```txt
Flask
pygame
mutagen
```

## 4. Add Music Files

Create a folder named:

```text
music
```

Place your MP3 files inside the folder:

```text
music/
├── song1.mp3
├── song2.mp3
├── song3.mp3
└── song4.mp3
```

By default, the Python server reads music from:

```text
./music
```

You can also use another music folder using the `MUSIC_FOLDER` environment variable.

### Windows PowerShell

```powershell
$env:MUSIC_FOLDER="C:\Users\YourName\Music"
python server/music_controller.py
```

### Linux / macOS

```bash
export MUSIC_FOLDER="/home/username/Music"
python server/music_controller.py
```

## 5. Run the Python Server

Start the server:

```bash
python server/music_controller.py
```

Example output:

```text
Pygame mixer initialized successfully.
Loaded 3 MP3 files.
Server: http://192.168.1.10:5000
Gesture endpoint: http://192.168.1.10:5000/gesture
```

Take note of the IP address displayed by the server.

Example:

```text
192.168.1.10
```

This IP address will be used in the ESP32 firmware.

Keep the Python server running while using the gesture controller.

# Arduino Setup

## 6. Install ESP32 Board Package

Open Arduino IDE.

Install the ESP32 board package using Boards Manager.

After installation, select the appropriate board:

```text
Tools
→ Board
→ ESP32 Arduino
```

For an AI Thinker ESP32-CAM, select:

```text
AI Thinker ESP32-CAM
```

Also select the correct serial port:

```text
Tools
→ Port
```

## 7. Install ArduinoJson

Open:

```text
Sketch
→ Include Library
→ Manage Libraries
```

Search for:

```text
ArduinoJson
```

Install the library.

# Edge Impulse Setup

## 8. Prepare the Dataset

Capture hand gesture images using the ESP32 camera.

Create gesture classes such as:

```text
NEXT
PREVIOUS
```

Upload the images to Edge Impulse Studio.

## 9. Label the Dataset

Open:

```text
Data acquisition
```

Upload the images.

Then open:

```text
Labeling queue
```

Label each image according to its gesture.

Example:

```text
NEXT
PREVIOUS
```

## 10. Create the Impulse

Open:

```text
Impulse Design
→ Create Impulse
```

Configure the project for image processing and object detection.

The general workflow is:

```text
Image Data
     ↓
Image Processing
     ↓
Object Detection
```

Save the impulse.

## 11. Generate Features

Open the image processing section.

Select the appropriate image settings.

Generate the features:

```text
Generate Features
```

## 12. Train the Model

Open:

```text
Object Detection
```

Configure the training parameters.

Start training:

```text
Save & Train
```

Evaluate the model performance before deploying it to the ESP32.

## 13. Export the Edge Impulse Model

After training is complete, open:

```text
Deployment
```

Select:

```text
Arduino Library
```

Then click:

```text
Build
```

Download the generated `.zip` file.

## 14. Install Edge Impulse Library

Open Arduino IDE.

Select:

```text
Sketch
→ Include Library
→ Add .ZIP Library
```

Select the ZIP file generated by Edge Impulse.

The firmware currently uses:

```cpp
#include <GestureSpotifyControl_inferencing.h>
```

Make sure the generated Edge Impulse library contains this header.

If your generated library uses another name, for example:

```cpp
#include <HandGesture_inferencing.h>
```

change the include statement in:

```text
firmware/gesture_controller.ino
```

to match the generated Edge Impulse library.

# ESP32 Configuration

## 15. Configure Wi-Fi

Open:

```text
firmware/gesture_controller.ino
```

Find:

```cpp
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverAddress = "YOUR_PC_IP";
const int serverPort = 5000;
```

Replace the values with your configuration.

Example:

```cpp
const char* ssid = "MyWiFi";
const char* password = "MyWiFiPassword";
const char* serverAddress = "192.168.1.10";
const int serverPort = 5000;
```

The value of:

```cpp
serverAddress
```

must be the local IP address of the computer running:

```text
music_controller.py
```

The ESP32 and computer must be connected to the same Wi-Fi network.

> Never upload your real Wi-Fi password to a public GitHub repository.

## 16. Configure the Camera

The current firmware uses:

```cpp
#define CAMERA_MODEL_AI_THINKER
```

This configuration is intended for the AI Thinker ESP32-CAM.

If you use another ESP32 camera board, adjust the camera model and GPIO configuration according to your hardware.

## 17. Upload the Firmware

Open:

```text
firmware/gesture_controller.ino
```

Click:

```text
Verify
```

to compile the firmware.

If compilation succeeds, click:

```text
Upload
```

After uploading the firmware, open:

```text
Tools
→ Serial Monitor
```

Set the baud rate to:

```text
115200
```

A successful connection should display output similar to:

```text
Connecting to WiFi: MyWiFi
....
WiFi connected!
IP address: 192.168.1.20
Camera initialized
```

# Testing

## 18. Test the Flask Server

Run:

```bash
python server/music_controller.py
```

Then open:

```text
http://127.0.0.1:5000
```

or use the computer's local IP:

```text
http://192.168.1.10:5000
```

A successful response indicates that the music control server is running.

## 19. Test the API Manually

Before testing hand gesture recognition, test the Flask API directly.

### Next Track

Windows PowerShell:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:5000/gesture `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"gesture":"next"}'
```

Expected response:

```json
{
  "status": "success",
  "message": "Next track played."
}
```

### Previous Track

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:5000/gesture `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"gesture":"previous"}'
```

Expected response:

```json
{
  "status": "success",
  "message": "Previous track played."
}
```

# Running the Complete System

Run the system in the following order:

```text
1. Connect the computer to Wi-Fi

2. Run the Python Flask server

3. Get the computer local IP address

4. Configure the IP address in the ESP32 firmware

5. Upload the firmware to ESP32

6. ESP32 connects to Wi-Fi

7. Camera captures the hand gesture

8. Edge Impulse performs inference

9. Gesture is detected

10. ESP32 sends an HTTP request

11. Flask receives the command

12. Pygame changes the music track
```

The complete workflow is:

```text
Hand
 ↓
Camera
 ↓
ESP32
 ↓
Edge Impulse
 ↓
Gesture Detection
 ↓
HTTP JSON
 ↓
Flask Server
 ↓
Pygame
 ↓
MP3 Playback
```

# API Reference

## Server Status

### Request

```http
GET /
```

Example:

```text
http://192.168.1.10:5000/
```

## Gesture Control

### Endpoint

```http
POST /gesture
```

### Content Type

```http
Content-Type: application/json
```

### Next Track Request

```json
{
  "gesture": "next"
}
```

### Previous Track Request

```json
{
  "gesture": "previous"
}
```

## Available Commands

| Command | Action |
|---|---|
| `next` | Play next music track |
| `previous` | Play previous music track |

# How It Works

The ESP32 continuously captures images using its camera.

The image is processed by the Edge Impulse machine learning model.

The firmware checks the confidence score of the detected gesture.

The default threshold is:

```cpp
const float confidence_threshold = 0.50;
```

If the gesture is detected as:

```text
NEXT
```

the ESP32 sends:

```json
{
  "gesture": "next"
}
```

If the gesture is detected as:

```text
PREVIOUS
```

or:

```text
PREV
```

the ESP32 sends:

```json
{
  "gesture": "previous"
}
```

The request is sent to:

```text
http://COMPUTER_IP:5000/gesture
```

The Flask server receives the command and uses Pygame to change the music track.

# Troubleshooting

## ESP32 Cannot Connect to Wi-Fi

Check:

- Wi-Fi SSID
- Wi-Fi password
- Wi-Fi signal
- Network compatibility
- ESP32 and computer are on the same network

Check the Serial Monitor for connection information.

## ESP32 Cannot Reach the Flask Server

Make sure:

```text
serverAddress = computer local IP
serverPort = 5000
```

For example:

```cpp
const char* serverAddress = "192.168.1.10";
const int serverPort = 5000;
```

Also check the operating system firewall.

Allow Python or TCP port:

```text
5000
```

to communicate through the local network.

## Music Is Not Playing

Make sure:

- The `music` folder exists
- The folder contains `.mp3` files
- Pygame initialized successfully
- The computer has a working audio device
- The MP3 files are valid
- The correct `MUSIC_FOLDER` is configured

## Edge Impulse Header Not Found

If Arduino IDE displays:

```text
GestureSpotifyControl_inferencing.h:
No such file or directory
```

make sure the generated Edge Impulse Arduino library has been installed.

Open:

```text
Sketch
→ Include Library
→ Add .ZIP Library
```

and select the library generated by Edge Impulse.

Also verify that the header name matches the generated project.

## Camera Initialization Failed

If Serial Monitor displays:

```text
Camera init failed
```

check that the configured camera model matches the actual hardware.

For AI Thinker ESP32-CAM:

```cpp
#define CAMERA_MODEL_AI_THINKER
```

Using an incorrect GPIO configuration can prevent the camera from working.

## Low Gesture Detection Accuracy

If gestures are not detected correctly:

- Improve lighting conditions
- Keep the hand visible to the camera
- Add more training images
- Include different hand positions
- Include different backgrounds
- Retrain the Edge Impulse model
- Evaluate the confidence threshold

The default threshold is:

```text
0.50
```

# Security

Do not commit sensitive information to a public repository.

Do not upload:

```text
Wi-Fi passwords
API keys
Personal credentials
Private configuration files
Personal MP3 files
```

Use placeholders:

```cpp
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverAddress = "YOUR_PC_IP";
```

It is recommended to add sensitive files to:

```text
.gitignore
```

Example:

```gitignore
.env
secrets.h
__pycache__/
*.pyc
.venv/
venv/
.vscode/
.idea/
.DS_Store
Thumbs.db
*.mp3
*.wav
build/
dist/
```

# Future Development

Possible improvements include:

- Play and pause gesture
- Volume up gesture
- Volume down gesture
- More gesture classes
- Improved object detection accuracy
- Adjustable confidence threshold
- Web dashboard
- Music playlist management
- Automatic server discovery
- MQTT communication
- WebSocket communication
- Real-time monitoring
- Improved TinyML performance
- XIAO ESP32-S3 Sense support

# Authors

Developed by:

- Benny Pratama
- Baso Syarif
- Ahmad Firji Altra Zaki

# Third-Party Components

This project uses several open-source technologies and libraries, including:

- Edge Impulse
- Arduino ESP32 Core
- ArduinoJson
- Flask
- Pygame
- Mutagen

Parts of the ESP32 machine learning implementation are based on Edge Impulse Arduino examples. Their respective copyright and license notices remain applicable.

# License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for more information.

```text
MIT License

Copyright (c) 2026 Benny Pratama, Baso Syarif, Ahmad Firji Altra Zaki
```
