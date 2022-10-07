import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import serial
import time
import random
import numpy as np

reset_button_1 = 16 
reset_button_2 = 17
reset_button_3 = 27

randomize_color_switch = 26 

submit_switch_1 = 6 
submit_switch_2 = 24
submit_switch_3 = 23

reset_game_pin = 5

SETUP = False
MAX_BUFF_LEN = 255

port1 = None
port2 = None
port3 = None

target = [0, 0, 0]

prev = time.time()

while(not SETUP):
    try:
    # 					 Serial port(windows-->COM), baud rate, timeout msg
        port1 = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
        port2 = serial.Serial("/dev/ttyUSB1", 115200, timeout=1)
        port3 = serial.Serial("/dev/ttyUSB2", 115200, timeout=1)

    except: # Bad way of writing excepts (always know your errors)
        if(time.time() - prev > 2): # Don't spam with msg
            print("No serial detected, please plug your uController")
            prev = time.time()

    if(port1 is not None and port2 is not None and port3 is not None): # We're connected //and port2 is not None
        SETUP = True
        print("connected")


def reset_board_1(channel):
    print("Reset board!")
    reset_board = "b\n"
    port1.write(reset_board.encode())
    return;

def reset_board_2(channel):
    print("Reset board!")
    reset_board = "b\n"
    port2.write(reset_board.encode())
    return;

def reset_board_3(channel):
    print("Reset board!")
    reset_board = "b\n"
    port3.write(reset_board.encode())
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
    port2.write(reset_mem.encode())
    port3.write(reset_mem.encode())
    print(reset_mem)

    return;

def submit_color_1(channel):
    print("Submit color!")
    sub_col = "s\n"
    port1.write(sub_col.encode())
    return;

def submit_color_2(channel):
    print("Submit color!")
    sub_col = "s\n"
    port2.write(sub_col.encode())
    return;

def submit_color_3(channel):
    print("Submit color!")
    sub_col = "s\n"
    port3.write(sub_col.encode())
    return;

def winnerFlash(player):
    print("Flashing Winner" + str(player) + "!")
    return;

def reset_game(channel):
    global target
    string = "r\n"
    port1.write(string.encode())
    port2.write(string.encode())
    port3.write(string.encode())

    target = [0, 0, 0]
    print("Reset game!")
    return;


def main():
    global reset_button_1
    global reset_button_2
    global reset_button_3

    global submit_switch_1
    global submit_switch_2
    global submit_switch_3

    global reset_game_pin
    global randomize_color_switch

    global target

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(reset_button_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(reset_button_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(reset_button_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.setup(submit_switch_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(submit_switch_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(submit_switch_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.setup(reset_game_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(randomize_color_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    GPIO.add_event_detect(reset_button_1,GPIO.RISING,callback=reset_board_1, bouncetime = 500) 
    GPIO.add_event_detect(reset_button_2,GPIO.RISING,callback=reset_board_2, bouncetime = 500) 
    GPIO.add_event_detect(reset_button_3,GPIO.RISING,callback=reset_board_3, bouncetime = 500) 
    
    GPIO.add_event_detect(submit_switch_1,GPIO.RISING,callback=submit_color_1, bouncetime = 500) 
    GPIO.add_event_detect(submit_switch_2,GPIO.RISING,callback=submit_color_2, bouncetime = 500) 
    GPIO.add_event_detect(submit_switch_3,GPIO.RISING,callback=submit_color_3, bouncetime = 500) 

    GPIO.add_event_detect(reset_game_pin,GPIO.RISING,callback=reset_game, bouncetime = 500) 
    GPIO.add_event_detect(randomize_color_switch,GPIO.RISING,callback=resetTarget, bouncetime = 500)

    while(1):

        string1 = port1.read()
        string1 = string1.decode()
        if(len(string1)):
            if(string1 == "w"):
                winnerFlash(0)

        string2 = port2.read()
        string2 = string2.decode()
        if(len(string2)):
            if(string2 == "w"):
                winnerFlash(1)

        string3 = port3.read()
        string3 = string3.decode()
        if(len(string3)):
            if(string3 == "w"):
                winnerFlash(2)
                
            
if __name__=="__main__":
    main()
