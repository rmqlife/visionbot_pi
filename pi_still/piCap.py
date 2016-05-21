#  http://docs.opencv.org/3.1.0/dd/d43/tutorial_py_video_display.html#gsc.tab=0
#  http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
# http://raspi.tv/2013/another-way-to-convert-raspberry-pi-camera-h264-output-to-mp4 

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
        
        pass
   
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
        
        tic = time.time()
        # capture frames from the camera
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            self.writer.write(image)
            movefunc_ret = movefunc()
            time.sleep(0.3)
            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)
            # need to stop
            if (time.time() - tic > timeout) or (not self._running) or (not movefunc_ret):
                break

        # release the writer
        self.writer.release()
        
    def terminate(self):    
        self._running = False
        pass

            
if __name__ == "__main__":
    # init video recording
    video = VideoStream()
    # init motors, establish bluetooth
    from motors import Motors
    motors = Motors()

    motors.arm_scan_init()
    # start to recording
    video.record(motors.arm_scan_loop,'result/scan1.avi')
    motors.arm_scan_init()
    video.record(motors.arm_scan_loop,'result/scan2.avi')
