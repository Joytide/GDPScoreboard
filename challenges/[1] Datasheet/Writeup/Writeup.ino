char s[10];

void setup() {
  Serial.begin(9600);
}

// Connecter GND sur GND
// D4 (TXD1) du broadcaster sur notre RX (RXD0) (Transmitter vers Receiver), qui est l'entré RX par défaut lorsqu'on initialise un Serial


void loop() {
  Serial.readBytes(s,10);
  Serial.print("Received:");
  Serial.println(s);
  delay(1000);
}
