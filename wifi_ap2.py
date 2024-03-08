# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-web-server-micropython/

# Import necessary modules
import network
import socket
import time
import random
from machine import Pin

# Set up Soft Access Point (AP)
ssid = 'Cloud9Shoe'
password = '123456789'
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)


print('Connection is successful')
print(ap.ifconfig())

# HTML template for the webpage
def webpage(random_value, state):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pico Web Server</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <h1>Raspberry Pi Pico Web Server</h1>
        <h2>Led Control</h2>
        <form action="./lighton">
            <input type="submit" value="Light on" />
        </form>
        <br>
        <form action="./lightoff">
            <input type="submit" value="Light off" />
        </form>
        <p>LED state: {state}</p>
        <h2>Fetch New Value</h2>
        <form action="./value">
            <input type="submit" value="Fetch value" />
        </form>
        <p>Fetched value: {random_value}</p>
    </body>
    </html>
    """
    return str(html)

# Main loop
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 80))
s.listen(5)

# while True:
#     conn, addr = s.accept()
#     request = conn.recv(1024)
#     response = serve_web_page()
#     conn.send(response)
#     conn.close()
    
# Create an LED object on pin 'LED'
led = machine.Pin("WL_GPIO0", machine.Pin.OUT)
    
# Initialize variables
state = "OFF"
random_value = 0

# Main loop to listen for connections
while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        
        # Receive and parse the request
        request = conn.recv(1024)
        request = str(request)
        print('Request content = %s' % request)

        try:
            request = request.split()[1]
            print('Request:', request)
        except IndexError:
            pass
        
        # Process the request and update variables
        if request == '/lighton?':
            print("LED on")
            led.value(1)
            state = "ON"
        elif request == '/lightoff?':
            led.value(0)
            state = 'OFF'
        elif request == '/value?':
            random_value = random.randint(0, 20)

        # Generate HTML response
        response = webpage(random_value, state)  

        # Send the HTTP response and close the connection
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()

    except OSError as e:
        conn.close()
        print('Connection closed')