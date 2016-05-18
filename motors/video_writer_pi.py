#  http://docs.opencv.org/3.1.0/dd/d43/tutorial_py_video_display.html#gsc.tab=0
#  http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
import cv2
import time

from picamera.array import PiRGBArray
import picamera

from threading import Thread


class VideoStream:
    def __init__(self):
        # the flag of the thread running
        self._running = True
        # init the camera
        self.camera = self.camera_init()
        # initialize the camera and grab a reference to the raw camera capture
        self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        # codec
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.writer  = cv2.VideoWriter('output.avi', fourcc, float(self.camera.framerate), self.camera.resolution)
        # allow the camera to warmup
        time.sleep(0.1)
        pass
   
    # setting the camera     
    def camera_init(self):
        camera = picamera.PiCamera()    
        camera.hflip = True
        camera.vflip = True
        camera.resolution = (1080, 720)
        camera.framerate = 32        
        return camera
        
        
    def record(self, length = 20):
        tic = time.time()
        # capture frames from the camera
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
	        image = frame.array
	        self.writer.write(image)
	        # clear the stream in preparation for the next frame
	        self.rawCapture.truncate(0)
	        
	        if (time.time() - tic > length) or (not self._running):
	            break
	    # release the writer
        self.writer.release()
	    
    def terminate(self):    
        self._running = False
        pass
    
            
if __name__ == "__main__":
    vs = VideoStream()
    thread_vs = Thread(target = vs.record, args = (100,))
    thread_vs.start()
    # start to control camera's movements
    import motors
    m = motors.Motors()
    m.arm_scan()

    vs.terminate()
    
