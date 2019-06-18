#!/bin/bash
# Measure cpu frequency
# Usage: sleep duration is 0.1s:
# bash get_cpu_freq.sh 0.1
startTime=$(date +%s.%N)
sleepDurationSeconds=$1
echo "time,freq"

while true; do
    currentTime=$(date +%s.%N)

    # calculate the avg cpu freq
    CPU_Freq_List=$(cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq)
    CPU_Freq=$(echo "$CPU_Freq_List" | awk -F " " '{ total += $1; count++ } END { print total/count }')
    elapsedTime=$(echo "$currentTime-$startTime" | bc)

    echo "$elapsedTime,$CPU_Freq"

    sleep $sleepDurationSeconds
done