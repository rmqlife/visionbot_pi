# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

class PiStill:
    def __init__(self):
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.hflip = True
        self.camera.vflip = True
        self.camera.resolution = (640, 480)
        # allow the camera to warmup
        time.sleep(0.1)
        

    def imread(self):
        # grab an image from the camera
        rawCapture = PiRGBArray(self.camera)
        self.camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        return image


if __name__ == "__main__":
    cap = PiStill()

    # start to control camera's movements
    import motors
    m = motors.Motors(range(0,180,30),[90,120,150])
    import marker    
    import movement
    num = 0
    while m.arm_scan_loop():
        time.sleep(0.15)
        img = cap.imread()
        cv2.imwrite("result/"+str(num)+".jpg", img)
        num += 1    
        mlist = marker.marker().find(img,debug = 0, show = 0)
        if (len(mlist)>0):
            num,pos = mlist[0]
            center = tuple(np.int0( np.mean(pos.reshape(4,2), axis = 0)))
            img_center = tuple(img.shape[:2])
            img_center = (img_center[1]/2,img_center[0]/2)

            h,v = movement.move2obj(center,img_center)
            break

    tweak_times = 0    
    while abs(h)>0.1 and abs(v)>0.1 and tweak_times < 5:
        time.sleep(0.15)
        img = cap.imread()
        cv2.imwrite("result/tweak"+str(tweak_times)+".jpg", img)
        tweak_times += 1
        mlist = marker.marker().find(img,debug = 0, show = 0)
        if (len(mlist)>0):
            num,pos = mlist[0]
            center = tuple(np.int0( np.mean(pos.reshape(4,2), axis = 0)))
            img_center = tuple(img.shape[:2])
            img_center = (img_center[1]/2,img_center[0]/2)
            import movement
            h,v = movement.move2obj(center,img_center)
            hnow,vnow = m.arm_status
            m.arm_move((int(hnow+40*h), int(vnow+40*v)))
        else
                
            
        
