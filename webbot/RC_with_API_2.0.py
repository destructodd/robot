import RPi.GPIO as GPIO
import time
import pigpio
import os
import flask
from flask import request, jsonify, render_template, Response
from camera_pi import Camera

os.system("sudo pigpiod")

app = flask.Flask(__name__)
app.config["DEBUG"] = False

pi = pigpio.pi()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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
    pi.set_PWM_dutycycle(7, 0)
    pi.set_PWM_dutycycle(8, duty_input)
    pi.set_PWM_dutycycle(9, duty_input)
    pi.set_PWM_dutycycle(10, 0)

def bwd(duty_input):
    pi.set_PWM_dutycycle(7, duty_input)
    pi.set_PWM_dutycycle(8, 0)
    pi.set_PWM_dutycycle(9, 0)
    pi.set_PWM_dutycycle(10, duty_input)

def cw(duty_input):
    pi.set_PWM_dutycycle(7, 0)
    pi.set_PWM_dutycycle(8, duty_input)
    pi.set_PWM_dutycycle(9, 0)
    pi.set_PWM_dutycycle(10, duty_input)

def acw(duty_input):
    pi.set_PWM_dutycycle(7, duty_input)
    pi.set_PWM_dutycycle(8, 0)
    pi.set_PWM_dutycycle(9, duty_input)
    pi.set_PWM_dutycycle(10, 0)

def stop():
    pi.set_PWM_dutycycle(7, 0)
    pi.set_PWM_dutycycle(8, 0)
    pi.set_PWM_dutycycle(9, 0)
    pi.set_PWM_dutycycle(10, 0)

duty=75
pi.set_servo_pulsewidth(17, 1500)
pi.set_servo_pulsewidth(27, 1500) 

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')
    
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
               
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_speed/<speed>')
def set_speed(speed):
    global duty
    duty = speed
    stop()
    return speed
    
@app.route('/stuff/blah')
def blah():
    return ("blah")

@app.route('/move/<direction>')
def move(direction):
    if direction == 'forward':
        fwd(duty)
        print("forward")
        print(duty)
    if direction == 'backward':
        bwd(duty)
    if direction == 'left':
        cw(duty)
    if direction == 'right':
        acw(duty)
    if direction == 'stop':
        stop()
    return direction
    
@app.route('/cam/<move>')
def cam(move):
    if move == 'up':
        x = pi.get_servo_pulsewidth(27) - 30
        if x < 800: x = 800 
        pi.set_servo_pulsewidth(27, x)
    if move == 'down':
        x = pi.get_servo_pulsewidth(27) + 30
        if x > 2200: x = 2200 
        pi.set_servo_pulsewidth(27, x)
    if move == 'left':
        x = pi.get_servo_pulsewidth(17) + 30
        if x > 2200: x = 2200 
        pi.set_servo_pulsewidth(17, x)
    if move == 'right':
        x = pi.get_servo_pulsewidth(17) - 30
        if x < 800: x = 800 
        pi.set_servo_pulsewidth(17, x)
    if move == 'centre':
        pi.set_servo_pulsewidth(17, 1500)
        time.sleep(0.5)
        pi.set_servo_pulsewidth(27, 1500) 
    return move

app.run(debug = False, port=5000, use_reloader=False,host='0.0.0.0', threaded = True)






 
    
    
