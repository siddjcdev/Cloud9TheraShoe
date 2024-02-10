from machine import ADC, Pin
import time
import utime
# create an ADC object with pin 26
adc = ADC(29)

# set the resistor value in ohms
R = 10000
FRS = 1

# Define the pin number where the LED is connected
led_pin = Pin(25, Pin.OUT)  # GPIO 25 (physical pin 16)




# loop forever
while True:
    # read the raw value from the ADC
    raw = adc.read_u16()
    
    # convert the raw value to a voltage
    V = raw * 3.3 / 65535
    
    # convert the voltage to a resistance
    FRS = V / (3.3 / (R + FRS) - V)
    
    # print the voltage and resistance
    print("Raw: {:.2f} ".format(raw))
    #print("Voltage: {:.2f} V".format(V))
    #print("Resistance: {:.2f} ohms".format(FRS))
    
    led_pin.on()  # Turn the LED on
    utime.sleep(0.5)  # Wait for 0.5 seconds
    led_pin.off()  # Turn the LED off
    utime.sleep(0.5)  # Wait for another 0.5 second
    
    # wait for 1 second
    #time.sleep(1)