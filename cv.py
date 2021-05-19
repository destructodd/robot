import cv2
import numpy as np

cap = cv2.VideoCapture(0)

kernel = np.ones((5,5), np.uint8)

def empty(a):
    pass

def getContours(img):
    x, y, w, h, area = 0, 0, 0, 0, 0
    blah, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print(len(contours), 'contours detected')
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 200:
            #cv2.drawContours(imgContour,cnt, -1, (255,0,0),3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            corners = len(approx)
            print(corners)
            if corners >6:
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(imgContour,(x, y), (x+w, y+h),(255,0,0),2)  
                break
    return x+(w/2), y+(h/2), area

while True:
    success, img = cap.read()
    imgContour = img.copy()
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower = np.array([35, 76, 83])
    upper = np.array([42, 232, 209])
                     
    mask = cv2.inRange(imgHSV, lower, upper)
    imgMasked = cv2.bitwise_and(img, img, mask=mask)
    imgCanny = cv2.Canny(imgMasked,50,500)
    imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)
    x, y, area = getContours(imgDialation)
    print('x=', x,'y=', y, 'area=', area)

    cv2.imshow("Contour",imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
