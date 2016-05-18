# reference:
# video play problem: http://www.raspberrypi-spy.co.uk/2013/05/capturing-hd-video-with-the-pi-camera-module/

import time
import bluetooth
import picamera
# initial with addr file
def init():
    with open("addr",'r') as faddr:
        addr = faddr.readline().strip()
    port  = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((addr,port))
    return sock

def arm_scan(sock):
    for v in range(90,180,20):
        sock.send("V"+chr(v)+'\n')
        for h in range(0,180,20):
            sock.send('H'+chr(h)+'\n')
            time.sleep(0.2)

    sock.send('H'+chr(90))
    sock.send('V'+chr(90))
    pass

def camera_init():
    camera = picamera.PiCamera()    
    camera.hflip = True
    camera.vflip = True
    return camera

def live():
    # import the necessary packages
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    import time
    import cv2
     
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
     
    # allow the camera to warmup
    time.sleep(0.1)
     
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	    # grab the raw NumPy array representing the image, then initialize the timestamp
	    # and occupied/unoccupied text
	    image = frame.array
     
	    # clear the stream in preparation for the next frame
	    rawCapture.truncate(0)
     
if __name__ == "__main__":
    sock = init()
    
    live()
    
    sock.close()
    
