#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <SoftwareSerial.h>

// Challenge 1: Datasheet

// For monitors:
// The sender print on a custom TX (here GPIO2) a token for students to read on their RX, each token is 
// retreived from the server and each time a token is used, the /tokens endpoint won't send this token anymore
// So each token is for one team only, the tokens are fetched every 5 seconds, and are of length 6







const char* ssid = "";
const char* password = "";

// SoftwareSerial(rxPin, txPin)
SoftwareSerial ser(0, 2);  //    0/2 == GPIO 0/GPIO 2 == D3/D4

String url = "http://gdp.devinci.fr/tokens-datasheet";  

void setup()  {
  ser.begin(9600);
  WiFi.begin(ssid, password);
  //Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    //Serial.print(".");
  }
} 
void loop() {
    
    //Serial.write("Token");
    String tokens[100];

    if(WiFi.status()== WL_CONNECTED){
      WiFiClient client;
      HTTPClient http;

      http.begin(client, url.c_str());
      int httpResponseCode = http.GET();
      if (httpResponseCode>0) {
        String payload = http.getString();
        char p[1024];
        payload.toCharArray(p, 2048);
        String token = strtok(p,"[],\" \n");
        int token_len = 0;
        
        while (token!=NULL){
          //Serial.println(token);
          tokens[token_len] = token;
          token = strtok(NULL,"[],\" \n");
          token_len++;
        }
      }
      
      http.end();
    }

    for (int i=0;i<10;i++){
      ser.println(tokens[0]);
      delay(500);
    }
}
