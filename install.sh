#!/bin/bash 
# 
# install.sh 
# 
# install PiLedLightingController as a service 
# 
# by Darren Dunford 
# 
 
 
# script control variables 
servicedir="/opt/ledcontrol" 
 
# install required modules
# (commented out as no modules required at the moment) 
# apt-get install -y xxx
 
# create directory structure for apps 
mkdir -p $servicedir/bin 
mkdir -p $servicedir/etc 
chown -R pi:pi $servicedir 
 
# copy app and service files 
cp ledcontrol.py $servicedir/bin 
cp ledcontrol.service /lib/systemd/system 
chmod 644 /lib/systemd/system/ledcontrol.service 
 
# restart systemd and enable service on boot 
systemctl daemon-reload 
systemctl enable ledcontrol.service 
systemctl start ledcontrol.service