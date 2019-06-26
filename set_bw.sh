#!/bin/bash
# Set bw using the wondershaper tool
# Usage: to set a 100kbps bandwidth on both up and down link:
# sudo bash set_bw.sh 100 
# You may have to change the path to your wondershaper tool
bw=$1

/home/pi/wondershaper/wondershaper -c -a wlan0
/home/pi/wondershaper/wondershaper -a wlan0 -u $bw -d $bw