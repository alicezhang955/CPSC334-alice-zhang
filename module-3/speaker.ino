/*********
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp-now-many-to-one-esp32/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*********/
#include <esp_now.h>
#include <WiFi.h>

// Structure example to receive data
// Must match the sender structure
typedef struct struct_message {
  int id;
  int y;
  int z;
  int state;
}struct_message;

// Create a struct_message called myData
struct_message myData;

int y;
int yprev;
int z;
int zprev;
int state;

const int ledPin = 25;  // 16 corresponds to GPIO16
const int ledPin2 = 26;

const int freq = 400;
const int ledChannel = 0;
const int ledChannel2 = 2;
const int resolution = 8;


// callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac_addr, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
  yprev = y;
  zprev = z;
  y = myData.y;
  z = myData.z;
  state = myData.state;
  Serial.printf("x value: %d \n", y);
  Serial.printf("y value: %d \n", z);
  Serial.printf("state: %d \n", state);
  Serial.println();
}
 
void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  esp_now_register_recv_cb(OnDataRecv);

  ledcSetup(ledChannel, freq, resolution);
  ledcSetup(ledChannel2, freq, resolution);
  
  ledcAttachPin(ledPin, ledChannel);
  ledcAttachPin(ledPin2, ledChannel2);
}
 
void loop() {

  // if(z <= -8){ledcWriteNote(ledChannel, NOTE_C, 4);} else
  // if(z <= -7){ledcWriteNote(ledChannel, NOTE_Cs, 4);} else
  // if(z <= -6){ledcWriteNote(ledChannel, NOTE_D, 4);} else
  // if(z <= -5){ledcWriteNote(ledChannel, NOTE_Eb, 4);} else
  // if(z <= -3){ledcWriteNote(ledChannel, NOTE_E, 4);} else
  // if(z <= -1){ledcWriteNote(ledChannel, NOTE_F, 4);} else
  // if(z <= 1){ledcWriteNote(ledChannel, NOTE_Fs, 4);} else
  // if(z <= 3){ledcWriteNote(ledChannel, NOTE_G, 4);} else
  // if(z <= 5){ledcWriteNote(ledChannel, NOTE_Gs, 4);} else
  // if(z <= 6){ledcWriteNote(ledChannel, NOTE_A, 4);} else
  // if(z <= 7){ledcWriteNote(ledChannel, NOTE_Bb, 4);} else
  // if(z <= 8){ledcWriteNote(ledChannel, NOTE_B, 4);} else
  // {ledcWriteNote(ledChannel, NOTE_C, 5);}
  if(z != zprev){
    if(z <= -8){ledcWriteNote(ledChannel, NOTE_C, 4);} else
    if(z <= -6){ledcWriteNote(ledChannel, NOTE_D, 4);} else
    if(z <= -3){ledcWriteNote(ledChannel, NOTE_Eb, 4);} else
    if(z <= -1){ledcWriteNote(ledChannel, NOTE_F, 4);} else
    if(z <= 3){ledcWriteNote(ledChannel, NOTE_G, 4);} else
    if(z <= 6){ledcWriteNote(ledChannel, NOTE_Gs, 4);} else
    if(z <= 8){ledcWriteNote(ledChannel, NOTE_Bb, 4);} else
    {ledcWriteNote(ledChannel, NOTE_C, 5);}
  }
  

  // if(y <= -8){ledcWriteNote(ledChannel2, NOTE_C, 4);} else
  // if(y <= -7){ledcWriteNote(ledChannel2, NOTE_Cs, 4);} else
  // if(y <= -6){ledcWriteNote(ledChannel2, NOTE_D, 4);} else
  // if(y <= -5){ledcWriteNote(ledChannel2, NOTE_Eb, 4);} else
  // if(y <= -3){ledcWriteNote(ledChannel2, NOTE_E, 4);} else
  // if(y <= -1){ledcWriteNote(ledChannel2, NOTE_F, 4);} else
  // if(y <= 1){ledcWriteNote(ledChannel2, NOTE_Fs, 4);} else
  // if(y <= 3){ledcWriteNote(ledChannel2, NOTE_G, 4);} else
  // if(y <= 5){ledcWriteNote(ledChannel2, NOTE_Gs, 4);} else
  // if(y <= 6){ledcWriteNote(ledChannel2, NOTE_A, 4);} else
  // if(y <= 7){ledcWriteNote(ledChannel2, NOTE_Bb, 4);} else
  // if(y <= 8){ledcWriteNote(ledChannel2, NOTE_B, 4);} else
  // {ledcWriteNote(ledChannel2, NOTE_C, 5);}


  if(state == 1){
    ledcDetachPin(ledPin2);
  }
  else if(yprev != y){
    ledcAttachPin(ledPin2, ledChannel2);
    if(y <= -8){ledcWriteNote(ledChannel2, NOTE_C, 3);} else
    if(y <= -6){ledcWriteNote(ledChannel2, NOTE_D, 3);} else
    if(y <= -3){ledcWriteNote(ledChannel2, NOTE_Eb, 3);} else
    if(y <= -1){ledcWriteNote(ledChannel2, NOTE_F, 3);} else
    if(y <= 3){ledcWriteNote(ledChannel2, NOTE_G, 3);} else
    if(y <= 6){ledcWriteNote(ledChannel2, NOTE_Gs, 3);} else
    if(y <= 8){ledcWriteNote(ledChannel2, NOTE_Bb, 3);} else
    {ledcWriteNote(ledChannel2, NOTE_C, 4);}    
  }
  

  delay(100); 
}