

from flask import Flask, Response
import picamera
import threading
import os
import time
from datetime import datetime
from io import BytesIO

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

def save_flagged_frames():
    """Waits for the 'flag' signal to capture and save 10 frames."""
    global camera
    while True:
        # Wait until the 'flag' event is triggered
        flag_event.wait()
        flag_event.clear()  # Reset the event after it's triggered

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print("Flag received. Capturing 10 frames starting at {}...".format(timestamp))

        # Capture 10 frames, 1 second apart
        for i in range(10):
            frame_name = "{}/frame_{}_{}.jpg".format(output_dir, timestamp, i + 1)
            with frame_lock:
                camera.capture(frame_name, format='jpeg')
            print("Saved: {}".format(frame_name))
            time.sleep(1)

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

def monitor_flag_input():
    """Monitors for the 'flag' input."""
    while True:
        user_input = input("Enter 'flag' to capture frames: ").strip().lower()
        if user_input == "flag":
            flag_event.set()

if __name__ == "__main__":
    # Start the camera frame capture thread
    threading.Thread(target=capture_frames, daemon=True).start()

    # Start the flagged frame capture thread
    threading.Thread(target=save_flagged_frames, daemon=True).start()

    # Start the flag input monitoring thread
    threading.Thread(target=monitor_flag_input, daemon=True).start()

    # Start the Flask app
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        camera.close()
