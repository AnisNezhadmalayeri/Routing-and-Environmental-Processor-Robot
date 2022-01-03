
import cv2
import numpy as np


    image = frame.array
    frame = image
    hsv_img= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    brightness = 50
    contrast = 50
    hsv_img= np.int16(hsv_img)
    hsv_img= hsv_img* (contrast/127+1) - contrast + brightness
    hsv_img= np.clip(hsv_img, 0, 255)
    hsv_img= np.uint8(hsv_img)
    frame=hsv_img
    lower_red = np.array([0, 150, 100], dtype = "uint16")
    upper_red= np.array([20, 255, 255], dtype = "uint16")
    mask_red = cv2.inRange(hsv_img, lower_red, upper_red)
    image = cv2.bitwise_and(hsv_img, hsv_img, mask=mask_red)
    img=cv2.medianBlur(frame,15)
    imgg=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    imgg=cv2.blur(imgg,(3,3))
    
    circles=cv2.HoughCircles(imgg,cv2.HOUGH_GRADIENT,1,120,param1=100,param2=30,minRadius=20,maxRadius=200)
    time.sleep(0.2)

    if circles is None:
        print("No Circle rotate R")
                    
    elif(1==1) :
    #circles=np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv2.circle(imgg,(i[0],i[1]), 2, (0, 0, 255), 3)
            #print(i)
            cv2.circle(imgg,(i[0],i[1]),2,(255,255,255),3)
            if(i[0]>280 and i[0]<350):
                print (" C")
                            #print (GetDistance())
            elif (i[0]>350):
                print ("  R")
            elif (i[0]<280):
                print ("L")
                        
    cv2.imshow("imgg",imgg)
    cv2.imshow('image',image)
    key2 = cv2.waitKey(1) & 0xFF
    rawCapture.truncate()
    rawCapture.seek(0)
            #continue
            #keypad.registerKeyPressHandler(printKey2)
            #key=printKey2
    if key2 == ord("q"):
        break

cv2.destroyAllWindows()
