#!/usr/bin/env python3
#
# Raspberry Pi LED Light Controller
# for APA102C and SK9822 LED strips
#
# by Darren Dunford

# Import Libraries
from driver import apa102

# initialise LED strip, uses SPI pins (BCM10 and BCM11) by default
ledstrip = apa102.APA102(num_led=146)
ledstrip.clear_strip()

for i in range(146):
    ledstrip.set_pixel(i,255,0,0,10)
ledstrip.show()

