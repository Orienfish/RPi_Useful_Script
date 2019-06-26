# Raspberry Pi Useful Scripts

This repo contains some useful scripts on RPi, including performance monitoring, setting and how to use bluetooth as well as Wi-Fi on RPi. In the last part, I also include a link to some RPi benchmarks in another repo.

## List of Content

[CPU Frequency](#CPU-Frequency)

[CPU Uitlization](#CPU-Uitlization)

[CPU Temperature](#CPU-Temperature)

[Performance Counters](#Performance-Counters)

[Bandwidth](#Bandwidth)

[Bluetooth on RPi](#Bluetooth-on-RPi)

[Wi-Fi on RPi](#Wi-Fi-on-RPi)

[Benchmarks on RPi]()(#Benchmarks-on-RPi)

## Performance Monitoring and Setting

Different from other micro-controller platforms that require reading low-level code or setting register values to access performance values, on RPi, **scripts reading/setting certain files** (everything on Linux is a file!) and some **helpful tools (e.g. perf, wondershaper)** will be enough!

If you are interested in working with the following performance metrics on Linux, this is the right place for you!

Note:

* All the code in this repo are tested on RPi 3B. It may work on traditional Linux, or will work after some modifications.
* There are a lot of system monitor software such as conky, psensor, etc. These may be the perfect tools in certain applications, but this repo focuses on the **simple script-based methods where the data can be printed out to terminal and obtained remotely**.

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

2. `set_freq.sh` sets the CPU frequency of all cores to your specified value. RPi 3B could only be set to either 600MHz or 1200MHz. 

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

* A simple command can be used to get CPU temperature in millidegrees Celsius, on Linux-based system:

  ```sh
  cat /sys/class/thermal/thermal_zone0/temp
  ```

  This is the kernel-based interfaces for thermal zone devices (sensors) and thermal cooling devices (fan, processor...), being part of the thermal sysfs driver. The following command displays which the temperation-zone matching: 

  ```sh
  $ paste <(cat /sys/class/thermal/thermal_zone*/type) <(cat /sys/class/thermal/thermal_zone*/temp) | column -s $'\t' -t | sed 's/\(.\)..$/.\1°C/'
  ```

  For more information, check the [kernel documentation](https://www.kernel.org/doc/Documentation/thermal/sysfs-api.txt).

* On RPi, the [vcgencmd](https://elinux.org/RPI_vcgencmd_usage) tool can be used to obtain the core temperature of BCM2835 SoC (This is what they said in their doc, but no idea on the specific location of the sensor, CPU?Or GPU?) Use the following command to get CPU temperature:

  ```sh
  /opt/vc/bin/vcgencmd measure_temp
  ```

  To get only the temperature value in Celsius:

  ```sh
  vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'
  ```

I combine those two commands into one script `get_temp.sh`, which is adapted from [here](https://www.cyberciti.biz/faq/linux-find-out-raspberry-pi-gpu-and-arm-cpu-temperature-command/). To use it:

```sh
bash get_temp.sh
```

### Performance Counters

I use the `perf stat` tool that is built in Linux to monitor performance counter values. The events can be monitored include instruction counts, cache misses, etc. For more information, refer to the [manual page](http://man7.org/linux/man-pages/man1/perf-stat.1.html) of `perf stat`.

In the `perf_script.sh` script, I simply use the following commands:

```sh
sudo perf stat -a -I 200 -x, -e instructions,cache-misses,L1-dcache-loads,L1-dcache-stores,branch-instructions,branch-misses,cache-references,cpu-cycles,r110,r13C,r1A2,r1C2 sleep infinity 2>&1
```

### Bandwidth

The [wondershaper](https://github.com/magnific0/wondershaper) is a magic tool that can limit the bandwidth of any network adapters through commands. Two scripts based on wondershaper is included in this repo:

To set the Wi-Fi bandwidth to 100kbps, use:

```sh
sudo bash set_bw.sh 100
```

To clear all the bandwidth settings:

```sh
sudo bash reset_bw.sh
```

Note that you may have to *change the path* to your wondershaper tool inside the scripts.

## Bluetooth on RPi

The Bluetooth on RPi is a little tricky.

1. By default, RPi turns off the Bluetooth. You may want to use the following commands, which is in the `bluetooth/wake_bluetooth.sh` script:

   ```sh
   sudo rfkill unblock bluetooth 
   sudo hciconfig hci0 up
   ```

   To check the status of the Bluetooth, you can check the Bluetooth icon at you up-right corner of the screen (if you connect a screen), or you can try:

   ```sh
   hciconfig
   ```

   to see whether the state is UP or DOWN.

   Reversing the above commands, `cut_bluetooth.sh` turns off Bluetooth. To use it:

   ```sh
   sudo bash cut_bluetooth.sh
   ```

2. There are some command-line tools to use the Bluetooth. [Bluetoothctl](http://www.linux-magazine.com/Issues/2017/197/Command-Line-bluetoothctl) is a very convenient built-in tool for using Bluetooth on Linux. With simple commands, you can **scan, pair and connect** to another Bluetooth device. Pay attention to the difference between "pair" and "connect" - some devices need the 6-digit code match step which is completed in "connect" rather than "pair".

3. For Python API on RPi,

   * [Bluetooth Comm API](https://bluedot.readthedocs.io/en/latest/btcommapi.html) is a well-wrapped API, with which you can ignore all the scanning and pairing details, treating the Bluetooth as a client/server model. 
   * [pybluez](https://github.com/pybluez/pybluez) includes more fine-grained control, such as scanning and connecting. It does not distinguish pair and connect - it wraps the connection part into a client/server model.
   * [bluetool](https://pypi.org/project/bluetool/) is a Python API for Bluetooth D-Bus calls on Linux. It has modes of scanning, pairing and connecting, while sending and receiving packets are excluded. As far as I know, its current version (0.2.3) does not support RPi.

   In this repo, I choose pybluez.

4. The installation of pybluez may be annoying - there are a bunch of dependencies to be satisfied. [This tutorial](https://learn.adafruit.com/install-bluez-on-the-raspberry-pi/installation) covers the installation steps. And it has some additional requirements for the BLE mode. Unfortunately I was not able to find the link I refer to.

5. For the scripts in this repo, I provide the whole process of **turning on Bluetooth, scanning, establishing client/server connection and sending packets to server** in `bluetooth/rfcomm_client.py`.

   Another script `bluetooth/rfcomm_server.py` is running on the other Bluetooth device to receive packets.

## Wi-Fi on RPi

Wi-Fi is the most commonly used part on RPi, thus I won't explain much. This part acts as a cheat sheet, a place to look for when encountering Wi-Fi setting problems in the future.

In the `wifi` folder, there are 6 available code files:

* `wake_network.sh` turns on wlan0 on RPi.
* `cut_network.sh` cuts all the network connection on RPi.
* `tcp_client.py` and `tcp_server.py` are the Python code to establish simple TCP connection.
* `udp_client.py` and `udp_client.py` establish UDP connection.

## Benchmarks on RPi

In [another repo](https://github.com/Orienfish/IoTSim_Model), a CPU workload is constructed based on the work in [Roy Longbottom's Raspberry Pi, Pi 2 and Pi 3 Benchmarks](http://www.roylongbottom.org.uk/Raspberry Pi Benchmarks.htm), combining Dhrystone, Whetstone, Linpack, and their multi-thread versions.