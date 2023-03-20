#include <ESP32SPISlave.h>
#include <ArduinoJson.h>
#include <WiFi.h>

const char* ssid = "";
const char* password = "";

const char* server_ip = "http://54.90.46.38:8888/";

float timestamps[32];

ESP32SPISlave slave;

static constexpr uint32_t BUFFER_SIZE {32};
uint8_t spi_slave_tx_buf[BUFFER_SIZE];
uint8_t spi_slave_rx_buf[BUFFER_SIZE];


void initWIFI() {
  Serial.begin(115200);
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

float convertTime(int16_t timestamp){
  float standard_time = (float) timestamp/1000;
  return standard_time;
}



void setup() {
    // HSPI = CS: 15, CLK: 14, MOSI: 13, MISO: 12 -> default
    // VSPI = CS:  5, CLK: 18, MOSI: 23, MISO: 19

    Serial.begin(115200);

    // initWIFI();

    // WiFiClient client;

    // //connect to client
    // client.setTimeout(10000);
    // if (!client.connect(server_ip, 80)) {
    //   Serial.println(F("Connection failed"));
    //   return;
    // }


    slave.setDataMode(SPI_MODE0);
    slave.begin(HSPI);
}


void loop() {
    // block until the transaction comes from master
    // slave.wait(spi_slave_rx_buf, spi_slave_tx_buf, BUFFER_SIZE);

    uint8_t tmp = 69;
    spi_slave_tx_buf[0] = tmp;

    if (slave.remained() == 0) {
      slave.queue(spi_slave_rx_buf, spi_slave_tx_buf, BUFFER_SIZE);
    }

    // if transaction has completed from master,
    // available() returns size of results of transaction,
    // and `spi_slave_rx_buf` is automatically updated
    
         
    while (slave.available()) {
        // do something with `spi_slave_rx_buf`
        int16_t tap_data = (spi_slave_rx_buf[0] << 8 | spi_slave_rx_buf[1]); // reconstruct data 
        // convertTime(tap_data);
        printf("Tap detected ");
        printf("Time since last tap: ");
        printf("%d\n", tap_data);
        slave.pop();
    }



}
