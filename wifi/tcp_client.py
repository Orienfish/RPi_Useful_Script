# TCP client
# Wake up Wi-Fi, connect server and send packets
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
# Connect server
#########################################################
TCP_IP = "192.168.1.58"
TCP_PORT = 5005
MSG1="A"*1000 # 1kB packet
MSG2="b"*10000 # 10KB packet
MSG3="c"*100000 # 100kB packet
MSG4="D"*1000000 # 1000KB packet
CNT = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = False
time.sleep(5) # give it some time to recover
while (connect == False):
    try:
	stTime = time.time()
	s.connect((TCP_IP, TCP_PORT))
	FinTime = time.time()
        connect = True
    except:
        print "No network!"
        time.sleep(5)

#########################################################
# Sending various packets
#########################################################
stTime = time.time()
s.send(MSG1)
FinTime = time.time()
time.sleep(4.0)

stTime = time.time()
s.send(MSG2)
FinTime = time.time()
time.sleep(4.0)

stTime = time.time()
s.send(MSG3)
FinTime = time.time()
time.sleep(4.0)

stTime = time.time()
s.send(MSG4)
FinTime = time.time()
time.sleep(4.0)

#########################################################
# Finish
#########################################################
s.close()
