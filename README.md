# Raspberry Pi Useful Scripts

This repo contains some useful scripts on RPi, including performance monitoring, setting and how to use bluetooth as well as Wi-Fi on RPi. 

## Performance Monitoring and Setting

As a powerful system running Linux-like OS, RPi is different from other micro-controller platforms running RTOS. The performance-related operations on RPi do not require reading low-level code or setting register values. Instead, **scripts reading/setting certain files (everything on Linux is a file!) and some helpful tools (e.g. perf, wondershaper) will be enough!**

If you are interested in working with the following performance metrics on Linux, this is the right place for you!

Note:

* All the code in this repo are tested on RPi 3B. It may work on traditional Linux, or will work after some modifications.
* There are a lot of system monitor software such as conky, psensor, etc. These may be the perfect tools in certain applications, but this repo focuses on the **simplest script-based methods where the data can be obtained remotely**.

### CPU Frequency

There are 3 scripts related to CPU frequency:

1. `get_cpu_freq.sh` reads average frequency across all cores.

   Run the script with:

   ```sh
   bash get_cpu_freq.sh 0.1
   ```

   where `0.1` specifies the sleep between successive samplings.

   The key of this script is the following command that gets the current frequency of all cores:

   ```sh
   cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq
   ```

   If you are interested in certain cores, replace `*` with the core number.

2. `set_freq.sh` sets the CPU frequency of all cores to your specified value. RPi could only be set to either 600MHz or 1200MHz. 

   To set the frequency to 600MHz (note the unit of the parameter is kHz):

   ```sh
   sudo bash set_freq.sh 600000
   ```

   It needs 2 commands to set the frequency, both requiring root permissions:

   ```sh
   # set userspace governor
   echo "userspace" > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor
   # set frequency
   echo $freq > /sys/devices/system/cpu/cpufreq/policy0/scaling_setspeed
   ```

3. `reset_freq.sh` clears the frequency setting, or in other words, resets the frequency governor to on-demand mode. This is the default mode for Linux systems, where the frequency could be adjusted by OS according to workload.

   To run the script:

   ```sh
   sudo bash reset_freq.sh
   ```

### CPU Utilization

CPU utilization is a very useful metric to evaluate CPU power and performance. However, in my observation, the task of sampling CPU utilization itself triggers about 30% utilization on RPi 3B, thus also introduces power overhead. So there is a trade-off on sampling interval and overhead here. The script `get_cpu_util.sh` samples CPU utilization with a user-specified sleep interval between two successive samples. To use it:

```sh
bash get_cpu_util.sh 0.1
```

where `0.1` refers to sleeping 0.1s after one processing. 

The following command is the key of this script:

```sh
cat /proc/stat
```

which prints the cycle usage break-down in each CPU core. All the script needs to do is adding certain numbers and calculating the percentage of time that this CPU core is working. Finally, the script prints out the average CPU utilization across all cores.

### CPU Temperature

### Performance Counters

We use the [perf stat](http://man7.org/linux/man-pages/man1/perf-stat.1.html) tool that is built in Linux to monitor performance counter values. The events can be monitored include instruction counts, cache misses, etc. For more information, refer to the [manual page](http://man7.org/linux/man-pages/man1/perf-stat.1.html) of `perf stat`.

### Bandwidth

## Bluetooth on RPi

## Wi-Fi on RPi

