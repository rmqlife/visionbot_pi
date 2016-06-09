#  http://docs.opencv.org/3.1.0/dd/d43/tutorial_py_video_display.html#gsc.tab=0
#  http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
# http://raspi.tv/2013/another-way-to-convert-raspberry-pi-camera-h264-output-to-mp4 

import numpy as np
from marker import marker
from motors import Motors
from videostream import VideoStream
import movement


# init motors, establish bluetooth
motors = Motors()



def findmarker(img):
    mlist = marker().find(img,debug = 0, show = 0)
    if len(mlist)>0:
        return 2 # find marker
    else:
        # if scan if ending, return True
        if motors.arm_scan_loop():
            return 1
        else: # not the end
            return 0

def barescan(img):
    return motors.arm_scan_loop()

def aimmarker(img): 
    mlist = marker().find(img, debug = 0, show = 0)
    
    print "aim:",mlist
    if len(mlist)==1:
        num,pos = mlist[0]
        center = tuple(np.int0( np.mean(pos.reshape(4,2), axis = 0)))
        img_center = tuple(img.shape[:2])
        img_center = (img_center[1]/2,img_center[0]/2)
        h, v = movement.move2obj(center, img_center)
        print h,v
        
        T = 0.1        
        if abs(h)<T and abs(v)<T: # and abs(v)<0.1:
            return 2 # aim at it 
        import math
        if abs(v)>T:
            motors.arm_move_delta(0, int(math.copysign(ceil(abs(v)*10),v)))
            return 0
        if abs(h)>T:
            motors.arm_move_delta(int(math.copysign(ceil(abs(h)*10),h)), 0)
            return 0
    return 0


if __name__ == "__main__":
    motors.arm_scan_init(hlist=range(10,170,10), vlist=range(60,120,20))
    # start to recording
    # init video recording
    video = VideoStream()
    ret = video.record(findmarker, path = 'result/find.avi', timeout = 30)
    
    #if ret==2: # yes, find the marker
    print video.record(aimmarker, path = 'result/aim.avi', timeout = 10)
        
