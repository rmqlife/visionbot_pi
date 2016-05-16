# reference: 
# RANSAC: https://en.wikipedia.org/wiki/RANSAC
# stitching: http://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/
# about homography http://www.learnopencv.com/homography-examples-using-opencv-python-c/
# 2016-4-28

import cv2
import numpy as np

class Stitcher:
    def stitch(self, imgs, ratio=0.75, reprojThresh = 4.0, showMatches = False):
        (imgB, imgA) = imgs
        (kpsA, descsA) = self.detect(imgA)  
        (kpsB, descsB) = self.detect(imgB)
        
        #convert kp class to np matrix
        kpsB = np.float32([kp.pt for kp in kpsB])
        kpsA = np.float32([kp.pt for kp in kpsA])
        #match key points
        M = self.match(kpsA,kpsB,descsA,descsB,ratio,reprojThresh)
        if M is None:
            return None
        (matches,H,status) = M

        # show matches of invariant descriptor
        if showMatches:
            vis = self.drawMatches(imgA,imgB,kpsA,kpsB,matches,status)
            cv2.imshow('vis',vis)
            cv2.waitKey()        
        else:
            vis = imgA
        # stitch images
        (hA,wA) = imgA.shape[:2]
        (hB,wB) = imgB.shape[:2]
        result = cv2.warpPerspective(imgA, H, (wA + wB, hA))
        result[0:hB,0:int(wB*0.6)] = imgB[:,0:int(wB*0.6)]

        return (result,vis)
        
    def detect(self,img):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        detector = cv2.AKAZE_create()
        (kps, descs) = detector.detectAndCompute(gray, None)
        return (kps,descs)
    
    def match(self, kpsA, kpsB, featuresA, featuresB,
        ratio, reprojThresh):
        # compute the raw matches and initialize the list of actual
        # matches
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        # using knn to find top 2 nearest neighbors in featuresB for each element in featuresA
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []
        
        # show index of points pairs, query idx in A only appears once while train idx in B not
        # print ([(m[0].queryIdx,m[0].trainIdx) for m in rawMatches])
        
        # loop over the raw matches
        for m in rawMatches:
            # ensure the distance is within a certain ratio of each
            # other (i.e. Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))
        # show index matches
        #print matches
        
        # computing a homography requires at least 4 matches
        if len(matches) > 4:
            # construct the two sets of points, 2Dl coordinates (x,y)
            ptsA = np.float32([kpsA[i] for (_,i) in matches])
            ptsB = np.float32([kpsB[i] for (i,_) in matches])
            
            # compute the homography between the two sets of points
            (H,status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)
            
            # return the matches along with the homography matrix, which is 3*3 transformation matrix
            # and status of each matched point, which is true or false
            
            return (matches, H, status)
        return None
    
    #visualize key points match    
    def drawMatches(self, imgA, imgB, kpsA, kpsB, matches, status):
        (hA, wA) = imgA.shape[:2]
        (hB, wB) = imgB.shape[:2]
        # init the output background, depth=3, unsigned int 8 [0,255]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imgA
        vis[0:hB, wA:] = imgB
        # loop over the matches
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            # only process the match if the status is true
            if s == 1:
                #draw match a line
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0])+wA, int(kpsB[trainIdx][1]))
                cv2.line(vis,ptA,ptB, (0,255,0), 1)
        return vis 
    
    
if __name__=="__main__":
    import sys
    fnA = '/home/rmqlife/Pictures/capture0.jpg'
    fnB = '/home/rmqlife/Pictures/capture1.jpg'
    if len(sys.argv)>2:
        fnA = sys.argv[1]
        fnB = sys.argv[2]
    imgA = cv2.imread(fnA)
    imgB = cv2.imread(fnB)

    (result,vis) = Stitcher().stitch((imgA,imgB),showMatches=True)

    if len(sys.argv)>3:
        cv2.imwrite(sys.argv[3],result)
    else:
        cv2.imshow('result',result)
        cv2.waitKey(0)
  
    if len(sys.argv)>4:
        cv2.imwrite(sys.argv[4],vis)
    
    
