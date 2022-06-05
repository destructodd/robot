# robot
RPI Robot
Code to operate an RPI based wheeled robot. 

**Components**   
- Devastator Tank Robot Platform  
- RPI 4 A+  
- 3A 4V-16V 2 Channel DC Motor Driver  
- RPI camera  
- Servo powered pan and tilt camera platform  
- A PNY Curve 5200 powerbank is used to power the RPI and camera platform
- 6x AA batteries holder to power motors
- Lots of patch cables

**RPI GPIO Pin connections**
GPIO Pin No.  Connection
7             M1B motor driver input
8             M1A motor driver input
9             M2A motor driver input
10            M2B motor driver input
17            Horizontal camera servo input
27            Vertical camera servo input

**Current functionality**   

**web_bot** Remote control and video feed from the robot via a web app using flask. This version has been refactored to a class based system, with the robot class stored in a separate module. It runs the web app on port 5000, which will need to be opened on your router to allow access outside of your network.  

**RC_bot** Operate as a remote control device using a wireless game contoller. Video footage from camera returned to RPI desktop.  

**ball_bot** Identify and move towards a tennis ball, using OpenCV to identify the correct shape and colour of the object.   

**wip** Multiple object seeking using computer vision 

**Compatibility**
This was built on RPI 3 A Plus, using the Buster version of Raspberry Pi OS. It is  not functional on Bullseye, due to an overhaul of the camera implementation. 

