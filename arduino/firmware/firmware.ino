#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

#include <NTPClient.h>
#include <WiFiUdp.h>

#include ".env/credentials.h"
#include ".env/api.h"

#define RST_PIN 5
#define SS_PIN 4

MFRC522 mfrc522(SS_PIN, RST_PIN);
int scan_delay = 20;

// Define UTC offset
int utcOffset = 1; // 1 = Winter, 2 = Summer
int utcOffsetInSeconds = utcOffset * 60 * 60;
int updateInterval = 1000;

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds, updateInterval);

void setup()
{
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();
  delay(10);
  Serial.println('\n');

  WiFi.begin(SSID, PASSWORD); // Connect to the network
  Serial.println("Connecting to " + String(SSID) + " ...");

  for (int i = 1; WiFi.status() != WL_CONNECTED; i++)
  {
    delay(1000);
    Serial.print(String(i) + " ");
  }

  Serial.print("\nConnection established!\nIP address:\t");
  Serial.println(WiFi.localIP());

  timeClient.begin();
  timeClient.update();
  if(timeClient.isTimeSet() == false)
  {
    timeClient.forceUpdate();
  }
}

void loop()
{
  if (scan_delay >= 20)
  {
    scan_delay = 0;
    if (!mfrc522.PICC_IsNewCardPresent())
      return;
    if (!mfrc522.PICC_ReadCardSerial())
      return;

    String epochTime = "";
    String uid = "";

    for (byte i = 0; i < mfrc522.uid.size; i++)
      uid.concat(String(mfrc522.uid.uidByte[i], HEX));
    Serial.println("\nUID: " + uid);

    if (WiFi.status() == WL_CONNECTED)
    {
      WiFiClient client;
      HTTPClient http;
      String serverPath = String(API_ADDRESS) + "/log";
      
      
      epochTime = String(timeClient.getEpochTime()); 

      Serial.println("TIME: " + epochTime + " (" + timeClient.getFormattedTime() + ")");

      http.begin(client, serverPath.c_str());
      http.addHeader("Content-Type", "application/json");

      int httpResponseCode = http.POST("{\"key\": \"" + String(API_KEY) + "\",\"data\":{\"UID\": \"" + uid + "\",\"TIME\": \"" + epochTime +"\"}");

      if (httpResponseCode > 0)
      {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
      }
      else
      {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
        // String payload = http.getString();
        // Serial.println(payload);
      }
      http.end();
    }
    else
    {
      Serial.println("Error: WiFi Disconnected");
    }
  }
  else
  {
    delay(10);
    scan_delay++;
  }
}
