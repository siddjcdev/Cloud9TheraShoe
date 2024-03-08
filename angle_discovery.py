# Import necessary libraries
import machine
import time
import struct
from math import atan, sqrt, pi

# I2C address of the MPU6050
MPU6050_ADDRESS = 0x68

# Initialize I2C communication
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
mpu6050 = i2c.scan()[0]

# Configure MPU6050
i2c.writeto_mem(mpu6050, 0x6B, b'\x00')  # Wake up MPU6050

# Read raw accelerometer and gyroscope data
def read_mpu6050():
    data = i2c.readfrom_mem(mpu6050, 0x3B, 14)
    ax, ay, az, gx, gy, gz = struct.unpack('>hhhhhh', data)
    return ax, ay, az, gx, gy, gz

# Calculate pitch angle (in degrees)
def calculate_pitch(ax, ay, az):
    pitch_rad = atan(ax / sqrt(ay**2 + az**2))
    return pitch_rad * (180 / pi)

def calculate_roll(ax, ay, az):
    roll_rad = atan(ay / sqrt(ax**2 + az**2))
    return roll_rad * (180 / pi)

def calculate_yaw(ax, ay, az):
    yaw_rad = atan(az / sqrt(ax**2 + ay**2))
    return yaw_rad * (180 / pi)



# x= RAD_TO_DEG * (atan2(-yAng, -zAng)+PI);
# y= RAD_TO_DEG * (atan2(-xAng, -zAng)+PI);
# z= RAD_TO_DEG * (atan2(-yAng, -xAng)+PI);

# Main loop
while True:
    ax, ay, az, gx, gy, gz = read_mpu6050()
    pitch_angle = calculate_pitch(ax, ay, az)
    roll_angle = calculate_roll(ax, ay, az)
    yaw_angle = calculate_yaw(ax, ay, az)
    print(f"Pitch Angle: {pitch_angle:.2f} degrees,Roll Angle: {roll_angle:.2f} degrees,Yaw Angle: {yaw_angle:.2f} degrees")
    time.sleep(0.1)