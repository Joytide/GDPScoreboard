// DHT11 setup
#include "DHT.h"
#define DHTPIN 2     // D4
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);

// Wifi and mqtt setup
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
const char* ssid = "";
const char* password = "";
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient); 
char *mqttServer = "";
int mqttPort = 1883;

const char* mqtt_user = "";
const char* mqtt_password = "";

const char* temp_topic = "challenge5/0/temp";
const char* hum_topic = "challenge5/0/hum";


void setupMQTT() {
  mqttClient.setServer(mqttServer, mqttPort);
  // set the callback function
  mqttClient.setCallback(callback);
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
  
}

void setup() {

  Serial.begin(9600);
  setup_wifi();
  setupMQTT();
  Serial.println(F("DHTxx test!"));

  dht.begin();
}

void reconnect() {
  Serial.println("Connecting to MQTT Broker...");
  while (!mqttClient.connected()) {
      Serial.println("Reconnecting to MQTT Broker..");
      String clientId = "ESP32Client-";
      clientId += String(random(0xffff), HEX);
      
      if (mqttClient.connect(clientId.c_str(),mqtt_user,mqtt_password)) {
        Serial.println("Connected.");
        mqttClient.subscribe("challenge4/1/token");
      }
      
  }
}

void loop() {
  if (!mqttClient.connected())
    reconnect();
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t) ) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  mqttClient.publish(temp_topic, String(t).c_str());                            
  Serial.printf("Publishing on topic %s at QoS 1, packetId: %i ", temp_topic);
  Serial.printf("Message: %.2f \n", t);
  
  mqttClient.publish(hum_topic, String(h).c_str());                            
  Serial.printf("Publishing on topic %s at QoS 1, packetId: %i ", hum_topic);
  Serial.printf("Message: %.2f \n", h);
  delay(15000);
}


void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Callback - ");
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
}
