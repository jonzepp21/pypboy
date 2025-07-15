from gpiozero import Button
from time import sleep

clk = Button(17, pull_up=True)
dt = Button(27, pull_up=True)
#sw = Button(22, pull_up=True)

def dial_up():
    trigger_action("dial_up")
    sleep(0.002)
    
def dial_down():
    trigger_action("dial_down")
    sleep(0.002)

button_dial_up.when_pressed = dial_up
button_dial_down.when_pressed = dial_down

