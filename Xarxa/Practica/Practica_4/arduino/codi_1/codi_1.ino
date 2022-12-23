#include "ESP8266WiFi.h"
#include "ThingSpeak.h"
#include "DFRobot_CCS811.h"


// Network parameters
const char* ssid = "Junjie_8266";   // Your wireless network name (SSID)
const char* password = "12345678";  // Your wireless netword password

// ThingSpeak information
char thingSpeakAddress[] = "api.thingspeak.com";
unsigned long channelID = 1990985;
char* writeAPIKey = "FYSIIM5CAMKJ4KDU";
char* readAPIKey = "GY4Z2EPNG0OOOW4D";
unsigned int postingInterval = 20 * 1000;
unsigned int RSSIField = 1;
unsigned int AirQualityField = 2;
unsigned int CO2Field = 3;
unsigned int TVOCField = 4;

WiFiClient client;
DFRobot_CCS811 CCS811;

// CLEAR DATA OF CHANNEL:
// curl -v --request DELETE "https://api.thingspeak.com/channels/1990985/" --header "host.api.thingspeak.com" --data "api_key=user_token"
// curl -v --request DELETE "https://api.thingspeak.com/channels/1990985/feeds.json" api_key=user_token

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) {
    // wait for serial port to connect. Needed for native USB port only
    delay(1000);
  }

  // Initialize ESP8266WiFi
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  // Initialize ThingSpeak
  ThingSpeak.begin(client);

  // Wait for the chip to be initialized completely, and then exit
  while (CCS811.begin() != 0) {
    Serial.println("failed to init chip, please check if the chip connection is fine");
    delay(1000);
  }

  delay(2000);
  Serial.println("Setup done");
  Serial.println("start connecting...");
}

void loop() {
  // put your main code here, to run repeatedly:

  Serial.println("Scan start");
  int n = WiFi.scanNetworks();

  if (n == 0) {
    Serial.println("no networks found");
  } else {
    for (int i = 0; i < n; i++) {
      if (WiFi.SSID(i) == "Junjie_8266") {
        Serial.print(WiFi.SSID(i));
        Serial.print("(");
        Serial.print(WiFi.RSSI(i));
        Serial.print(")");
        Serial.println((WiFi.encryptionType(i) == ENC_TYPE_NONE) ? " " : "*");
        if (WiFi.status() != WL_CONNECTED) {
          connectToWiFi(ssid, password);
        }
        long rssi = WiFi.RSSI();
        Serial.print("WiFi RSSI: ");
        Serial.println(rssi);
        //writeTSData(channelID, RSSIField, rssi);
        ThingSpeak.setField(RSSIField, rssi);
      }
      delay(100);
    }
  }

  // Judge if there is data to read the result of checking
  if (CCS811.checkDataReady() == true) {

    // get the current baseline number
    // Hexadecimal number of the current baseline number
    long airclear = CCS811.readBaseLine();
    Serial.print("Clear Air Baseline: ");
    Serial.println(airclear);
    //writeTSData(channelID, AirQualityField, airclear);
    ThingSpeak.setField(AirQualityField, airclear);


    // Get the current carbon dioxide concentration
    // current carbon dioxide concentration, unit:ppm
    long co2ppm = CCS811.getCO2PPM();
    Serial.print("CO2: ");
    Serial.print(co2ppm);
    Serial.println("ppm");
    //writeTSData(channelID, CO2Field, co2ppm);
    ThingSpeak.setField(CO2Field, co2ppm);


    // Get current TVOC concentration
    // Return current TVOC concentration, unit: ppb
    long tvocppb = CCS811.getTVOCPPB();
    Serial.print("TVOC: ");
    Serial.print(tvocppb);
    Serial.println("ppb");
    //writeTSData(channelID, TVOCField, tvocppb);
    ThingSpeak.setField(TVOCField, tvocppb);

  } else {
    Serial.println("Data is not ready!");
  }

  writeTSData(channelID);

  Serial.println("*********************************");
  // wait a bit before scanning again

  delay(postingInterval);
}



void connectToWiFi(const char* ssid, const char* password) {

  int count = 0;
  if (WiFi.status() != WL_CONNECTED) {

    Serial.println("Try to connecting...");

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Connecting...");
      count++;
      if (count > 10) {
        break;
      }
    }
  } else {
    Serial.print("Connection Successful");
  }
}


// int writeTSData(long TSChannel, unsigned int TSField, float data) {
int writeTSData(long TSChannel) {
  // Write the data to the channel
  // int writeSuccess = ThingSpeak.writeField(TSChannel, TSField, data, writeAPIKey);
  int writeSuccess = ThingSpeak.writeFields(TSChannel, writeAPIKey);
  if (writeSuccess == 200) {
    Serial.println("Channel update successful.");
  } else {
    Serial.println("Problem updating channel. HTTP error code " + String(writeSuccess));
  }
  return writeSuccess;
}
