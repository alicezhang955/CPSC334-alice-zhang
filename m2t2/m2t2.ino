#include <EasyButton.h>

#define NO_STATE 0
#define B_STATE 1
#define T_STATE 2
#define CMD_BUFF_LEN 13

int rled = 23;
int rval = 0;
int bled = 22;
int bval = 0; 
int gled = 21;
int gval = 0;

int rledMain = 7;
int bledMain = 8;
int gledMain = 15;

int ledArray[3] = {0, 0, 0}; //0 = red, 1 = green, 2 = blue
int mainLed[3] = {100, 200, 100};

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
    increment = 1;
  }
  else if(joyinput > 4000){
    increment = -1;
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

void setMainLed(int r, int g, int b){
  mainLed[0] = r;
  mainLed[1] = g;
  mainLed[2] = b;
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
  // Serial.write(c);
  if(c == 'b'){
    return B_STATE;
  }
  else if(c == 't'){
    return T_STATE; 
  }
  else{
    return NO_STATE;
  }

}

void setup(){
  Serial.begin(115200);          //  setup serial
  pinMode(rled, OUTPUT);
  pinMode(bled, OUTPUT);
  pinMode(gled, OUTPUT);
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
      // Serial.write(c);
    }
    else{ // Done reading
      str[idx] = '\0'; // Convert it to a string
      comstate = interpret(str[0]);
      
      if(comstate == T_STATE){
          int i;
          char *ptr = str;
          while (*ptr) { 
              if (isdigit(*ptr) || ( (*ptr=='-'||*ptr=='+') && isdigit(*(ptr+1)) )) {
                  i = 1;
                  Serial.write("G");
                  mainLed[i] = strtol(ptr, &ptr, 10); 
                  i++;
              } else { 
                  ptr++; 
              } 
          }
      }
      idx = 0;
    }
  }
  if(millis() % 500 == 0){
    int joyinput = analogRead(joypin);
    setColors(joyinput, state);

    if(comstate == B_STATE){
      Serial.write("B");
      ledArray[0] = 0;
      ledArray[1] = 0;
      ledArray[2] = 0;     
      comstate = NO_STATE;
    }
    else if(comstate == T_STATE){
      // Serial.write("A");
      ledArray[0] = mainLed[0];
      ledArray[1] = mainLed[1];
      ledArray[2] = mainLed[2];
      if(mainLed[0] > mainLed[1]){
        Serial.write("P");
      }
      // if(mainLed[0] > mainLed[2]){
      //   Serial.write("Y");
      // }
      // if(mainLed[1] > mainLed[2]){
      //   Serial.write("M");
      // }
      // analogWrite(rledMain, mainLed[0]);
      // analogWrite(gledMain, mainLed[1]);
      // analogWrite(bledMain, mainLed[2]);
      comstate = NO_STATE;
    }
    // analogWrite(rledMain, mainLed[0]);
    // analogWrite(gledMain, mainLed[1]);
    // analogWrite(bledMain, mainLed[2]);
    analogWrite(rled, ledArray[0]);
    analogWrite(gled, ledArray[1]);
    analogWrite(bled, ledArray[2]);
    // Serial.println(ledArray[0]);
    // Serial.println(ledArray[1]);
    // Serial.println(ledArray[2]);


  }
}