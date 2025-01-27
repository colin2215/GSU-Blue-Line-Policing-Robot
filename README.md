# GSU-Blue-Line-Policing-Robot

Developed an autonomous robot designed for public safety applications, featuring planned path movement, object avoidance, and autonomous decision-making. The project combined hardware integration software development and computer vision to address real-world challenges.

---

## Features

- **Route Mapping & Navigation**: Utilizes the Google Maps API to define a safe path along sidewalks around Georgia State University Blue Line.
- **Proximity Detection**: Equipped with GoPiGo3 proximity sensors to detect and avoid obstacles, enabling seamless autonomous movement along the designated route.
- **Noise Detection**: A microphone monitors noise levels to detect abnormal sounds, such as shouting or crashing.
- **Vision-Based Detection**: Integrates a pre-trained violence detection model to identify violent behavior and potential weapons while live-streaming the feed.
- **Siren Activation**: When a threat is detected, the robot activates a siren light and emits a siren sound to alert people nearby.
- **Automated Notifications**: Sends an automatic email notification to designated recipients, providing real-time alerts about the detected threat.

---

## Hardware Requirements 

- **Raspberry Pi** (Raspberry Pi 3 Model B)
- **GoPiGo3** (Robotics Dev Kit)
- **Distance Sensor** (Measures distance between sensor and an object)
- **International Measurment Unit (IMU) Sensor** (Detects motion, orientation and position)
- **Sound Sensor** 
- **Camera Module** (for threat detection)
- **GoPiGo robot chasis** (Includes chasis, tires, motors)
- **Power Supply**
- **Micro SD Card** (for data storage)

---

## Software Requirements

- **Python 3.x**
- **Raspberry Pi OS** (Formerly Raspbian)
- `picamera`:For capturing images and video from the Raspberry Pi camera.
- `flask`:For creating the web application to stream video.
- `threading`:For handling multi-threading (this is part of Python's standard library).
- `smtplib & email.mime.text`:For sending emails (part of Python's standard library).
- `RPi.GPIO`:For interacting with the GPIO pins (for the sound sensor).
- `google-cloud-vision`:For interacting with the Google Cloud Vision API for SafeSearch detection.
- `time & datetime`:For managing time and timestamps (these are part of Python's standard library).
- `os`:For file and directory manipulation (part of Python's standard library).

Install missing packages using:
```bash
pip install flask google-cloud-vision RPi.GPIO picamera
```

 ---

 
