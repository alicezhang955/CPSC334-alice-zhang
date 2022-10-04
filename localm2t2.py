import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import serial
import time
import random
import numpy as np

butpin1 = 26
butpin2 = 0

swpin = 16

subpin1 = 6
subpin2 = 0

resetpin = 5
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
        port1 = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
        port2 = serial.Serial("/dev/ttyUSB1", 115200, timeout=1)
        # port2 = serial.Serial("/dev/ttyUSB1", 115200, timeout=1)

    except: # Bad way of writing excepts (always know your errors)
        if(time.time() - prev > 2): # Don't spam with msg
            print("No serial detected, please plug your uController")
            prev = time.time()

    if(port1 is not None and port2 is not None): # We're connected
        SETUP = True
        print("connected")


def button_callback1(channel):
    print("Reset board!")
    reset_board = "b\n"
    port1.write(reset_board.encode())
    return;

def resetTarget(channel):
    global target
    reset_mem = "t "

    for i in range(3):
        target[i] = random.randint(0, 255)
        reset_mem = reset_mem + str(target[i]) + " "
    print("Reset target!")
    reset_mem = reset_mem + '\n'
    port1.write(reset_mem.encode())
    print(reset_mem)

    return;

def submitColor1(channel):
    print("Submit color!")
    sub_col = "s\n"
    port1.write(sub_col.encode())
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
    # GPIO.add_event_detect(butpin,GPIO.RISING,callback=button_callback, bouncetime = 500) 
    return;

def winnerFlash(player):
    global winner
    global gameOver
    gameOver = 1

    for i in range(3):
        winner[i] = 0

    string = "w" + player + '\n'
    port1.write(string.encode())
    print("Flashing Winner" + player + "!")
    return;

def reset_game(channel):
    global gameOver
    gameOver = 0
    string = "r\n"
    port1.write(string.encode())
    print("Reset game!")
    return;


def main():
    global butpin
    global target
    global swpin
    global subpin
    global resetpin
    global read_state
    global gameOver

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(butpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(resetpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(swpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(subpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(butpin1,GPIO.RISING,callback=button_callback1, bouncetime = 500) 
    # GPIO.add_event_detect(butpin2,GPIO.RISING,callback=button_callback, bouncetime = 500) 
    GPIO.add_event_detect(resetpin,GPIO.RISING,callback=reset_game, bouncetime = 500) 
    GPIO.add_event_detect(swpin,GPIO.RISING,callback=resetTarget, bouncetime = 500)
    GPIO.add_event_detect(subpin1,GPIO.RISING,callback=submitColor1, bouncetime = 500) 
    # GPIO.add_event_detect(subpin2,GPIO.RISING,callback=submitColor, bouncetime = 500) 

    while(1):
        time.sleep(0.5)

        if(not gameOver):
            for i in range(3):
                if(winner[i] == 1):
                    winnerFlash(str(i))

        string = port1.read()
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
                    # GPIO.remove_event_detect(butpin)
                    extractVals(val_string)
                else:
                    val_string += string
                
                


if __name__=="__main__":
    main()
