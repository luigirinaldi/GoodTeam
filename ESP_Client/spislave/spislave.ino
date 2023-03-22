#include <ESP32SPISlave.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>

// GLOBALS
int valid_tap_time = -1;
int time_since_valid;

// SERVER STUFF
const char* ssid = "iPhone di Luigi";
const char* password = "chungusVBD";

const char* host = "100.26.142.78";
const int httpPort = 8888;

// RECEIVE MESSAGE


// TAP SEND


TaskHandle_t ServerRequestTask;

int DeviceID = 0;
int RecipientID = 0;

String msg = "READY TO SEND"; // Message that gets printed to the FPGA
int count =0;

float array_timestamps[256];

int count_timestamps = 0; //the number of timestamps that have been added to array_timestamp

ESP32SPISlave slave;

static constexpr uint32_t BUFFER_SIZE {2};
uint8_t spi_slave_tx_buf[BUFFER_SIZE];
uint8_t spi_slave_rx_buf[BUFFER_SIZE];

void taskServerRequests( void * pvParameters ){
  while(true){
    String newMessage;
    if(pingServer(DeviceID, newMessage)){
      Serial.println(newMessage);
      msg = newMessage; // display this on the FPGA
    } 
    else {
      Serial.print(newMessage);
    }

    
    delay(1000);
  }
}

bool pingServer(int deviceID, String &ReceivedMsg) {
  HTTPClient client;
  client.begin(host, httpPort, "/ping");
  bool returnVal = false;
  String pingPayload = "{\"DeviceID\":" + String(deviceID) + "}";

  int response = client.sendRequest("GET", pingPayload); // send GET request
  
  if (response == 200){
    Serial.print("Getting ping info");
    DynamicJsonDocument doc(1024);
    String payload = client.getString();
    Serial.println(payload);
    DeserializationError error = deserializeJson(doc, payload);
    if (error) {
      Serial.println("Deserialization failed!");
      Serial.println(error.f_str());
      return false;
    }
    int sender = doc["messages"][0]["from"];
    JsonArray message = doc["messages"][0]["message"].as<JsonArray>();

    ReceivedMsg = String(sender) + ":";

    for (JsonVariant word : message) {
      ReceivedMsg += word.as<String>() + " ";
    }
    ReceivedMsg.remove(ReceivedMsg.length() - 1);
    // ReceivedMsg += doc["message"][0].as<String>();

    returnVal = true;
  } else if (response == 206) {
    ReceivedMsg = "";    
    returnVal = false;
  } else {
    Serial.print("Error: ");
    Serial.println(response);
    // String payload = client.getString();
    // Serial.println(payload);

    ReceivedMsg = "Something went wrong\n";
  }

  client.end();
  return returnVal;
}

void initWIFI() {
  Serial.println("Attempting to connect...");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}

bool connectToServer() {
  HTTPClient client;
  client.begin(host, httpPort, "/start");
  bool returnVal = false;
  int response = client.GET(); // send GET request
  
  if (response == 200){
    DynamicJsonDocument doc(1024);
    String payload = client.getString();
    Serial.println(payload);
    DeserializationError error = deserializeJson(doc, payload);

    if (error) {
      Serial.println("Deserialization failed!");
      Serial.println(error.f_str());

      client.end();
      return false;
    }
    
    // change global variable
    DeviceID = doc["deviceID"].as<int>();

    returnVal = true;
  } else {
    Serial.print("Error: ");
    Serial.println(response);
    returnVal = false;
  }

  client.end();
  return returnVal;
}

float convertTime(int16_t timestamp){
  float standard_time = (float) timestamp/1000;
  array_timestamps[count_timestamps++] = standard_time;
  return standard_time;
}

void sendJSON(float array_timestamps[]){
  DynamicJsonDocument request(2048);

  request["DeviceID"] = DeviceID;
  request["RecipientID"] = RecipientID;

  JsonArray timestamps = request.createNestedArray("taps");

  timestamps.add(0);

  for(int i=1; i < count_timestamps; i++){
        timestamps.add(array_timestamps[i]); // Add floats to JSON array starting from second value, first value 0;
  }
  
  serializeJsonPretty(request, Serial);

  // SEND TO SERVER

  HTTPClient client;
  client.begin(host, httpPort, "/");

  String tapPayload;
  serializeJson(request, tapPayload);
  Serial.println("");
  
  int response = client.sendRequest("GET", tapPayload); // send GET request
  
  if (response == 200){
    Serial.println("Data sent successfully");
    Serial.println(client.getString());
  } else {
    Serial.println("Sending data went wrong: " + String(response));
  }

  client.end();
  
  // reset counter 
  count_timestamps = 0;
}



void setup() {
    // HSPI = CS: 15, CLK: 14, MOSI: 13, MISO: 12 -> default
    // VSPI = CS:  5, CLK: 18, MOSI: 23, MISO: 19

    Serial.begin(115200);

    while(!Serial);

    initWIFI();
    
    while(!connectToServer()){
      Serial.println("Trying to connect to the server");
      delay(1000);
    }

    Serial.println("Connected to server with ID" + String(DeviceID));

    slave.setDataMode(SPI_MODE0);
    slave.begin(HSPI);

    xTaskCreatePinnedToCore(
      taskServerRequests, /* Function to implement the task */
      "ServerRequests", /* Name of the task */
      10000,  /* Stack size in words */
      NULL,  /* Task input parameter */
      0,  /* Priority of the task */
      &ServerRequestTask,  /* Task handle. */
      0); /* Core where the task should run */

    delay(2000);
}




void loop() {

    if (msg.length() > 0){  // when new message send to the FPGA
      spi_slave_tx_buf[0] = 255;
      spi_slave_tx_buf[1] = msg.length(); // assuming lengths is less than 256

      slave.wait(spi_slave_rx_buf, spi_slave_tx_buf, BUFFER_SIZE); // send number of chars
      
      while (slave.available()) { slave.pop(); }

      for (int i = 0; i < msg.length(); i ++){
        spi_slave_tx_buf[0] = 0;
        spi_slave_tx_buf[1] = msg[i]; 
        slave.wait(spi_slave_rx_buf, spi_slave_tx_buf, BUFFER_SIZE); // send each char
        while (slave.available()) { slave.pop(); }
      }
      
      msg = "";      
    }
    

    spi_slave_tx_buf[0] = 0;
    spi_slave_tx_buf[1] = 0;



    slave.wait(spi_slave_rx_buf, spi_slave_tx_buf, BUFFER_SIZE);

    // if (slave.remained() == 0) {
      // slave.queue(spi_slave_rx_buf, spi_slave_tx_buf, BUFFER_SIZE);
    // }

    // if transaction has completed from master,
    // available() returns size of results of transaction,
    // and `spi_slave_rx_buf` is automatically updated
    
         
    while (slave.available()) {
      // do something with `spi_slave_rx_buf
      time_since_valid = millis();

      if((valid_tap_time != -1) && (time_since_valid - valid_tap_time > 2000)){
        //send HTTP request
        Serial.println("Exceeded 2 sec, send request");
        sendJSON(array_timestamps);

        valid_tap_time = -1;
      }

      int16_t tap_data;
      if (spi_slave_rx_buf[0] & 0x80) { // check MSbit to be one

        valid_tap_time = millis(); // Take time when valid tap received

        tap_data = (spi_slave_rx_buf[0] << 8 | spi_slave_rx_buf[1]) & 0x7FFF; // reconstruct data, ignore the MSbit
        convertTime(tap_data);
        printf("Tap detected ");
        printf("%d\n", tap_data);
      }


      slave.pop();
    }



}
