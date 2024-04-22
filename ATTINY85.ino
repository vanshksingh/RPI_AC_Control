#include <IRremote.h>
#include <MideaIR.h>

#define IR_EMITTER    1  // IR LED is connected to pin 1
#define CONTROL_PIN_3 3
#define CONTROL_PIN_4 4

// Create an IRsend object and a MideaIR object
IRsend irsend;
MideaIR remote_control(&irsend);

void setup() {
    pinMode(IR_EMITTER, OUTPUT);

    // Define control pins as inputs and enable pull-up resistors
    pinMode(CONTROL_PIN_3, INPUT_PULLUP);
    pinMode(CONTROL_PIN_4, INPUT_PULLUP);

    // Send air conditioner turn off command at startup
    remote_control.turnOFF();
    remote_control.emit();
}

void loop() {
  // Add a delay to prevent rapid IR transmissions
    delay(50000);
    // Read the current state of control pins
    int state_3 = digitalRead(CONTROL_PIN_3);
    int state_4 = digitalRead(CONTROL_PIN_4);

    // Control the air conditioner based on the current states of the control pins
    if (state_3 == LOW && state_4 == LOW) {
        // Both pins are LOW: turn off the air conditioner
        remote_control.turnOFF();
    } else {
        remote_control.turnON();
        remote_control.setMode(mode_cool);

        if (state_3 == HIGH && state_4 == LOW) {
            // Pin 3 HIGH and Pin 4 LOW: set temperature to 25°C
            remote_control.setTemperature(25);
        } else if (state_3 == LOW && state_4 == HIGH) {
            // Pin 3 LOW and Pin 4 HIGH: set temperature to 22°C
            remote_control.setTemperature(22);
        } else if (state_3 == HIGH && state_4 == HIGH) {
            // Both pins are HIGH: set temperature to 20°C
            remote_control.setTemperature(20);
        }
    }

    // Emit the IR command
    remote_control.emit();

    
}
