import time
import bluetooth
addr='30:14:11:17:21:57'
result=bluetooth.lookup_name(addr,timeout=5)
if (result !=None):
	print result+" is on"
else:
	print "offline"
port=1
sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((addr,port))
sock.send("n\n")
sock.close()

