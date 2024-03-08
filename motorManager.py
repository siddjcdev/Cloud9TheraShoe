from machine import Pin, PWM
from time import sleep
import uasyncio as asyncio



async def intensity(level):
    print("start motors")
    led = Pin("WL_GPIO0", Pin.OUT)
    led.off()

    # Set up PWM Pin
    motor1 = Pin(6, Pin.PULL_UP)
    motor1_pwm = PWM(motor1)
    motor2 = Pin(10, Pin.PULL_UP)
    motor2_pwm = PWM(motor2)


    duty_cycle = 0  #
    duty_step = 16384

    #Set PWM frequency
    frequency = 500
    motor1_pwm.freq(frequency)
    motor2_pwm.freq(frequency)

    iteration = 1

    
    if level == 0:
        duty_cycle = 0
        print("The motors are off.")
    else:
        duty_cycle = duty_step * level
        print("Intensity level:", level)
    
    try:
      while True:
        motor1_pwm.duty_u16(duty_cycle)
        motor2_pwm.duty_u16(duty_cycle)
 
        led.toggle()
        #print("Toggled led. iteration:", iteration)
        iteration +=1
        await asyncio.sleep_ms(1000) 
            
    except Exception as e:
        led.off()
        print ("An error has occurred. Please try again. The error is:")
        print (e)      

        pass
