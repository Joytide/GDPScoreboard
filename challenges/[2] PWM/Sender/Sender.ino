
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

//Challenge 2: PWM

//Pins: GND and 3.3 to the two top pins of the potentiometer
// A0 to bottom of potentiometer
// RX to TX of student's NodeMCU


// Student:
// GND to GND
// A0 to bottom of potentiometer
// TX to RX


const char* ssid = "";
const char* password = "";

const int analogInPin = A0;

String url = "";


void setup()  {
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
} 



void loop()  { 
  int value = analogRead(analogInPin);
  Serial.print("Reading: ");
  Serial.println(value);

  String student_input = Serial.readStringUntil('/');

  Serial.println("Student guess was:"+student_input);

  if(WiFi.status()== WL_CONNECTED){
      WiFiClient client;
      HTTPClient http;

      http.begin(client, url.c_str());
      
      String httpRequestData=student_input+"#"+String(value);
      int httpResponseCode = http.POST(httpRequestData);
      if(httpResponseCode>0){
        String response = http.getString();  //Get the response to the request
        Serial.println(httpResponseCode);   //Print return code
        Serial.println(response);           //Print request answer
      } else {
        Serial.print("Error on sending POST: ");
        Serial.println(httpResponseCode);
    
        http.end();
    
     }
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    delay(2000);
}
