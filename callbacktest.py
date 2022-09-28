import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

state = 0
state_change = 0

def button_callback(channel):
    print("Button was pushed!")
    global state_change
    state_change  = 1

def main():
    global state
    global state_change
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM) # Use physical pin numbering
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(27,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
    #message = input("Press enter to quit\n\n") # Run until someone presses enter
    print("before while")
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

    GPIO.cleanup() # Clean up

if __name__=="__main__":
    main()
