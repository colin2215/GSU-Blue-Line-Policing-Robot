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

## Setup Instructions

1. **Hardware Configuration**:
   - Connect the Raspberry Pi Camera Module and ensure it's working.
   - Connect the sound sensor to GPIO pins, with SOUND_PIN connected to GPIO 19 (or another GPIO pin based on your preference).

2. **Set Up Email Server (Optional)**:
   - Edit the `FROM_EMAIL`, `TO_EMAIL`, `SMTP_SERVER`, and `SMTP_PORT` in the script to match your email server settings.

---

## Project Workflow

1. **Camera Capture (capture_frames)**:
   - The camera module captures continuous frames at 640x480 resolution.
   - Frames are stored in the current_frame variable for the live video feed.

2. **Sound Sensor Monitoring (monitor_sound_sensor)**:
   - Continuously monitors the sound sensor connected to the Raspberry Pi GPIO pin.
   - If a loud sound (above a threshold) is detected, a flag event is triggered, and an alarm is activated.

3. **Flag Event Processing (save_and_process_flagged_frames)**:
   - When the flag_event is triggered by a sound sensor input, the system saves 10 frames over 10 seconds and processes them.
   - The frames are sent to the Google Cloud Vision API for detection of violent content.
   - If violence is detected in 5 or more frames, an email alert is sent.

4. **Video Streaming (video_feed)**:
   - A Flask-based web server serves the video stream at /video in real-time.

5. **Email Notification (send_email)**:
   - If violence is detected, an email is sent to notify the specified recipient.

---

## Outputs

1. **Real-Time Video Feed**:
   - The /video endpoint provides a real-time video stream of the Raspberry Pi camera. You can access it via a web browser (e.g., http://<raspberry-pi-ip>:5000/video).
2. **Logs**:
   - The system logs every flag event, including detection results, in the activity_log.log file.
     The log will contain information like:
        - Time of detection
        - Whether violent content was detected
        - Any email alerts sent
3. **Sound Sensor Detection**:
   - The system will print to the terminal whenever noise is detected by the sensor, with messages such as:
        - Noise Detected
        - SOUND ALARM
        - No Noise Detected
4. **Violence Detection**:
   - The system prints the results of violence detection for each frame:
        - Frame <frame_name> detected as: Violence
        - Frame <frame_name> detected as: No Violence
   - If violence is detected in enough frames (e.g., 5 or more), the system sends an email with a warning message. 
6. **Email Alert**:
   - If violence is detected, the system sends an email with the subject "Violent Activity Warning" and a message indicating the detection time and severity.

---

## Acknowledements

I would like to express my gratitude to everyone who contributed to the successful completion of this project:
- **Open-Source Communities**: For developing and maintaining the libraries and tools used in this project, including Raspberry Pi, GoPiGo, Flask, RPi.GPIO, picamera, and Google Cloud Vision.
- **Collaborators**: For their support and contributions to brainstorming, troubleshooting, and refining the implementation.


