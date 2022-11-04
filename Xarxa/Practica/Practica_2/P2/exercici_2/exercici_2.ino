#include "ESP8266WiFi.h"

int contador = 0;
// char *ssid = "Junjie_8266";
// char *password = "12345678";
const char *ssid;
const char *password;
String str_ssid;
String str_password;


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
  // put your main code here, to run repeatedly

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

        wifiNetworkSelection();

        str_ssid.trim();
        ssid = str_ssid.c_str();

        str_password.trim();
        password = str_password.c_str();

        connectToWiFi(ssid, password);
      }
      delay(100);
    }
  }

  Serial.println("*********************************");
  // wait a bit before scanning again

  delay(5000);
}


void wifiNetworkSelection() {
  if (WiFi.status() != WL_CONNECTED) {

    Serial.println("SSID? >");
    while (!Serial.available())
      ;
    str_ssid = Serial.readString();
    Serial.print("SSID selected > ");
    Serial.println(str_ssid);
    delay(1000);

    Serial.println("Password? > ");
    while (!Serial.available())
      ;
    str_password = Serial.readString();
    Serial.print("PWD > ");
    Serial.println(str_password);
    delay(1000);
  }
}


// str to char
char *strToChar(String txt, char *c) {
  int len = txt.length();
  free(c);
  c = NULL;
  c = (char *)malloc(len);
  for (int i = 0; i < len; i++) {
    c[i] = txt[i];
  }
  return c;
}


void connectToWiFi(const char *&ssid, const char *&password) {

  if (WiFi.status() != WL_CONNECTED) {

    Serial.println("Try to connecting...");

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Connecting...");
      contador++;
      if (contador == 10) {
        Serial.println("Connecting error...");
        contador = 0;
        break;
      }
    }
  } else {
    Serial.println("WiFi connecting successful");
    Serial.println(WiFi.localIP());
  }
}