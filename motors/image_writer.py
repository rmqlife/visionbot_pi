# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2


class PiStill:

    def __init__(self):
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(camera)

        self.camera.hflip = True
        self.camera.vflip = True
        self.camera.resolution = (1080, 720)
        # allow the camera to warmup
        time.sleep(0.1)
        

    def imread(self):
        # grab an image from the camera
        self.camera.capture(self.rawCapture, format="bgr")
        image = self.rawCapture.array
        return image


if __name__ == "__main__":
    cap = PiStill()

    # start to control camera's movements
    import motors
    m = motors.Motors()
    
    num = 0
    while m.arm_scan_loop():
        img = cap.imread()
        cv2.imwrite("data/"+str(num)+".jpg")
        num += 1
