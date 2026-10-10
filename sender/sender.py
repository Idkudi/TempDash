import network
import espnow
import json
import machine
import time


wlan = network.WLAN(network.STA_IF)
wlan.active(True)

#create message
message=['BatteryError', 'TempError']

#esp now
e=espnow.ESPNow()
receiver=espnow.Peer(mac=b'MAC-ADDRESS')
e.peers.append(peer)
e.active(True)
print("ESPNow is active")

# temperature sensor
def messureTemp():
    return temp

# send temperature data
def send_temperature_data():
    message[1]=messureTemp()
    jmess=json.dump(message)
    e.send(jmess)

while True:
    send_temperature_data()
    machine.lightsleep(1000*60)

