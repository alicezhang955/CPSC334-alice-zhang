import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import serial
import time
import random

butpin = 26
swpin = 16
subpin = 6
SETUP = False
MAX_BUFF_LEN = 255
port = None

target = [0, 0, 0]

prev = time.time()

while(not SETUP):
    try:
    # 					 Serial port(windows-->COM), baud rate, timeout msg
        port = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)

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

def submitColor(channel):
    print("Submit color!")
    sub_col = "s\n"
    port.write(sub_col.encode())

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


def main():
    global butpin
    global target
    global swpin
    global subpin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(butpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(swpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(subpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(butpin,GPIO.RISING,callback=button_callback, bouncetime = 500) 
    GPIO.add_event_detect(swpin,GPIO.RISING,callback=resetTarget, bouncetime = 500)
    GPIO.add_event_detect(subpin,GPIO.RISING,callback=submitColor, bouncetime = 500) 

    while(1):
        time.sleep(0.5)

        string = port.read()
        string = string.decode()
        if(len(string)):
            print("String: ", string)


if __name__=="__main__":
    main()
