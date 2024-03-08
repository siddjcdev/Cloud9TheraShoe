# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-pwm-micropython/
from machine import Pin   , PWM
from time import sleep

mtr_AI1 = machine.Pin(8, machine.Pin.OUT)
mtr_AI2 = machine.Pin(7, machine.Pin.OUT)

# Set up PWM Pin
#motor = machine.Pin(6, Pin.PULL_UP)
motor = machine.Pin(6)
motor_pwm = PWM(motor)
duty_step = 5000  # Step size for changing the duty cycle 129

#Set PWM frequency
frequency = 500
motor_pwm.freq (frequency)

# mtr_AI1.value(1)
# mtr_AI2.value(0)

led = machine.Pin("WL_GPIO0", machine.Pin.OUT)
led.on()

iteration =1
try:
    while True:
      # Increase the duty cycle gradually
        print("Increase the duty cycle gradually for iteration:", iteration)
#       for duty_cycle in range(32000, 65536, duty_step):
        motor_pwm.duty_u16(65536)
#         print("duty_step:", duty_step)
        sleep(3)
        
        led.toggle()
        print("led.toggle")
      
      # Decrease the duty cycle gradually
        print("Decrease the duty cycle gradually for iteration:", iteration)
#       for duty_cycle in range(65536, 32000, -duty_step):
#        motor_pwm.duty_u16(0)
#         print("duty_step:", duty_step)
#        sleep(1)
    
        led.toggle()
        print("led.toggle")
        print("iteration:", iteration)
        iteration +=1
        
except KeyboardInterrupt:
    print("Keyboard interrupt")
    motor_pwm.duty_u16(0)
    print(motor_pwm)
    motor_pwm.deinit()
    led.off()

