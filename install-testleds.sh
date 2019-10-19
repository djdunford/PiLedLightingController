#!/bin/bash 
# 
# install.sh 
# 
# install PiLedLightingController as a service 
# 
# by Darren Dunford 
# 
 
# install pip3
apt-get install -y python3-pip

# install required python modules from requirements.txt
pip3 install -r requirements.txt
