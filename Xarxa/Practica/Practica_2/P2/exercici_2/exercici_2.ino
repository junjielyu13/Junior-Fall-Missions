#include "ESP8266WiFi.h"

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}


void connectToWiFi(void){
  if(WiFi.status() != WL_CONNECTED){
    WiFi.begin(c_ssid, c_pwd);
    while(WiFi.status() != WL_CONNECTED){
      delay(1000);
      Serial.println("Connecting...");
      contador++;
      if(contador == 10){
        break;
      }
    }
  }
}


void wifiNetworkSelection(void){
  if(WiFi.status() != WL_CONNECTED){
    Serial.println("SSID? >");
    while(!Serial.available());
    ssid = Serial.readString();
    Serial.print("SSID selected > ");
    Serial.println(ssid);
    delay(1000);
    Serial.print("Password? > ");
    while(!Serial.available());
    password = Serial.readString();
    Serial.print("PWD > ");
    Serial.println(password);
    delay(1000);
  }
}


void strToChar(String txt, char* c){

  if(WiFi.status() != WL_CONNECTED){
    int len = txt.length();
    Serial.println(len);
    Serial.println("*********************************");
    c = (char *)malloc(len);
    for(int i=0; i<len; i++){
      c[i] = txt[i];
      Serial.print(c[i]);
    }
  }
}