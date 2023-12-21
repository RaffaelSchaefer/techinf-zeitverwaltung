#include <SPI.h>      
#include <MFRC522.h>  

#define RST_PIN     5          
#define SS_PIN      4 

MFRC522 mfrc522(SS_PIN, RST_PIN);
String last_card = "";

void setup() {
  Serial.begin(115200);   
  SPI.begin();      
  mfrc522.PCD_Init();   
}

void loop() {
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  String new_card = "";
  //Zeigt die UID im serial monitor
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    new_card.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    new_card.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  if (new_card != last_card) {
    last_card = new_card;
    Serial.println();
    Serial.print(" UID tag  :"+ new_card);
  }
} 
