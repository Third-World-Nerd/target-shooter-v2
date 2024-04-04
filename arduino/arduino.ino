#include <Servo.h>

// Define the servo objects
Servo servoX;
Servo servoY;

// Define the pulse width range for the servos (in microseconds)
const int minPulseWidth = 500; // 0.5 ms
const int maxPulseWidth = 2500; // 2.5 ms

// Define the pins for the servos
const int servoXPin = 5;
const int servoYPin = 6;
const int arcPin = 7;

void setup() {
  // Attach the servos to their respective pins
  servoX.attach(servoXPin);
  servoY.attach(servoYPin);
  pinMode(arcPin, OUTPUT);
  servoX.writeMicroseconds(minPulseWidth);
  servoY.writeMicroseconds(minPulseWidth);


  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the input from serial monitor
    int inputX = Serial.parseInt();
    int inputY = Serial.parseInt();
    int arc = Serial.parseInt();

    // Write the mapped values to the servos
    servoX.writeMicroseconds(inputX);
    servoY.writeMicroseconds(inputY);
    delay(1000);
    digitalWrite(arcPin, arc);
    delay(1000);
    digitalWrite(arcPin, LOW);
    // Serial.println(inputX);
    // Serial.println(inputY);
    // Serial.println(arc);
    Serial.read();
    }
}