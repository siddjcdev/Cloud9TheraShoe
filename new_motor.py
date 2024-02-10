# Potentiometer demo
# Kevin McAleer
# May 2021

from machine import Pin, ADC, PWM
from time import sleep_ms

#pot = ADC(26)# the middle pin on the Potentiometer
motor = PWM(Pin(15))
motor.freq(2000)

def map(x, in_min, in_max, out_min, out_max):
    """ Maps two ranges together """
    return int((x-in_min) * (out_max-out_min) / (in_max - in_min) + out_min)

while True:
    # print("Value is:",pot.read_u16())
    #motor.duty_u16(pot.read_u16())

    #pot_value = pot.read_u16()
    #percentage = map(pot_value,288, 65535,0,100)
    percentage = 50
    motor_value = map(percentage,0,100,0,65535)
    print("Percentage:", percentage, "motor value",motor_value)
    motor.duty_u16(motor_value)
    sleep_ms(1000)
    
    
    
    
    
    
    
    
    
    
    
    
    