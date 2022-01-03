# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import RPi.GPIO as GPIO
import numpy as np

# Pretrained classes in the model
classNames = {0: 'background',
              1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
              7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
              13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
              18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
              24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
              32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
              37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
              41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
              46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
              51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
              56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
              61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
              67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
              75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
              80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
              86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}
class_id = 0
mode = True
state = 0 

def id_class_name(class_id, classes):
    for key, value in classes.items():
        if class_id == key:
            return value
def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26,GPIO.OUT)
    GPIO.setup(20,GPIO.OUT)
def move(mode):
    init()
    if mode == True :
        GPIO.output(26,GPIO.HIGH)
        GPIO.output(20,GPIO.HIGH)
    elif mode == False :
        GPIO.output(26,GPIO.LOW)
        GPIO.output(20,GPIO.LOW)
        
model = cv2.dnn.readNetFromTensorflow('models/frozen_inference_graph.pb',
                                      'models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (304, 304)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(304, 304))
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
count = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    move(mode)
    state = 0
    
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    image_height, image_width, _ = image.shape

    model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))
    output = model.forward()
    print(output[0,0,:,:].shape)
    


    for detection in output[0,0,:,:]:
        confidence = detection[2]
        if confidence > .5:
            class_id = detection[1]
            if class_id == 1 :
               state = 4
               # break
            if class_id == 13 :
               state = 1
              # break
            if (class_id == 10) & (state == 0) :
                state = 2
               # break
            
            class_name=id_class_name(class_id,classNames)
            print(str(str(class_id) + " " + str(detection[2])  + " " + class_name))
            
            box_x = detection[3] * image_width
            box_y = detection[4] * image_height
            box_width = detection[5] * image_width
            box_height = detection[6] * image_height
            
            cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (23, 230, 210), thickness=1)
            cv2.putText(image,class_name ,(int(box_x), int(box_y+.05*image_height)),cv2.FONT_HERSHEY_SIMPLEX,(.005*image_width),(0, 0, 255))
    if state == 4 :
        count = count+1
        convert_count = str(count)
        print(convert_count)
    elif state == 1 :
        mode = False
    elif state == 2 :
       
        light = image[ int(box_y) : int(box_height) , int(box_x) : int(box_width)]
        #cv2.imshow('light' , light)
        light = cv2.cvtColor(light, cv2.COLOR_BGR2HSV)
                
        lower_red = np.array([161, 155, 84])
        upper_red = np.array([179, 255, 255])
                
        lower_green= np.array([65, 60, 60])
        upper_green= np.array([80,255,255])
                
        mask_red= cv2.inRange(light, lower_red, upper_red)
        mask_green= cv2.inRange(light, lower_green, upper_green)
                
               #cv2.imshow("red" , mask_red)
               #cv2.imshow("green" , mask_green)
                
        if cv2.countNonZero(mask_red) > 50:
            print('Light is red')
            mode = False
                    
        elif cv2.countNonZero(mask_green) > 50:
            print('Light is green')
            mode = True
    else :
        mode = True
    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        GPIO.output(26,GPIO.LOW)
        GPIO.output(20,GPIO.LOW)
        GPIO.cleanup()
        
        break