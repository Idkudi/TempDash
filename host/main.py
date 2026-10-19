import network
import espnow
import json
import asyncio
import machine
import time
import socket
import random
import utime
from machine import Pin, I2C
from time import sleep
import BME280


SSID=""
PASSWORD=""


#set up temp sensor
i2c = I2C(scl=Pin(25), sda=Pin(26), freq=10000)


wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# connect to wifi
wlan.connect(SSID,PASSWORD)
while not wlan.isconnected():
    time.sleep(0.5)
if wlan.isconnected(): print('WLAN connected')
#get own mac address
print(wlan.ifconfig())

#create message

#esp now
e=espnow.ESPNow()
e.active(True)
print("ESPNow is active")

# Variable to hold the latest received sensor data globally
latest_data = {
    "host": None,
    "time": None,
    "temp":None,
}

# temperature sensor
def messureTemp():
    bme = BME280.BME280(i2c=i2c)
    temp = str(bme.temperature)[:-1]
    hum = str(bme.humidity)[:-1]
    pres = str(bme.pressure)[:-3]
    return temp,hum,pres
    #return random.randint(1,30)

async def logData():
    #get time
    now = time.localtime()
    
    timestring = "{:02d}:{:02d}:{:02d}:{:02d}:{:04d}".format(
        now[4],  # Minute
        now[3],  # Hour
        now[2],  # Day
        now[1],  # Month
        now[0]   # Year
    )
    #temp,hum,pres=messureTemp()
    data=timestring+';'+';'.join(messureTemp())+'\n'
    with open("data", "a", encoding="utf-8") as datei:
        datei.write(data)
    await asyncio.sleep(3600)
# webserver setup
# 4. Setup Socket Server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
s.setblocking(False)
print('listening on port 80')
logData()


async def webserver():
    while True:
        #alogData()

        # try:
        #     host, msg = e.recv(100)
        #     if msg:             # msg == None if timeout in recv()
        #         print(host, msg)
        #         data=[host, time.localtime(), json.load(msg)]
        #         try:
        #             decodms=msg.decode('utf-8')
        #             data=[host, time.localtime(), json.load(decodms)]
        #         except:
        #             pass
        # except:pass
        try:
            conn, client_addr = s.accept()
            request = conn.recv(1024)
            request_str = request.decode('utf-8')
            with open('website.html', 'r') as f:
                website=f.read()
            
            print(messureTemp())
            #get last data from file
            with open('data', 'r') as datafile:
                lines=datafile.readlines()
            tempL, pressL, humiL, timeL = [], [], [], []
            parts=[]
            try:
                with open('data', 'r') as datafile:
                    lines = datafile.readlines()
                    for line in lines[-10:]:
                        parts = line.strip().split(";")
                        print(parts)
                        timeL.append(parts[0])
                        tempL.append(parts[1])
                        humiL.append(parts[2])
                        pressL.append(parts[3])
            except OSError:
                # File might not exist yet
                pass
            print(timeL,tempL,humiL,pressL)       
            # Generate webpage incorporating the latest ESP-NOW data
            website = website.replace("[tempList]",str(tempL))
            print('1')
            website = website.replace("[pressureList]",str(pressL))
            print('1')

            website = website.replace("[humidityList]",str(humiL))
            print('1')

            website = website.replace("[timeList]", str(timeL))
            print('2')
            tt=[]
            for z in messureTemp():
                tt.append(z)
            website = website.replace("{temp}", str(tt[0])+'C°')
            website = website.replace("{humi}", str(tt[1])+'%')
            website = website.replace("{press}", str(tt[2])+'hPa')
            
            # Send HTTP headers and body back to browser
            conn.send('HTTP/1.1 200 OK\r\n')
            conn.send('Content-Type: text/html\r\n')
            conn.send('Connection: close\r\n\r\n')
            conn.sendall(website)
            conn.close()
        except OSError:
            # Timeout exceptions are expected here when no web client is connecting
            pass
        except Exception as e_gen:
            print("Web server error:", e_gen)
            await asyncio.sleep(0.1)

async def main():
    # Starte beide Aufgaben parallel
    asyncio.create_task(logData())
    asyncio.create_task(webserver())
    
    # Halte die Hauptschleife am Laufen
    while True:
        await asyncio.sleep(1)

# Starte das Event-System
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Programm gestoppt")
