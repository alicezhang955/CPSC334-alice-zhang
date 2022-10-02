import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import serial
import time

butpin = 26
SETUP = False
MAX_BUFF_LEN = 255
port = None

target = [0, 0, 0]

prev = time.time()

while(not SETUP):
    try:
    # 					 Serial port(windows-->COM), baud rate, timeout msg
        port = serial.Serial("/dev/ttyUSB3", 115200, timeout=1)

    except: # Bad way of writing excepts (always know your errors)
        if(time.time() - prev > 2): # Don't spam with msg
            print("No serial detected, please plug your uController")
            prev = time.time()

    if(port is not None): # We're connected
        SETUP = True
        print("connected")


def button_callback(channel):
    print("Reset board!")
    port.write(1)

def read_ser(num_char = 1):
    string = port.read(num_char)
    return string.decode()

def main():
    global butpin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(butpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(butpin,GPIO.RISING,callback=button_callback, bouncetime = 500) 

    while(1):
        time.sleep(1)


if __name__=="__main__":
    main()
