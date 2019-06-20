import socket
import signal

TCP_IP = "192.168.1.60"
PORT = 5006
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, PORT))

while (1):
	s.listen(1)
	print "Listening..."

	conn, addr = s.accept()
	print "Connection address:", addr
	try:
	    while True:
	        data = conn.recv(1024)
	        if len(data) == 0: break
	        print("received [%s]" % data)
	except IOError:
	    pass

	conn.close()
