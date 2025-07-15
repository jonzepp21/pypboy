import RPi.GPIO as GPIO
import os
import threading
import time

GPIO.setmode(GPIO.BCM)
SHUTDOWN_PIN = 3

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(SHUTDOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(SHUTDOWN_PIN, GPIO.FALLING, callback=shutdown_pi, bouncetime=2000)
	
def shutdown_pi(channel):
	print("Power button pressed.  Shutting down...")
	time.sleep(0.5)
	os.system("sudo shutdown -h now")
