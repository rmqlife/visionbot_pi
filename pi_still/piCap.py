#  http://docs.opencv.org/3.1.0/dd/d43/tutorial_py_video_display.html#gsc.tab=0
#  http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
# http://raspi.tv/2013/another-way-to-convert-raspberry-pi-camera-h264-output-to-mp4 

import numpy as np
from marker import marker
from motors import Motors
from videoStream import VideoStream
import movement

# init motors, establish bluetooth
motors = Motors()

def findmarker(img):
    mlist = marker().find(img,debug = 0, show = 0)
    if len(mlist)>0:
        return 2 # find marker
    else:
        # if scan if ending, return True
        motors.turn()
        import time
        time.sleep(0.1)
            
if __name__ == "__main__":
    # start to recording
    # init video recording
    motors.arm_move((90,90))
    video = VideoStream()
    ret = video.record(findmarker, path = 'result/find.avi', timeout = 30)
    
