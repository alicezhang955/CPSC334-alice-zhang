#include <EasyButton.h>

#define NO_STATE 0
#define B_STATE 1
#define T_STATE 2
#define S_STATE 3
#define W_STATE 4
#define R_STATE 5
#define CMD_BUFF_LEN 13

int rled = 23;
int rval = 0;
int bled = 22;
int bval = 0; 
int gled = 21;
int gval = 0;

int rledMain = 0;
int bledMain = 2;
int gledMain = 15;

int ledArray[3] = {0, 0, 0}; //0 = red, 1 = green, 2 = blue
int mainLed[3] = {0, 0, 0};

int state = 0;

int joypin = 25;
EasyButton button(33);

int clearBoard = 0;

char c; // IN char
char str[CMD_BUFF_LEN];
uint8_t idx = 0; // Reading index
String bufferRead;

int comstate = 0;

void setColors(int joyinput, int state){ //state = color index, increment = -1, 0, 1
  int increment;
  if(joyinput < 100){
    increment = -1;
  }
  else if(joyinput > 4000){
    increment = 1;
  }
  else{
    increment = 0;
  }
  ledArray[state] += increment * 5;

  if(ledArray[state] > 255){
    ledArray[state] = 255;
  }
  else if(ledArray[state] < 0){
    ledArray[state] = 0;
  }
}

void setState(){
  if(state == 0){
    state = 1;
  }
  else if(state == 1){
    state = 2;
  }
  else{
    state = 0;
  }
}

int interpret(char c){
  if(c == 'b'){
    return B_STATE;
  }
  else if(c == 't'){
    return T_STATE; 
  }
  else if(c == 's'){
    return S_STATE;
  }
  else if(c == 'w'){
    return W_STATE;
  }
  else if(c == 'r'){
    return R_STATE;
  }
  else{
    return NO_STATE;
  }

}

int calculateDist(){
  int val1 = ledArray[0];
  int val2 = ledArray[1];
  int val3 = ledArray[2];
  int ret = 0;

  double distance = sqrt((val1 - mainLed[0])^2 + (val2 - mainLed[1])^2 + (val3 - mainLed[2])^2);

  if(distance < 100){
    ret = 1;
  }

  return ret;
}

void setup(){
  Serial.begin(115200);          //  setup serial
  pinMode(rled, OUTPUT);
  pinMode(bled, OUTPUT);
  pinMode(gled, OUTPUT);
  pinMode(rledMain, OUTPUT);
  pinMode(bledMain, OUTPUT);
  pinMode(gledMain, OUTPUT);
  pinMode(joypin, INPUT);
  button.begin();
  button.onPressed(setState);
}

void loop(){
  button.read(); 
  if(Serial.available() > 0){
    c = Serial.read();
    if(c != '\n'){ // Still reading
      str[idx++] = c; // Parse the string byte (char) by byte
    }
    else{ // Done reading
      str[idx] = '\0'; // Convert it to a string
      comstate = interpret(str[0]);
      
      if(comstate == T_STATE){
        int i1, i2, i3;
        if (3 == sscanf(str, "%*[^0123456789]%d%*[^0123456789]%d%*[^0123456789]%d", &i1, &i2, &i3)){
          mainLed[0] = i1;
          mainLed[1] = i2;
          mainLed[2] = i3;
        }
      }
      idx = 0;
    }
  }
  if(millis() % 500 == 0){
    int joyinput = analogRead(joypin);
    setColors(joyinput, state);

    if(comstate == B_STATE){
      ledArray[0] = 0;
      ledArray[1] = 0;
      ledArray[2] = 0;     
      comstate = NO_STATE;
    }
    else if(comstate == T_STATE){
      comstate = NO_STATE;
    }
    else if(comstate == S_STATE){ //calculate in ESP
      int win = calculateDist();

      if(win){
        Serial.write("w");
        comstate = W_STATE;
      }
      else{
        comstate = NO_STATE;
      }
    }
    else if(comstate == W_STATE){
      if(millis() % 1000 >= 500){
        ledArray[0] = 0;
        ledArray[1] = 0;
        ledArray[2] = 0;
      }
      else{
        ledArray[0] = 255;
        ledArray[1] = 255;
        ledArray[2] = 255;        
      }
    }
    else if(comstate == R_STATE){
        ledArray[0] = 0;
        ledArray[1] = 0;
        ledArray[2] = 0;
        mainLed[0] = 0;
        mainLed[1] = 0;
        mainLed[2] = 0;      
      comstate = NO_STATE;
    }
    analogWrite(rledMain, mainLed[0]);
    analogWrite(gledMain, mainLed[1]);
    analogWrite(bledMain, mainLed[2]);
    analogWrite(rled, ledArray[0]);
    analogWrite(gled, ledArray[1]);
    analogWrite(bled, ledArray[2]);
    // Serial.println(ledArray[0]);
    // Serial.println(ledArray[1]);
    // Serial.println(ledArray[2]);
  }
}