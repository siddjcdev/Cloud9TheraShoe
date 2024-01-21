# ************************
# Web Server in ESP32 using
# web sockets (wifi station)
# Author: George Bantique
# Date: October 28, 2020
# Feel free to modify it
# according to your needs
# ************************
import json
import machine
led = machine.Pin(2,machine.Pin.OUT)
led.off()

# ************************
# Configure the ESP32 wifi
# as STAtion mode.
import network
import wifi_credentials

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
      min-width: 310px;
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
  <h2>ESP Weather Station</h2>
  <div id="chart-temperature" class="container"></div>
  <div id="chart-humidity" class="container"></div>
  <div id="chart-pressure" class="container"></div>
</body>
<script>
var chartT = new Highcharts.Chart({
  chart:{ renderTo : "chart-temperature" },
  title: { text: "BME280 Temperature" },
  series: [{
    showInLegend: false,
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
    title: { text: "Temperature (Celsius)" }
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
      console.log('data' + data.data);
      var x = (new Date()).getTime(),
          y = parseFloat(data.data);
      
      if(chartT.series[0].data.length > 40) {
        chartT.series[0].addPoint([x, y], true, true, true);
      } else {
        chartT.series[0].addPoint([x, y], true, false, true);
      }
    }
  };
  xhttp.open("GET", "/temp", true);
  xhttp.send();
}, 10000 ) ;
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
#try:
while True:
    # Socket accept() 
    conn, addr = s.accept()
    print("Got connection from %s" % str(addr))
    
    # Socket receive()
    request=conn.recv(1024)
    print("")
    print("")
    print("Content %s" % str(request))
    
    # Socket send()
    request = str(request)
    led_on = request.find("/?LED=1")
    led_off = request.find("/?LED=0")
    temperature = request.find("/temp")
    if temperature == 6:
        print("temperature")
        if random == 1:
            response = {"data" : "20"}
            random = 2
        elif random == 2:
            response = {"data" : "30"}
            random = 3
        else:
            response = {"data" : "35"}
            random = 1
        
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