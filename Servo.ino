
// Code tp control the ac by directly manipulating the remote buttons using servos 








#include <Servo.h>

Servo STATES;
Servo TEMPS;



// Define control pins
#define CONTROL_PIN_3 3
#define CONTROL_PIN_4 4

// Variable to track the on/off state and temperature
bool acOn = false;
int temperature = 25; // Local temperature value (default)
int globalTemperature = 25; // Global temperature value (initially same as local)

// Function to handle turning the air conditioner on
void turnAirConditionerOn() {
    // Add your code to turn the air conditioner on
    Serial.println("Air conditioner is turned ON");
    STATES.write(40);
    delay(500);
    STATES.write(90);
    // Add the necessary actions to turn on the air conditioner here
}

// Function to handle turning the air conditioner off
void turnAirConditionerOff() {
    // Add your code to turn the air conditioner off
    Serial.println("Air conditioner is turned OFF");
    STATES.write(40);
    delay(500);
    STATES.write(90);
    // Add the necessary actions to turn off the air conditioner here
}

// Function to decrement the local temperature until it matches the global temperature
void decrementTemperatureToMatchGlobal() {
    while (temperature > globalTemperature) {
        // Decrement the local temperature by one degree
        temperature--;
        Serial.print("Temperature decreased to: ");
        Serial.println(temperature);
        TEMPS.write(40);
        // Add a delay to prevent rapid changes
        delay(500); // Adjust delay as needed
        TEMPS.write(90);
    }
}

// Function to increment the local temperature until it matches the global temperature
void incrementTemperatureToMatchGlobal() {
    while (temperature < globalTemperature) {
        // Increment the local temperature by one degree
        temperature++;
        Serial.print("Temperature increased to: ");
        Serial.println(temperature);
        TEMPS.write(140);
        // Add a delay to prevent rapid changes
        delay(500); // Adjust delay as needed
        TEMPS.write(90);
    }
}

void setup() {
    Serial.begin(9600);



    STATES.attach(9);
    TEMPS.attach(10);

    STATES.write(90);
    TEMPS.write(90);
    // Define control pins as inputs and enable pull-up resistors

    pinMode(CONTROL_PIN_3, INPUT_PULLUP);
    pinMode(CONTROL_PIN_4, INPUT_PULLUP);
}

void loop() {
    // Add a delay to prevent rapid state changes
    delay(100); // Adjust the delay as needed

    // Read the current state of control pins
    int state_3 = digitalRead(CONTROL_PIN_3);
    int state_4 = digitalRead(CONTROL_PIN_4);

    // Update the AC on/off state and temperature based on the states of control pins
    bool newAcOn = !(state_3 == LOW && state_4 == LOW);

    // Execute the appropriate function if the acOn state changes
    if (newAcOn != acOn) {
        if (newAcOn) {
            turnAirConditionerOn();
        } else {
            turnAirConditionerOff();
        }
        acOn = newAcOn;
    }

    // Set the global temperature based on the state of the control pins
    if (acOn) {
        if (state_3 == HIGH && state_4 == LOW) {
            // Pin 3 HIGH and Pin 4 LOW: set global temperature to 25°C
            globalTemperature = 22;
        } else if (state_3 == LOW && state_4 == HIGH) {
            // Pin 3 LOW and Pin 4 HIGH: set global temperature to 22°C
            globalTemperature = 25;
        } else if (state_3 == HIGH && state_4 == HIGH) {
            // Both pins HIGH: set global temperature to 20°C
            globalTemperature = 20;
        }
    }

    // Adjust the local temperature to match the global temperature if needed
    if (temperature > globalTemperature) {
        decrementTemperatureToMatchGlobal();
    } else if (temperature < globalTemperature) {
        incrementTemperatureToMatchGlobal();
    }

    // You can use the temperature variable in the rest of your program as needed
    Serial.print("Temperature: ");
    Serial.println(temperature);
}
