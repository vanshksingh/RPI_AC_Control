import cv2
import imutils
import numpy as np
import time
import requests

# Constants for ThingSpeak
WRITE_API = '90Z1CET44YNY08I0'  # PUT YOUR WRITE KEY HERE
BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API)

# Other constants
BG_UPDATE_INTERVAL = 60  # Update background every 60 seconds
CHANGE_THRESHOLD = 40    # Threshold for change in pixel intensities
MIN_CONTOUR_AREA = 1000  # Minimum contour area for person detection
DISTANCE_THRESHOLD = 100  # Distance threshold for person validation

class BackgroundUpdater:
    def __init__(self):
        self.last_update_time = time.time()

    def update(self, frame, bg_subtractor):
        current_time = time.time()
        if current_time - self.last_update_time >= BG_UPDATE_INTERVAL:
            bg_subtractor.apply(frame, learningRate=-1)  # Update the background model
            self.last_update_time = current_time

def detect_limb(frame):
    # Convert image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of skin color in HSV
    lower_skin = np.array([0, 48, 80], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Threshold the HSV image to get only skin color
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Convert to grayscale and blur the image
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image to get binary image
    _, thresh = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours
    for contour in contours:
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)

    return frame, contours

def validate_detection(face, limb_centroid):
    # Calculate distance between face centroid and limb centroid
    distance = np.linalg.norm(np.array([face[0] + face[2]//2, face[1] + face[3]//2]) - limb_centroid)
    return distance < DISTANCE_THRESHOLD  # Adjust the distance threshold as needed

def send_to_thingspeak(value):
    url = BASE_URL + "&field1={}".format(value)
    requests.get(url)

def detect(frame, HOGCV, face_cascade, bg_subtractor, bg_updater):
    # Background subtraction
    fg_mask = bg_subtractor.apply(frame)

    # Remove noise
    fg_mask = cv2.medianBlur(fg_mask, 5)

    # Calculate standard deviation of pixel intensities in the foreground mask
    std_dev = np.std(fg_mask)

    # Detect people
    bounding_box_cordinates, _ = HOGCV.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.03)
    persons = []

    for x, y, w, h in bounding_box_cordinates:
        if std_dev > CHANGE_THRESHOLD:
            # Filter out small contours
            if w * h > MIN_CONTOUR_AREA:
                persons.append((x, y, w, h))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Detect faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Detect limbs
    frame, contours = detect_limb(frame)

    # Validate people count
    validated_persons = 0
    for face in faces:
        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if validate_detection(face, (cX, cY)):
                    validated_persons += 1
                    break  # Move to the next face

    # Display total count
    cv2.putText(frame, 'Status : Detecting ', (40, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    cv2.putText(frame, f'Total Persons (HOG) : {len(bounding_box_cordinates)}', (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    cv2.putText(frame, f'Total Persons (Validated) : {validated_persons}', (40, 100), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)

    # Send the validated person count to ThingSpeak
    send_to_thingspeak(validated_persons)

    cv2.imshow('output', frame)

    return frame

def detectByCamera():
    HOGCV = cv2.HOGDescriptor()
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Load Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Background subtraction
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()
    bg_updater = BackgroundUpdater()

    video = cv2.VideoCapture(0)
    print('Detecting people, faces, and limbs...')
    start_time = time.time()
    while True:
        check, frame = video.read()
        if not check:
            break

        frame = imutils.resize(frame, width=min(800, frame.shape[1]))
        frame = detect(frame, HOGCV, face_cascade, bg_subtractor, bg_updater)

        elapsed_time = time.time() - start_time
        if elapsed_time >= 10:
            start_time = time.time()
            send_to_thingspeak(0)  # Reset the value after 10 seconds

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detectByCamera()
