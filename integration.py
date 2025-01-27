import logging
from flask import Flask, Response
import picamera
import threading
import os
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from io import BytesIO
from violenceDetection import detect_safesearch  # Import the violence detection function
import RPi.GPIO as GPIO  # Import GPIO for sound sensor

# Configure logging to append messages to activity_log.log
log_file = "activity_log.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(message)s'
)

# Disable Flask's default access log
flask_log = logging.getLogger('werkzeug')
flask_log.setLevel(logging.ERROR)  # Set to ERROR to suppress access logs

# Initialize Flask app and camera
app = Flask(__name__)
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24

# Shared variables
frame_lock = threading.Lock()
current_frame = None
flag_event = threading.Event()

# Create a directory to store frames
output_dir = "flagged_frames"
os.makedirs(output_dir, exist_ok=True)

# Sound sensor setup
SOUND_PIN = 19  # GPIO4 (Physical pin 35)
PIN1 = 4 # GPIO17 (Physical pin 7)
SMTP_SERVER = 'smtp.freesmtpservers.com'
SMTP_PORT = 25
FROM_EMAIL = 'eliastreadwayofficial@gmail.com'
TO_EMAIL = 'treadwaydesignsofficial@gmail.com'

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(SOUND_PIN, GPIO.IN) # Make input Pin
GPIO.setup(PIN1, GPIO.OUT, initial = GPIO.HIGH) # Initialize PIN1 as HIGH

def capture_frames():
    """Continuously captures frames from the Raspberry Pi camera."""
    global current_frame
    stream = BytesIO()
    for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
        with frame_lock:
            stream.seek(0)
            current_frame = stream.read()
        stream.seek(0)
        stream.truncate()
        
def send_email(msg):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        
        message = MIMEText(msg, 'plain')
        
        message['Subject'] = 'Violent Activity Warning'
        
        smtp.sendmail(FROM_EMAIL, TO_EMAIL, message.as_string())
        
        print("Email Sent")

def save_and_process_flagged_frames():
    """Waits for the 'flag' signal to capture, save, and process 10 frames."""
    while True:
        # Wait until the 'flag' event is triggered
        flag_event.wait()
        flag_event.clear()  # Reset the event after it's triggered

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print("Flag received. Capturing 10 frames starting at {}...".format(timestamp))

        frames = []
        # Capture 10 frames, 1 second apart
        for i in range(10):
            frame_name = "{}/frame_{}_{}.jpg".format(output_dir, timestamp, i + 1)
            with frame_lock:
                camera.capture(frame_name, format='jpeg')
            print("Saved: {}".format(frame_name))
            frames.append(frame_name)
            time.sleep(1)

        # Process the frames for violence detection
        violent_count = 0
        for frame in frames:
            result = detect_safesearch(frame)  # Call the detection function
            print("Frame {} detected as: {}".format(frame, result))  # Debugging output
            if result == "Violence":  # Increment count for violence frames
                violent_count += 1

        # Log message based on the result
        if violent_count >= 5:
            message = "Violent Activity detected on {} at {}".format(timestamp.split('_')[0], timestamp.split('_')[1])
            
            # Send Email
            send_email(message)
            
            print("flag2")
        else:
            message = "False Alarm, no Violent Activity detected on {} at {}".format(timestamp.split('_')[0], timestamp.split('_')[1])
            print("noFlag")

        # Log the message to the log file
        logging.info(message)
        print("Logged message: {}".format(message))

def generate_frames():
    """Generate frames for the live video feed."""
    global current_frame
    while True:
        with frame_lock:
            if current_frame is None:
                continue
            frame = current_frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video_feed():
    """Video streaming route. Accessible at /video."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def monitor_sound_sensor():
    while True:
        # Read Digital Pin State
        if GPIO.input(SOUND_PIN) == GPIO.HIGH:
            flag_event.set()
            print("Noise Detected")  # Output 'flag' for loud sound
            
            GPIO.output(PIN1, GPIO.LOW)  # Turn on the alarm
            print("SOUND ALARM")
            
            time.sleep(5)  # Alarm sound duration (5 seconds)
            
            GPIO.output(PIN1, GPIO.HIGH)  # Turn off the alarm
            print("QUIET ALARM")
            
            time.sleep(20)  # Wait 20 seconds before detecting sound again
        else:
            time.sleep(0.3)  # Continue checking every 300ms
            print("No Noise Detected")


if __name__ == "__main__":
    # Start the camera frame capture thread
    threading.Thread(target=capture_frames, daemon=True).start()

    # Start the flagged frame capture and processing thread
    threading.Thread(target=save_and_process_flagged_frames, daemon=True).start()

    # Start the sound sensor monitoring thread
    threading.Thread(target=monitor_sound_sensor, daemon=True).start()

    # Start the Flask app
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        camera.close()
        GPIO.cleanup()
