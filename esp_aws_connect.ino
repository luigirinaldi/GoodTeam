
#include "secrets.h"
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "WiFi.h"

 
#define AWS_IOT_PUBLISH_TOPIC   "esp32/pub" //To publish: esp32/sub in publish section
#define AWS_IOT_SUBSCRIBE_TOPIC "esp32/sub" //To subscribe: esp32/pub in subscribe section
 


WiFiClientSecure net = WiFiClientSecure();
PubSubClient client(net);
 
void connectAWS()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
 
  Serial.println("Connecting to Wi-Fi");
 
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to wifi");
  }
 
  // Configure WiFiClientSecure to use the AWS IoT device credentials
  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);
 
  // Connect to the MQTT broker on the AWS endpoint we defined earlier
  client.setServer(AWS_IOT_ENDPOINT, 8883);
 
  // Create a message handler
  client.setCallback(messageHandler);
 
  Serial.println("Connecting to AWS IOT");
 
  while (!client.connect(THINGNAME))
  {
    Serial.print("connecting to aws iot");
    delay(100);
  }
 
  if (!client.connected())
  {
    Serial.println("AWS IoT Timeout!");
    return;
  }
 
  // Subscribe to a topic
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);
 
  Serial.println("AWS IoT Connected!");
}
 
void publishMessage()
{
  StaticJsonDocument<200> doc;
  doc["humidity"] = 404;
  doc["temperature"] = 32;
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer); // print to client
 
  client.publish(AWS_IOT_PUBLISH_TOPIC, jsonBuffer);
}
 
void messageHandler(char* topic, byte* payload, unsigned int length)
{
  Serial.print("incoming: ");
  Serial.println(topic);
 
  StaticJsonDocument<200> doc;
  deserializeJson(doc, payload);
  const char* message = doc["message"];
  Serial.println(message);
}
 
void setup()
{
  Serial.begin(115200);
  connectAWS();
  
}
 
void loop()
{

 
 
  Serial.print(F("Test: "));
  Serial.print(101);
  Serial.print(F("%  Hey: "));
  Serial.print(66);
  Serial.println(F("°C "));
 
  publishMessage();
  client.loop();
  delay(1000);
}
















































































//#include "secrets.h"
//#include <WiFiClientSecure.h>
//#include <PubSubClient.h>
//#include <MQTTClient.h>
//#include <ArduinoJson.h>
//#include "WiFi.h"
//
//// The MQTT topics that this device should publish/subscribe
//#define AWS_IOT_PUBLISH_TOPIC   "esp32/pub"
//#define AWS_IOT_SUBSCRIBE_TOPIC "esp32/sub"
//#define AWS_MAX_RECONNECT_TRIES 50
//unsigned long previousMillis = 0;
//unsigned long interval = 30000;
//
//
//WiFiClientSecure net = WiFiClientSecure();
//MQTTClient client = MQTTClient();
//
//
////Connecting to local WiFi
//void InitWifi()
//{
//  WiFi.mode(WIFI_STA);
//  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
//  Serial.println("Connecting to WiFi ..");
//  while (WiFi.status() != WL_CONNECTED) {
//    Serial.println('.');
//    delay(1000);
//  }
//  Serial.println(WiFi.localIP());
//}
//
//void connectAWS()
//{
//    
//  // Configuring WiFiClientSecure to use the AWS IoT device credentials
//  net.setCACert(AWS_CERT_CA);
//  Serial.println("certif 1 ok");
//  net.setCertificate(AWS_CERT_CRT);
//  Serial.println("certif 2 ok");
//  net.setPrivateKey(AWS_CERT_PRIVATE);
//  Serial.println("certif 3 ok");
//  
//  // Connect to the MQTT broker on the AWS endpoint we defined earlier
//  client.begin(AWS_IOT_ENDPOINT, 8883, net);
//  // Try to connect to AWS and count how many times we retried.
//  int retries = 0;
//  while (!client.connect(THINGNAME) && retries < AWS_MAX_RECONNECT_TRIES) {
//    Serial.print(".");
//    delay(100);
//    retries++;
//  }
////  Serial.print("Connecting to AWS IOT");
////  // Create a message handler
////  client.setCallback(messageHandler);
////  Serial.println("Connecting to AWS IOT");
////  Serial.println("Connected");
////  while (!client.connect(THINGNAME)) {
////     Serial.println(".. waiting ..");
////     delay(100);
////  }
//  
//  // Check if timeout
//  if(!client.connected()){
//     Serial.println("AWS IoT Timeout!");
//     return;
//  }
//  
//  // Subscribe to a topic
//  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);
//  Serial.println("AWS IoT Connected!");
//  
//}
//
//
////
//void publishMessage()
//{
//  StaticJsonDocument<200> doc;
//  doc["time"] = millis();
//  doc["sensor_a0"] = analogRead(0);
//  char jsonBuffer[512];
//  serializeJson(doc, jsonBuffer); // print to client
//
//  client.publish(AWS_IOT_PUBLISH_TOPIC, jsonBuffer);
//}
//
//void messageHandler(char* topic, byte* payload, unsigned int length) {
//   Serial.print("incoming: ");
//   Serial.println(topic);
//
////  StaticJsonDocument<200> doc;
////  deserializeJson(doc, payload);
////  const char* message = doc["message"];
//}
//
//void setup() {
//  Serial.begin(115200);
//  InitWifi();
//  connectAWS();
//  Serial.print("RSSI: ");
//  Serial.println(WiFi.RSSI());
//  
//}
//
//void loop() {
//
//  
//  unsigned long currentMillis = millis();
//  if ((WiFi.status() != WL_CONNECTED) && (currentMillis - previousMillis >=interval)) {
//    Serial.print(millis());
//    Serial.println("Reconnecting to WiFi...");
//    WiFi.disconnect();
//    WiFi.reconnect();
//    previousMillis = currentMillis;
//  }
//    publishMessage(); 
//    client.loop();
//    delay(1000);
//}
