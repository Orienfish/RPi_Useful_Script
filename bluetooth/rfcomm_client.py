# Bluetooth client
# Wake up bluetooth, scan, connect to server and send data
import os
import sys
import time
# from bluetool import Bluetooth # not workable on raspberry
import bluetooth as bt
from bluetooth.ble import DiscoveryService

#########################################################
# Turn on Bluetooth
#########################################################
UP_CMD = "sudo rfkill unblock bluetooth; sudo hciconfig hci0 up;"
os.system(UP_CMD)

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

print "scanning..."
devs = scan_non_ble(10)

if devs:
    print "Find %d devices: " %len(devs)
    for name, addr in devs:
	print name, addr

#########################################################
# Connect
#########################################################
addr = "9C:B6:D0:F5:34:5A" # address of the bluetooth target
port = 1 # default port used by rfcomm server

time.sleep(4.0) # idle
try:
    stTime = time.time()
    sock = bt.BluetoothSocket( bt.RFCOMM )
    sock.connect((addr, port))
    FinTime = time.time()
except Exception as e:
    print(e)
    sys.exit()

#########################################################
# Send
#########################################################
MSG1="A"*1000 # 1kB packet
MSG2="b"*10000 # 10KB packet
MSG3="c"*100000 # 100kB packet
MSG4="D"*1000000 # 1000KB packet

time.sleep(4.0) # idle
sock.send(MSG1)

time.sleep(4.0) # idle
sock.send(MSG2)

time.sleep(4.0) # idle
sock.send(MSG3)

time.sleep(4.0) # idle
sock.send(MSG4)

sock.close()
