# UDP client
# Wake up Wi-Fi and send UDP packets
import os
import sys
import time
import socket

#########################################################
# Turn on Wi-Fi
#########################################################
UP_CMD = "sudo ifconfig wlan0 up; sudo ifconfig ifb0 up;"
os.system(UP_CMD)

#########################################################
# Wait util connect to AP
# Unlike TCP, UDP does not have connecting step
#########################################################
time.sleep(30)

#########################################################
# Sending different size at different BW in 1 second
#########################################################
UDP_IP = "192.168.1.60"
UDP_PORT = 5006

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
BW = [1e3, 2e3, 5e3, 1e4, 2e4, 5e4, 1e5, 2e5, 5e5, 1e6]
SIZE = [1e3, 2e3, 5e3, 1e4, 2e4, 5e4, 5e4, 5e4, 5e4, 5e4] # Byte
T = [1, 1, 1, 1, 1, 1, 0.5, 0.25, 0.1, 0.05]
PERIOD = 5

for bw in BW: 
    SET_BW= "sudo bash /home/pi/Desktop/Target_Pi1/set_bw.sh %d" %bw
    os.system(SET_BW)
    time.sleep(1.0)

    for i in range(0, len(T)):
        MSG = "A" * int(SIZE[i])
	rate = (float)(SIZE[i] / T[i])
	print "Testing %d B/s %d kbps bw" %(rate, bw)
        
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
                        

#########################################################
# Finish
#########################################################
s.close()
