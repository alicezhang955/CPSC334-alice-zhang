import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

butpin = 26

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


def button_callback(channel):
    print("Reset board!")


def main():

    GPIO.setup(butpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(butpin,GPIO.RISING,callback=button_callback, bouncetime = 500) 

    # while(1):
    #     string = read_ser(MAX_BUFF_LEN)
    #     if(len(string)):
    #         print(string)

    #     cmd = input() # Blocking, there're solutions for this ;)
    #     if(cmd):
    #         write_ser(cmd)


if __name__=="__main__":
    main()