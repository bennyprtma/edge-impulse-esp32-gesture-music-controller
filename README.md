# edge-impulse-esp32-gesture-music-controller
Hand gesture-based music controller using ESP32-CAM, Edge Impulse, Flask, and Python.
# ESP32 Hand Gesture Music Controller

A hand gesture-based music control system using ESP32-CAM,
Edge Impulse, Python, Flask, and Pygame.

The system recognizes hand gestures using an Edge Impulse
machine learning model deployed on ESP32. Detected gestures
are sent through HTTP to a Python Flask server, which controls
music playback on a computer.

## Overview

This project enables touchless music control using hand gestures.

The ESP32 camera captures hand images and performs machine
learning inference locally using an Edge Impulse model.

When a gesture is detected, ESP32 sends an HTTP POST request
to the Python server.

Supported commands:

- NEXT → Play the next track
- PREVIOUS → Play the previous track

## System Architecture

Hand Gesture
      ↓
ESP32 Camera
      ↓
Edge Impulse Model
      ↓
Gesture Classification
      ↓
HTTP POST Request
      ↓
Python Flask Server
      ↓
Pygame Music Player
      ↓
Next / Previous Track

## Hardware

- ESP32-CAM / XIAO ESP32-S3 Sense
- Camera module
- Computer or laptop
- Wi-Fi network
- USB cable

## Software

- Arduino IDE
- Edge Impulse Studio
- Python 3
- Flask
- Pygame
- Mutagen

## Machine Learning

The hand gesture recognition model was developed using
Edge Impulse Studio.

The workflow consists of:

1. Image acquisition
2. Image labeling
3. Impulse design
4. Image preprocessing
5. Feature generation
6. Object detection training
7. Model deployment as an Arduino library

The trained model is deployed to ESP32 for real-time
gesture recognition.

## ESP32 Setup

1. Install ESP32 board support in Arduino IDE.
2. Configure the appropriate camera model.
3. Install the Edge Impulse Arduino library.
4. Configure Wi-Fi credentials.
5. Configure the IP address of the computer running the server.
6. Upload the firmware to ESP32.
7. Open Serial Monitor at 115200 baud.

Example configuration:

```cpp
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverAddress = "YOUR_COMPUTER_IP";
const int serverPort = 5000;
