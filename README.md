# ThingsBoard-Platform-Protocol-Tester
Using this application user can able to test CoAP, MQTT & HTTP Protocol with your ThingsBoard Instance

![alt text](https://github.com/shiyazt/ThingsBoard-Platform-Protocol-Tester/blob/master/images/MainWindow_Help.png)

1) URL Field : Enter your Platform instance URL
2) Access Token Field :  Enter your Device Access Token
3) Protocol Selector : Select the Protocol type , CoAP / HTTP / MQTT
4) Data Type : Select Data Type, Client Attributes/Telemetry Data
5) Upload Button : Upload the Test data in JSON Format
6) Send Button :  Button send the Message to the your Platform Instance
7) Log Window :  Displays the log level message from the application to the user
8) Progress Bar :  Indicates the progress level.
9) Cancel Button : Cancel the operation and resets the user entry fields.

Screenshots
===========

CoAP Protocol:
-------------
![alt text](https://github.com/shiyazt/ThingsBoard-Platform-Protocol-Tester/blob/master/images/CoAP_Protocol.png)

MQTT Protocol:
-------------
![alt text](https://github.com/shiyazt/ThingsBoard-Platform-Protocol-Tester/blob/master/images/MQTT_Protocol.png)

HTTP Protocol:
-------------
![alt text](https://github.com/shiyazt/ThingsBoard-Platform-Protocol-Tester/blob/master/images/HTTP_Protocol.png)

ThingsBoard Demo Instance Latest Telemetry
------------------------------------------
![alt text](https://github.com/shiyazt/ThingsBoard-Platform-Protocol-Tester/blob/master/images/TB%20Data.png)

Installation:
============

Ubuntu / Linuxmint / Debian:
-----------------------------
1) Install these packages:
```
sudo apt-get install build-essential

sudo apt-get install qt5-default

sudo apt-get install python3-pyqt5

sudo apt install pyqt5-dev-tools

sudo apt install python3-pip

sudo apt-get install python3-setuptools

pip3 install wheel

pip3 install paho-mqtt

sudo npm install coap-cli -g
```
2) Clone this project 
  ```git clone https://github.com/shiyazt/ThingsBoard-Platform-Protocol-Tester.git
  ```
3) go to src folder
  ``` cd src
  ```
 4) Run the Python script
  ```python3 tester.py
  ```

#**Tested and Worked on Ubuntu 18.04, Linuxmint 19.1 & Ubuntu 16.04**
