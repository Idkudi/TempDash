import network
import espnow
import json
import asyncio
import machine
import time


wlan = network.WLAN(network.STA_IF)
wlan.active(True)


#get own mac address
mymac=wlan.ipconfig('addr6')

#create message

#esp now
e=espnow.ESPNow()
e.active(True)
print("ESPNow is active")

# temperature sensor
def messureTemp():
    return temp

while True():
    host, msg = e.recv()
    if msg:             # msg == None if timeout in recv()
        print(host, msg)
        data=[host, time.localtime() json.load(msg)]
        if msg == b'end':
            break