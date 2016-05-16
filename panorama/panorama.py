import bluetooth
import time
import picamera

# move from horizontal, or vertical
def move(h, v = 0):
    cmd = ""
    if h>0 :
        # turn right
        for i in xrange(h):
            cmd += "R" 
    else:
        # left
        for i in xrange(-h):
            cmd += "L"
            
    if v>0 :
        # up
        for i in xrange(v):
            cmd += "U"
        # down
        for i in xrange(v):
            cmd += "D"
    
    return cmd

if __name__ == "__main__":
    with open("../webcam/bluetooth/addr") as bt_addr:
        addr = bt_addr.readline().strip()
    port = 1
    
    sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((addr,port))
    camera = picamera.PiCamera()
    camera.hflip = True
    camera.vflip = True
    camera.brightness = 60
    
    #reset to the original place
    sock.send(move(-180)+"\n")
    
    #mk dir
    import os
    foldername = "data"+time.strftime("-%Y-%m-%d-%H:%M:%S")
    os.mkdir(foldername)

    step=10
    for i in range(10,170,step):
        sock.send(move(step)+"\n")
        time.sleep(0.4)
        camera.capture(os.path.join(foldername,str(i)+".jpg"))
        
