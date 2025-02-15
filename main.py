import cv2
import pickle
import cvzone
import numpy as np

# Video feed
video = cv2.VideoCapture(0)
address= "http://192.168.0.221:8080/video"
video.open(address)


with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48

def checkParkingSpace(imgPro):
    spaceCounter = 0
    for pos in posList:
        x,y = pos
       

        imgCrop = imgPro[y:y+height,x:x+width]
        #cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        #cvzone.putTextRect(img,str(count),(x,y+height-4), scale = 1, thickness= 2, offset=0, colorR =(0,0,225) )

        if count <900:
            color = (0, 255,0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness) 
    #cvzone.putTextRect(img,str(count),(x,y+height-4), scale = 1, thickness= 2, offset=0, colorR = color)         
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}',(100, 50), scale = 3, thickness= 5, offset=20, colorR =(0,200,225) )
        

while True:

    if video.get(cv2.CAP_PROP_POS_FRAMES) == video.get(cv2.CAP_PROP_FRAME_COUNT):
     video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = video.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV,25,16)
    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    checkParkingSpace(imgDilate)

    #for pos in posList:
        #cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 225), 2)
    

    cv2.imshow("Image", img)
   # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageBlur", imgBlur)
    #cv2.imshow("ImageThres", imgMedian)
    cv2.waitKey(10)