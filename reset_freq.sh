#!/bin/bash
# Reset the frequency governor to ondemand
# Usage: bash ./reset_freq.sh
# set ondemand governor
echo "ondemand" > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor