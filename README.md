# robot
RPI Robot
Code to operate an RPI based wheeled robot. 

**Components**   
- Devastator Tank Robot Platform  
- RPI 4 A+  
- 3A 4V-16V 2 Channel DC Motor Driver  
- RPI camera  
- Servo powered pan and tilt platform  
- A PNY Curve 5200 powerbank is used to power the RPI  
- 6x AA batteries holder  

**Current functionality**   

**web_bot** Remote control via a public web page, using flask to generate a web server on the rpi. This version has been refactored to a class based system, with the robot class stored in a separate module. 

**RC_bot** Operate as a remote control device using a wireless game contoller. Video footage from camera returned to RPI desktop.  

**ball_bot** Identify and move towards a tennis ball, using OpenCV to identify the correct shape and colour of the object.   

**wip** Multiple object seeking using computer vision 


