#include "ESP8266WiFi.h"
#include "ThingSpeak.h"
#include "DFRobot_CCS811.h"

// char ssid[] = "MyWiFi_8266";
// char password[] = "password";

const char* ssid = "MIWIFI_2G_bPkR";  // Your wireless network name (SSID)
const char* password = "4J5cnqEP";    // Your wireless netword password

// ThingSpeak information
const char* web = "https://thingspeak.com/channels/1991175";
char thingSpeakAddress[] = "api.thingspeak.com";
unsigned long channelID = 1991175;
char* writeAPIKey = "YL11BUSH85GYKLTD";
char* readAPIKey = "7GVSONR74G5OGXLH";
unsigned int postingInterval = 20 * 1000;
unsigned int RSSIField = 1;
unsigned int AirQualityField = 2;
unsigned int CO2Field = 3;
unsigned int TVOCField = 4;

WiFiClient client;
DFRobot_CCS811 CCS811;


// Set web server port number to 80
WiFiServer server(80);


// Variable to store the HTTP request
String header;


// Current time
unsigned long currentTime = millis();
// Previous time
unsigned long previousTime = 0;
// Define timeout time in milliseconds (example: 2000ms = 2s)
const long timeoutTime = 2000;


int writeTSData(long TSChannel, unsigned int TSField, float data) {
// int writeTSData(long TSChannel) {
  // Write the data to the channel
  int writeSuccess = ThingSpeak.writeField(TSChannel, TSField, data, writeAPIKey);
  // int writeSuccess = ThingSpeak.writeFields(TSChannel, writeAPIKey);
  if (writeSuccess == 200) {
    Serial.println("Channel update successful.");
  } else {
    Serial.println("Problem updating channel. HTTP error code " + String(writeSuccess));
  }
  return writeSuccess;
}



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) {
    // wait for serial port to connect. Needed for native USB port only
    delay(1000);
  }
  // Serial.println("WiFi access point test");
  // WiFi.mode(WIFI_AP);
  // WiFi.softAP(ssid, password);
  // Serial.println("WiFi on");

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


  // Connect to Wi-Fi network with SSID and password
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop() {
  WiFiClient client = server.available();  // Listen for incoming clients

  if (client) {  // If a new client connects,
    Serial.println("New Client.");
    String currentLine = "";

    currentTime = millis();
    previousTime = currentTime;
    // loop while the client's connected
    while (client.connected() && currentTime - previousTime <= timeoutTime) {
      currentTime = millis();
      if (client.available()) {  // if there's bytes to read from the client,
        char c = client.read();
        Serial.write(c);
        header += c;
        if (c == '\n') {  // if the byte is a newline character
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();


            if (header.indexOf("GET /1") >= 0) {

              Serial.println("Scan start");
              int n = WiFi.scanNetworks();

              if (n == 0) {
                Serial.println("no networks found");
              } else {
                for (int i = 0; i < n; i++) {
                  if (WiFi.SSID(i) == "MIWIFI_2G_bPkR") {
                    Serial.print(WiFi.SSID(i));
                    Serial.print("(");
                    Serial.print(WiFi.RSSI(i));
                    Serial.print(")");
                    long rssi = WiFi.RSSI(i);
                    Serial.print("WiFi RSSI: ");
                    Serial.println(rssi);
                    writeTSData(channelID, RSSIField, rssi);
                  }
                  delay(100);
                }
              }
            } else if (header.indexOf("GET /2") >= 0) {
              long airclear = CCS811.readBaseLine();
              Serial.print("Clear Air Baseline: ");
              Serial.println(airclear);
              writeTSData(channelID, AirQualityField, airclear);
            } else if (header.indexOf("GET /3") >= 0) {
              long co2ppm = CCS811.getCO2PPM();
              Serial.print("CO2: ");
              Serial.print(co2ppm);
              Serial.println("ppm");
              writeTSData(channelID, CO2Field, co2ppm);
            } else if (header.indexOf("GET /4") >= 0) {
              long tvocppb = CCS811.getTVOCPPB();
              Serial.print("TVOC: ");
              Serial.print(tvocppb);
              Serial.println("ppb");
              writeTSData(channelID, TVOCField, tvocppb);
            }


            client.println("<!DOCTYPE html>");
            client.println("<html lang=\"en\">");
            client.println("<head>");
            client.println("<meta charset=\"UTF-8\">");
            client.println("<meta http-equiv=\" X-UA-Compatible \" content=\"IE=edge\">");
            client.println("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">");
            client.println("<title>ESP8266_Junjie Web Server</title>");
            client.println("<style>");
            client.println("*{ margin: 0;}");
            client.println("body{font-size: 16;font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif}");
            client.println(".container{margin: 0 auto;width: 80%;}");
            client.println(".header{margin: 0 auto; width: 100%; height: 50px; background-color: #2f7eb2;}");
            client.println(".header-item-pos{ padding-top: 10px; padding-left: 10%; width: 100%;}");
            client.println(".header-item-pos a{display: inline-block;width: 160px;text-decoration: none;text-align: left;font-size: 18px;font-weight: 500;color: #fff;}");
            client.println(".title{margin: 40px auto;width: 100% ; text-align: center;font-size: 28px;font-weight: 700;}");
            client.println(".main-title{font-size: 30px;}");
            client.println(".sub-title{font-size: 32px;}");
            client.println(".description{margin: 0 auto;width: 80% ; font-size: 20px;}");
            client.println(".main{margin: 40px auto;text-align: center;height: 300px;}");
            client.println(".top,.bottom{margin: 0 auto;width: 90% ; height: 200px;}");
            client.println(".top-left,.top-right,.bottom-left,.bottom-right{width: 270px;height: 80px;line-height: 80px;background-color: #46bc79;text-align: center;border-radius: 40px;}");
            client.println(".top-left a,.top-right a,.bottom-left a,.bottom-right a{text-decoration: none;color: #fff;font-size: 20px;font-weight: 600;}");
            client.println(".footer{width: 100% ; height: 50px;background-color: #333;}");
            client.println(".footer-pos{padding-top: 11px;width: 80% ; padding-left:  10% ; color: #fff;font-size: 14px;font-weight: 200;}");
            client.println(".footer-left{float: left;}");
            client.println(".footer-left a{text-decoration: none;color: #fff;}");
            client.println(".footer-right{float: right;}");
            client.println("</style>");
            client.println("</head>");
            client.println("<body>");
            client.println("<div class =\"header\">");
            client.println("<div class = \"header-item-pos\">");
            client.println("<a href = \"https://thingspeak.com/\"> ThingSpeak</a>");
            client.println("<a href = \"https://www.generationrobots.com/media/adafruit-feather-huzzah-esp8266-user-guide-tutorial.pdf\"> ESP8266</a>");
            client.println("<a href = \"https://www.dfrobot.com/product-2065.html\"> CCS811 Air Quality</a>");
            client.println("</div>");
            client.println("</div>");
            client.println("<div class =\"container\">");
            client.println("<div class =\"title\">");
            client.println("<p class = \"main-title\"> ESP8266 + CCS811 Air Quality + ThingSpeak</ p><p class = \"sub-title\"> Web Server</p></div>");
            client.println("<div class = \"description\"> Aquest web està creat amb ESP8266,");
            client.println("podeu utilitzar ESP8266 i CCS811 Air Quality per mesurar dades i enviar - les al lloc web de ThingSpeak : <a href = \"https://thingspeak.com/channels/1991175\"> Aquí.</a></div>");
            client.println("<div class = \"main\">");
            client.println("<div class = \"top\">");
            client.println("<div class = \"top-left\" style = \"float: left;\"><a href = \"1\"><div>GET RSSI</div></a></div>");
            client.println("<div class = \"top-right\" style = \"float: right;\"><a href = \"2\"><div> GET Clear Air baselines numbers</div></a></div></div>");
            client.println("<div class = \"bottom\">");
            client.println("<div class = \"bottom-left\" style = \"float: left;\"><a href = \"3\"><div>GET CO2 (ppm)</div></a></div>");
            client.println("<div class = \"bottom-right\" style = \"float: right;\"><a href = \"4\"><div>GET TVOC (ppb)</div></a></div>");
            client.println("</div>");
            client.println("</div>");
            client.println("</div>");
            client.println("<div class = \"footer\"><div class = \"footer-pos\"><div class = \"footer-left\">");
            client.println("Autors : <a href = \"https://github.com/junjielyu13\"> @Junjie Li,");
            client.println("</a>");
            client.println("<a href = \"https://github.com/TheExorcit\"> @Manuel Liu Wang.</a>");
            client.println("</div>");
            client.println("<div class = \"footer-right\">©2022 Xarxa, UB.</ div>");
            client.println("</div>");
            client.println("</div>");
            client.println("</body>");
            client.println("</html>");

            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
          currentLine += c;
        }
      }
    }
    header = "";    // Clear the header variable
    client.stop();  // Close the connection
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}