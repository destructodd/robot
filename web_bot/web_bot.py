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

webbot = robot()

#API commands
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
    webbot.move('stop')
    webbot.set_duty(speed)
    return speed

@app.route('/move/<direction>')
def move(direction):
    webbot.move(direction)
    return direction
    
@app.route('/cam/<move>')
def cam(move):
    webbot.cam(move)
    return move

app.run(debug = False, port=5000, use_reloader=False,host='0.0.0.0', threaded = True)






 
    
    
