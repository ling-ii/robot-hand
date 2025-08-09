#include <Arduino.h>
#include <Servo.h>

// Global variables
uint8_t controlPin_1 = 2;
uint8_t controlPin_2 = 3;
Servo servo_1 = Servo();
Servo servo_2 = Servo();

const float alpha = 0.2;
float smoothedAngle_1 = 0.;
float smoothedAngle_2 = 0.;

unsigned long lastUpdate = 0;
const unsigned long updateInterval = 30;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Attach the servo to the control pin
  servo_1.attach(controlPin_1);
  servo_2.attach(controlPin_2);

  // Set initial position of the servo
  servo_1.write(0);
  servo_2.write(0);
  delay(100);
}

void loop() {

    // Tweak update interval for responsiveness
    unsigned long now = millis();
    if (now - lastUpdate >= updateInterval) {
      lastUpdate = now;
      if (Serial.available() >= 2) {
        
        // Reading position from serial input
        uint8_t servoPosition_1 = Serial.read();
        uint8_t servoPosition_2 = Serial.read();
        
        smoothedAngle_1 = uint8_t(alpha * servoPosition_1 + (1 - alpha) * smoothedAngle_1);
        smoothedAngle_2 = uint8_t(alpha * servoPosition_2 + (1 - alpha) * smoothedAngle_2);
        
        if (smoothedAngle_1 >= 90) smoothedAngle_1 = 90;
        if (smoothedAngle_2 >= 90) smoothedAngle_2 = 90;

        // Actuate servo
        servo_1.write(smoothedAngle_1);
        servo_2.write(smoothedAngle_2);
      }
    }
}