// currently tag is module #5
// The purpose of this code is to set the tag address and antenna delay to default.
// this tag will be used for calibrating the anchors.

#include <SPI.h>
#include <DW1000Ranging.h>
//#include "DW1000.h"
#include <WiFi.h>
#include "link.h"

#define SPI_SCK 18
#define SPI_MISO 19
#define SPI_MOSI 23
#define DW_CS 4

// connection pins
const uint8_t PIN_RST = 27; // reset pin
const uint8_t PIN_IRQ = 34; // irq pin
const uint8_t PIN_SS = 4;   // spi select pin

const char *ssid = "ASUS";
const char *password = "cuni3103&";
const char *host = "192.168.1.55";
WiFiClient client;

// TAG antenna delay defaults to 16384
// leftmost two bytes below will become the "short address"
char tag_addr[] = "01:00:00:00:00:00:00:00";

struct MyLink *uwb_data;
int index_num = 0;
long runtime = 0;
String all_json = "";

void setup()
{
  Serial.begin(115200);

//  WiFi.disconnect(true);
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
      delay(500);
      Serial.print(".");
  }
  Serial.println("Connected");
  Serial.print("IP Address:");
  Serial.println(WiFi.localIP());

  if (client.connect(host, 30001))
  {
      Serial.println("Success");
//      client.print(String("GET /") + " HTTP/1.1\r\n" +
//                   "Host: " + host + "\r\n" +
//                   "Connection: close\r\n" +
//                   "\r\n");
  } else {
      Serial.println("Unsuccessfull connection");
    }
    
  delay(1000);


  Serial.println("Init the configuration..");
  //init the configuration
  SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
//  Serial.println("Init com/munication..");//
  DW1000Ranging.initCommunication(PIN_RST, PIN_SS, PIN_IRQ); //Reset, CS, IRQ pin
  DW1000Ranging.attachNewRange(newRange);
//  Serial.println("Attching new device..");
  DW1000Ranging.attachNewDevice(newDevice);
//  Serial.println("Attching inactive device..");
  DW1000Ranging.attachInactiveDevice(inactiveDevice);

// start as tag, do not assign random short address

  Serial.println("Starting as tag..");
  DW1000Ranging.startAsTag(tag_addr, DW1000.MODE_LONGDATA_RANGE_LOWPOWER);
  uwb_data = init_link();
  
  Serial.println("Configuration is initialized...");
}

void loop()
{
  DW1000Ranging.loop();
//  Serial.println("In loop...");
  if ((millis() - runtime) > 1000)
  {
      Serial.println("In loop making json...");
      
      make_link_json(uwb_data, &all_json);
      Serial.println("json is made...");
      send_udp(&all_json);
      runtime = millis();
  }
}

void newRange()
{
  char c[30];
  Serial.print("from: ");
  Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
  Serial.print("\t Range: ");
  Serial.print(DW1000Ranging.getDistantDevice()->getRange());
  Serial.print(" m");
  Serial.print("\t RX power: ");
  Serial.print(DW1000Ranging.getDistantDevice()->getRXPower());
  Serial.println(" dBm");
  
  fresh_link(uwb_data, DW1000Ranging.getDistantDevice()->getShortAddress(), DW1000Ranging.getDistantDevice()->getRange(), DW1000Ranging.getDistantDevice()->getRXPower());
}

void newDevice(DW1000Device *device)
{
  Serial.print("ranging init; 1 device added ! -> ");
  Serial.print(" short:");
  Serial.println(device->getShortAddress(), HEX);

  add_link(uwb_data, device->getShortAddress());
}

void inactiveDevice(DW1000Device *device)
{
  Serial.print("delete inactive device: ");
  Serial.println(device->getShortAddress(), HEX);

  delete_link(uwb_data, device->getShortAddress());
}


void send_udp(String *msg_json)
{
    Serial.println("sending UDP");
    
    if (client.connected())
    {
        client.print(*msg_json);
        Serial.println("UDP send");
    }
}
