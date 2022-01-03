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
    lower_blue=np.array([0,0,0])
    upper_blue=np.array([130,160,80])
    res=img
    hsv=cv2.cvtColor(res,cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    edges=cv2.Canny(gray,50,150,apertureSize=3)
    edges=cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
    mask3=cv2.inRange(edges,lower_blue,upper_blue)
    _,contours,_=cv2.findContours(mask3,1,2)
    c=contours[0]
    area_list=[]
    rect=cv2.minAreaRect(c)
    box=cv2.boxPoints(rect)
    box=np.int0(box)
    img2=cv2.drawContours(res,[box],-1,(0,0,255),10)
    m=cv2.moments(contours[0])
    cx=int(m['m10']/m['m00'])
    cy=int(m['m01']/m['m00'])
    if(cx>260):
        print("  R")
    elif(cx<220):
        print("L")
    else:
        print(' C')
    cv2.imshow('out',img2)
    k=cv2.waitKey(1) & 0xff
    if k==27:
        break

cv2.destroyAllWindows()



