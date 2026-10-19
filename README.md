<h1>TempDash</h1>
With this project I built a webserver which shows the current temperatur,humidity and air pressure, as well as these messurements over the 10 last ours in a diagramm. all the data will be able to get downloaded via a button on the website.

For the Diagramm I used Chart.js

To set this up, you need a esp32 and a bme280 connected to pin 25 and 26
you will need to modify the python file to add your wifi ssid and password. Drag the html and python file to the esp32 and then create a file called data. Then go to the ip of your esp32 and enjoy :)


<h2>Wiring Diagramm</h2>
<img src="Wiring-Diagramm.jpeg" alt="Wiring Diagramm">

<h2>Preview in Browser</h2>
<img src="safari preview1.png" alt="Preview">

<h2>How to set it up?</h2>
First set up thonny IDE and install micropython on your esp32. After that connect the sensor as described on the wiring diagram(disconnect your esp32 for that). Then download all the files which are in the folder host and copy the bme280 library(used the one from this tutorial:'https://randomnerdtutorials.com/micropython-bme280-esp32-esp8266/') (this is the github repo: 'https://github.com/RuiSantosdotme/ESP-MicroPython/blob/master/code/WiFi/HTTP_Client_IFTTT_BME280/BME280.py') to the esp32 and save it as 'BME280.py'. Also copy the other files from the host folder to the esp32. Then create a file named 'data'. After that you will need to add the SSID and Password of your router in main.py. Now you can start the programm. When you start the programm the esp 32 will output his ip address. You will need to use this ip to access the website. It's important that your device and the esp32 are in the same network. 
