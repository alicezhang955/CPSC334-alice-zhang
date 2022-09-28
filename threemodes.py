import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

state = 0
state_change = 0
butpin = 27
swpin = 17
joypin = 22

def button_callback(channel):
    print("State change!")
    global state_change
    state_change  = 1

def swinput(state, input):
    if input:
        if state == 0:
            print("sw on")
        elif state == 1:
            print("sW oN")
        else:
            print("SW ON")

def joyinput(state, input):
    if input:
        if state == 0:
            print("joy left")
        elif state == 1:
            print("jOy LeFt")
        else:
            print("JOY LEFT")

def main():
    global state
    global state_change
    global butpin
    global swpin
    global joypin
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(butpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(swpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(joypin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(butpin,GPIO.RISING,callback=button_callback) 

    while True:
        print(state_change, state)
        time.sleep(1)
        if state_change:
            if state == 0:
                state = 1
            elif state == 1:
                state = 2
            else:
                state = 0
            state_change = 0
        print(state)
        joyinput(state, GPIO.input(joypin))
        swinput(state, GPIO.input(swpin))

    GPIO.cleanup() # Clean up

if __name__=="__main__":
    main()
