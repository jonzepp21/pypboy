import RPi.GPIO as GPIO
from threading import Thread
import time
from settings import MODULE_TEXT
from settings import KNOB_LIST
import pygame

# Rotary Encoder GPIO Pins
PIN_CLK = 15
PIN_DT = 24
PIN_SW = 22

PIN_CLK2 = 27
PIN_DT2 = 17
#PIN_SW2 = 22  non functioning

# Encoder state
clk_last_state = GPIO.HIGH
clk2_last_state = GPIO.HIGH
module_index = 0
KNOB_INDEX = 0

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    #setup rotary 2
    GPIO.setup(PIN_CLK2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_DT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    

def rotary_watcher(pypboy_instance, MODULE_TEXT):
    global clk_last_state, module_index
    debounce_time = 0.01  # 10ms debounce delay

    while True:
        clk_state = GPIO.input(PIN_CLK)
        dt_state = GPIO.input(PIN_DT)

        if clk_last_state == GPIO.HIGH and clk_state == GPIO.LOW:
            if dt_state == GPIO.HIGH:
                try:
                    pypboy_instance.handle_action("dial_up")
                except Exception as e:
                    import traceback
                    print("error calling up")
                    traceback.print_exc()
            else:
                try:
                    pypboy_instance.handle_action("dial_down")
                except Exception as e:
                    print("error calling down")
                    
        clk_last_state = clk_state
        time.sleep(debounce_time)
        
      
def rotary_watcher2(pypboy_instance, KNOB_LIST):
    global KNOB_INDEX
    debounce_time = 0.003  # 10ms debounce delay
    
    clk_last = GPIO.input(PIN_CLK2)
    dt_last = GPIO.input(PIN_DT2)
    last_encoded = (clk_last << 1) | dt_last
    
    transition_table = {
        (0b00, 0b01): +1,
        (0b01, 0b11): +1,
        (0b11, 0b10): +1,
        (0b10, 0b00): +1,
        (0b00, 0b10): -1,
        (0b10, 0b11): -1,
        (0b11, 0b01): -1,
        (0b01, 0b00): -1
}
    stable_count = 0

    while True:
        clk = GPIO.input(PIN_CLK2)
        dt = GPIO.input(PIN_DT2)
        encoded = (clk << 1) | dt
        
        if not KNOB_LIST:
            print(f"Knob list is empty")
            return

        if encoded != last_encoded:
            movement = transition_table.get((last_encoded, encoded), 0)
            last_encoded = encoded
            
            if movement != 0:
                stable_count += 1
                if stable_count >= 2:
                    stable_count = 0
                    KNOB_INDEX = (KNOB_INDEX + movement) % len(KNOB_LIST)
                    CURRENT_KNOB = KNOB_LIST[KNOB_INDEX]
                    print(f"Currnet knob: {CURRENT_KNOB}")
                
                    key_lookup = {
                        "knob_1": pygame.K_1,
                        "knob_2": pygame.K_2,
                        "knob_3": pygame.K_3,
                        "knob_4": pygame.K_4,
                        "knob_5": pygame.K_5,
                    }
                
                    key = key_lookup.get(CURRENT_KNOB)
                    if key:
                        print(f"Posting keydown for {CURRENT_KNOB}")
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key":key}))
        else:
            stable_count = 0    
            
        #clk2_last_state = clk_state

        #if GPIO.input(PIN_SW) == GPIO.LOW:
            #print("🔘 Button Pressed → Selecting", MODULE_TEXT[module_index])
            #module_key = "module_" + MODULE_TEXT[module_index].lower()
            #try:
                #pypboy_instance.switch_module(module_key)
            #except Exception as e:
                #print("❌ Error switching module:", e)
            #time.sleep(0.25)  # button debounce

        time.sleep(debounce_time)

def start_rotary_thread(pypboy_instance, MODULE_TEXT):
    setup_gpio()
    rotary_thread = Thread(target=rotary_watcher, args=(pypboy_instance, MODULE_TEXT), daemon=True)
    rotary_thread.start()
    rotary2_thread = Thread(target=rotary_watcher2, args=(pypboy_instance, KNOB_LIST), daemon=True)
    rotary2_thread.start()


