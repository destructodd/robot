import RPi.GPIO as GPIO
import time
import multiprocessing
import cv2
import pigpio
import os
import pygame

os.system("sudo pigpiod")

pi = pigpio.pi()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_EXPOSURE,5)

pygame.init()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
joystick = pygame.joystick.Joystick(0)
joystick.init()
axes = joystick.get_numaxes()
buttons = joystick.get_numbuttons()


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#set pause after each command
a = 0.01
#a = 0.1

freq = 20

#set freqency for right wheels
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

def bwd(duty_input):
    pi.set_PWM_dutycycle(7, duty_input)
    pi.set_PWM_dutycycle(10, duty_input)

def cw(duty_input):
    pi.set_PWM_dutycycle(8, duty_input)
    pi.set_PWM_dutycycle(10, duty_input)

def acw(duty_input):
    pi.set_PWM_dutycycle(7, duty_input)
    pi.set_PWM_dutycycle(9, duty_input)

def stop():
    pi.set_PWM_dutycycle(8, 0)
    pi.set_PWM_dutycycle(7, 0)
    pi.set_PWM_dutycycle(9, 0)
    pi.set_PWM_dutycycle(10, 0)

def RC():
    
    duty = 64
    then = time.time()
    pi.set_servo_pulsewidth(17, 1500)
    pi.set_servo_pulsewidth(27, 1500) 
    
    try:
        while True:
            pygame.event.pump()
            axis_values = []
            button_values = []
            #create a list of axes values
            for i in range(axes):
                axis_values.append(joystick.get_axis(i))
            for i in range(buttons):
                button_values.append(joystick.get_button(i))
            
            
            if axis_values[2] > 0.3:
                x = pi.get_servo_pulsewidth(17) - 1
                if x < 800: x = 800 
                pi.set_servo_pulsewidth(17, x)
            elif axis_values[2] < -0.3:
                x = pi.get_servo_pulsewidth(17) + 1
                if x > 2200: x = 2200 
                pi.set_servo_pulsewidth(17, x)
            elif axis_values[5] < -0.3:
                x = pi.get_servo_pulsewidth(27) - 1
                if x < 800: x = 800 
                pi.set_servo_pulsewidth(27, x)
            elif axis_values[5] > 0.3:
                x = pi.get_servo_pulsewidth(27) + 1
                if x > 2200: x = 2200 
                pi.set_servo_pulsewidth(27, x)
            elif button_values[11] == 1:
                pi.set_servo_pulsewidth(27, 1500)
                pi.set_servo_pulsewidth(17, 1500)
            
            #print(char)
            
            if button_values[2] == 1:
                break
            elif axis_values[1] < -0.2:
                duty = 255*(axis_values[1]*-1)
                fwd(duty)
            elif axis_values[1] > 0.2:
                duty = 255*axis_values[1]
                bwd(duty)
            elif axis_values[0] < -0.2:
                duty = 255*(axis_values[0]*-1)
                cw(duty)
            elif axis_values[0] > 0.2:
                duty = 255*axis_values[0]
                acw(duty)
            else:
                stop()
             
    finally:
        GPIO.cleanup()
        pi.set_servo_pulsewidth(27, 2200)
        pi.set_servo_pulsewidth(17, 1500)
     
def RC_vision():
    while True: 
        success, img = cap.read()
        #img = cv2.rotate(img, cv2.ROTATE_180)
        cv2.imshow("vid",img)
        cv2.waitKey(1)
        pygame.event.pump()
        a = joystick.get_button(2) 
        if a== 1: break                     
    
multiprocessing.Process(target=RC_vision).start()
RC()






 
    
    
