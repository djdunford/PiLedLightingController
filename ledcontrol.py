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
from driver import apa102

# define status post function 
def statusPost(status): 
    syslog.syslog(status) 
    return 
     
# set global trigger to False - a callback routine can set this to a value to trigger a particular sequence 
btnTrigger = 0 

# set current sequence to false
stsSequence = 0
 
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

# initialise LED strip, uses SPI pins (BCM10 and BCM11) by default
ledstrip = apa102.APA102(num_led=146)
ledstrip.clear_strip()

# post status message 
statusPost("RUNNING") 

# loop forever 
while True: 
 
    # if button 1 pressed show Red
    # if already Red toggle off
    if btnTrigger == 1:
        if stsSequence == 1:
            statusPost('Sequence 1 cleared')
            ledstrip.clear_strip()
            stsSequence = 0
        else:
            statusPost('Sequence 1 triggered') 
            for i in range(146):
                ledstrip.set_pixel(i,255,0,0,10)
            ledstrip.show()
            stsSequence = 1
        btnTrigger = 0 

    # if button 2 pressed show Green
    # if already Green toggle off
    if btnTrigger == 2:
        if stsSequence == 2:
            statusPost('Sequence 2 cleared')
            ledstrip.clear_strip()
            stsSequence = 0
        else:
            statusPost('Sequence 2 triggered') 
            for i in range(146):
                ledstrip.set_pixel(i,0,255,0,10)
            ledstrip.show()
            stsSequence = 2
        btnTrigger = 0 

    # if button 3 pressed show Blue          
    # if already Blue toggle off
    if btnTrigger == 3:
        if stsSequence == 3:
            statusPost('Sequence 3 cleared')
            ledstrip.clear_strip()
            stsSequence = 0
        else:
            statusPost('Sequence 3 triggered') 
            for i in range(146):
                ledstrip.set_pixel(i,0,0,255,10)
            ledstrip.show()
            stsSequence = 3
        btnTrigger = 0 
