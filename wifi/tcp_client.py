# Wi-Fi power test
# Preparation: set freq, set bw, turn off all network
import os
import sys
import time
import socket

startTime = time.time()
if (len(sys.argv) > 1):
    version = sys.argv[1]

#filename = "./realtime_wifi/" + version + ".txt"
#EXEC_CMD = "bash ./get_cpu_usage.sh 0 > %s &" %filename
#os.system(EXEC_CMD)

#########################################################
# Turn on Wi-Fi
#########################################################
time.sleep(4)
timefile = "./realtime_measure/time_" + version + ".txt"
f = open(timefile, "w")
UP_CMD = "sudo ifconfig wlan0 up; sudo ifconfig ifb0 up;"
os.system(UP_CMD)
f.write(str(time.time() - startTime) + "\r\n") # turn on time

#########################################################
# Connect AP
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
time.sleep(5)
while (connect == False):
    try:
	stTime = time.time()
	s.connect((TCP_IP, TCP_PORT))
	FinTime = time.time()
        connect = True
    except:
        print "No network!"
        time.sleep(5)
f.write("%f,%f\r\n" %(stTime - startTime, FinTime - startTime))

#########################################################
# Sending various packets
#########################################################
time.sleep(4.0) # idle
stTime = time.time()
s.send(MSG1)
FinTime = time.time()
f.write("%f,%f\r\n" %(stTime - startTime, FinTime - startTime))
time.sleep(4.0)

stTime = time.time()
s.send(MSG2)
FinTime = time.time()
f.write("%f,%f\r\n" %(stTime - startTime, FinTime - startTime))
time.sleep(4.0)

stTime = time.time()
s.send(MSG3)
FinTime = time.time()
f.write("%f,%f\r\n" %(stTime - startTime, FinTime - startTime))
time.sleep(4.0)

stTime = time.time()
s.send(MSG4)
FinTime = time.time()
f.write("%f,%f\r\n" %(stTime - startTime, FinTime - startTime))
time.sleep(4.0)

#########################################################
# Finish
#########################################################
s.close()
f.close()
#KILL_CMD = "killall -9 bash"
#os.system(KILL_CMD)



