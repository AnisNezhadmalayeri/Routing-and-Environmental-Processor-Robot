import RPi._GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2

camera=PiCamera()
camera.resolution=(640,480)
camera.framerate=60
rawCapture=PiRGBArray(camera,size=(640,480))

for frame in camera.capture_continuous(rawCapture,format="bgr"):
    img= frame.array
    for i in range(10):
        img=cv2.line(img,(0,i*100),(1400,i*100),(255,255,255),2)

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_blue=np.array([0,0,0])
    upper_blue=np.array([130,160,80])
    mask1=cv2.inRange(hsv,lower_blue,upper_blue)

    _,contours,hi = cv2.findContours(mask1,1,2)
    for cnt in contours:
        if(cv2.contourArea(cnt)>400 and cv2.contourArea(cnt)<10000):
            rect=cv2.minAreaRect(cnt)
            box=cv2.boxPoints(rect)
            box=np.int0(box)
            img2=cv2.drawContours(image,[box],0,(0,255,0),2)

            m=cv2.moments(cnt)
            if(m['m00']!=0):
                cx=int(m['m10']/m['m00'])
                cy=int(m['m01']/m['m00'])
            #print(cx)
            #print(cy)
            #print()
                if(cx>260):
                    print("  R")
                elif(cx<220):
                    print("L")
                else:
                    print(' C')
            else:
                print("zero")
            #cv2.imshow('img',img2)
            #cv2.waitKey()
        else:
            print("false countour")
    rawCapture.truncate()
    rawCapture.seek(0)
    
cv2.destroyAllWindows()



