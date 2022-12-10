#include "ESP8266WiFi.h"
#include "ThingSpeak.h"


// Network parameters
char* ssid = "Junjie_8266";     // Your wireless network name (SSID)
char* password = "12345678";    // Your wireless netword password

// // ThingSpeak information
// char thingSpeakAddress[] = "api.thingspeak.com";
// unsigned long channelID = 1976222;
// char* writeAPIKey = "0H5BGHUZ992NFXCW";
// char* readAPIKey = "V88CWWDFL3LCLQWC";
// const unsigned int postingInterval = 20*1000;
// unsigned int RSSIField = 1;

// WiFiClient client;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(2000);
  Serial.println("Setup done");
  Serial.println("start connecting...");
}

void loop() {
  // put your main code here, to run repeatedly:

  // long rssi = WiFi.RSSI();
  // writeTSData(channelID, RSSIField, rssi);
  // delay(postingInterval);

  Serial.println("Scan start");
  int n = WiFi.scanNetworks();
  
  if(n==0){
    Serial.println("no networks found");
  }else{
    for(int i = 0; i<n; i++){
      if (WiFi.SSID(i) == "Junjie_8266") {
        Serial.print(WiFi.SSID(i));
        Serial.print("(");
        Serial.print(WiFi.RSSI(i));
        Serial.print(")");
        Serial.println((WiFi.encryptionType(i) == ENC_TYPE_NONE) ? " " : "*");
        connectToWiFi(ssid, password);
      }
      delay(100);
      
    }
  }

  Serial.println("*********************************");
  // wait a bit before scanning again

  delay(10000);

}

void connectToWiFi(char *ssid, char *password) {

  if (WiFi.status() != WL_CONNECTED) {

    Serial.println("Try to connecting...");

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Connecting...");
    }
  } else {
    Serial.println("WiFi connecting successful");
    Serial.println(WiFi.localIP());
  }
}


// int writeTSData(long TSChannel, unsigned int TSField, float data){
//   // Write the data to the channel
//   int writeSuccess = ThingSpeak.writeField(TSChannel, TSField, data, writeAPIKey);
//   if (writeSuccess) {
//     Serial.print(String(data) + " writeen to ThingSpeak.");
//   } 
//   return writeSuccess;
// }

