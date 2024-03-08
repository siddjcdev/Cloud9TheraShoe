# main.py -- put your code here!
from machine import Pin, ADC
import time

adc = ADC(Pin(26))

while True:
    fsr_value = adc.read_u16()
    print("FSR Value:", fsr_value)
    time.sleep(1)