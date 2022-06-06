import RPi.GPIO as GPIO
import os
import flask
from flask import request, jsonify, render_template, Response
from camera_pi import Camera
from robot_class import robot

#startup stuff
os.system("sudo pigpiod")

app = flask.Flask(__name__)
app.config["DEBUG"] = False

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#initialise robot
webbot = robot()

#camera feed
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

#API commands
@app.route('/set_speed/<speed>')
def set_speed(speed):
    webbot.set_duty(speed)
    webbot.drive(webbot.last_direction)
    return speed

@app.route('/drive/<direction>')
def drive(direction):
    webbot.drive(direction)
    return direction
    
@app.route('/cam/<direction>')
def cam_move(direction):
    webbot.cam_move(direction)
    return direction

@app.route('/cam_absolute_x/<value>')
def cam_increment_x(value):
    webbot.cam_increment(0, value)
    return value

@app.route('/cam_absolute_y/<value>')
def cam_increment_y(value):
    webbot.cam_increment(1, value)
    return value

app.run(debug = False, port=5000, use_reloader=False,host='0.0.0.0', threaded = True)






 
    
    
