#include "ESP8266WiFi.h"

int m = 0;

void setup(){
  //put your setup code here, to run once:
  Serial.begin(9600);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(2000);
  Serial.println("Setup done");
}



void loop(){

  Serial.println("Scan start");
  delay(10000);

  Serial.print("Distancia: ");
  m = Serial.readString().toInt();
  Serial.print(m);
  Serial.print("m :");

  int n = WiFi.scanNetworks();
  if(n==0)
    Serial.println("no networks found");
  else{
    for(int i = 0; i<n; i++){
      if (WiFi.SSID(i) == "MIWIFI_2G_bPkR"){
        Serial.print(WiFi.SSID(i));
        Serial.print("(");
        Serial.print(WiFi.RSSI(i));
        Serial.print(")");
        Serial.println((WiFi.encryptionType(i) == ENC_TYPE_NONE) ? " " : "*");
      }
      delay(100);
    }
  }

  Serial.println("*********************************");
  // wait a bit before scanning again

  delay(10000);
}