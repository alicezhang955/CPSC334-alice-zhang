import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import serial
import time
import random
import numpy as np

reset_button_1 = 16
reset_button_2 = 17
reset_button_3 = 27

randomize_color_switch = 0

submit_switch_1 = 6
submit_switch_2 = 24
# submit_switch_3 = 0

reset_game_pin = 5

SETUP = False
MAX_BUFF_LEN = 255

port1 = None
port2 = None
port3 = None

read_state_1 = 0
read_state_2 = 0
read_state_3 = 0

target = [0, 0, 0]

prev = time.time()

winner = [0, 0, 0]

gameOver = 0

while(not SETUP):
    try:
    # 					 Serial port(windows-->COM), baud rate, timeout msg
        port1 = serial.Serial("/dev/ttyUSB1", 115200, timeout=1)
        #port2 = serial.Serial("/dev/ttyUSB3", 115200, timeout=1)
        # port3 = serial.Serial("/dev/ttyUSB2", 115200, timeout=1)

    except: # Bad way of writing excepts (always know your errors)
        if(time.time() - prev > 2): # Don't spam with msg
            print("No serial detected, please plug your uController")
            prev = time.time()

    if(port1 is not None): # We're connected //and port2 is not None
        SETUP = True
        print("connected")


def reset_board_1(channel):
    print("Reset board!")
    reset_board = "b\n"
    port1.write(reset_board.encode())
    return;

# def reset_board_2(channel):
#     print("Reset board!")
#     reset_board = "b\n"
#     port2.write(reset_board.encode())
#     return;

# def reset_board_3(channel):
#     print("Reset board!")
#     reset_board = "b\n"
#     port3.write(reset_board.encode())
#     return;

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

def submit_color_1(channel):
    print("Submit color!")
    sub_col = "s\n"
    port1.write(sub_col.encode())
    return;

# def submit_color_2(channel):
#     print("Submit color!")
#     sub_col = "s\n"
#     port2.write(sub_col.encode())
#     return;

# def submit_color_3(channel):
#     print("Submit color!")
#     sub_col = "s\n"
#     port3.write(sub_col.encode())
#     return;

def calculateDist(val1, val2, val3, player):
    global target
    global winner
    distance = np.sqrt((val1 - target[0])**2 + (val2 - target[1])**2 + (val3 - target[2])**2)
    print("vals = ", val1, val2, val3, target[0], target[1], target[2], "distance = ", distance)
    if(distance < 100):
        winner[player] = 1
        print("WINNER = ", player)
    return;


def extractVals(string, player):
    global target
    count = 0
    val1 = ""
    val2 = ""
    val3 = ""

    # player = string[1]

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
    calculateDist(int(val1), int(val2), int(val3), player)
    # GPIO.add_event_detect(butpin,GPIO.RISING,callback=button_callback, bouncetime = 500) 
    return;

def winnerFlash(player):
    global winner
    global gameOver
    gameOver = 1

    for i in range(3):
        winner[i] = 0

    string = "w" + player + '\n'
    if(player == "1"):
        port1.write(string.encode())
    # elif(player == "2"):
    #     port2.write(string.encode())
    # else:
    #     port3.write(string.encode())
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
    global reset_button_1
    global reset_button_2
    # global reset_button_3

    global submit_switch_1
    global submit_switch_2
    # global submit_switch_3

    global reset_game_pin
    global randomize_color_switch

    global read_state_1
    global read_state_2
    global read_state_3
    global gameOver
    global target

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(reset_button_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(reset_button_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(reset_button_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.setup(submit_switch_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(submit_switch_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.setup(submit_switch_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(reset_game_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(randomize_color_switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    GPIO.add_event_detect(reset_button_1,GPIO.RISING,callback=reset_board_1, bouncetime = 500) 
    # GPIO.add_event_detect(reset_button_2,GPIO.RISING,callback=reset_board_2, bouncetime = 500) 
    # GPIO.add_event_detect(reset_button_3,GPIO.RISING,callback=reset_board_3, bouncetime = 500) 
    
    GPIO.add_event_detect(submit_switch_1,GPIO.RISING,callback=submit_color_1, bouncetime = 500) 
    # GPIO.add_event_detect(submit_switch_2,GPIO.RISING,callback=submit_color_2, bouncetime = 500) 
    # GPIO.add_event_detect(submit_switch_3,GPIO.RISING,callback=submit_color_3, bouncetime = 500) 

    GPIO.add_event_detect(reset_game_pin,GPIO.RISING,callback=reset_game, bouncetime = 500) 
    GPIO.add_event_detect(randomize_color_switch,GPIO.RISING,callback=resetTarget, bouncetime = 500)

    while(1):
        time.sleep(0.5)

        if(not gameOver):
            for i in range(3):
                if(winner[i] == 1):
                    winnerFlash(str(i))

        string1 = port1.read()
        string1 = string1.decode()
        if(len(string1)):
            print("String: ", string1)
            if(string1 == "p"):
                val_string1 = ""
                read_state_1 = 1
            if(read_state_1 > 0):
                if(string1 == "d"):
                    read_state_1 = 0
                    print(val_string1)
                    # GPIO.remove_event_detect(butpin)
                    extractVals(val_string1, 1)
                else:
                    val_string1 += string1

        # string2 = port2.read()
        # string2 = string2.decode()
        # if(len(string2)):
        #     print("String: ", string2)
        #     if(string2 == "p"):
        #         val_string2 = ""
        #         read_state_2 = 1
        #     if(read_state_2 > 0):
        #         if(string2 == "d"):
        #             read_state_2 = 0
        #             print(val_string2)
        #             # GPIO.remove_event_detect(butpin)
        #             extractVals(val_string2, 2)
        #         else:
        #             val_string2 += string2

        # string3 = port3.read()
        # string3 = string3.decode()
        # if(len(string3)):
        #     print("String: ", string3)
        #     if(string3 == "p"):
        #         val_string3 = ""
        #         read_state_3 = 1
        #     if(read_state_3 > 0):
        #         if(string3 == "d"):
        #             read_state_3 = 0
        #             print(val_string3)
        #             # GPIO.remove_event_detect(butpin)
        #             extractVals(val_string3, 3)
        #         else:
        #             val_string3 += string3
                
                


if __name__=="__main__":
    main()
