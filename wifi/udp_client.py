# Wi-Fi power test
# Preparation: set freq, set bw, turn off all network
import os
import sys
import time

startTime = time.time()
if (len(sys.argv) > 1):
    version = sys.argv[1]

timefile = "./exp_udp/time_" + version + ".txt"
f = open(timefile, "w")

#########################################################
# Import
#########################################################
# This import part is time and power consuming
import socket

#########################################################
# Idle
#########################################################
time.sleep(1.0)
stTime = time.time()
time.sleep(5)
FinTime = time.time()
f.write("idle,%f,%f\r\n" %(stTime - startTime, FinTime - startTime)) # idle time

#########################################################
# Turn on Wi-Fi
#########################################################
time.sleep(1.0)
UP_CMD = "sudo ifconfig wlan0 up; sudo ifconfig ifb0 up;"
stTime = time.time()
os.system(UP_CMD)
FinTime = time.time()
f.write("turn_on,%f,%f\r\n" %(stTime - startTime, FinTime - startTime)) # turn on time

#########################################################
# Idle
#########################################################
stTime = time.time()
time.sleep(5)
FinTime = time.time()
f.write("turn_on_idle,%f,%f\r\n" %(stTime - startTime, FinTime - startTime)) # idle time

#########################################################
# wait util connect to AP
#########################################################
stTime = time.time()
time.sleep(30)
FinTime = time.time()
f.write("connect_idle,%f,%f\r\n" %(stTime - startTime, FinTime - startTime)) # idle time

#########################################################
# Sending different size at different BW in 1 second
#########################################################
UDP_IP = "192.168.1.60"
UDP_PORT = 5006

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
BW = [1e2, 2e2, 5e2, 1e3, 2e3, 5e3, 1e4, 2e4, 5e4, 1e5] # kbps
#BW = [1e3, 2e3, 5e3, 1e4, 2e4, 5e4, 1e5, 2e5, 5e5, 1e6]
#SIZE = [1e3, 2e3, 5e3, 1e4, 2e4, 5e4, 5e4, 5e4, 5e4, 5e4] # Byte
#T = [1, 1, 1, 1, 1, 1, 0.5, 0.25, 0.1, 0.05]
SIZE = 1e4
T = [1, 0.5, 0.25, 0.2, 0.167, 0.125, 0.1, 0.05, 0.02]
PERIOD = 5

for bw in BW: 
    time.sleep(1.0)
    SET_BW= "sudo bash /home/pi/Desktop/Target_Pi1/set_bw.sh %d" %bw
    os.system(SET_BW)
    time.sleep(1.0)

    for i in range(0, len(T)):
        #MSG = "A" * int(SIZE[i])
	#rate = (float)(SIZE[i] / T[i])
	#print "Testing %d B/s %d kbps bw" %(rate, bw)
	MSG = "A" * int(SIZE)
        rate = (1.0 / T[i])
	print "Testing %d pkt/s %d kbps bw" %(rate, bw)
        
        stTime = time.time()
        t = 0
        while t < PERIOD:
            cur_call = time.time()
            # print cur_call - stTime
            s.sendto(MSG, (UDP_IP, UDP_PORT))
            if (time.time() - cur_call < T[i]):
                time.sleep(cur_call + T[i] - time.time())
            else:
                print "overload"
            t += T[i]
                        
        FinTime = time.time()
        f.write("%d,%d,%f,%f\r\n" %(bw, rate, stTime - startTime, FinTime - startTime))

#########################################################
# Finish
#########################################################
s.close()
f.close()
os.system("ssh pi@192.168.1.39 \"bash -c 'killall -9 bash'\"")


