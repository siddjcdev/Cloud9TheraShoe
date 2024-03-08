# ************************
# Web Server in ESP32 using
# web sockets (wifi station)
# Author: George Bantique
# Date: October 28, 2020
# Feel free to modify it
# according to your needs
# ************************
import json
import network
import wifi_credentials
import time 
from machine import Pin, I2C
import struct
from math import atan, sqrt, pi
import network
import wifi_credentials

sta = network.WLAN(network.STA_IF)
import ustruct
led = machine.Pin("WL_GPIO0", machine.Pin.OUT)
led.off()

# ************************
# Configure the ESP32 wifi
# as STAtion mode.
sta = network.WLAN(network.STA_IF)
if not sta.isconnected():
    print("connecting to network...")
    sta.active(True)
    #sta.connect("your wifi ssid", "your wifi password")
    sta.connect(wifi_credentials.ssid, wifi_credentials.password)
    while not sta.isconnected():
        pass
print("network config:", sta.ifconfig())

# ************************
# Configure the socket connection
# over TCP/IP
import socket

# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
# SOCK_DGRAM means that it is a UDP socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("",80)) # specifies that the socket is reachable 
#                 by any address the machine happens to have
s.listen(5)     # max of 5 socket connections

# ************************
# Function for creating the
# web page to be displayed
def web_page():
    if led.value()==1:
        led_state = "ON"
        print("led is ON")
    elif led.value()==0:
        led_state = "OFF"
        print("led is OFF")

    html_page = """   
      <!DOCTYPE HTML><html>
<!-- Rui Santos - Complete project details at https://RandomNerdTutorials.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files.
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. -->
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="https://code.highcharts.com/highcharts.js"></script>
  <style>
    body {
      min-width: 310px;>>> 
    	max-width: 800px;
    	height: 400px;
      margin: 0 auto;
    }
    h2 {
      font-family: Arial;
      font-size: 2.5rem;
      text-align: center;
    }
  </style>
</head>
<body>
  <h2>Foot Diagnostics</h2>
  <div id="chart-temperature" class="container"></div>
  <div id="chart-humidity" class="container"></div>
  <div id="chart-pressure" class="container"></div>
</body>
<script>
var chartT = new Highcharts.Chart({
  chart:{ renderTo : "chart-temperature" },
  title: { text: "ADXL345 acceleration measurement" },
  series: [{
    name: 'X',
    color: '#1B518A',
    showInLegend: true,
    data: []
  }, {
    name: 'Y',
    color: '#FF0000',
    showInLegend: true,
    data: []
  }, {
    name: 'Z',
    color: '#FF9B00',
    showInLegend: true,
    data: []
  }],
  plotOptions: {
    line: { animation: false,
      dataLabels: { enabled: true }
    },
    series: { color: "#059e8a" }
  },
  xAxis: { type: "datetime",
    dateTimeLabelFormats: { second: "%H:%M:%S" }
  },
  yAxis: {
    title: { text: "Acceleration" }
    //title: { text: "Temperature (Fahrenheit)" }
  },
  credits: { enabled: false }
});
setInterval(function ( ) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log('response' + this);
      console.log('responseText' + this.responseText);
      const data = JSON.parse(this.responseText);
      console.log('data' + data.x);
      var d = (new Date()).getTime(),
          //y = parseFloat(data.data);
          x = parseFloat(data.x);
          y = parseFloat(data.y);
          z = parseFloat(data.z);
      
      if(chartT.series[0].data.length > 40) {
        chartT.series[0].addPoint([d, x], true, true, true);
      } else {
        chartT.series[0].addPoint([d, x], true, false, true);
      }
      if(chartT.series[1].data.length > 40) {
        chartT.series[1].addPoint([d, y], true, true, true);
      } else {
        chartT.series[1].addPoint([d, y], true, false, true);
      }
      if(chartT.series[2].data.length > 40) {
        chartT.series[2].addPoint([d, z], true, true, true);
      } else {
        chartT.series[2].addPoint([d, z], true, false, true);
      }
    }
  };
  xhttp.open("GET", "/accel", true);
  xhttp.send();
}, 1000 ) ;
</script>
        <center>   
         <form>   
          <button name="LED" type="submit" value="1"> LED ON </button>   
          <button name="LED" type="submit" value="0"> LED OFF </button>   
         </form>   
        </center>   
        <center><p>LED is now <strong>""" + led_state + """</strong>.</p></center>   
      </body>   
      </html>"""  
    return html_page   
random = 1
#===================imu - MPU-6050========================================================================================

# i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
# imu_measure = MPU6050(i2c)

# I2C address of the MPU6050
MPU6050_ADDRESS = 0x68

# Initialize I2C communication
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
mpu6050 = i2c.scan()[0]

# Configure MPU6050
i2c.writeto_mem(mpu6050, MPU6050_ADDRESS, b'\x00')  # Wake up MPU6050

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


while True:
    # Socket accept() 
    conn, addr = s.accept()
    print("Got connection from %s" % str(addr))
    
    # Socket receive()
    request=conn.recv(1024)
    print("")
    print("")

    print("Content %s" % str(request))
    
    #==========================MPU-6050===============
    
    
    ax, ay, az, gx, gy, gz = read_mpu6050()
    pitch_angle = calculate_pitch(ax, ay, az)
    roll_angle = calculate_roll(ax, ay, az)
    yaw_angle = calculate_yaw(ax, ay, az)
    print("ax",ax,"\t","ay",ay,"\t","az",az,"\t","gx",gx,"\t","gy",gy,"\t","gz",gz,"\t","        ",end="\r")
    print(f"Pitch Angle: {pitch_angle:.2f} degrees,Roll Angle: {roll_angle:.2f} degrees,Yaw Angle: {yaw_angle:.2f} degrees")
    print("\r")
    time.sleep(0.1)

    # Socket send()
    request = str(request)
    led_on = request.find("/?LED=1")
    led_off = request.find("/?LED=0")
    acceleration = request.find("/accel")
    if acceleration == 6:
        
        #==========================ADXL345=============================
        print("acceleration")
 
        #response = {"x" : x*G_TO_N,"y" : y*G_TO_N, "z" : z*G_TO_N}
        #====================MPU-6050===================================
        
        # Get the acceleration values
        response = {"x" : roll_angle,"y" : pitch_angle, "z" : yaw_angle}
        
        
        #imu_measure = MPU6050(i2c)
        json_str = json.dumps(response) # convert the dictionary to a JSON string
        data_bytes = bytes(json_str, "utf-8") # convert the string to bytes

        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: application/json\n")
        conn.send("Connection: close\n\n")
        conn.sendall(data_bytes)
    else:
        if led_on == 6:
            print("The LED is ON")
            print(str(led_on))
            led.value(1)

        else:
            #if led_off == 6:
            print("LED OFF")
            print(str(led_off))
            led.value(0)

        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
            
    
    # Socket close()
    conn.close()
#except:
    #s.close()
    #print("exception")
    
