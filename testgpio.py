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
			print("no sw")
		else:
			print("SW ON")

def joyinput(state, input):
	if not input:
    		if state == 0:
    			print("joy left")
		elif state == 1:
			print("tfel yoj")
		else:
			print("JOY LEFT")
    		

while True:
	# joyinput = GPIO.input(24)
	# print(joyinput)
	# if GPIO.input(butpin):
	# 	print("button not pressed")
	# else:
	# 	print("button presed")

	# if GPIO.input(swpin):
	# 	print("sw off")
	# else:
	# 	print("sw on")

	if GPIO.input(butpin):
	    	if state == 0:
    			state = 1
		elif state == 1:
    			state = 2
		else:
    			state = 0

	swinput(state, GPIO.input(swpin)
	joyinput(state, GPIO.input(joypin)
	time.sleep(1)

