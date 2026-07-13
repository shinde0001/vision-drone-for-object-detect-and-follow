# Vision Drone - Target Follow

A standalone, offline-capable vision AI system for autonomous drone tracking. This software launches a physics simulation with custom targets, streams the drone's FPV camera using GStreamer, detects targets in real-time using YOLOv8 and OpenCV, and uses visual servoing via MAVSDK to follow the object.

## Features
- **Offline Capability**: All models (YOLOv8n) and dependencies are local. No internet required.
- **Custom Gazebo Environment**: Pre-configured world with 5 distinct targets (Person, Red Sphere, Blue Cube, Green Cone, Yellow Cylinder).
- **Computer Vision Pipeline**: Uses YOLOv8 for complex objects (e.g. Person, Car) and HSV color masking for fast geometric object tracking.
- **Web Dashboard**: Modern Glassmorphism UI showing live annotated video feed, MAVSDK telemetry, and flight controls.
- **Autonomous Follow**: PD-based visual servoing controller to keep the drone fixed on the target at a safe distance.

## Requirements
* Ubuntu / Linux with standard PX4 SITL toolchain installed (`~/PX4-Autopilot`).
* Gazebo 11 Classic
* ROS 2 Humble (optional, for dependencies)
* Python 3.10+
* GStreamer

## Setup & Running

**1. Launch Everything**
We have provided a unified script that safely cleans up any old running instances (Gazebo, PX4, and the Web Server) before launching both the simulation and the backend in a single terminal:
```bash
cd "/path/to/vision drone for object follow"
./start_all.sh
```

**2. Access the Dashboard**
Open your web browser and navigate to:
```
http://localhost:8080/
```

## How to Use
1. **Connect**: The dashboard will automatically connect via WebSockets.
2. **Arm & Takeoff**: Click `ARM`, then click `TAKEOFF (5m)`. The drone will launch and hover.
3. **Select Target**: Choose a target from the Target Selection grid (e.g., Red Sphere).
4. **Follow**: Click `▶ FOLLOW TARGET`. The drone will autonomously rotate and move towards the target based on the live computer vision feed.
5. **Land**: Click `⏹ STOP FOLLOW` and then `LAND` to safely return to the ground.

## Architecture
* `gazebo/`: Custom models and world files.
* `src/camera_stream.py`: GStreamer UDP feed capture.
* `src/detector.py`: YOLOv8 inference and OpenCV color filtering.
* `src/drone_controller.py`: MAVSDK abstraction for flight commands.
* `src/follower.py`: Visual servoing logic (PD controller).
* `web/`: FastAPI backend and HTML/CSS/JS frontend.
* `models/`: Bundled YOLO weights.
