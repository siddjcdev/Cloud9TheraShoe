import network
import config

def do_connect(ssid, pwd):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
 
def do_establish(ssid,pwd):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=pwd)
    ap.active(True)

    while ap.active == False:
        pass

    print("Access point is active.")
    print(ap.ifconfig())


# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
 
# Attempt to connect to WiFi network
#do_connect(config.ssid, config.pwd)
    
# Establish WiFi network
do_establish(config.ssid, config.pwd)
 
# # import webrepl
# # webrepl.start()
