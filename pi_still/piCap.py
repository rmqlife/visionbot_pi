#  http://docs.opencv.org/3.1.0/dd/d43/tutorial_py_video_display.html#gsc.tab=0
#  http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
# http://raspi.tv/2013/another-way-to-convert-raspberry-pi-camera-h264-output-to-mp4 

import numpy as np
from marker import marker
from motors import Motors
from videoStream import VideoStream

class Move:
    def __init__(self):
        # initialize the status
        self.dist = 1
        self.dist_prev = 2
        self.act_prev = 'r'
        # init motors, establish bluetooth
        self.motors = Motors()
        self.motors.arm_move((90,90))
    
    def targetDist(self,targetCenter, imgCenter):
        # range from 0 to 1
        h = float(imgCenter[0]-targetCenter[0])/imgCenter[0]
        v = float(imgCenter[1]-targetCenter[1])/imgCenter[1]
        return h
        
    def findmarker(self, img):
        # return > 0 to end finding process  
        print self.dist
 
        if abs(self.dist)>abs(self.dist_prev):
        # the result got worse
            if self.act_prev == 'r':
                self.act = 'l'
            if self.act_prev == 'l':
                self.act = 'r'
        if abs(self.dist)<=abs(self.dist_prev):
        # the result got better or same, keep doing
            self.act = self.act_prev          
        
        self.motors.turn(self.act)
        import time
        time.sleep(0.1)
        self.act_prev = self.act
        self.dist_prev = self.dist
             
        mlist = marker().find(img, debug = 0, show = 0)
        #default dist, which means the not found response
           
        if len(mlist)==1:
            num, pos = mlist[0]
            center = tuple(np.int0( np.mean( pos.reshape(4,2), axis = 0)))
            img_center = tuple( img.shape[:2])
            img_center = (img_center[1]/2, img_center[0]/2)
            self.dist = self.targetDist(center, img_center)
        else:
            self.dist = 2
        return 0  
        
                     
if __name__ == "__main__":
    # start to recording
    # init video recording
    move = Move()
    video = VideoStream()
    ret = video.record(move.findmarker, path = 'result/find.avi', timeout = 30)
    
