import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import pigpio
import os
#from imutils.video import VideoStream
import imutils.video
import imutils
import threading

os.system("sudo pigpiod")
pi = pigpio.pi()

freq = 20
x= 0
y= 0
servo_yduty = 1500
last_seen = 'right'
kernel = np.ones((5,5), np.uint8)
resolution = (320,240)

cap = imutils.video.VideoStream(src=0, usePiCamera = True, resolution = resolution, framerate=32).start()
time.sleep(2)

pi.set_servo_pulsewidth(27, 1500)


def readCam():
    img = cap.read()
    #img = cv2.rotate(img, cv2.ROTATE_180)
    return img

def trackBall(img):
    x, y, area = 0, 0, 0
    blank, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print(len(contours), 'contours detected')
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 300:
            (x,y), radius = cv2.minEnclosingCircle(cnt)
            centre = (int(x),int(y))
            radius = int(radius)
            cv2.circle(imgContour, centre, radius, (255,0,0),2)
            #cv2.circle(imgContour, centre, 1, (0,0,255),2)
            break
    return x, y, area

def calcBoundaries(area):
    if area == 0: area = 1 
    rBound = 185 + (50*(300/area))
    cv2.line(imgContour, (int(rBound),0),(int(rBound),480),(255,0,0),2)
    lBound = 135 - (50*(300/area))
    cv2.line(imgContour, (int(lBound),0),(int(lBound),480),(255,0,0),2)
    return lBound, rBound

def process_img():
    img = readCam()
    #take a copy before processing to display
    imgContour = img.copy()
    #img = cv2.GaussianBlur(img, (11,11), 0)
    #convert to HSV color format
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #define upper and lower HSV values in an array
    lower = np.array([39, 78, 47])
    upper = np.array([41, 255, 225])
    #create mask to remove everything except ball
    mask = cv2.inRange(img, lower, upper)
    #apply mask to img
    
    img = cv2.bitwise_and(img, img, mask=mask)
    #apply filter that finds contours
    #img = cv2.Canny(img,50,500)
    img = imutils.auto_canny(img)
    #dilate contours
    img = cv2.dilate(img, kernel, iterations=1)
    return img, imgContour

def camera_move(y):
    servo_yduty = pi.get_servo_pulsewidth(27)
    if y == 0: servo_yduty = 1500
    elif y > 140:
        servo_yduty += ((y-140)/140) * 60
        print(servo_yduty)
    elif y < 100:
        servo_yduty -= (1-(y/100)) * 60
        print(servo_yduty)
        
    if servo_yduty > 2200: servo_yduty = 2200
    if servo_yduty < 800: servo_yduty = 800
    print('yduty', servo_yduty)
    pi.set_servo_pulsewidth(27, servo_yduty)
    


#right wheels
pi.set_PWM_frequency(8, freq)
pi.set_PWM_frequency(7, freq)
#left wheels
pi.set_PWM_frequency(9, freq)
pi.set_PWM_frequency(10, freq)

#start with duty cycle of 0
pi.set_PWM_dutycycle(8, 0)
pi.set_PWM_dutycycle(7, 0)
pi.set_PWM_dutycycle(9, 0)
pi.set_PWM_dutycycle(10, 0)

def fwd(duty_input):
    pi.set_PWM_dutycycle(8, duty_input)
    pi.set_PWM_dutycycle(9, duty_input)
    pi.set_PWM_dutycycle(7, 0)
    pi.set_PWM_dutycycle(10, 0)

def bwd(duty_input):
    pi.set_PWM_dutycycle(7, duty_input)
    pi.set_PWM_dutycycle(10, duty_input)
    pi.set_PWM_dutycycle(8, 0)
    pi.set_PWM_dutycycle(9, 0)

def cw(duty_input):
    pi.set_PWM_dutycycle(8, duty_input)
    pi.set_PWM_dutycycle(10, duty_input)
    pi.set_PWM_dutycycle(7, 0)
    pi.set_PWM_dutycycle(9, 0)

def acw(duty_input):
    pi.set_PWM_dutycycle(7, duty_input)
    pi.set_PWM_dutycycle(9, duty_input)
    pi.set_PWM_dutycycle(8, 0)
    pi.set_PWM_dutycycle(10, 0)

def stop():
    pi.set_PWM_dutycycle(8, 0)
    pi.set_PWM_dutycycle(7, 0)
    pi.set_PWM_dutycycle(9, 0)
    pi.set_PWM_dutycycle(10, 0)

def drive(x, last_seen):
    if x == 0:
        if last_seen == 'left':
            cw(190)
            print(last_seen)
        elif last_seen == 'right':
            acw(190)
            print(last_seen)
    elif area > 4500:
        stop()
    elif x < lBound:
        cw(50+(50*area_modifier))
    elif x > rBound:
        acw(50+(50*area_modifier))
    else:
        fwd(128+(100*area_modifier))


start = time.time()
count = 0
while True:
    #read camera and output stored image
    img, imgContour = process_img()
    #store previous x value
    x_last = x
    #pass image to trackball function which outputs coords and size of object
    x, y, area = trackBall(img)
    print('x=', x,'y=', y, 'area=', area)
    threading.Thread(target=camera_move, args=(y,), daemon=True).start()
    
    area_modifier = 1 - (area / 4500)
    
    #if no object is found, remember where if it was last seen left or right
    if x == 0 and x_last < 160 and x_last != 0: last_seen ='left'
    if x == 0 and x_last > 160: last_seen ='right'
    
    #pass areas value to function which calcualtes boundaries
    lBound, rBound = calcBoundaries(area)
   
    drive(x, last_seen)
    #threading.Thread(target = drive, args = (x,last_seen)).start()
    
    camera_move(y)
    #threading.Thread(target = camera_move, args = (y,)).start()
    
    cv2.imshow("Contour",imgContour)
    
    count += 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        cap.stop()
        cv.DestroyWindow("Contour")
    

end = time.time()
print("loops per second ", count/(end-start))

