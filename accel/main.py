from inertia import MPU6050
from time import sleep
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu_measure = MPU6050(i2c)

while True:
    ax=round(imu_measure.accel.x,2)
    ay=round(imu_measure.accel.y,2)
    az=round(imu_measure.accel.z,2)
    gx=round(imu_measure.gyro.x)
    gy=round(imu_measure.gyro.y)
    gz=round(imu_measure.gyro.z)
    tem=round(imu_measure.temperature,2)
    print("ax",ax,"\t","ay",ay,"\t","az",az,"\t","gx",gx,"\t","gy",gy,"\t","gz",gz,"\t","Temperature",tem,"        ",end="\r")
    sleep(0.2)
