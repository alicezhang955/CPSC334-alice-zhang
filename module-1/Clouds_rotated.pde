import java.util.*;

Random random = new Random();

int numScreen = 6;
float scoffsetx = 1680;
float scoffsety = 1060;

cloud [] clouds;
int numCloud = 15;

float maxSP = 8;
float minSP = 2;
int xdim = 4080 * 2;
int ydim = 768;
int [] starMod;

float [] starx;
float [] stary;
int numStar = 80;

int [] dotMod;
float [] dotx;
float [] doty;
int numDot = 80;

moon moo;
int ncrater = 6;
float r1 = 100;
float r2 = 40;
float moonx = 150 + xdim/numScreen * 2 + scoffsetx;
float moony = ydim - r1 - 50;

void setup() {
 fullScreen(SPAN);
 size(8156, 766);
 fill(225, 50);
 noStroke();
 clouds = new cloud[numCloud];
 for (int i = 0; i < numCloud; i++) {
  clouds[i] = new cloud();
 }

 starx = new float[numStar];
 stary = new float[numStar];
 starMod = new int[numStar];
 
 for (int i = 0; i < numStar; i++) {
  starMod[i] = (int) random(60, 120); 
 }
 
 dotx = new float[numDot];
 doty = new float[numDot];
 dotMod = new int[numDot];
 
 for (int i = 0; i < numDot; i++) {
  dotMod[i] = (int) random(60, 120); 
 }
 
 moo = new moon();
 
}

void draw() {
  background(12, 23, 34);
  for (int i = 0; i < numStar; i++) {
    if (frameCount % starMod[i] == 0) {
      starx[i] = random(0,xdim) + scoffsetx;
      stary[i] = random(0,ydim);  
    }
    
    pushStyle();
    if (frameCount % starMod[i] < starMod[i]/2) {
      fill(204, 153, 0, 255 * (frameCount % starMod[i])/(starMod[i]/2));
    }
    else {
      fill(204, 153, 0, 255 * (starMod[i] - (frameCount % starMod[i]))/(starMod[i]/2));    
    }
    
    star(starx[i], stary[i], 2.5, 15);
    popStyle();
  }
  
  for (int i = 0; i < numDot; i++) {
    if (frameCount % dotMod[i] == 0) {
      dotx[i] = random(0,xdim) + scoffsetx;
      doty[i] = random(0,ydim);  
    }
    
    pushStyle();
    if (frameCount % dotMod[i] < dotMod[i]/2) {
      fill(255, 255 * (frameCount % dotMod[i])/(dotMod[i]/2));
    }
    else {
      fill(255, 255 * (dotMod[i] - (frameCount % dotMod[i]))/(dotMod[i]/2));    
    }
    
    circle(dotx[i], doty[i], 5);
    popStyle();
  }
  
  moo.display();
  
  fill(180, 50);
  
  for (int i = 0; i < numCloud; i++) {
    clouds[i].display();
    clouds[i].move();
  }
}

class cloud {
  float speed;
  int numCir;
  float yoffset;
  float[] counter;
  float ycenter;
  float[] yamp;
  float[] ypos;
  float[] yposorig;
  float[] xpos;
  float[] size;
  float xlower;
  float xupper;
  float ylower;
  float yupper;
  
  cloud(){
    setCloud();
  }

  void move () {
    for (int i = 0; i < numCir; i++){
      counter[i] += 0.1;
      xpos[i] -= speed;
      ypos[i] = yposorig[i] + yamp[i]*sin(counter[i]*yoffset);
      
      if(xpos[i] < -90) {
        if(yposorig[i] >= xdim/numScreen * 3 + scoffsetx && yposorig[i] <= xdim/numScreen * 4 + scoffsetx) { //screen 4
          if(getXpos() < -90){
            setCloud();
          }
        }
        else if(yposorig[i] <= xdim/numScreen + scoffsetx) { //screen 3
          xpos[i] = ydim + 150;
          yposorig[i] += xdim/numScreen * 5;
        }
        else {
          if((yposorig[i] >= xdim/numScreen + scoffsetx && yposorig[i] <= xdim/numScreen * 2 + scoffsetx) || (yposorig[i] >= xdim/numScreen * 5 + scoffsetx)) {
            xpos[i] = ydim + 500;
          }
          else {
            xpos[i] = ydim + 150;
          }
          yposorig[i] -= xdim/numScreen;
        }
      }
    }
  }
  
  void display() {
    for (int i = 0; i < numCir; i++) {
     circle(ypos[i], xpos[i], size[i]);
    }
  }
  
  float getXpos() {
    float lastCir = -100;
    for (int i = 0; i < numCir; i++) {
      if (lastCir < xpos[i]) {
        lastCir = xpos[i];
      }
    }
   return lastCir; 
  }
  
  void setCloud() {
    speed = random(minSP, maxSP);
    numCir = (int) random(20,40);
    ycenter = (int) random(200, xdim/numScreen - 200) + scoffsetx;
    yoffset = random(0.5, 0.9);
    xlower = random(100, 300);
    xupper = random(500, 700);
    ylower = random(-80, -50);
    yupper = random(50, 80);
    
    xpos = new float[numCir];
    size = new float[numCir];
    ypos = new float[numCir];
    yposorig = new float[numCir];
    yamp = new float[numCir];
    counter = new float[numCir];
    

    for (int i = 0; i < numCir; i++) {
     xpos[i] = random(random(xlower, 200), random(400, xupper)) + ydim;
     size[i] = random(50, 100)*2;
     ypos[i] = random(ylower, yupper) + ycenter + xdim/numScreen * 2;
     yposorig[i] = ypos[i];
     yamp[i] = random(8, 15);
     counter[i] = random(0,PI/yoffset);
    }    
  }
}

void star(float x, float y, float rad1, float rad2) {
  float angle = 2*PI / 8;
  float state = 1;
  
  beginShape();
  for (int i = 0; i < 8; i++) {
    if (state == 0) {
      float xcoor = x + rad1*cos(angle * i);
      float ycoor = y + rad1*sin(angle * i);
      vertex(xcoor, ycoor);
      state = 1;
    }
    else {
      float xcoor = x + rad2*cos(angle * i);
      float ycoor = y + rad2*sin(angle * i);
      vertex(xcoor, ycoor);
      state = 0;
    }
  }
  endShape(CLOSE);
  
}

class moon{
 float xpos;
 float ypos;
 int numCrater;
 float rad1;
 float rad2;
 float [] craterx;
 float [] cratery;
 float [] cratersize;
 
 moon() {
  xpos = moonx;
  ypos = moony;
  numCrater = ncrater;
  rad1 = r1;
  rad2 = r2;
  craterx = new float[numCrater];
  cratery = new float[numCrater];
  cratersize = new float[numCrater];
  
  for (int i = 0; i < numCrater; i++) {
    float xcneg = (float) (xpos - (rad1 - rad2)/Math.sqrt(1.5));
    float xcpos = (float) (xpos + (rad1 - rad2)/Math.sqrt(1.5));
    float ycneg = (float) (ypos - (rad1 - rad2)/Math.sqrt(1.5));
    float ycpos = (float) (ypos + (rad1 - rad2)/Math.sqrt(1.5));
    craterx[i] = random(xcneg, xcpos);
    cratery[i] = random(ycneg, ycpos);
    cratersize[i] = random(rad2 - 15, rad2 + 25);
  }
 }
 
 void display() {
   pushStyle();
   fill(220, 255);
   circle(xpos, ypos, 2*rad1);
   popStyle();
   
   pushStyle();
   fill(100, 40);
   for (int i = 0; i < numCrater; i++) {
     circle(craterx[i], cratery[i], cratersize[i]);
   }
   popStyle();
 }
}
