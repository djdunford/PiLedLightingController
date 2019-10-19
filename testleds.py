#!/usr/bin/env python3
#
# Raspberry Pi LED Light Controller
# for APA102C and SK9822 LED strips
#
# by Darren Dunford

# Import Libraries
from driver import apa102
import time

# initialise LED strip, uses SPI pins (BCM10 and BCM11) by default
ledstrip = apa102.APA102(num_led=146)
ledstrip.clear_strip()

# loop forever
while True:

    for i in range(146):
        ledstrip.set_pixel(i,255,0,0,10)
    ledstrip.show()

    time.sleep(1);

    for i in range(146):
        ledstrip.set_pixel(i,0,255,0,10)
    ledstrip.show()

    time.sleep(1);

    for i in range(146):
        ledstrip.set_pixel(i,0,0,255,10)
    ledstrip.show()

    time.sleep(1);
    
    ledstrip.clear_strip();
    time.sleep(1);
    
    
