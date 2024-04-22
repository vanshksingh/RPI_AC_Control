
# Raspberry Pi Face Detection and Air Conditioner Control

![IMG_3418](https://github.com/vanshksingh/RPI_AC_Control/assets/114809624/355f19f1-f731-4b2b-97be-8632e7abe6ef)



This project integrates a Raspberry Pi camera with OpenCV for face detection and uses GPIO pins and an IR emitter to control an air conditioner based on the number of detected faces. The project consists of two main components: a Python script for face detection and an Arduino sketch for controlling the air conditioner.

## Prerequisites

1. **Hardware Requirements**
    - Raspberry Pi (e.g., Raspberry Pi 3, 4)
    - Raspberry Pi Camera Module
    - LCD Display
    - Infrared Emitter (IR LED)
    - IR Receiver (optional)
    - Air Conditioner with IR remote control compatibility
    - GPIO pins for controlling the air conditioner
    - Breadboard and jumper wires

2. **Software Requirements**
    - Python 3.x
    - OpenCV (cv2) library
    - RPi.GPIO library for controlling GPIO pins
    - `drivers` library for LCD control
    - Arduino IDE (for programming the Arduino)

## Installation

1. **Setting Up the Python Script**
    - Clone the repository to your Raspberry Pi.
    - Install the required Python libraries using:
      ```shell
      pip install opencv-python numpy RPi.GPIO
      ```

2. **Setting Up the Arduino**
    - Connect the IR emitter to the designated GPIO pin on the Raspberry Pi.
    - Use the Arduino IDE to upload the provided Arduino sketch to the microcontroller.
    - Connect the control pins to the appropriate GPIO pins on the Raspberry Pi.

3. **Configuring the Camera and LCD Display**
    - Ensure the Raspberry Pi camera is properly connected and enabled.
    - Connect the LCD display to the Raspberry Pi using the necessary pins.

## Usage

1. **Running the Python Script**
    - Run the Python script to start the face detection and air conditioner control:
      ```shell
      python3 script.py
      ```

2. **Configuring the Air Conditioner**
    - Modify the control pins and modes in the Arduino sketch as necessary.

3. **Operating**
    - The script will display the video feed with detected faces highlighted.
    - The number of faces and corresponding air conditioner settings will be displayed on the LCD.
    - The IR emitter will send commands to the air conditioner based on the number of detected faces.

## Troubleshooting

- Ensure all necessary connections (camera, LCD, GPIO pins) are properly secured.
- Check the installation of the required Python libraries.
- If the air conditioner does not respond, verify the IR emitter and its alignment with the air conditioner.

## Disclaimer

This project is intended for educational purposes. The code and configuration provided are not guaranteed to work with all hardware setups and air conditioner models. Please modify the code and circuit setup according to your specific needs and equipment.

---

This README provides an overview of the project, its prerequisites, installation instructions, and usage guidelines. Adjust the information as needed for your specific project and environment. Let me know if you need any more help.

![IMG_3696](https://github.com/vanshksingh/RPI_AC_Control/assets/114809624/990bd947-2244-4ada-b4dd-9287d6784f5c)

