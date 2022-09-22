
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
	

while True:
	joyinput = GPIO.input(24)
	print(joyinput)
	if GPIO.input(butpin):
		print("button not pressed")
	else:
		print("button presed")

	if GPIO.input(swpin):
		print("sw off")
	else:
		print("sw on")


	time.sleep(1)

