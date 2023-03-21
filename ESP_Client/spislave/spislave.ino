#include <ArduinoJson.h>
#include <ArduinoJson.hpp>

#include <ESP32SPISlave.h>
#include <ArduinoJson.h>
#include <WiFi.h>

// GLOBALS

const char* ssid = "";
const char* password = "";

const char* server_ip = "http://54.90.46.38:8888/";

String msg = "CARPO DIEM"; // Message that gets printed to the FPGA
int count =0;

float timestamps[32];

ESP32SPISlave slave;

static constexpr uint32_t BUFFER_SIZE {2};
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

void IRAM_ATTR HTTP_request_ISR(){
  Serial.print("TEST");
  Serial.println(count);
  msg = "TEST" + String(count++);  
}

hw_timer_t *Timer0_Cfg = NULL;

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

    // INTERRUPT ROUTINE FOR POLLING THE SERVER
    Timer0_Cfg = timerBegin(0, 80, true); // use timer 0, prescaler of 80 and count up
    timerAttachInterrupt(Timer0_Cfg, &HTTP_request_ISR, true); // att ach interrupt
    timerAlarmWrite(Timer0_Cfg, 1000000, true);  // set the period
    timerAlarmEnable(Timer0_Cfg); // start the timeer

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
        tap_data = (spi_slave_rx_buf[0] << 8 | spi_slave_rx_buf[1]) & 0x7FFF; // reconstruct data, ignore the MSbit
        // convertTime(tap_data);
        printf("Tap detected ");
        printf("%d\n", tap_data);
        // printf("Time since last tap: ");
        // printf("%d\n",   tap_data);          
        // printf("%d, %d\n", spi_slave_rx_buf[0], spi_slave_rx_buf[1]);
      }
      slave.pop();
    }



}
