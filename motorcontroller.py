from machine import Pin
from time import sleep_ms
import uasyncio as asyncio

led = Pin(2, Pin.OUT)
motor1 = Pin(32,Pin.OUT)
motor2 = Pin(33, Pin.OUT)
motor3 = Pin(27,Pin.OUT)
motor4 = Pin(12, Pin.OUT)
motor5 = Pin(13,Pin.OUT)
motor6 = Pin(10, Pin.OUT)

async def start_motors():
    print("start motors")
    try:
        while True:
            led.value(1)
            motor1.value(1)
            motor2.value(1)
            motor3.value(1)
            motor4.value(1)
            motor5.value(1)
            motor6.value(1)
            await asyncio.sleep_ms(1000)
            led.value(0)
            await asyncio.sleep_ms(1000)
    except Exception as e:
        led.value(0)
        motor1.value(0)
        motor2.value(0)
        motor3.value(0)
        motor4.value(0)
        motor5.value(0)
        motor6.value(0)
    
        print ("An error has occurred. Please try again. The error is:")
        print (e)      

        pass    
    

async def stop_motors():
    print("stopping motors...")
    try:
            led.value(0)
            motor1.value(0)
            motor2.value(0)
            motor3.value(0)
            motor4.value(0)
            motor5.value(0)
            motor6.value(0)
            await asyncio.sleep_ms(1000)
    except Exception as e:
        led.value(0)
        motor1.value(0)
        motor2.value(0)
        motor3.value(0)
        motor4.value(0)
        motor5.value(0)
        motor6.value(0)
    
        print ("An error has occurred. Please try again. The error is:")
        print (e)
        

        pass    



















