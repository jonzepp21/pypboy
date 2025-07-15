try:
	import RPi.GPIO as GPIO
	GPIO_AVAILABLE = True
except ImportError:
	print("[!] GPIO not available, using mock.")
	GPIO_AVAILABLE = False
	
WHITE_LED_PINS = [25, 8]
YELLOW_LED_PINS = [7, 1, 12, 16]
ALL_LED_PINS = WHITE_LED_PINS + YELLOW_LED_PINS

def setup_leds():
	if not GPIO_AVAILABLE:
		return
	
	GPIO.setmode(GPIO.BCM)
	for pin in ALL_LED_PINS:
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.HIGH)
		
def cleanup_leds():
	if not GPIO_AVAILABLE:
		return
	for pin in ALL_LED_PINS:
		GPIO.output(pin, GPIO.LOW)
	GPIO.cleanup()
