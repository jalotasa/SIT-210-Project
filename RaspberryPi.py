import RPi.GPIO as GPIO
import time
from azure.iot.device import IoTHubDeviceClient, Message
import urllib.request
import requests
import threading
import json

WRITE_api ="68NKTMLPHMH311FX"
CONNECTION_STRING = "HostName=Distance.azure-devices.net;DeviceId=MyPi;SharedAccessKey=QZTLCy8s1EA2lP56YRiRptybyjwPoLAfazSwUk09FmY=" //insert your api

distance = 0 
MSG_TXT = '{{"Distance": {distance}}'

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

    


TRIG=17
ECHO=27
GPIO.setmode(GPIO.BCM)
while True:
    print("distance measurement in progress")
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG,False)
    print("waiting for sensor to settle")
    time.sleep(0.2)
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
    while GPIO.input(ECHO)==0:
        pulse_start=time.time()
    while GPIO.input(ECHO)==1:
        pulse_end=time.time()
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    print("distance:",distance,"cm")
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
            # Build the message with simulated telemetry values.
        distance = distance

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body

            # Send the message.
        message = Message("distance",distance)
        client.send_message(message)
        print ( "Message successfully sent" )//confirmation
        val= distance
        URl='https://api.thingspeak.com/update?api_key='//sending to thingspeak
        KEY='68NKTMLPHMH311FX'//insert your api key
        HEADER='&field1={}&field2={}'.format(val,val)
        NEW_URL = URl+KEY+HEADER
        print(NEW_URL)
        data=urllib.request.urlopen(NEW_URL)
        print(data)
        r = requests.get('https://maker.ifttt.com/trigger/motion_detected/with/key/cBP_0a207xrli5GAG56Uhl', params={"value1":"none","value2":"none","value3":"none"})//insertyour own web hook
            
        if(r=="off")://When web-hook recieved in while loop system breaks;
            break;  //system can also be paused for alonger time with delay() allowing the queue to move
        time.sleep(10)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )


   
