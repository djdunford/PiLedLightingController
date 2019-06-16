#!/usr/bin/env python3 
# 
# Raspberry Pi LED Light Controller
# for APA102C and SK9822 LED strips
#
# by Darren Dunford 
 
# Import Libraries 
import os 
import RPi.GPIO as GPIO 
import blinkt
import syslog 
 
# override parameters in blinkt library
blinkt.NUM_PIXELS = 144
blinkt.DAT = 17
blinkt.CLK = 27

# change current working directory
os.chdir(os.path.dirname(sys.argv[0]))

# define status post function 
def statusPost(status): 
	syslog.syslog(status) 
	return 
	 
# set global trigger to False - a callback routine can set this to a value to trigger a particular sequence 
btnTrigger = 0 
 
# Set the GPIO PIN naming mode
GPIO.setmode(GPIO.BCM)

# Suppress warnings for GPIO usage clashes
GPIO.setwarnings(False)

# create array for BCM lines corresponding to buttons
# format is [ BCM line , button_number ]
buttons = [[3,1],[22,2],[9,3]]

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

# Set default brightness for Blinkt! LEDs 
set_brightness(0.1) 
 
# post status message 
statusPost("RUNNING") 
 
# loop forever 
while True: 
 
	# if button 1 pressed show Red 
	if btnTrigger == 1: 
		statusPost('Sequence 1 triggered') 
		blinkt.setall(255,0,0)
		blinkt.show(); 
		btnTrigger = 0 

	# if button 2 pressed show Red 
 	if btnTrigger == 2: 
		statusPost('Sequence 2 triggered') 
		blinkt.setall(0,255,0)
		blinkt.show(); 
		btnTrigger = 0 

	# if button 3 pressed show Red 		 
	if btnTrigger == 3: 
		statusPost('Sequence 3 triggered') 
		blinkt.setall(0,0,255)
		blinkt.show(); 
		btnTrigger = 0 
  