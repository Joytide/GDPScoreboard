//Challenge 2: PWM

//Pins: GND and 3.3 to the two top pins of the potentiometer
// A0 to bottom of potentiometer
// RX to TX of student's NodeMCU


// Student:
// GND to GND
// A0 to bottom of potentiometer
// TX to RX

const int analogInPin = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int value = analogRead(analogInPin);
  Serial.println("1#"+String(value)+"/");
  delay(200);
}
