#include <ArduinoJson.h>
#include <ArduinoJson.hpp>

#include <ESP32SPISlave.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>

// GLOBALS

// SERVER STUFF
const char* ssid = "iPhone di Luigi";
const char* password = "chungusVBD";

String server_ip = "http://54.237.83.228:8888/";

const char* host = "54.237.83.228";
const int httpPort = 8888;

String SERVER_PING = server_ip + "ping";
String SERVER_START = server_ip + "start";
String SERVER_SUSSY = server_ip + "status";

// RECEIVE MESSAGE

// StaticJsonBuffer<300> jsonRXBuffer;

// TAP SEND


TaskHandle_t ServerRequestTask;

int deviceID = 0;

String msg = "CARPO DIEM"; // Message that gets printed to the FPGA
int count =0;

float timestamps[32];

ESP32SPISlave slave;

static constexpr uint32_t BUFFER_SIZE {2};
uint8_t spi_slave_tx_buf[BUFFER_SIZE];
uint8_t spi_slave_rx_buf[BUFFER_SIZE];

void taskServerRequests( void * pvParameters ){
  while(true){
    pingServer();
    Serial.printf("DeviceID: %d\n", count);
    delay(1000);
  }
}

void pingServer() {
  HTTPClient client;
  client.begin(host, httpPort, "/status");

  int response = client.GET(); // send GET request
  
  if (response == 200){
    Serial.print("Successfull Startup request!");
    String payload = client.getString();
    Serial.println(payload);
  } else {
    Serial.print("Error: ");
    Serial.println(response);
    String payload = client.getString();
    Serial.println(payload);
  }

  client.end();
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

void connectToServer() {
  HTTPClient client;
  client.begin(SERVER_START);
  pingClient.begin(SERVER_PING);

  int response = client.GET(); // send GET request
  
  if (response == 200){
    Serial.print("Successfull Startup request!");
    String payload = client.getString();
    Serial.println(payload);
  } else {
    Serial.print("Error: ");
    Serial.println(response);
    String payload = client.getString();
    Serial.println(payload);
  }

  client.end();
}

float convertTime(int16_t timestamp){
  float standard_time = (float) timestamp/1000;
  return standard_time;
}


void setup() {
    // HSPI = CS: 15, CLK: 14, MOSI: 13, MISO: 12 -> default
    // VSPI = CS:  5, CLK: 18, MOSI: 23, MISO: 19

    Serial.begin(115200);

    initWIFI();
    
    connectToServer();

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

    pingServer();
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
      int16_t tap_data;
      if (spi_slave_rx_buf[0] & 0x80) { // check MSbit to be one
        count++;
        tap_data = (spi_slave_rx_buf[0] << 8 | spi_slave_rx_buf[1]) & 0x7FFF; // reconstruct data, ignore the MSbit
        // convertTime(tap_data);
        Serial.printf("Tap detected ");
        Serial.printf("%d\n", tap_data);
        // printf("Time since last tap: ");
        // printf("%d\n",   tap_data);          
        // printf("%d, %d\n", spi_slave_rx_buf[0], spi_slave_rx_buf[1]);
      }
      slave.pop();
    }



}
