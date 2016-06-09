import cv2
import time

from picamera.array import PiRGBArray
import picamera

class VideoStream:
    def __init__(self):
        # the flag of the thread running
        self._running = True
        # init the camera
        self.camera = self.camera_init()
        # initialize the camera and grab a reference to the raw camera capture
        self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        
   
    # setting the camera     
    def camera_init(self):
        camera = picamera.PiCamera()    
        camera.hflip = True
        camera.vflip = True
        #camera.resolution = (640, 480)
        #camera.framerate = 10        
        return camera
        
        
    def record(self, movefunc, path = 'result/output.avi', timeout = 100):
        # init the file recording file
        # codec
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.writer  = cv2.VideoWriter(path , fourcc, float(self.camera.framerate), self.camera.resolution)
        
        time.sleep(0.2)
        self.rawCapture.truncate(0)
        tic = time.time()
            
        # capture frames from the camera
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            self.writer.write(image)
            movefunc_ret = movefunc(image)
            time.sleep(0.3)
             # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)
            # need to stop
            if (time.time() - tic > timeout) or (not self._running) or (movefunc_ret>0):
                break

        # release the writer
        self.writer.release()
        return movefunc_ret

    def terminate(self):    
        self._running = False
        pass
