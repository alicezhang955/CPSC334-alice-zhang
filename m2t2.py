import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import serial
import time
import random
import numpy as np

butpin = 26
swpin = 16
subpin = 6
SETUP = False
MAX_BUFF_LEN = 255
port = None

read_state = 0

target = [0, 0, 0]

prev = time.time()

winner = [0, 0, 0]

gameOver = 0

while(not SETUP):
    try:
    # 					 Serial port(windows-->COM), baud rate, timeout msg
        port = serial.Serial("/dev/ttyUSB2", 115200, timeout=1)

    except: # Bad way of writing excepts (always know your errors)
        if(time.time() - prev > 2): # Don't spam with msg
            print("No serial detected, please plug your uController")
            prev = time.time()

    if(port is not None): # We're connected
        SETUP = True
        print("connected")


def button_callback(channel):
    print("Reset board!")
    reset_board = "b\n"
    port.write(reset_board.encode())
    return;

def resetTarget(channel):
    global target
    reset_mem = "t "

    for i in range(3):
        target[i] = random.randint(0, 255)
        reset_mem = reset_mem + str(target[i]) + " "
    print("Reset target!")
    reset_mem = reset_mem + '\n'
    port.write(reset_mem.encode())
    print(reset_mem)

    return;

def submitColor(channel):
    print("Submit color!")
    sub_col = "s\n"
    port.write(sub_col.encode())
    return;

def calculateDist(val1, val2, val3, player):
    global target
    global winner
    distance = np.sqrt((val1 - target[0])**2 + (val2 - target[1])**2 + (val3 - target[2])**2)
    print("vals = ", val1, val2, val3, target[0], target[1], target[2], "distance = ", distance)
    if(distance < 100):
        winner[player] = 1
        print("WINNER = ", player)
    return;


def extractVals(string):
    global target
    count = 0
    val1 = ""
    val2 = ""
    val3 = ""

    player = string[1]

    for i in range(len(string)):
        if(string[i] == " "):
            count += 1

        if(count == 1):
            val1 += string[i]
        elif(count == 2):
            val2 += string[i]
        elif(count == 3):
            val3 += string[i]


    print("player: ", player, " val1: ", val1, " val2: ", val2, " val3: ", val3)
    calculateDist(int(val1), int(val2), int(val3), int(player))
    GPIO.add_event_detect(butpin,GPIO.RISING,callback=button_callback, bouncetime = 500) 
    return;

def winnerFlash(player):
    global gameOver
    gameOver = 1
    string = "w" + player + '\n'
    port.write(string.encode())
    print("Flashing Winner" + player + "!")
    return;


def main():
    global butpin
    global target
    global swpin
    global subpin
    global read_state
    global gameOver

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(butpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(swpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(subpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(butpin,GPIO.RISING,callback=button_callback, bouncetime = 500) 
    GPIO.add_event_detect(swpin,GPIO.RISING,callback=resetTarget, bouncetime = 500)
    GPIO.add_event_detect(subpin,GPIO.RISING,callback=submitColor, bouncetime = 500) 

    while(1):
        time.sleep(0.5)

        if(not gameOver):
            for i in range(3):
                if(winner[i] == 1):
                    winnerFlash(str(i))

        string = port.read()
        string = string.decode()
        if(len(string)):
            print("String: ", string)
            if(string == "p"):
                val_string = ""
                read_state = 1
            if(read_state > 0):
                if(string == "d"):
                    read_state = 0
                    print(val_string)
                    GPIO.remove_event_detect(butpin)
                    extractVals(val_string)
                else:
                    val_string += string
                
                


if __name__=="__main__":
    main()
