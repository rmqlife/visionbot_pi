#  http://docs.opencv.org/3.1.0/dd/d43/tutorial_py_video_display.html#gsc.tab=0
import cv2
import time
def write(length=5):
    cap = cv2.VideoCapture(0)
    # codec
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out  = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

    tic = time.time()
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            # show
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
            
        if time.time() - tic > length:
            break    
    cap.release()
    out.release()
        

if __name__ == "__main__":
    write()
