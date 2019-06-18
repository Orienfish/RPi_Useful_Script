#!/bin/bash
# Set the frequency
# Usage: to set the frequency to 600MHz: 
# sudo bash ./set_freq.sh 600000
freq=$1

# set userspace governor
echo "userspace" > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor

# set frequency
echo $freq > /sys/devices/system/cpu/cpufreq/policy0/scaling_setspeed