import cv2
import numpy as np


def move2obj(center,img_center=(320,240)):
    h = float(img_center[0] - center[0])/img_center[0] 
    v = float(img_center[1] - center[1])/img_center[1]
    return h,v

if __name__ == "__main__":
    img = cv2.imread('result/16.jpg')
    from marker import marker
    rlist = marker().find(img, debug = 0, show =0)
    if len(rlist) > 0 :
        num, pos = rlist[0]
        center = tuple(np.int0( np.mean(pos.reshape(4,2), axis = 0)))
        img_center = tuple(img.shape[:2])
        img_center = (img_center[1]/2,img_center[0]/2)
        print move2obj(center,img_center)

