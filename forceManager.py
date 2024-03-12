from machine import Pin, ADC
import time, random


def getForce():
    try:
        forePin = ADC(Pin(26))
        midPin = ADC(Pin(27))
        hindPin = ADC(Pin(28))

        fore_force = forePin.read_u16()
        mid_force = midPin.read_u16()
        hind_force = hindPin.read_u16()

        print(f"fore force: {fore_force:.2f} ,mid force: {mid_force:.2f} ,hind force: {hind_force:.2f} ")
            
        time.sleep(1)

        return fore_force, mid_force, hind_force
    except Exception as e:
        print ("An error has occurred while getting force data. Please try again. The error is:")
        print (e)      
        return f"{random.randrange(5,10):.2f}", f"{random.randrange(5,10):.2f}", f"{random.randrange(8,10):.2f}"