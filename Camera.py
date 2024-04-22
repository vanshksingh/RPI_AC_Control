import time
import picamera
import io
import cv2
import numpy as np
import RPi.GPIO as GPIO
import math
# Import necessary libraries for communication and display use
import drivers
from time import sleep


display = drivers.Lcd()



# Load the pre-trained Haar cascade classifiers for frontal and profile face detection
frontal_face_cascade = cv2.CascadeClassifier('/home/vanshksingh/Downloads/haarcascade_frontalface_default.xml')
profile_face_cascade = cv2.CascadeClassifier('/home/vanshksingh/Downloads/haarcascade_profileface.xml')

# Create a stream object for the video capture
stream = io.BytesIO()

# Initialize OpenCV window
cv2.namedWindow('Video Feed', cv2.WINDOW_NORMAL)

# Initialize GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # GPIO pin for condition 1
GPIO.setup(18, GPIO.OUT)  # GPIO pin for condition 2

# Function to control GPIO pins based on the sum of face counts
def control_gpio_pins(frontal_count, profile_count):
    sum_faces = frontal_count + profile_count
    print("Total faces:", sum_faces)
    if sum_faces == 0:
        display.lcd_clear()
        display.lcd_backlight(0)
        display.lcd_display_string("Person Count :" + str(sum_faces), 1)   # Write line of text to first line of display
        display.lcd_display_string("AC Turned OFF", 2)
        sleep(1) 
        GPIO.output(17, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
    elif sum_faces == 1:
        display.lcd_clear()
        display.lcd_backlight(1)
        display.lcd_display_string("Person Count :" + str(sum_faces), 1)   # Write line of text to first line of display
        display.lcd_display_string("AC Set to 25", 2)
        sleep(1) 
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(18, GPIO.LOW)
    elif sum_faces <= 3:
        display.lcd_clear()
        display.lcd_backlight(1)
        display.lcd_display_string("Person Count :" + str(sum_faces), 1)   # Write line of text to first line of display
        display.lcd_display_string("AC Set to 22", 2)
        sleep(1) 
        GPIO.output(17, GPIO.LOW)
        GPIO.output(18, GPIO.HIGH)
    else sum_faces <= 5:
        display.lcd_clear()
        display.lcd_backlight(1)
        display.lcd_display_string("Person Count :" + str(sum_faces), 1)   # Write line of text to first line of display
        display.lcd_display_string("AC Set to 20", 2)
        sleep(1) 
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(18, GPIO.HIGH)

# Main loop
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    
    # Initialize variables for face count and time tracking
    frontal_face_count = 0
    profile_face_count = 0
    face_count_samples = 0
    start_time = time.time()
    
    # Continuously capture frames
    for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
        # Rewind the stream for reading
        stream.seek(0)
        
        # Convert the stream to OpenCV image format
        data = stream.getvalue()
        image = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
        
        # Convert the image to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect frontal faces in the image
        frontal_faces = frontal_face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Detect profile faces in the image
        profile_faces = profile_face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Update face counts
        frontal_face_count += len(frontal_faces)
        profile_face_count += len(profile_faces)
        face_count_samples += 1
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        # If 5 seconds have passed, report the average face counts and control GPIO pins
        if elapsed_time >= 5:
            frontal_face_average = math.ceil(frontal_face_count / face_count_samples)
            profile_face_average = math.ceil(profile_face_count / face_count_samples)
            print("Average frontal face count:", frontal_face_average)
            print("Average profile face count:", profile_face_average)
            control_gpio_pins(frontal_face_average, profile_face_average)
            
            # Reset variables
            frontal_face_count = 0
            profile_face_count = 0
            face_count_samples = 0
            start_time = time.time()
        
        # Draw rectangles around detected frontal faces
        for (x, y, w, h) in frontal_faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Draw rectangles around detected profile faces
        for (x, y, w, h) in profile_faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Display the image with face detection
        cv2.imshow('Video Feed', image)
        
        # Wait for 1 millisecond and check if the user pressed 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # Clear the stream in preparation for the next frame
        stream.seek(0)
        stream.truncate()
        
# Clean up GPIO
GPIO.cleanup()

# Clean up OpenCV
cv2.destroyAllWindows()
