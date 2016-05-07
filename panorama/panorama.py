import bluetooth
import time
import picamera
addr='30:14:11:17:21:57'
port=1
sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((addr,port))
camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True
camera.brightness = 60

steps=9
for i in xrange(steps):
    sock.send("3"+"\n")
    time.sleep(0.3)
    camera.capture("cap"+str(i)+".jpg")
    time.sleep(0.1)


#reset to the original place
for i in xrange(steps):
    sock.send("4\n")
    time.sleep(0.2)
    

