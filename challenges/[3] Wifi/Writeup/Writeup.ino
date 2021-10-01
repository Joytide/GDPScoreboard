#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>


// Challenge 3: Wifi connection

// Pour ce challenge, pas de broadcaster, mais vous devez vous-même aller valider le challenge avec votre 
// micro-contrôler. Vous devez tout d’abord vous connecter au réseau wifi avec ces informations : 
// faire une requête http POST sur la page /challenge-wifi (donc l’url complète doit être
// http://serveur_url/challenge-wifi) avec comme data [numéro d'équipe]#[token]. (le token fait toujours 6
// caractères.
// Par exemple, si vous êtes l'équipe 134, et que votre token est 08j7uk, alors votre payload (ou POST data), sera:
// 123#08j7uk



// For monitors: 
// This is only a writeup, no need for a sender part, everything is done by the server. We just have to email them
// or give them their token during the TP.
// Docu on ESP8266HTTPClient: https://github.com/esp8266/Arduino/blob/master/libraries/ESP8266HTTPClient/src/ESP8266HTTPClient.h



const char* ssid = "";
const char* password = "";


String url = "";

void setup()  {
  WiFi.begin(ssid, password);
  Serial.begin(9600);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
} 
void loop() {
    delay(5000);
    if(WiFi.status()== WL_CONNECTED){
      WiFiClient client;
      HTTPClient http;

      http.begin(client, url.c_str());
      //http.addHeader("Content-Type", "Content-Type: application/json"); 


      
      String httpRequestData="4#4v17lk";
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
    
    
}
