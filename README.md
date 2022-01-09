# robot
RPI Robot
Code to operate an RPI based wheeled robot. Components inlcude a Devastator Tank Robot Platform, a RPI 4 A+, a motor driver board, an RPI camera and a pan and tilt platform. A PNY Curve 5200 powerbank is used to power the RPI, and 6x AA batteries are used to power the motors. 

Current functionality includes - Operate as a remote control device using a wireless game contoller. Video footage from camera returned to RPI desktop

Remote control via a public web page, using flask to generate a web server on the rpi.

Identify and move towards a tennis ball, using OpenCV to identify the correct shape and colour of the object. 

Next step is to using YOLO to add ML  object detection. 
