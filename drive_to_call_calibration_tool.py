import cv2
import numpy as np
import imutils
import imutils.video

resolution = (320,240)
cap = imutils.video.VideoStream(src=0, usePiCamera = True, resolution = resolution).start()

kernel = np.ones((5,5), np.uint8)

def empty(a):
    pass

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("Hue Min", "TrackBars", 33, 179,empty)
cv2.createTrackbar("Hue Max", "TrackBars", 65, 179,empty)
cv2.createTrackbar("Sat Min", "TrackBars", 54, 255,empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255,empty)
cv2.createTrackbar("Val Min", "TrackBars", 78, 255,empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255,empty)


while True:
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")  
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    
    img = cap.read()
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    imgHSV = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
                     
    mask = cv2.inRange(imgHSV, lower, upper)
    imgMasked = cv2.bitwise_and(img, img, mask=mask)
    imgCanny = imutils.auto_canny(imgMasked)
    #imgDialation = cv2.erode(imgCanny, kernel, iterations=0)
    imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)
    
    cv2.imshow("Mask",imgMasked)
    cv2.imshow("vid",imgDialation)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

