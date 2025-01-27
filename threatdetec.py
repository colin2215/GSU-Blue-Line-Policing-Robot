import picamera
from google.cloud import vision
from google.cloud.vision import types

# Initialize the Vision API client
client = vision.ImageAnnotatorClient()

# Path to save the captured image
image = 'image.jpg'

def takephoto():
    """Captures an image using the Raspberry Pi camera."""
    camera = picamera.PiCamera()
    camera.capture(image)

def detect_safesearch(image_path):
    """Uses SafeSearch to detect violent or inappropriate content in an image."""
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Use types.Image to create the vision image
    vision_image = types.Image(content=content)

    # Perform SafeSearch detection
    response = client.safe_search_detection(image=vision_image)
    safe_search = response.safe_search_annotation

    if not safe_search:
        print("SafeSearch results are not available.")
        return

    # Check for violence or racy content
    is_violent = (safe_search.violence in (3, 4, 5)) or (safe_search.racy in (3, 4, 5))

    # Output only Violence or Nonviolence
    if is_violent:
        return "Violence"
    else:
        return "Nonviolence"

def main():
    global image
    takephoto()  # First, take a picture
    detect_safesearch(image)  # Then, analyze the image using SafeSearch

if __name__ == '__main__':
    main()
