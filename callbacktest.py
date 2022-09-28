import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

def button_callback(channel):
    print("Button was pushed!")
    state_change = 1

def main():
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM) # Use physical pin numbering
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(27,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
    print(state)
    message = input("Press enter to quit\n\n") # Run until someone presses enter

    while True:
        time.sleep(1)
        if state_change:
            if state == 0:
                state = 1
            elif state == 1:
                state = 2
            else:
                state = 0
            state_change = 1
        print(state)

    GPIO.cleanup() # Clean up

if __name__=="__main__":
    state = 0
    state_change = 0
    main()
