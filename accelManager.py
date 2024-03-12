# Import the libraries
import machine
import time
import struct
from math import atan, sqrt, pi
import json
import random



# Read raw accelerometer and gyroscope data
def read_mpu6050():
    data = i2c.readfrom_mem(mpu6050, 0x3B, 14)
    ax, ay, az, gx, gy, gz = struct.unpack('>hhhhhh', data)
    return ax, ay, az, gx, gy, gz

# Calculate pitch angle (in degrees)
def calculate_pitch(ax, ay, az):
    if (ax == 0 or ay == 0 or az == 0):
        print ("One or more measurements are equal to 0")
    pitch_rad = atan(ax / sqrt(ay**2 + az**2))
    return pitch_rad * (180 / pi)

def calculate_roll(ax, ay, az):
    if ax == 0 or ay == 0 or az == 0:
        print ("One or more measurements are equal to 0")
    roll_rad = atan(ay / sqrt(ax**2 + az**2))
    return roll_rad * (180 / pi)

def calculate_yaw(ax, ay, az):
    if ax == 0 or ay == 0 or az == 0:
        print ("One or more measurements are equal to 0")
    yaw_rad = atan(az / sqrt(ax**2 + ay**2))
    return yaw_rad * (180 / pi)

def get_data():
    print("Getting the accelerometer data")
    led = machine.Pin("WL_GPIO0", machine.Pin.OUT)
    led.off()
    
    try:
        # I2C address of the MPU6050
        MPU6050_ADDRESS = 0x68

        # Initialize I2C communication
        i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
        mpu6050 = i2c.scan()[0]

        # Configure MPU6050
        i2c.writeto_mem(mpu6050, MPU6050_ADDRESS, b'\x00')  # Wake up MPU6050
    except Exception as e:
            print ("An error has occurred during initialization. Please try again. The error is:")
            print (e)  
    
    try:

        while True:
            print("Entering into the while true loop...")
            led.on()
            data = i2c.readfrom_mem(mpu6050, 0x3B, 14)
            ax, ay, az, gx, gy, gz = struct.unpack('>hhhhhh', data)
            #ax, ay, az, gx, gy, gz = read_mpu6050()
            print(f"Pitch: {ax:.2f}, Roll: {ay:.2f},Yaw: {az:.2f}")
            pitch_angle = calculate_pitch(ax, ay, az)
            roll_angle = calculate_roll(ax, ay, az)
            yaw_angle = calculate_yaw(ax, ay, az)
            print(f"Pitch Angle: {pitch_angle:.2f} degrees,Roll Angle: {roll_angle:.2f} degrees,Yaw Angle: {yaw_angle:.2f} degrees")
          
            data = {
                "pitch": f"{pitch_angle:.2f}", 
                "roll": f"{roll_angle:.2f}",
                "yaw": f"{yaw_angle:.2f}",
                "fore":  f"{random.randrange(5,10):.2f}",
                "mid": f"{random.randrange(5,10):.2f}",
                "hind": f"{random.randrange(5,10):.2f}"

            }
            
            led.off()
            return json.dumps(data)
    except Exception as e:
        led.off()
        print ("An error has occurred. Please try again. The error is:")
        print (e)      
        data = {
            "pitch": f"{random.randrange(-18,10):.2f}",
            "roll": f"{random.randrange(18,40):.2f}",
            "yaw": f"{random.randrange(60,80):.2f}",
            "fore":  f"{random.randrange(5,10):.2f}",
            "mid": f"{random.randrange(5,10):.2f}",
            "hind": f"{random.randrange(8,10):.2f}"
        }
            
        return json.dumps(data)
        pass
