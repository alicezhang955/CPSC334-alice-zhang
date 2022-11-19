#include <Stepper.h>
#include <Wire.h>
#include <MPU6050_light.h>
#include <ESP32Servo.h>

Servo myservo; 

int pos = 0;    
int state = 0;
// Recommended PWM GPIO pins on the ESP32 include 2,4,12-19,21-23,25-27,32-33 
int servoPin = 12;
int photoPin = 34;

MPU6050 mpu(Wire);
unsigned long timer1 = 0;
unsigned long timer2 = 0;

const int stepsPerRevolution = 2048;  

int light_thres = 2500;

// ULN2003 Motor Driver Pins
#define IN1 19
#define IN2 18
#define IN3 5
#define IN4 17

// initialize the stepper library
Stepper stepper(stepsPerRevolution, IN1, IN3, IN2, IN4);

int x_rot;
int x_accel;

int prev_z = 0;

void setup() {
  Serial.begin(115200);
  stepper.setSpeed(5);
  Wire.begin();
  byte status = mpu.begin();
  delay(1000);
  mpu.calcOffsets(); // gyro and accelero
  ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	myservo.setPeriodHertz(50);    
	myservo.attach(servoPin, 500, 2400);
}

void loop() {
  int photo_value = analogRead(photoPin);
  mpu.update();
  if ((millis() - timer1) > 500) {
    int difference = prev_z - mpu.getAngleZ();

    if(difference > 10 || difference < -10){
      int steps = stepsPerRevolution*difference/360;
      Serial.println(difference);
      Serial.println(steps);
      stepper.step(steps);
    }

    prev_z = mpu.getAngleZ();
    timer1 = millis();
    }

    // if((millis() - timer2) > 10){
    //   Serial.print("Z : ");
    //   Serial.println(mpu.getAngleZ());
    // }

  if(photo_value < light_thres){ //open flower
    state = 1;
  }
  else{
    state = 2; //close flower
  }
 
  if(state == 1){
    pos += 1;
    if(pos >= 180){
      state = 0;
      pos = 180;
    }
  }
  else if(state == 2){
    pos -= 1;
    if(pos <= 0){
      state = 0;
      pos = 0;
    }
  }
  
  // Serial.println(state);
  // Serial.println(photo_value);
  // Serial.println(pos);
  // myservo.write(pos);
  delay(100);
}