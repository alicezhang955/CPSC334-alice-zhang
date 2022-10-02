import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import serial
import time

butpin = 26
SETUP = False
MAX_BUFF_LEN = 255
port = None

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

def read_ser(num_char = 1):
    string = port.read(num_char)
    return string.decode()

def main():
    global butpin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(butpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(butpin,GPIO.RISING,callback=button_callback, bouncetime = 500) 

    while(1):
        count = 1
        print(GPIO.input(butpin))

        time.sleep(1)
    #     cmd = input() # Blocking, there're solutions for this ;)
    #     if(cmd):
    #         write_ser(cmd)


if __name__=="__main__":
    main()
