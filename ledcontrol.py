#!/usr/bin/env python3 
# 
# Raspberry Pi LED Light Controller
# for APA102C and SK9822 LED strips
#
# by Darren Dunford 
 
# Import Libraries 
import os 
import RPi.GPIO as GPIO 
import syslog 
import sys
import time
import AWSIoTPythonSDK
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from driver import apa102
import configparser
import json

# change current working directory
os.chdir(os.path.dirname(sys.argv[0]))

# read config file and settings
config = configparser.ConfigParser()
config.read('ledcontrol.ini')

# retrieve AWSIoT settings
privateKeyPath = config['aws']['privatekeypath']
certificatePath = config['aws']['certificatepath']
host = config['aws']['host']
rootCAPath = config['aws']['rootcapath']
thingname = config['aws']['thingname']

# debug flag
debugdict = config['debug']
DEBUG = debugdict.getboolean('debug',fallback=False) # if debug true then additional logging to syslog is enabled
SYSLOG = debugdict.getboolean('syslog',fallback=True) # if syslog is false then all output to syslog is suppressed

# set global trigger to False - a callback routine can set this to a value to trigger a particular sequence 
btnTrigger = 0 

# set current sequence to false
stsSequence = 0

# define AWSIoT shadow functions and callbacks
class shadowCallbackContainer:

    # constructor
    def __init__(self, deviceShadowInstance):
        self.deviceShadowInstance = deviceShadowInstance
        self.callbackresponses = {}

    # Custom shadow callback for delta -> remote triggering
    def customShadowCallback_Delta(self, payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
        
        # declare global variables updated by this procedure
        global btnTrigger
        
        # DEBUG dump payload in to syslog
        if DEBUG and SYSLOG:
            syslog.syslog(payload)
        
        # create JSON dictionary from payload
        payloadDict = json.loads(payload)
        newPayload = {"state":{"reported":{"status":"RUNNING"},"desired":None}}

        # check for triggering
        try:
            newState = payloadDict["state"]["status"]
        except KeyError:
            pass
        else:    
            if newState == "TRIGGER":
                try:
                    sequence = int(payloadDict["state"]["sequence"])
                except KeyError:
                    pass
                else:    
                    
                    # trigger and update status
                    btnTrigger = int(sequence)
                    newPayload.update({"state":{"reported":{"status":"TRIGGERED","sequencerun":sequence,"sequence":None}}})

        if DEBUG and SYSLOG:
            syslog.syslog("Shadow update: "+json.dumps(newPayload))
            
        # update shadow instance status
        self.deviceShadowInstance.shadowUpdate(json.dumps(newPayload), None, 5)
        
    # post status update message to device shadow and, if enabled, syslog
    def statusPost(self,status):

        # create new JSON payload to update device shadow
        newPayload = {"state":{"reported":{"status":str(status),"sequencerun":None,"sequence":None},"desired":None}}
        self.deviceShadowInstance.shadowUpdate(json.dumps(newPayload), None, 20)
    
        # log to syslog
        if SYSLOG:
            syslog.syslog(status)
    
        return

# Set the GPIO PIN naming mode
GPIO.setmode(GPIO.BCM)

# Suppress warnings for GPIO usage clashes
GPIO.setwarnings(False)

# create array for BCM lines corresponding to buttons
# format is [ BCM line , button_number ]
buttons = [[4,1],[22,2],[9,3]]

# define button press callback function
def button_press_callback(channel):

    # access global variables
    global btnTrigger
    global buttons
    
    # add 0.1s debounce 
    time.sleep(0.1) 

    # set sequence based on button pressed
    for button in buttons:    
        if channel == button[0]:    
            if GPIO.input(button[0]) == False:
                btnTrigger = button[1]            
                
    return

# set each button as an input pin, with pullup,
# and set an event handler based on falling edge
# detection with debounce time
for button in buttons:
    GPIO.setup(button[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button[0], GPIO.FALLING, callback=button_press_callback, bouncetime=50)



# Init Shadow Client MQTT connection
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(thingname)
myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTShadowClient configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(20)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(20)  # 5 sec

# force shadow client to use offline publish queueing
# overriding the default behaviour for shadow clients in the SDK
MQTTClient = myAWSIoTMQTTShadowClient.getMQTTConnection()
MQTTClient.configureOfflinePublishQueueing(-1)

# Connect to AWS IoT with a 300 second keepalive
myAWSIoTMQTTShadowClient.connect(300)

# Create a deviceShadow with persistent subscription
Bot = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingname, True)

# create new instance of shadowCallbackContainer class
shadowCallbackContainer_Bot = shadowCallbackContainer(Bot)

# initialise LED strip, uses SPI pins (BCM10 and BCM11) by default
ledstrip = apa102.APA102(num_led=146)
ledstrip.clear_strip()

# set status, and clear any desired state
shadowCallbackContainer_Bot.statusPost('STARTING')
shadowCallbackContainer_Bot.statusPost('RUNNING')

# register AWSIoT callback to allow remote triggering and configuration
Bot.shadowRegisterDeltaCallback(shadowCallbackContainer_Bot.customShadowCallback_Delta)

# loop forever 
while True: 
 
    # if button 1 pressed show Red
    # if already Red toggle off
    if btnTrigger == 1:
        if stsSequence == 1:
            shadowCallbackContainer_Bot.statusPost('Sequence 1 cleared')
            ledstrip.clear_strip()
            stsSequence = 0
        else:
            shadowCallbackContainer_Bot.statusPost('Sequence 1 triggered') 
            for i in range(146):
                ledstrip.set_pixel(i,255,0,0,10)
            ledstrip.show()
            stsSequence = 1
        btnTrigger = 0 

    # if button 2 pressed show Green
    # if already Green toggle off
    if btnTrigger == 2:
        if stsSequence == 2:
            shadowCallbackContainer_Bot.statusPost('Sequence 2 cleared')
            ledstrip.clear_strip()
            stsSequence = 0
        else:
            shadowCallbackContainer_Bot.statusPost('Sequence 2 triggered') 
            for i in range(146):
                ledstrip.set_pixel(i,0,255,0,10)
            ledstrip.show()
            stsSequence = 2
        btnTrigger = 0 

    # if button 3 pressed show Blue          
    # if already Blue toggle off
    if btnTrigger == 3:
        if stsSequence == 3:
            shadowCallbackContainer_Bot.statusPost('Sequence 3 cleared')
            ledstrip.clear_strip()
            stsSequence = 0
        else:
            shadowCallbackContainer_Bot.statusPost('Sequence 3 triggered') 
            for i in range(146):
                ledstrip.set_pixel(i,0,0,255,10)
            ledstrip.show()
            stsSequence = 3
        btnTrigger = 0 
        
    # add delay to reduce processor load
    time.sleep(0.1)
