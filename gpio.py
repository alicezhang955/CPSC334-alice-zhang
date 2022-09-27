import RPi.GPIO as GPIO
import time

state = 0
butpin = 23
swpin = 17
joypin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(butpin, GPIO.IN)
GPIO.setup(swpin, GPIO.IN)
GPIO.setup(joypin, GPIO.IN)

def swinput(state, input):
    if not input:
        if state == 0:
            print("sw on")
        elif state == 1:
            print("sW oN")
        else:
            print("SW ON")

def joyinput(state, input):
    if not input:
        if state == 0:
            print("joy left")
        elif state == 1:
            print("jOy LeFt")
        else:
            print("JOY LEFT")


while True:
    if GPIO.input(butpin):
        if state == 0:
            state = 1
        elif state == 1:
            state = 2
        else:
            state = 0

    joyinput(state, GPIO.input(joypin))
    swinput(state, GPIO.input(swpin))

    time.sleep(1)