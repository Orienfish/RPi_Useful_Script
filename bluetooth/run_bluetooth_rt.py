# Bluetooth - time power test
# Preparation: set freq, turn off all network and bluetooth
import os
import sys
import time

startTime = time.time()
if (len(sys.argv) > 1):
    version = sys.argv[1]

# This import part is time and power consuming
timefile = "./realtime_bluetooth/time_" + version + ".txt"
f = open(timefile, "w")
f.write(str(time.time() - startTime) + "\r\n") # import time
# from bluetool import Bluetooth # not workable on raspberry
import bluetooth as bt
from bluetooth.ble import DiscoveryService

#########################################################
# Turn on Bluetooth
#########################################################
time.sleep(5)
UP_CMD = "sudo rfkill unblock bluetooth; sudo hciconfig hci0 up;"
os.system(UP_CMD)
f.write(str(time.time() - startTime) + "\r\n") # turn on time

#########################################################
# Scan
#########################################################
def scan_ble(duration=8):
    svc = DiscoveryService()
    devs = svc.discover(duration) 
    print "Find %d devices: " %len(devs)
    if devs:
        for name, addr in devs.items():
	    print name, addr
    return devs

def scan_non_ble(duration=8):
    devs = bt.discover_devices(duration=duration, flush_cache=True, \
	lookup_names=True)

time.sleep(2.0) # idle
print "scanning..."
stTime = time.time()
devs = scan_non_ble(10)
FinTime = time.time()

if devs:
    print "Find %d devices: " %len(devs)
    for name, addr in devs:
	print name, addr

f.write("%f,%f\r\n" %(stTime - startTime, FinTime - startTime))

#########################################################
# Connect
#########################################################
addr = "9C:B6:D0:F5:34:5A"
port = 1

time.sleep(4.0) # idle
try:
    stTime = time.time()
    sock = bt.BluetoothSocket( bt.RFCOMM )
    sock.connect((addr, port))
    FinTime = time.time()
except Exception as e:
    print(e)
    sys.exit()
f.write("%f,%f\r\n" %(stTime - startTime, FinTime - startTime))

#########################################################
# Send
#########################################################
MSG1="A"*1000 # 1kB packet
MSG2="b"*10000 # 10KB packet
MSG3="c"*100000 # 100kB packet
MSG4="D"*1000000 # 1000KB packet

time.sleep(4.0) # idle
stTime = time.time()
sock.send(MSG1)
FinTime = time.time()
f.write("%f,%f\r\n" %(stTime - startTime, FinTime - startTime))

time.sleep(4.0) # idle
stTime = time.time()
sock.send(MSG2)
FinTime = time.time()
f.write("%f,%f\r\n" %(stTime - startTime, FinTime - startTime))

time.sleep(4.0) # idle
stTime = time.time()
sock.send(MSG3)
FinTime = time.time()
f.write("%f,%f\r\n" %(stTime - startTime, FinTime - startTime))

time.sleep(4.0) # idle
stTime = time.time()
sock.send(MSG4)
FinTime = time.time()
f.write("%f,%f\r\n" %(stTime - startTime, FinTime - startTime))

sock.close()
f.close()

