# robot
RPI Robot
Code to operate an RPI based wheeled robot. 

Components 
Devastator Tank Robot Platform
RPI 4 A+
Motor driver board
RPI camera
Pan and tilt platform
A PNY Curve 5200 powerbank is used to power the RPI
6x AA batteries holder

Current functionality includes - Operate as a remote control device using a wireless game contoller. Video footage from camera returned to RPI desktop

Remote control via a public web page, using flask to generate a web server on the rpi.

Identify and move towards a tennis ball, using OpenCV to identify the correct shape and colour of the object. 

WIP - Multiple object seeking using computer vision 
