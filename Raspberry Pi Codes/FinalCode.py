import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26,GPIO.OUT)
    GPIO.setup(19,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)
    GPIO.setup(6,GPIO.OUT)
"F Forwarde , B Backward , L Left , R Right"
def Move(dirc,sec):
    init()
    if(dirc=="F"):
        GPIO.output(26,GPIO.HIGH)
        GPIO.output(19,GPIO.LOW)
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(6,GPIO.LOW)
        time.sleep(sec)
        GPIO.cleanup()
    elif(dirc=="B"):
        GPIO.output(26,GPIO.LOW)
        GPIO.output(19,GPIO.HIGH)
        GPIO.output(13,GPIO.LOW)
        GPIO.output(6,GPIO.HIGH)
        time.sleep(sec)
        GPIO.cleanup()
    elif(dirc=="L"):
        GPIO.output(26,GPIO.HIGH)
        GPIO.output(19,GPIO.LOW)
        GPIO.output(13,GPIO.LOW)
        GPIO.output(6,GPIO.HIGH)
        time.sleep(sec)
        GPIO.cleanup()
    elif(dirc=="R"):
        GPIO.output(26,GPIO.LOW)
        GPIO.output(19,GPIO.HIGH)
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(6,GPIO.LOW)
        time.sleep(sec)
        GPIO.cleanup()
        
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate =32
rawCapture = PiRGBArray(camera, size=(640, 480))
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True) :
            image = frame.array
            image= cv2.cvtColor(image,cv2.COLOR_BGR2HSV) 
            lower_red = np.array([0, 150, 100], dtype = "uint16")
            upper_red= np.array([20, 255, 255], dtype = "uint16")
            mask = cv2.inRange(image, lower_red, upper_red)
            resmask=cv2.GaussianBlur(mask,(5,5),0)
            resmask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
            resmask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
            resmask=cv2.GaussianBlur(mask,(5,5),0)
            image = cv2.bitwise_and(image, image, mask=resmask)
            image=cv2.medianBlur(image,15)
            image=cv2.blur(image,(3,3))
            _,contours,hirachy = cv2.findContours(resmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
       #switch     #_,contours,hirachy = cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

            area_list=[]
            for c in contours:
                area=cv2.contourArea(c)
                area_list.append(area)
            if len(area_list) :
                maxi=max(area_list)
                aa=(area_list.index(maxi))
                M=cv2.moments(contours[aa])
                if M['m00'] > 0:
                    cx=int(M['m10']/M['m00'])
                    cy=int(M['m01']/M['m00'])
                    
            if(cx>260):
                print("  R")
                Move("R",0.5)
            elif(cx<220):
                print("L  ")
                Move("L",0.5)
            else:
                print(" F ")
                Move("C",0.5)
            cv2.imshow('out',image)
            k=cv2.waitKey(1) & 0xff
            if key==ord('q'):
                GPIO.cleanup()
                break

cv2.destroyAllWindows()