#include <ESP8266WiFi.h>

// String incomingData;
// boolean TransmisioCompleta = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(1000);
  Serial.println("Hello World");
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    Serial.print(">");
    Serial.println(Serial.readString());
  }
}

