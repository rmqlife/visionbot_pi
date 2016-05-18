# reference:
# video play problem: http://www.raspberrypi-spy.co.uk/2013/05/capturing-hd-video-with-the-pi-camera-module/

import time
import bluetooth

class Motors:
    def __init__(self):
        # initial with addr file
        with open("addr",'r') as faddr:
            addr = faddr.readline().strip()
        port  = 1
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((addr,port))
    
    def arm_scan():
        for v in range(90,180,20):
            sock.send("V"+chr(v)+'\n')
            for h in range(0,180,20):
                sock.send('H'+chr(h)+'\n')
                time.sleep(0.2)

        sock.send('H'+chr(90))
        sock.send('V'+chr(90))
    
