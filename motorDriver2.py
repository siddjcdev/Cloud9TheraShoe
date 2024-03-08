# Raspberry Pi Pico Motor Test
# motor-test.py

# POT - Pico GPIO 26 ADC0 - Pin 32

# RED BUTTON - Pico GPIO 15 - Pin 20
# BLACK BUTTON - Pico GPIO 2 - Pin 4

# RED LED - Pico GPIO 10 - Pin 14
# GREEN LED - Pico GPIO 11 - Pin 15
# BLUE LED - Pico GPIO 14 - Pin 19

# DroneBot Workshop 2021
# https://dronebotworkshop.com

import machine
import utime

#potentiometer = machine.ADC(26)
potentiometer = 45000 #MAX: 65535 , Speed control
mtr_AI1 = machine.Pin(8, machine.Pin.OUT)
mtr_AI2 = machine.Pin(7, machine.Pin.OUT)
mtr_PWMa = machine.PWM(machine.Pin(6))

led = machine.Pin("WL_GPIO0", machine.Pin.OUT)
led.off()

# button_red = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)
# button_black = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)                                               
# 
# led_red = machine.Pin(10, machine.Pin.OUT)
# led_green = machine.Pin(11, machine.Pin.OUT)
# led_blue = machine.Pin(14, machine.Pin.OUT)
# 
# led_red.value(0)
# led_green.value(0)
# led_blue.value(1)

mtr_PWMa.freq(25)
mtr_AI1.value(1)
mtr_AI2.value(0)

while True:
    
    mtr_PWMa.duty_u16(potentiometer)
    
    #if button_red.value() == 1:
    mtr_AI1.value(1)
    mtr_AI2.value(0)
    led.on()
#         led_red.value(1)
#         led_green.value(0)
#         led_blue.value(0)
    utime.sleep(1) 
    #if button_black.value() == 0:
    mtr_AI1.value(1)
    mtr_AI2.value(0)
    led.off()
#         led_red.value(0)
#         led_green.value(1)
#         led_blue.value(0)
        
    utime.sleep(1) 

