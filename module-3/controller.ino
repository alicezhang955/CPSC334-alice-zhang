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
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

const int touchPin = 4;  
const int freq = 400;
const int ledChannel = 0;
const int resolution = 8;

int z;
uint8_t broadcastAddress[] = {0x30, 0xAE, 0xA4, 0xDF, 0xB6, 0xB4};

typedef struct struct_message {
    int id; 
    int y;
    int z;
    int state;
} struct_message;

struct_message myData;

esp_now_peer_info_t peerInfo;

// callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}
 
void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  esp_now_register_send_cb(OnDataSent);
  
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }
  mpu.begin();
  Serial.println("MPU6050 Found!");
}
 
void loop() {
	sensors_event_t a, g, temp;
	mpu.getEvent(&a, &g, &temp);

  myData.id = 1;
  myData.y = a.acceleration.y;
  myData.z = a.acceleration.z;

  int input = touchRead(touchPin);
  if(input > 30){
    myData.state = 0;
  }
  else{
    myData.state = 1;
  }

  Serial.println(myData.state);

  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));
   
  if (result == ESP_OK) {
    Serial.println("Sent with success");
  }
  else {
    Serial.println("Error sending the data");
  }

  delay(500);
}